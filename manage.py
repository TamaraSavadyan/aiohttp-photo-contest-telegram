#! /usr/bin/env python

import click
from ktstools.collections.getters import path
from ktstools.settings import Settings
from ktstools.settings.loaders.env import EnvLoader
from ktstools.settings.loaders.file import FileLoader
from ktstools.setup.cli import autodiscover_commands
from ktstools.setup.sentry import setup_sentry
from ktstools.web.aiohttp.log import setup_logging

from kts_backend import __version__


@click.group()
@click.option(
    "--config",
    help="config file path",
    default="etc/config.yaml",
    envvar="CONFIG",
    show_envvar=True,
)
@click.option(
    "--log",
    help="log path",
    default=None,
    envvar="LOG",
    show_envvar=True,
    show_default=True,
)
@click.option(
    "--debug",
    help="turn on the debug",
    default=None,
    is_flag=True,
    envvar="DEBUG",
    show_envvar=True,
)
@click.pass_context
def cli(ctx, config, log, debug):
    ctx.obj = Settings(
        loaders=[
            FileLoader(config),
            FileLoader("./local/etc/config.yaml"),
            EnvLoader(),
        ],
        debug=debug,
    )
    ctx.obj.load_config()
    setup_logging(log_path=log)
    setup_sentry(
        dsn=path(ctx.obj.config, "sentry", "dsn"),
        environment=path(ctx.obj.config, "sentry", "env", default="dev"),
        release=__version__,
    )


autodiscover_commands(cli, "kts_backend.daemons")
autodiscover_commands(cli, "kts_backend.commands")

if __name__ == "__main__":
    cli()
