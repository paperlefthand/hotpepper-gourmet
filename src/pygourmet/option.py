"""リクエストパラメータ定義モジュール。

このモジュールは、ホットペッパーグルメ検索APIに送信するリクエストパラメータを定義します。
詳細な仕様については、[ホットペッパーWebサービス APIリファレンス](https://webservice.recruit.co.jp/doc/hotpepper/reference.html)を参照してください。
"""

from pydantic import BaseModel, Field, field_serializer


class Option(BaseModel, frozen=True):
    """グルメ検索APIのリクエストパラメータを保持するクラス。

    APIキー(`key`)およびレスポンス形式(`format`)はクライアント内部で自動的に設定されるため、
    このクラスで明示的に指定することはできません。

    Attributes:
        id (str | None): お店ID。
        name (str | None): お店名。
        name_kana (str | None): お店名かな。
        name_any (str | None): お店名名称検索。
        tel (str | None): 電話番号。
        address (str | None): 住所。
        special (str | None): 特集コード。
        special_or (str | None): 特集コード（OR検索）。
        special_category (str | None): 特集カテゴリコード。
        special_category_or (str | None): 特集カテゴリコード（OR検索）。
        large_service_area (str | None): 大サービスエリアコード。
        service_area (str | None): サービスエリアコード。
        large_area (str | None): 大エリアコード。
        middle_area (str | None): 中エリアコード。
        small_area (str | None): 小エリアコード。
        keyword (str | None): キーワード。
        lat (float | None): 緯度（世界測地系）。
        lng (float | None): 経度（世界測地系）。
        range (int): 検索範囲（1: 300m, 2: 500m, 3: 1000m, 4: 2000m, 5: 3000m）。デフォルトは3(1000m)。
        datum (str | None): 測地系（world: 世界測地系, tokyo: 日本測地系）。デフォルトはworld。
        ktai_coupon (int | None): 携帯クーポン有無（1: あり, 0: なし）。
        genre (str | None): ジャンルコード。
        budget (str | list[str] | None): 予算コード。2つまで指定可能。
        party_capacity (int | None): 最大宴会収容人数以上で絞り込む整数値。
        wifi (bool | None): Wi-Fi有無。
        wedding (bool | None): ウェディング・二次会。
        course (bool | None): コースあり。
        free_drink (bool | None): 飲み放題あり。
        free_food (bool | None): 食べ放題あり。
        private_room (bool | None): 個室あり。
        horigotatsu (bool | None): 掘りごたつあり。
        tatami (bool | None): 座敷あり。
        cocktail (bool | None): カクテル充実。
        shochu (bool | None): 焼酎充実。
        sake (bool | None): 日本酒充実。
        wine (bool | None): ワイン充実。
        card (bool | None): カード決済OK。
        non_smoking (bool | None): 禁煙席あり。
        charter (bool | None): 貸切可。
        ktai (bool | None): 携帯電話OK。
        parking (bool | None): 駐車場あり。
        barrier_free (bool | None): バリアフリー。
        sommelier (bool | None): ソムリエがいる。
        night_view (bool | None): 夜景が見える。
        open_air (bool | None): オープンエア。
        show (bool | None): ライブ・ショーあり。
        equipment (bool | None): エンタメ設備。
        karaoke (bool | None): カラオケあり。
        band (bool | None): バンド演奏可。
        tv (bool | None): TV・プロジェクター。
        lunch (bool | None): ランチあり。
        midnight (bool | None): 23時以降も営業。
        midnight_meal (bool | None): 23時以降食事OK。
        english (bool | None): 英語メニューあり。
        pet (bool | None): ペット可。
        child (bool | None): お子様連れOK。
        credit_card (str | list[str] | None): クレジットカード。2つまで指定可能。
        type (str | None): 検索タイプ（lite: 軽量版）。
        order (int): ソート順。デフォルトは4。
        start (int | None): 検索開始位置。
        count (int | None): 検索件数。
    """

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
    party_capacity: int | None = Field(default=None, description="最大宴会収容人数以上")
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
        """真偽値をAPI形式（0または1）に変換します。

        Args:
            v (bool | None): 変換前の真偽値。

        Returns:
            int | None: 変換後の値。
        """
        if v is None:
            return None
        return 1 if v else 0

    @field_serializer("budget", "credit_card")
    def serialize_list(self, v: str | list[str] | None) -> str | None:
        """リストをAPI形式（カンマ区切り文字列）に変換します。

        Args:
            v (str | list[str] | None): 変換前の値。

        Returns:
            str | None: 変換後のカンマ区切り文字列。
        """
        if isinstance(v, list):
            return ",".join(v)
        return v
