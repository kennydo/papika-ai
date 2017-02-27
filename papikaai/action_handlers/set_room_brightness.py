import logging

from papikaai.action_handlers import BaseActionHandler

log = logging.getLogger(__name__)


class SetRoomBrightness(BaseActionHandler):
    def execute(self, slack_context, parameters):
        log.info("Executing parameters: %s", parameters)
