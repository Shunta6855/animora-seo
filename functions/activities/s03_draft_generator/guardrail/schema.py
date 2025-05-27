# ---------------------------------------------------------------------------------  # 
# 　　　　　　                  Pydanticを用いて構文・制約チェック　　　               　　　 #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
from pydantic import BaseModel, Field, field_validator
from typing import Annotated

# ----------------------------------
# Pydantic Schema
# ----------------------------------
class Section(BaseModel):
    h2: str = Field(..., min_length=15, max_length=45)
    h3_list: Annotated[list[str], Field(min_items=1, max_items=3)]
    class Config:
        extra = "forbid"

class Outline(BaseModel):
    title: str = Field(..., max_length=32)
    h2_list: Annotated[list[Section], Field(min_items=3, max_items=3)]
    class Config:
        extra = "forbid"

class SectionAll(BaseModel):
    h2: str = Field(..., min_length=15, max_length=45)
    h3_list: Annotated[list[str], Field(min_items=1, max_items=3)]
    content_list: Annotated[list[str], Field(min_items=1, max_items=3)]

    @field_validator("content_list")
    def content_length(cls, v):
        for content in v:
            if not (200 <= len(content) <= 2_500):
                raise ValueError("content length must be between 300 and 2500")
        return v

    class Config:
        extra = "forbid"

class Draft(BaseModel):
    title: str = Field(..., max_length=32)
    h2_list: Annotated[list[SectionAll], Field(min_items=3, max_items=3)]
    
    @field_validator("h2_list")
    def unique_headings(cls, v):
        hs = [s.h2 for s in v]
        assert len(hs) == len(set(hs)), "duplicate H2"
        return v
