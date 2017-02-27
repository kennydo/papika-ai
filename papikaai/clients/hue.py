import logging
from typing import List
from typing import NamedTuple
from typing import Optional

import phue

log = logging.getLogger(__name__)

#: Maximum hue light brightness
MAX_BRIGHTNESS = 254


LightGroupStatus = NamedTuple('LightGroupStatus', [
    ('group_id', int),
    ('is_on', bool),
    ('brightness', int),
    ('brightness_percentage', float),
])


class HueClient:
    def __init__(self, *, ip: str, username: str) -> None:
        self._hue_bridge = phue.Bridge(
            ip=ip,
            username=username,
        )

    def turn_on_lights_in_group(self, group_id: int, set_brightness_percentage: Optional[int]=None) -> None:
        group = phue.Group(self._hue_bridge, group_id)

        log.info("Turning lights in group %s on", group_id)

        # Make sure to turn the lighs on before changing the brightness for the brightness change to have effect
        group.on = True

        if set_brightness_percentage is None:
            group.brightness = MAX_BRIGHTNESS
        elif set_brightness_percentage:
            group.brightness = (set_brightness_percentage / 100) * MAX_BRIGHTNESS

    def turn_off_lights_in_group(self, group_id: int) -> None:
        group = phue.Group(self._hue_bridge, group_id)

        log.info("Turning lights in group %s off", group_id)
        group.on = False

    def set_room_brightness(self, group_id: int, brightness_percentage: int) -> None:
        group = phue.Group(self._hue_bridge, group_id)

        on_state = True

        if brightness_percentage >= 100:
            brightness = MAX_BRIGHTNESS
        elif brightness_percentage > 0:
            brightness = (brightness_percentage / 100) * MAX_BRIGHTNESS
        else:
            brightness = 0
            on_state = False

        brightness = int(brightness)

        log.info("Setting lights in group %s to brightness %s", group_id, brightness)

        group.on = on_state
        group.brightness = brightness

    def list_light_status(self) -> List[LightGroupStatus]:
        statuses = []

        for group in self._hue_bridge.groups:
            status = LightGroupStatus(
                group_id=group.group_id,
                is_on=group.on,
                brightness=group.brightness,
                brightness_percentage=float((group.brightness / MAX_BRIGHTNESS) * 100),
            )
            statuses.append(status)

        return statuses
