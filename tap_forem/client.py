"""REST client handling, including ForemStream base class."""

from pathlib import Path
from typing import Any, Dict, Optional

import requests
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.streams import RESTStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class ForemStream(RESTStream):
    """Forem stream class."""

    records_jsonpath = "$[*]"

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["api_url"]

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object."""
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="api-key",
            value=self.config["api_key"],
            location="header",
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        headers["User-Agent"] = f"{self.tap_name}/{self._tap.plugin_version}"
        return headers

    def get_next_page_token(
        self,
        response: requests.Response,
        previous_token: Optional[Any],
    ) -> Any:
        """Get next page offset.

        Args:
            response: API response.
            previous_token: Previous offset.

        Returns:
            Page offset.
        """
        if not len(response.json()):
            return None

        return 1 if previous_token is None else previous_token + 1

    def get_url_params(
        self,
        context: Optional[dict],
        next_page_token: Optional[Any],
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        return {
            "page": next_page_token,
            "per_page": self._page_size,
        }
