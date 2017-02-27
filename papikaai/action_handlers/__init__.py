from typing import Any
from typing import Dict


class BaseActionHandler:
    def __init__(self, bot: 'PapikaAIBot') -> None:
        self.bot = bot

    def execute(self, slack_context: 'SlackContext', parameters: Dict[str, Any]) -> None:
        raise NotImplementedError()
