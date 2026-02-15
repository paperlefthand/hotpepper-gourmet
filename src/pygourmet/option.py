from pydantic import BaseModel, Field, field_serializer


# NOTE
# 指定できるオプションは[APIリファレンス](https://webservice.recruit.co.jp/doc/hotpepper/reference.html)を参照
# keyとformatは指定できないようにしている
class Option(BaseModel, frozen=True):
    """検索時に指定するパラメータ"""

    id: str | None = Field(default=None)
    name: str | None = Field(default=None)
    name_kana: str | None = Field(default=None)
    name_any: str | None = Field(default=None)
    tel: str | None = Field(default=None)
    address: str | None = Field(default=None)
    special: str | None = Field(default=None)
    special_or: str | None = Field(default=None)
    special_category: str | None = Field(default=None)
    special_category_or: str | None = Field(default=None)
    large_service_area: str | None = Field(default=None)
    service_area: str | None = Field(default=None)
    large_area: str | None = Field(default=None)
    middle_area: str | None = Field(default=None)
    small_area: str | None = Field(default=None)
    keyword: str | None = Field(default=None)
    lat: float | None = Field(default=None)
    lng: float | None = Field(default=None)
    range: int = Field(default=3, ge=1, le=5, description="対象範囲(初期値1000m)")
    datum: str | None = Field(default=None)
    ktai_coupon: int | None = Field(default=None)
    genre: str | None = Field(default=None)
    budget: str | list[str] | None = Field(default=None, description="2つまで指定可能")
    party_capacity: bool | None = Field(default=None)
    wifi: bool | None = Field(default=None)
    wedding: bool | None = Field(default=None)
    course: bool | None = Field(default=None)
    free_drink: bool | None = Field(default=None)
    free_food: bool | None = Field(default=None)
    private_room: bool | None = Field(default=None)
    horigotatsu: bool | None = Field(default=None)
    tatami: bool | None = Field(default=None)
    cocktail: bool | None = Field(default=None)
    shochu: bool | None = Field(default=None)
    sake: bool | None = Field(default=None)
    wine: bool | None = Field(default=None)
    card: bool | None = Field(default=None)
    non_smoking: bool | None = Field(default=None)
    charter: bool | None = Field(default=None)
    ktai: bool | None = Field(default=None)
    parking: bool | None = Field(default=None)
    barrier_free: bool | None = Field(default=None)
    sommelier: bool | None = Field(default=None)
    night_view: bool | None = Field(default=None)
    open_air: bool | None = Field(default=None)
    show: bool | None = Field(default=None)
    equipment: bool | None = Field(default=None)
    karaoke: bool | None = Field(default=None)
    band: bool | None = Field(default=None)
    tv: bool | None = Field(default=None)
    lunch: bool | None = Field(default=None)
    midnight: bool | None = Field(default=None)
    midnight_meal: bool | None = Field(default=None)
    english: bool | None = Field(default=None)
    pet: bool | None = Field(default=None)
    child: bool | None = Field(default=None)
    credit_card: str | list[str] | None = Field(
        default=None, description="2つまで指定可能"
    )
    type: str | None = Field(default=None)
    order: int = Field(default=4)
    start: int | None = Field(default=None)
    count: int | None = Field(default=None)

    @field_serializer(
        "party_capacity",
        "wifi",
        "wedding",
        "course",
        "free_drink",
        "free_food",
        "private_room",
        "horigotatsu",
        "tatami",
        "cocktail",
        "shochu",
        "sake",
        "wine",
        "card",
        "non_smoking",
        "charter",
        "ktai",
        "parking",
        "barrier_free",
        "sommelier",
        "night_view",
        "open_air",
        "show",
        "equipment",
        "karaoke",
        "band",
        "tv",
        "lunch",
        "midnight",
        "midnight_meal",
        "english",
        "pet",
        "child",
    )
    def serialize_bool(self, v: bool | None) -> int | None:
        if v is None:
            return None
        return 1 if v else 0

    @field_serializer("budget", "credit_card")
    def serialize_list(self, v: str | list[str] | None) -> str | None:
        if isinstance(v, list):
            return ",".join(v)
        return v
