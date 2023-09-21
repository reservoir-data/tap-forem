"""REST client handling, including ForemStream base class."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Sequence

from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.pagination import BasePageNumberPaginator
from singer_sdk.streams import RESTStream

if TYPE_CHECKING:
    import requests

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class ForemPaginator(BasePageNumberPaginator):
    """A paginator for Forem endpoints."""

    def has_more(self, response: requests.Response) -> bool:
        """Whether the endpoint has more records.

        Returns:
            True if the endpoint has more data to sync.
        """
        return len(response.json()) > 0


class ForemStream(RESTStream):
    """Forem stream class."""

    records_jsonpath = "$[*]"

    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize Forem stream."""
        super().__init__(*args, **kwargs)

        # "List" is invariant -- see
        # https://mypy.readthedocs.io/en/stable/common_issues.html#variance
        # Consider using "Sequence" instead, which is covariant
        self.child_streams: Sequence[ForemStream] = []

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
        return {"User-Agent": f"{self.tap_name}/{self._tap.plugin_version}"}

    def should_sync(
        self,
        context: dict | None,  # noqa: ARG002
    ) -> bool:
        """Check whether stream should be synced based on context."""
        return True

    def _sync_children(self, child_context: dict) -> None:
        for child_stream in self.child_streams:
            if (
                child_stream.selected or child_stream.has_selected_descendents
            ) and child_stream.should_sync(child_context):
                child_stream.sync(context=child_context)


class PaginatedForemStream(ForemStream):
    """Forem stream with pagination."""

    def get_new_paginator(self) -> ForemPaginator:
        """Get a fresh paginator.

        Returns:
            A new paginator for the Forem API.
        """
        return ForemPaginator(1)

    def get_url_params(
        self,
        context: dict | None,  # noqa: ARG002
        next_page_token: Any | None,  # noqa: ANN401
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        return {
            "page": next_page_token,
            "per_page": self._page_size,
        }
