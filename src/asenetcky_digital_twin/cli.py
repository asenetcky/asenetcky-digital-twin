"""Console script for asenetcky_digital_twin."""

import typer
from rich.console import Console

from asenetcky_digital_twin import utils

app = typer.Typer()
console = Console()


@app.command()
def main() -> None:
    """Console script for asenetcky_digital_twin."""
    console.print("Replace this message by putting your code into asenetcky_digital_twin.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    utils.do_something_useful()


if __name__ == "__main__":
    app()
