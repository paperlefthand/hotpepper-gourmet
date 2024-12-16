import math
import sys
from typing import Any

from pydantic import BaseModel, Field, HttpUrl, model_validator


class LargeServiceArea(BaseModel, frozen=True):
    code: str | None = Field(default=None)
    name: str | None = Field(default=None)


class ServiceArea(BaseModel, frozen=True):
    code: str | None = Field(default=None)
    name: str | None = Field(default=None)


class LargeArea(BaseModel, frozen=True):
    code: str | None = Field(default=None)
    name: str | None = Field(default=None)


class MiddleArea(BaseModel, frozen=True):
    code: str | None = Field(default=None)
    name: str | None = Field(default=None)


class SmallArea(BaseModel, frozen=True):
    code: str | None = Field(default=None)
    name: str | None = Field(default=None)


class Genre(BaseModel, frozen=True):
    code: str | None = Field(default=None)
    name: str | None = Field(default=None)
    catch: str | None = Field(default=None)


class SubGenre(BaseModel, frozen=True):
    code: str | None = Field(default=None)
    name: str | None = Field(default=None)


class Budget(BaseModel, frozen=True):
    average: str | None = Field(default=None)
    code: str | None = Field(default=None)
    name: str | None = Field(default=None)


class Urls(BaseModel, frozen=True):
    pc: HttpUrl | None = Field(default=None)


class PhotoPc(BaseModel, frozen=True):
    l: HttpUrl | None = Field(default=None)
    m: HttpUrl | None = Field(default=None)
    s: HttpUrl | None = Field(default=None)


class PhotoMobile(BaseModel, frozen=True):
    l: HttpUrl | None = Field(default=None)
    s: HttpUrl | None = Field(default=None)


class Photo(BaseModel, frozen=True):
    pc: PhotoPc | None = Field(default=None)
    mobile: PhotoMobile | None = Field(default=None)


class CouponUrls(BaseModel, frozen=True):
    pc: HttpUrl | None = Field(default=None)
    sp: HttpUrl | None = Field(default=None)


# NOTE 項目なしor空文字が来たらNoneとなるように前処理する
class Shop(BaseModel, frozen=True):
    """お店データを保持するクラス"""

    id: str | None = Field(default=None)
    name: str | None = Field(default=None)
    logo_image: HttpUrl | None = Field(default=None)
    name_kana: str | None = Field(default=None)
    address: str | None = Field(default=None)
    station_name: str | None = Field(default=None)
    ktai_coupon: int | None = Field(default=None)
    large_service_area: LargeServiceArea | None = Field(default=None)
    service_area: ServiceArea | None = Field(default=None)
    large_area: LargeArea | None = Field(default=None)
    middle_area: MiddleArea | None = Field(default=None)
    small_area: SmallArea | None = Field(default=None)
    lat: float | None = Field(default=None)
    lng: float | None = Field(default=None)
    genre: Genre | None = Field(default=None)
    sub_genre: SubGenre | None = Field(default=None)
    budget: Budget | None = Field(default=None)
    budget_memo: str | None = Field(default=None)
    catch: str | None = Field(default=None)
    capacity: int | None = Field(default=None)
    access: str | None = Field(default=None)
    mobile_access: str | None = Field(default=None)
    urls: Urls | None = Field(default=None)
    photo: Photo | None = Field(default=None)
    open: str | None = Field(default=None)
    close: str | None = Field(default=None)
    party_capacity: int | None = Field(default=None)
    wifi: str | None = Field(default=None)
    wedding: str | None = Field(default=None)
    course: str | None = Field(default=None)
    free_drink: str | None = Field(default=None)
    free_food: str | None = Field(default=None)
    private_room: str | None = Field(default=None)
    horigotatsu: str | None = Field(default=None)
    tatami: str | None = Field(default=None)
    card: str | None = Field(default=None)
    non_smoking: str | None = Field(default=None)
    charter: str | None = Field(default=None)
    ktai: str | None = Field(default=None)
    parking: str | None = Field(default=None)
    barrier_free: str | None = Field(default=None)
    other_memo: str | None = Field(default=None)
    sommelier: str | None = Field(default=None)
    open_air: str | None = Field(default=None)
    show: str | None = Field(default=None)
    equipment: str | None = Field(default=None)
    karaoke: str | None = Field(default=None)
    band: str | None = Field(default=None)
    tv: str | None = Field(default=None)
    english: str | None = Field(default=None)
    pet: str | None = Field(default=None)
    child: str | None = Field(default=None)
    lunch: str | None = Field(default=None)
    midnight: str | None = Field(default=None)
    shop_detail_memo: str | None = Field(default=None)
    coupon_urls: CouponUrls | None = Field(default=None)

    @model_validator(mode="before")
    def check_empty_values(cls, data: dict[str, Any]) -> dict[str, Any]:
        return {key: (value if bool(value) else None) for key, value in data.items()}

    def meters_to_point(self, lat: float, lng: float) -> int:
        if (self.lat is None) or (self.lng is None):
            return sys.maxsize
        else:
            km = 6371 * math.acos(
                math.sin(math.radians(lat)) * math.sin(math.radians(self.lat))
                + math.cos(math.radians(lat))
                * math.cos(math.radians(self.lat))
                * math.cos(math.radians(lng) - math.radians(self.lng))
            )
            return int(1000 * km)
