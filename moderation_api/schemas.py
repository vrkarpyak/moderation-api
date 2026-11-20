from pydantic import BaseModel, ConfigDict, Field


class item_request(BaseModel):
    model_config = ConfigDict(
        strict=True,
        str_strip_whitespace=True,
        extra="forbid",
    )

    seller_id: int = Field(gt=0)
    is_verified_seller: bool
    item_id: int = Field(gt=0)
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    category: int = Field(gt=0)
    images_qty: int = Field(ge=0)
