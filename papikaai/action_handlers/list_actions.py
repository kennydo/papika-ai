import logging

from papikaai.action_handlers import BaseActionHandler

log = logging.getLogger(__name__)


class ListActions(BaseActionHandler):
    def execute(self, slack_context, parameters):
        user_id = slack_context.user
        all_actions = sorted(self.bot.action_handlers.keys())

        allowed_actions = []
        disallowed_actions = []

        for action in all_actions:
            has_access = self.bot.acl_engine.has_access_to_action(user_id=user_id, action=action)

            if has_access:
                allowed_actions.append(action)
            else:
                disallowed_actions.append(action)

        lines = []

        if allowed_actions:
            lines.append("User <@{0}> has access to these actions:".format(user_id))
            lines.append(', '.join('`{0}`'.format(a) for a in allowed_actions))

        if disallowed_actions:
            lines.append("User <@{0}> does not have access to these actions:".format(user_id))
            lines.append(', '.join('`{0}`'.format(a) for a in disallowed_actions))

        self.bot.papika_client.send_message(
            slack_context.channel,
            "\n".join(lines),
        )
