from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

HundredScale = Annotated[int, Field(ge=0, le=100)]


class RatingResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    rating: Annotated[
        HundredScale,
        Field(description="Predicted rating for the requested scent aspect."),
    ]
    reference: Annotated[
        str, Field(description="Reference molecule used to make prediction.")
    ]
    explanation: Annotated[
        str, Field(description="Justification for the given predictions.")
    ]


def get_response_pydantic(response_type):
    if response_type == "rating":
        return RatingResponse


def get_response_schema(response_type) -> dict:
    if response_type == "rating":
        return RatingResponse.model_json_schema()
