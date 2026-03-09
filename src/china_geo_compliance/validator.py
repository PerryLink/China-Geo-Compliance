"""核心验证器类"""

from dataclasses import dataclass
from typing import List, Dict, Any
from pathlib import Path
import json

from shapely.geometry import shape
from shapely.ops import unary_union
import geojson


@dataclass
class ValidationResult:
    """验证结果数据类"""
    is_compliant: bool
    missing_regions: List[str]
    extra_regions: List[str]
    coverage_percentage: Dict[str, float]
    warnings: List[str]
    errors: List[str]


class GeoComplianceValidator:
    """中国地理边界合规性验证器"""

    def __init__(self, standard_data_path: str, tolerance: float = 0.01):
        """
        Args:
            standard_data_path: 标准边界数据文件路径
            tolerance: 几何比对容差（度数），默认 0.01° ≈ 1.1km
        """
        self.tolerance = tolerance
        self.standard_features = self._load_standard_data(standard_data_path)
        self.critical_regions = self._extract_critical_regions()

    def _load_standard_data(self, path: str) -> Dict:
        """加载标准边界数据"""
        with open(path, 'r', encoding='utf-8') as f:
            return geojson.load(f)

    def _extract_critical_regions(self) -> Dict[str, Any]:
        """提取关键区域的 Shapely 几何对象"""
        regions = {}
        for feature in self.standard_features['features']:
            region_type = feature['properties']['region_type']
            regions[region_type] = shape(feature['geometry'])
        return regions

    def validate(self, user_geojson_path: str, strict: bool = False) -> ValidationResult:
        """
        验证用户 GeoJSON 文件的合规性

        Args:
            user_geojson_path: 用户 GeoJSON 文件路径
            strict: 严格模式（不允许任何偏差）

        Returns:
            ValidationResult 对象
        """
        try:
            # 1. 加载用户数据
            user_geometry = self._load_user_geometry(user_geojson_path)

            # 2. 检查关键区域
            missing_regions = []
            coverage = {}

            for region_name, standard_geom in self.critical_regions.items():
                if region_name == 'national_boundary':
                    # 检查用户边界是否包含标准边界
                    coverage_ratio = self._calculate_coverage(
                        user_geometry, standard_geom
                    )
                    coverage[region_name] = coverage_ratio

                    if strict and coverage_ratio < 0.99:
                        missing_regions.append(region_name)
                    elif coverage_ratio < 0.95:
                        missing_regions.append(region_name)
                else:
                    # 检查关键区域是否被包含
                    if not self._contains_region(user_geometry, standard_geom):
                        missing_regions.append(region_name)
                        coverage[region_name] = 0.0
                    else:
                        coverage[region_name] = 1.0

            # 3. 检查是否有多余区域（超出标准边界）
            extra_regions = self._detect_extra_regions(
                user_geometry,
                self.critical_regions['national_boundary']
            )

            # 4. 生成结果
            is_compliant = len(missing_regions) == 0 and len(extra_regions) == 0

            return ValidationResult(
                is_compliant=is_compliant,
                missing_regions=missing_regions,
                extra_regions=extra_regions,
                coverage_percentage=coverage,
                warnings=[],
                errors=[]
            )
        except Exception as e:
            return ValidationResult(
                is_compliant=False,
                missing_regions=[],
                extra_regions=[],
                coverage_percentage={},
                warnings=[],
                errors=[str(e)]
            )

    def _load_user_geometry(self, path: str):
        """加载用户 GeoJSON 并转换为 Shapely 几何对象"""
        with open(path, 'r', encoding='utf-8') as f:
            data = geojson.load(f)

        # 处理 Feature/FeatureCollection/Geometry
        if data['type'] == 'FeatureCollection':
            geometries = [shape(f['geometry']) for f in data['features']]
            return unary_union(geometries)
        elif data['type'] == 'Feature':
            return shape(data['geometry'])
        else:
            return shape(data)

    def _calculate_coverage(self, user_geom, standard_geom) -> float:
        """计算用户几何对象对标准几何对象的覆盖率"""
        try:
            # 使用缓冲区处理容差
            buffered_user = user_geom.buffer(self.tolerance)
            intersection = buffered_user.intersection(standard_geom)
            return intersection.area / standard_geom.area
        except Exception:
            return 0.0

    def _contains_region(self, user_geom, region_geom) -> bool:
        """检查用户几何对象是否包含指定区域"""
        buffered_user = user_geom.buffer(self.tolerance)
        return buffered_user.contains(region_geom) or \
               buffered_user.intersection(region_geom).area / region_geom.area > 0.95

    def _detect_extra_regions(self, user_geom, standard_geom) -> List[str]:
        """检测超出标准边界的区域"""
        buffered_standard = standard_geom.buffer(self.tolerance)
        difference = user_geom.difference(buffered_standard)

        if difference.is_empty or difference.area < 0.01:
            return []

        return ["超出标准边界的区域"]
