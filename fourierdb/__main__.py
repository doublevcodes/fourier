import json
from typing import Optional
import pathlib
import sys
from fourierdb.server import run_server

import click


@click.group()
@click.pass_context
def fourier(ctx):
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
@click.pass_context
def run(ctx, port: Optional[int]):
    click.secho(f"Starting FourierDB server on port {port}", fg="green")
    click.secho(f"FourierDB running on port {port} ✅", fg="green", bold=True)
    run_server(port)


@fourier.command()
@click.pass_context
def databases(ctx):
    if not ((pathlib.Path.home() / ".fourier").exists()):
        integer = click.style("0", fg="bright_cyan", bold=True)
        click.secho(f"You have currently have {integer} databases")
        return
    databases = [
        f.stem for f in (pathlib.Path.home() / ".fourier" / "databases").glob("*.db")
    ]
    integer = click.style(str(len(databases)), fg="bright_cyan")
    click.secho(
        f"You have currently have {integer} databases! {(click.style(':(', fg='red')) if integer == 0 else ''}"
    )
    for num, db in enumerate(databases):
        click.secho(str(num + 1), fg="yellow", nl=False)
        click.echo(f". {db}")


@fourier.command()
@click.pass_context
def status(ctx):
    cache = json.load(open(pathlib.Path.home() / ".fourier" / ".cache.json"))
    if not cache["server"]:
        click.echo(
            f"You do not currently have a server running {click.style(':(', fg='red')}"
        )
        suggested_cmd = click.style(
            f"{sys.executable.split('/')[-1]} -m fourier run --help",
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
    click.echo(f"You do have a Fourier server running {click.style(':)', fg='green')}")
    click.echo(f"It is running on port {port}")
    click.echo(f"Checking if server is responding")


if __name__ == "__main__":
    fourier()
