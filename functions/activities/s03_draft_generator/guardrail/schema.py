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
    h2_list: Annotated[Section, Field(min_items=3, max_items=6)]
    class Config:
        extra = "forbid"

class SectionAll(BaseModel):
    h2: str = Field(..., min_length=15, max_length=45)
    h3_list: Annotated[list[str], Field(min_items=1, max_items=3)]
    content: str = Field(..., min_length=300, max_length=2_500)
    class Config:
        extra = "forbid"

class Draft(BaseModel):
    title: str = Field(..., max_length=32)
    h2_list: Annotated[SectionAll, Field(min_items=3, max_items=6)]
    
    @field_validator("h2_list")
    def unique_headings(cls, v):
        hs = [s.h2 for s in v]
        assert len(hs) == len(set(hs)), "duplicate H2"
        return v
