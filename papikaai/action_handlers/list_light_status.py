import logging

from papikaai.action_handlers import BaseActionHandler

log = logging.getLogger(__name__)


class ListLightStatus(BaseActionHandler):
    def execute(self, slack_context, parameters):
        log.info("Executing parameters: %s", parameters)

        statuses = self.bot.hue_client.list_light_status()

        lines = ["Room light statuses:"]
        for status in statuses:
            room = self.bot.room_db.hue_group_id_to_room.get(status.group_id)

            if not room:
                continue

            if status.is_on:
                line = ":full_moon: {0}: {1}%".format(room.human_name, status.brightness_percentage)
            else:
                line = ":new_moon: {0}: off".format(room.human_name)

            lines.append(line)

        self.bot.papika_client.send_message(
            slack_context.channel,
            "\n".join(lines),
        )

