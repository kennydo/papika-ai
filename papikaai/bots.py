import logging
import pkg_resources
from typing import Optional

from papikaai.action_handlers.fallback import Fallback
from papikaai.clients.api_ai import ApiAIClient
from papikaai.clients.hue import HueClient
from papikaai.clients.papika import PapikaClient
from papikaai.config import load_from_env_var_path
from papikaai.contexts import SlackContext
from papikaai.room_dbs import RoomDB

log = logging.getLogger(__name__)


class PapikaAIBot:
    def __init__(self) -> None:
        log.info("Loading configuration")
        self.config = load_from_env_var_path()

        log.info("Creating Api.AI client")
        self.api_ai_client = ApiAIClient(self.config['apiai']['client_access_token'])

        log.info("Creating Hue client")
        self.hue_client = HueClient(
            ip=self.config['hue']['bridge_ip'],
            username=self.config['hue']['bridge_username'],
        )

        log.info("Creating Papika client")
        self.papika_client = PapikaClient(
            bootstrap_servers=self.config['kafka']['bootstrap_servers'],
            group_id=self.config['kafka']['inbound_group_id'],
            inbound_topic=self.config['kafka']['inbound_topic'],
            outbound_topic=self.config['kafka']['outbound_topic'],
        )

        self.command_prefix = self.config['papika_ai']['command_prefix']
        self.admin_user = self.config['papika_ai']['admin_user']

        log.info("Loading action handlers")
        # Map Api.AI actions to classes to handle it
        self.action_handlers = {}

        group = 'papika_ai.action_handlers'
        for entry_point in pkg_resources.iter_entry_points(group):
            action = entry_point.name
            handler_class = entry_point.load()
            self.action_handlers[action] = handler_class

        # Load rooms
        log.info("Loading room data")
        self.room_db = RoomDB(self.config['rooms'])

    def extract_command_from_slack_message(self, text: str) -> Optional[str]:
        """Returns the command string if the text starts with the command prefix, else returns `None`."""
        if not text:
            return None

        text = text.strip()
        if not text.startswith(self.command_prefix):
            log.debug("Ignoring message since it doesn't have command prefix: %s", text)
            return None

        return text[len(self.command_prefix) + 1:]

    def handle_slack_event(self, event) -> None:
        command = self.extract_command_from_slack_message(event.get('text'))
        if not command:
            return

        slack_context = SlackContext.from_slack_event(event)

        log.info("Slack context %s command: %s", slack_context, command)

        # TODO: handle acls, handle intent routing better
        response = self.api_ai_client.text_query(command)

        action = response['result']['action']

        if slack_context.user != self.admin_user:
            log.info("Ignoring unauthorized command (%s) from user %s: %s", action, slack_context.user, command)
            self.papika_client.send_message(
                slack_context.channel,
                "User <@{0}> does not have permission to execute action `{1}` :smug_papika:".format(
                    slack_context.user, action),
            )
            return

        log.info("Parsed command '%s' into action: %s", command, action)

        handler_class = self.action_handlers.get(action)
        if not handler_class:
            log.info("Did not have registered action handler for action '%s', defaulting to fallback", action)
            handler_class = Fallback

        handler = handler_class(self)
        parameters = response['result']['parameters']
        handler.execute(slack_context, parameters)

    def run(self) -> None:
        log.info("Starting run loop")
        for event in self.papika_client.yield_slack_events():
            self.handle_slack_event(event)
