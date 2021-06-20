from json import load
from pathlib import Path
from sys import executable
from typing import Optional

import click

from fourierdb.helpers import get_databases
from fourierdb.server import run_server

@click.group()
def fourier():
    pass


@fourier.command()
@click.option(
    "-p",
    "--port",
    default=2359,
    type=int,
    show_default=True,
    help="The port to run the FourierDB server on",
)
def run(port: Optional[int]):
    click.secho(f"Starting FourierDB server on port {port}", fg="green")
    click.secho(f"FourierDB running on port {port} ✅", fg="green", bold=True)
    run_server(port)


@fourier.command()
def databases():
    if not ((Path.home() / ".fourier").exists()):
        integer = click.style("0", fg="bright_cyan", bold=True)
        click.secho(f"You have currently have {integer} databases")
        return
    databases = get_databases()
    integer = click.style(str(len(databases)), fg="bright_cyan")
    click.secho(f"You have currently have {integer} databases!")
    for num, db in enumerate(databases):
        click.secho(str(num + 1), fg="yellow", nl=False)
        click.echo(f". {db}")


@fourier.command()
def status():
    cache = load(open(Path.home() / ".fourier" / ".cache.json"))
    if not cache["server"]:
        click.echo(
            f"You do not currently have a server running {click.style(':(', fg='red')}"
        )
        suggested_cmd = click.style(
            f"{executable.split('/')[-1]} -m fourier run --help",
            fg="white",
            bg="black",
        )
        click.echo(
            f"{click.style('HINT:', fg='yellow')} Try running {suggested_cmd} to get more information on how to start a server"
        )
        click.echo(
            f"{click.style('HINT:', fg='yellow')} Fourier runs on a default port of {click.style('2359', fg='bright_cyan')}"
        )
        return
    port = click.style(str(cache["port"]), fg="bright_cyan")
    click.echo(f"You have a Fourier server running ✅")
    click.echo(f"Running on port {port}")


if __name__ == "__main__":
    fourier()
