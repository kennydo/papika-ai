import logging
from typing import Any
from typing import List
from typing import NamedTuple

log = logging.getLogger(__name__)


RoomEntry = NamedTuple('RoomEntry', [
    ('human_name', str),
    ('hue_group_id', int),
    ('apiai_entity_name', str),
])


class RoomDB:
    def __init__(self, rooms: List[Any]) -> None:
        self._rooms = []

        # Create the mappings we'll need later
        self.apiai_entity_name_to_room = {}
        self.hue_group_id_to_room = {}

        log.info("Loading %s rooms", len(rooms))

        for room in rooms:
            human_name = room['human_name']
            hue_group_id = int(room['hue_group_id'])
            apiai_entity_name = room['apiai_entity_name']

            room_entry = RoomEntry(
                human_name=human_name,
                hue_group_id=hue_group_id,
                apiai_entity_name=apiai_entity_name,
            )

            self._rooms.append(room_entry)
            self.apiai_entity_name_to_room[apiai_entity_name] = room_entry
            self.hue_group_id_to_room[hue_group_id] = room_entry

        log.info("Finished loading rooms")
