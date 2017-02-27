import logging

from papikaai.action_handlers import BaseActionHandler

log = logging.getLogger(__name__)


class Fallback(BaseActionHandler):
    def execute(self, parameters):
        log.info("Unknown intent")
