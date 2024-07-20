from typing import Optional

from pydantic import BaseModel, Field


class Option(BaseModel, frozen=True):
    """検索時に指定するパラメータ"""

    keyword: Optional[str] = None  # HACK
    lat: Optional[float] = None  # HACK
    lng: Optional[float] = None  # HACK
    radius: int = Field(500, ge=0, description="対象範囲(m)")
    count: int = Field(10, ge=1, le=100, description="取得件数")

    # def __str__(self):
    #     return f"{self.name}: {self.value}"

    # def __repr__(self):
    #     return f"Option({self.name}, {self.value})"

    # def __eq__(self, other):
    #     return self.name == other.name and self.value == other.value

    # def __hash__(self):
    #     return hash((self.name, self.value))
