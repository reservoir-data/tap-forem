"""Stream type classes for tap-forem."""

from typing import Any, Dict, Optional

from singer_sdk import typing as th

from tap_forem.client import ForemStream

USER_TYPE = th.ObjectType(
    th.Property("name", th.StringType),
    th.Property("username", th.StringType),
    th.Property("twitter_username", th.StringType),
    th.Property("github_username", th.StringType),
    th.Property("website_url", th.StringType),
    th.Property("profile_image", th.StringType),
    th.Property("profile_image_90", th.StringType),
)

ORG_TYPE = th.ObjectType(
    th.Property("name", th.StringType),
    th.Property("username", th.StringType),
    th.Property("slug", th.StringType),
    th.Property("profile_image", th.StringType),
    th.Property("profile_image_90", th.StringType),
)

FLARE_TAG_TYPE = th.ObjectType(
    th.Property("name", th.StringType),
    th.Property("bg_color_hex", th.StringType),
    th.Property("text_color_hex", th.StringType),
)


class Articles(ForemStream):
    """Articles stream."""

    name = "articles"
    path = "/articles"
    primary_keys = ["id"]

    schema = th.PropertiesList(
        th.Property(
            "id",
            th.IntegerType,
            description="The article's system ID",
            required=True,
        ),
        th.Property("type_of", th.StringType),
        th.Property("title", th.StringType),
        th.Property("description", th.StringType),
        th.Property("cover_image", th.StringType),
        th.Property("social_image", th.StringType),
        th.Property("city", th.StringType),
        th.Property("slug", th.StringType),
        th.Property("path", th.StringType),
        th.Property("url", th.StringType),
        th.Property("canonical_url", th.StringType),
        th.Property("created_at", th.DateTimeType),
        th.Property("edited_at", th.DateTimeType),
        th.Property("crossposted_at", th.DateTimeType),
        th.Property("published_at", th.DateTimeType),
        th.Property("last_comment_at", th.DateTimeType),
        th.Property("tag_list", th.ArrayType(th.StringType)),
        th.Property("collection_id", th.IntegerType),
        th.Property("reading_time_minutes", th.IntegerType),
        th.Property("comments_count", th.IntegerType),
        th.Property("positive_reactions_count", th.IntegerType),
        th.Property("public_reactions_count", th.IntegerType),
        th.Property("page_views_count", th.IntegerType),
        th.Property("user", USER_TYPE),
        th.Property("organization", ORG_TYPE),
        th.Property("flare_tag", FLARE_TAG_TYPE),
    ).to_dict()

    def get_url_params(
        self,
        context: Optional[dict],
        next_page_token: Optional[Any],
    ) -> Dict[str, Any]:
        """Get query parameters."""
        params = super().get_url_params(context, next_page_token)
        params["tag"] = self.config.get("tag")
        return params

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Get context for article children."""
        return {"article_id": record["id"]}


class Comments(ForemStream):
    """Comments stream."""

    name = "comments"
    path = "/comments"
    primary_keys = ["id"]
    parent_stream_type = Articles

    schema = th.PropertiesList().to_dict()

    def get_url_params(
        self,
        context: Optional[dict],
        next_page_token: Optional[Any],
    ) -> Dict[str, Any]:
        """Get query parameters."""
        params = super().get_url_params(context, next_page_token)
        if context:
            params["a_id"] = context["article_id"]
        return params
