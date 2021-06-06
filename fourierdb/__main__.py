from typing import Optional

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
@click.option(
    "--debug/--no-debug", default=True, help="Whether to run the server in debug mode"
)
@click.pass_context
def run(
    ctx,
    port: Optional[int],
    debug: bool,
):
    click.echo(f"Hi")


if __name__ == "__main__":
    fourierdb()
