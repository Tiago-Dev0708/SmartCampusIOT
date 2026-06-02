"""Base Pydantic schema with automatic snake_case → camelCase aliasing.

Every schema exposed by the REST API should inherit from ``BaseSchema``
so that JSON output uses the camelCase convention expected by the
React Native frontend while Python code stays snake_case.
"""

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    """Global base with camelCase serialisation and ORM compat."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
