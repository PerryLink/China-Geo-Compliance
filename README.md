# china-geo-compliance

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/china-geo-compliance)](https://pypi.org/project/china-geo-compliance/)

A CLI tool to validate GeoJSON files against China's official geographic boundary standards — helping developers avoid compliance issues before publishing map-based products.

---

## Features

- **Key Region Detection** — Checks South China Sea nine-dash line, Zangnan (South Tibet), and Aksai Chin
- **Precision Geometry** — Shapely 2.0-powered spatial comparison with configurable tolerance
- **Beautiful Output** — Rich-powered terminal reports with clear pass/fail indicators
- **Strict Mode** — Enforces ≥99% boundary coverage for production use
- **CI/CD Ready** — JSON report export for automated pipelines

## Quick Start

### Installation

```bash
pip install china-geo-compliance
```

Or with Poetry:

```bash
poetry add china-geo-compliance
```

### Basic Usage

```bash
# Run a compliance check
china-geo-compliance check map.geojson

# Strict mode (99%+ coverage required)
china-geo-compliance check map.geojson --strict

# Adjust tolerance (default: 0.01°)
china-geo-compliance check map.geojson --tolerance 0.005

# Export JSON report
china-geo-compliance check map.geojson --output report.json

# Verbose output
china-geo-compliance check map.geojson --verbose
```

## Project Structure

```
china-geo-compliance/
├── src/
│   └── china_geo_compliance/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py           # Typer CLI entrypoint
│       ├── validator.py     # Core boundary validation logic
│       ├── utils.py         # Helper utilities
│       └── data/
│           └── china_boundary.geojson   # Reference boundary data
├── tests/
├── pyproject.toml
└── README.md
```

## Tech Stack

| Library | Purpose |
|---------|---------|
| [Shapely 2.0+](https://shapely.readthedocs.io/) | Geometric operations |
| [Typer](https://typer.tiangolo.com/) | CLI framework |
| [Rich](https://rich.readthedocs.io/) | Terminal output |
| [geojson](https://python-geojson.readthedocs.io/) | GeoJSON parsing |

## Notes

- Default tolerance: `0.01°` (~1.1 km)
- Strict mode requires ≥99% boundary coverage
- This tool is for technical validation only and does not constitute legal advice
- Boundary data uses simplified reference polygons; more precise data updates planned for future releases

## License

Apache License 2.0 — see [LICENSE](LICENSE) for details.

Copyright 2026 Chance Dean (novelnexusai@outlook.com)

---

# china-geo-compliance（中文）

中国地图边界合规性检查工具 —— 帮助开发者在发布地图类产品前，验证 GeoJSON 文件是否符合中国官方地理边界标准，规避合规风险。

---

## 功能特性

- **关键区域检测** — 检查南海九段线、藏南地区、阿克赛钦
- **精确几何计算** — 基于 Shapely 2.0 的空间比对，支持自定义容差
- **美观终端输出** — 使用 Rich 库提供清晰的检查报告
- **严格模式** — 要求 99% 以上的边界覆盖率，适用于生产环境
- **CI/CD 集成** — 支持 JSON 报告导出，便于自动化流水线使用

## 快速开始

### 安装

```bash
pip install china-geo-compliance
```

或使用 Poetry：

```bash
poetry add china-geo-compliance
```

### 基本使用

```bash
# 运行合规性检查
china-geo-compliance check map.geojson

# 严格模式（要求 99% 以上覆盖率）
china-geo-compliance check map.geojson --strict

# 调整容差（默认 0.01°）
china-geo-compliance check map.geojson --tolerance 0.005

# 导出 JSON 报告
china-geo-compliance check map.geojson --output report.json

# 详细输出模式
china-geo-compliance check map.geojson --verbose
```

## 项目结构

```
china-geo-compliance/
├── src/
│   └── china_geo_compliance/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py           # Typer CLI 入口
│       ├── validator.py     # 核心边界校验逻辑
│       ├── utils.py         # 工具函数
│       └── data/
│           └── china_boundary.geojson   # 参考边界数据
├── tests/
├── pyproject.toml
└── README.md
```

## 技术栈

| 库 | 用途 |
|----|------|
| [Shapely 2.0+](https://shapely.readthedocs.io/) | 几何操作核心库 |
| [Typer](https://typer.tiangolo.com/) | 现代化 CLI 框架 |
| [Rich](https://rich.readthedocs.io/) | 终端美化输出 |
| [geojson](https://python-geojson.readthedocs.io/) | GeoJSON 解析 |

## 注意事项

- 默认容差为 `0.01°`（约 1.1km）
- 严格模式要求 99% 以上的覆盖率
- 本工具仅用于技术检查，不构成法律建议
- 当前边界数据使用简化参考多边形，后续版本将提供更精确的数据更新

## 许可证

Apache License 2.0 — 详见 [LICENSE](LICENSE) 文件。

Copyright 2026 Chance Dean (novelnexusai@outlook.com)
