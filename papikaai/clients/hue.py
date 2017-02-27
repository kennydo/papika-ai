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

    def turn_on_lights_in_group(self, group_id: int) -> None:
        group = phue.Group(self._hue_bridge, group_id)

        log.info("Turning lights in group %s on", group_id)
        group.on = True

    def turn_off_lights_in_group(self, group_id: int) -> None:
        group = phue.Group(self._hue_bridge, group_id)

        log.info("Turning lights in group %s off", group_id)
        group.on = False

