from pathlib import Path

import typer
from rich import print

from glvars.config import Loader
from glvars.synchronizer import VariableSynchronizer

app = typer.Typer()


@app.command()
def sync(
    config_path_str: str = typer.Option(
        None, "--config", "-c", help="Path to the config file, the default is $PWD/.glvars.yml"
    )
):
    config_path = Path(config_path_str) if config_path_str else Path.cwd() / ".glvars.yml"
    if not config_path.is_file():
        print(f"[red]Cannot read {config_path}[/red]")
        raise typer.Exit(1)
    loader = Loader(config_path)

    try:
        config = loader.load()
        synchronizer = VariableSynchronizer(config)
        synchronizer.sync()
    except Exception as e:
        print(f"[red]{e}[/red]")
        raise typer.Exit(1)
