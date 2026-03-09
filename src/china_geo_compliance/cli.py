"""CLI 命令定义"""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .validator import GeoComplianceValidator, ValidationResult
from .utils import get_standard_data_path, save_json_report, region_name_map

app = typer.Typer(
    name="china-geo-compliance",
    help="🗺️  中国地理边界合规性检查工具",
    add_completion=False
)
console = Console()


@app.command()
def check(
    file: Path = typer.Argument(
        ...,
        help="要检查的 GeoJSON 文件路径",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True
    ),
    strict: bool = typer.Option(
        False,
        "--strict",
        "-s",
        help="启用严格模式（不允许任何偏差）"
    ),
    tolerance: float = typer.Option(
        0.01,
        "--tolerance",
        "-t",
        help="几何比对容差（度数），默认 0.01° ≈ 1.1km"
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="输出 JSON 报告到指定文件"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="显示详细信息"
    )
):
    """检查 GeoJSON 文件的中国边界合规性"""

    try:
        # 1. 加载验证器
        validator = GeoComplianceValidator(
            standard_data_path=get_standard_data_path(),
            tolerance=tolerance
        )

        # 2. 执行验证
        with console.status("[bold blue]正在检查边界合规性..."):
            result = validator.validate(str(file), strict=strict)

        # 3. 显示结果
        display_result(result, verbose)

        # 4. 输出 JSON（如果指定）
        if output:
            save_json_report(result, output)
            console.print(f"\n[green]报告已保存到: {output}[/green]")

        # 5. 设置退出码
        raise typer.Exit(code=0 if result.is_compliant else 1)

    except Exception as e:
        console.print(f"[bold red]错误：{str(e)}[/bold red]")
        raise typer.Exit(code=2)


def display_result(result: ValidationResult, verbose: bool):
    """显示验证结果"""
    if result.errors:
        console.print(Panel(
            f"[bold red]✗ 检查失败[/bold red]\n\n错误: {', '.join(result.errors)}",
            title="检查结果",
            border_style="red"
        ))
        return

    if result.is_compliant:
        console.print(Panel(
            "[bold green]✓ 合规性检查通过[/bold green]\n\n"
            "您的地图数据符合中国地理边界标准。",
            title="检查结果",
            border_style="green"
        ))
    else:
        # 创建问题表格
        table = Table(title="检测到的问题", show_header=True)
        table.add_column("问题类型", style="cyan")
        table.add_column("详细信息", style="yellow")

        for region in result.missing_regions:
            table.add_row("缺失区域", region_name_map.get(region, region))

        for region in result.extra_regions:
            table.add_row("多余区域", region)

        console.print(Panel(
            "[bold red]✗ 合规性检查失败[/bold red]\n\n"
            "您的地图数据存在边界问题，可能导致产品下架风险！",
            title="检查结果",
            border_style="red"
        ))
        console.print(table)

    # 显示覆盖率（verbose 模式）
    if verbose and result.coverage_percentage:
        coverage_table = Table(title="区域覆盖率")
        coverage_table.add_column("区域", style="cyan")
        coverage_table.add_column("覆盖率", style="green")

        for region, percentage in result.coverage_percentage.items():
            coverage_table.add_row(
                region_name_map.get(region, region),
                f"{percentage * 100:.2f}%"
            )

        console.print(coverage_table)


if __name__ == "__main__":
    app()
