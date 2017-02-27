import json
import logging
from typing import Any
from typing import Dict

import apiai


log = logging.getLogger(__name__)


class ApiAIClient:
    def __init__(self, client_access_token: str) -> None:
        self._ai_client = apiai.ApiAI(client_access_token)

    def text_query(self, query: str) -> Dict[str, Any]:
        request = self._ai_client.text_request()
        request.query = query

        response = request.getresponse()
        return json.loads(response.read().decode())
