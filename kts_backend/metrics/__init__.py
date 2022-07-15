from typing import Optional

from ktstools.monit import Monit

from .. import __appname__, __version__


def init_monit(monit: Optional[Monit]):
    if not monit:
        return

    monit.metrics_registry.set_target_info(
        {
            "name": __appname__,
            "version": __version__,
        }
    )
