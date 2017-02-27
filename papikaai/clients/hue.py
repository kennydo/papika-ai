import logging
from typing import Optional

import phue

log = logging.getLogger(__name__)


class HueClient:
    def __init__(self, *, ip: str, username: str) -> None:
        self._hue_bridge = phue.Bridge(
            ip=ip,
            username=username,
        )
