import logging

from papikaai.action_handlers import BaseActionHandler

log = logging.getLogger(__name__)


class TurnOffRoomLights(BaseActionHandler):
    def execute(self, slack_context, parameters):
        log.info("Executing parameters: %s", parameters)

        room_entity_name = parameters['room']
        if not room_entity_name:
            # Default to turning off the lights in the living room
            room_entity_name = 'living_room'

        room = self.bot.room_db.apiai_entity_name_to_room.get(room_entity_name)

        if not room:
            self.bot.papika_client.send_message(
                slack_context.channel,
                "I don't know which room that is",
            )
            return

        self.bot.papika_client.send_message(
            slack_context.channel,
            "Turning off the lights in {0}".format(room.human_name),
        )
        self.bot.hue_client.turn_off_lights_in_group(room.hue_group_id)


