"""验证器单元测试"""

from pathlib import Path
import pytest

from china_geo_compliance.validator import GeoComplianceValidator
from china_geo_compliance.utils import get_standard_data_path


@pytest.fixture
def validator():
    """创建验证器实例"""
    return GeoComplianceValidator(get_standard_data_path())


@pytest.fixture
def fixtures_dir():
    """获取测试数据目录"""
    return Path(__file__).parent / "fixtures"


def test_compliant_geojson(validator, fixtures_dir):
    """测试合规的 GeoJSON"""
    result = validator.validate(str(fixtures_dir / "compliant.geojson"))
    assert result.is_compliant is True
    assert len(result.missing_regions) == 0
    assert len(result.errors) == 0


def test_non_compliant_geojson(validator, fixtures_dir):
    """测试不合规的 GeoJSON"""
    result = validator.validate(str(fixtures_dir / "non_compliant.geojson"))
    assert result.is_compliant is False
    assert len(result.missing_regions) > 0


def test_strict_mode(validator, fixtures_dir):
    """测试严格模式"""
    result = validator.validate(
        str(fixtures_dir / "compliant.geojson"),
        strict=True
    )
    assert result.is_compliant is True


def test_invalid_file(validator):
    """测试无效文件"""
    result = validator.validate("nonexistent.geojson")
    assert result.is_compliant is False
    assert len(result.errors) > 0
