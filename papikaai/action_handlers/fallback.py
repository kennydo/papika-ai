import logging

from papikaai.action_handlers import BaseActionHandler

log = logging.getLogger(__name__)


class Fallback(BaseActionHandler):
    def execute(self, slack_context, parameters):
        log.info("Unknown intent")

        self.bot.papika_client.send_message(
            slack_context.channel,
            'Unrecognized command!',
        )
