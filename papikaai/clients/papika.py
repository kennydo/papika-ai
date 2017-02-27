import json
import logging

from typing import List

import kafka

log = logging.getLogger(__name__)


class PapikaClient:
    def __init__(
        self,
        *,
        bootstrap_servers: List[str],
        group_id: str,
        inbound_topic: str,
        outbound_topic: str
    ) -> None:
        self._outbound_topic = outbound_topic

        api_version = (0, 9)

        self._kafka_producer = kafka.KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            api_version=api_version,
        )
        self._kafka_consumer = kafka.KafkaConsumer(
            inbound_topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            api_version=api_version,
        )

    def yield_slack_events(self):
        for event in self._kafka_consumer:
            try:
                slack_event = json.loads(event.value.decode())['event']
            except Exception:
                log.exception("Skipping event because it could not be decoded: %s", event.value)
                continue

            if slack_event.get('type') != 'message':
                log.debug("Ignoring non-message slack event: %s", slack_event)
                continue

            yield slack_event

    def send_message(self, channel: str, text: str) -> None:
        value = json.dumps({
            'channel': channel,
            'text': text,
        }).encode()

        self._kafka_producer.send(
            self._outbound_topic,
            value=value,
        )
