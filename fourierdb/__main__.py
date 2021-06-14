from typing import Optional
import pathlib
import logging
from fourierdb.server import run_server

import click


@click.group()
@click.pass_context
def fourierdb(ctx):
    pass


@fourierdb.command()
@click.option("-p", "--port", default=2359, type=int, show_default=True, help="The port to run the FourierDB server on")
@click.pass_context
def run(ctx, port: Optional[int]):
    click.secho(f"Starting FourierDB server on port {port}", fg="green")
    click.secho(f"FourierDB running on port {port} ✅", fg="green", bold=True)
    run_server(port)

@fourierdb.command()
@click.pass_context
def databases(ctx):
    if not((pathlib.Path.home()/ ".fourier").exists()):
        integer = click.style("0", fg="bright_cyan", bold=True)
        click.secho(f"You have currently have {integer} databases")
        return
    databases = [f.stem for f in (pathlib.Path.home() / ".fourier" / "databases").glob("*.db")]
    integer = click.style(str(len(databases)), fg="bright_cyan")
    click.secho(f"You have currently have {integer} databases:")
    for num, db in enumerate(databases):
        click.secho(str(num + 1), fg="yellow", nl=False)
        click.echo(f". {db}")

if __name__ == "__main__":
    fourierdb()
