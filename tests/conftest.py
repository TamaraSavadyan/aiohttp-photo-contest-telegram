import logging
import os
import sys

import click
import pytest
from aiohttp.test_utils import loop_context
from aiohttp.pytest_plugin import aiohttp_client
import datetime
from dateutil import tz
import copy
from freezegun import freeze_time
from ktstools.settings import Settings
from ktstools.settings.loaders.env import EnvLoader
from ktstools.settings.loaders.file import FileLoader
from ktstools.store import Connector
from ktstools.web.aiohttp.log import setup_logging

from kts_backend.web.app import ApiApplication


DEFAULT_DATETIME = datetime.datetime(2019, 11, 18, 12, tzinfo=tz.UTC)


@pytest.fixture(scope="session")
def loop():
    with loop_context() as _loop:
        yield _loop


@pytest.fixture(scope="session")
def event_loop(loop):
    yield loop


@pytest.fixture(scope="session")
def settings():
    setup_logging()
    settings = Settings(
        [
            FileLoader("./etc/config.yaml"),
            FileLoader(os.environ.get("CONFIG") or "./tests/config.yaml"),
            EnvLoader(),
        ]
    )
    settings.load_config()
    return settings


@pytest.fixture(scope="session")
async def api(loop, settings):
    app = ApiApplication(settings)
    yield app


@pytest.fixture
async def cli(aiohttp_client, api):
    client = await aiohttp_client(api)
    yield client


@pytest.fixture
async def freeze_t():
    now = copy.copy(DEFAULT_DATETIME)
    _freeze_time = freeze_time(now)
    _freeze_time.start()
    yield now
    _freeze_time.stop()


@pytest.fixture
async def _truncate_all(store):
    yield
    except_tables = ("alembic_version",)
    res = await store.pg.fetch(
        "select tablename from pg_catalog.pg_tables where schemaname = 'public' {};".format(
            "".join([f" and tablename != '{table}'" for table in except_tables])
        )
    )
    await store.pg.execute(
        "truncate table {}".format(", ".join(r["tablename"] for r in res))
    )
