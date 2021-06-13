from typing import Optional
from fourierdb.server import run_server

import click


@click.group()
@click.pass_context
def fourierdb(ctx):
    pass


@fourierdb.command()
@click.option(
    "-p",
    "--port",
    default=2359,
    type=int,
    show_default=True,
    help="The port to run the FourierDB server on",
)
@click.pass_context
def run(
    ctx,
    port: Optional[int],
):
    click.secho(f"Starting FourierDB server on port {port}", fg="green", bold=True, underline=True)
    click.secho(f"FourierDB running on port {port} ✓", fg="green", bold=True, underline=True)
    run_server(port)


if __name__ == "__main__":
    fourierdb()
