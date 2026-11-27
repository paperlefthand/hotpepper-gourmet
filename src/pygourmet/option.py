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
        id (str | None): お店ID。カンマ区切りで20個まで指定可能。
        name (str | None): 掲載店名（部分一致）。
        name_kana (str | None): 掲載店名かな（部分一致）。
        name_any (str | None): 掲載店名または掲載店名かなのOR検索（部分一致）。
        tel (str | None): 電話番号。
        address (str | None): 住所。
        special (str | None): 特集コード（AND検索）。カンマ区切りで複数指定可能。
        special_or (str | None): 特集コード（OR検索）。カンマ区切りで複数指定可能。
        special_category (str | None): 特集カテゴリコード（AND検索）。カンマ区切りで複数指定可能。
        special_category_or (str | None): 特集カテゴリコード（OR検索）。カンマ区切りで複数指定可能。
        large_service_area (str | None): 大サービスエリアコード。
        service_area (str | None): サービスエリアコード。カンマ区切りで3個まで指定可能。
        large_area (str | None): 大エリアコード。カンマ区切りで3個まで指定可能。
        middle_area (str | None): 中エリアコード。カンマ区切りで5個まで指定可能。
        small_area (str | None): 小エリアコード。カンマ区切りで5個まで指定可能。
        keyword (str | None): キーワード。半角スペース区切りでAND検索。
        lat (float | None): 緯度。測地系は `datum` で指定したもの。
        lng (float | None): 経度。測地系は `datum` で指定したもの。
        range (int): 検索範囲（1: 300m, 2: 500m, 3: 1000m, 4: 2000m, 5: 3000m）。デフォルトは3(1000m)。
        datum (str | None): 測地系（world: 世界測地系, tokyo: 旧日本測地系）。未指定時はworld。
        ktai_coupon (int | None): 携帯クーポン掲載（0: 携帯クーポンあり, 1: 携帯クーポンなし）。未指定時は絞り込まない。
        genre (str | None): お店ジャンルコード（サブジャンルを含む）。
        budget (str | list[str] | None): 検索用ディナー予算コード。2つまで指定可能。
        party_capacity (int | None): 宴会収容人数。指定した数より大きな収容人数のお店を検索する。
        wifi (bool | None): WiFi有無。
        wedding (bool | None): ウェディング・二次会等。
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
        card (bool | None): カード可。
        non_smoking (bool | None): 禁煙席あり。
        charter (bool | None): 貸切可。
        ktai (bool | None): 携帯電話OK。
        parking (bool | None): 駐車場あり。
        barrier_free (bool | None): バリアフリー。
        sommelier (bool | None): ソムリエがいる。
        night_view (bool | None): 夜景がキレイ。
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
        credit_card (str | list[str] | None): クレジットカード種別コード。複数指定可能。
        type (str | None): 出力タイプ（lite: 主要項目のみ, credit_card: クレジットカードを付加,
            special: 特集を付加）。`+` でつないで複数指定可能。未指定時はクレジットカードと特集以外をすべて出力する。
            なお `Shop` はクレジットカードと特集のフィールドを持たないため、付加された項目は無視される。
        order (int): ソート順（1: 店名かな順, 2: ジャンルコード順, 3: 小エリアコード順, 4: おススメ順）。デフォルトは4。
            位置検索では4以外を指定すると距離順になる。
        start (int | None): 検索の開始位置。未指定時は1。
        count (int | None): 1ページあたりの取得数（1〜100）。未指定時は10。
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
        default=None, description="複数指定可能"
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
