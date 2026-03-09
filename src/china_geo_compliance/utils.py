"""工具函数"""

import json
from pathlib import Path
from typing import Any, Dict

# 区域名称映射
region_name_map = {
    "nine_dash_line": "南海九段线",
    "south_tibet": "藏南地区",
    "aksai_chin": "阿克赛钦",
    "national_boundary": "国家边界"
}


def get_standard_data_path() -> str:
    """获取标准边界数据文件路径"""
    return str(Path(__file__).parent / "data" / "china_boundary.geojson")


def save_json_report(result: Any, output_path: Path) -> None:
    """保存 JSON 格式的检查报告"""
    report = {
        "is_compliant": result.is_compliant,
        "missing_regions": result.missing_regions,
        "extra_regions": result.extra_regions,
        "coverage_percentage": result.coverage_percentage,
        "warnings": result.warnings,
        "errors": result.errors
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
