from typing import Dict


class SlackContext:
    def __init__(self, *, channel: str, user: str) -> None:
        self.channel = channel
        self.user = user

    @classmethod
    def from_slack_event(cls, slack_event: Dict):
        channel = slack_event.get('channel')
        user = slack_event.get('user')
        return cls(
            channel=channel,
            user=user,
        )

    def __repr__(self) -> str:
        return '<SlackContext channel={channel} user={user}>'.format(
            channel=self.channel,
            user=self.user,
        )
