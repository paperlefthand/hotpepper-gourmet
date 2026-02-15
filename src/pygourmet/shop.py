"""レスポンスモデル定義モジュール。

このモジュールは、ホットペッパーグルメ検索APIから返却される店舗データのモデルを定義します。
"""

import math
import sys
from typing import Any

from pydantic import BaseModel, Field, HttpUrl, model_validator


class LargeServiceArea(BaseModel, frozen=True):
    """大サービスエリア情報を保持するクラス。

    Attributes:
        code (str | None): 大サービスエリアコード。
        name (str | None): 大サービスエリア名。
    """

    code: str | None = Field(default=None)
    name: str | None = Field(default=None)


class ServiceArea(BaseModel, frozen=True):
    """サービスエリア情報を保持するクラス。

    Attributes:
        code (str | None): サービスエリアコード。
        name (str | None): サービスエリア名。
    """

    code: str | None = Field(default=None)
    name: str | None = Field(default=None)


class LargeArea(BaseModel, frozen=True):
    """大エリア情報を保持するクラス。

    Attributes:
        code (str | None): 大エリアコード。
        name (str | None): 大エリア名。
    """

    code: str | None = Field(default=None)
    name: str | None = Field(default=None)


class MiddleArea(BaseModel, frozen=True):
    """中エリア情報を保持するクラス。

    Attributes:
        code (str | None): 中エリアコード。
        name (str | None): 中エリア名。
    """

    code: str | None = Field(default=None)
    name: str | None = Field(default=None)


class SmallArea(BaseModel, frozen=True):
    """小エリア情報を保持するクラス。

    Attributes:
        code (str | None): 小エリアコード。
        name (str | None): 小エリア名。
    """

    code: str | None = Field(default=None)
    name: str | None = Field(default=None)


class Genre(BaseModel, frozen=True):
    """ジャンル情報を保持するクラス。

    Attributes:
        code (str | None): ジャンルコード。
        name (str | None): ジャンル名。
        catch (str | None): ジャンルキャッチ。
    """

    code: str | None = Field(default=None)
    name: str | None = Field(default=None)
    catch: str | None = Field(default=None)


class SubGenre(BaseModel, frozen=True):
    """サブジャンル情報を保持するクラス。

    Attributes:
        code (str | None): サブジャンルコード。
        name (str | None): サブジャンル名。
        catch (str | None): サブジャンルキャッチ。
    """

    code: str | None = Field(default=None)
    name: str | None = Field(default=None)
    catch: str | None = Field(default=None)


class Budget(BaseModel, frozen=True):
    """予算情報を保持するクラス。

    Attributes:
        average (str | None): 予算備考。
        code (str | None): 予算コード。
        name (str | None): 予算名。
    """

    average: str | None = Field(default=None)
    code: str | None = Field(default=None)
    name: str | None = Field(default=None)


class Urls(BaseModel, frozen=True):
    """お店URL情報を保持するクラス。

    Attributes:
        pc (HttpUrl | None): PC向けURL。
        qr (HttpUrl | None): QRコードURL。
        mobile (HttpUrl | None): 携帯向けURL。
    """

    pc: HttpUrl | None = Field(default=None)
    qr: HttpUrl | None = Field(default=None)
    mobile: HttpUrl | None = Field(default=None)


class PhotoPc(BaseModel, frozen=True):
    """PC向け写真URL情報を保持するクラス。

    Attributes:
        l (HttpUrl | None): 写真Lサイズ。
        m (HttpUrl | None): 写真Mサイズ。
        s (HttpUrl | None): 写真Sサイズ。
    """

    l: HttpUrl | None = Field(default=None)
    m: HttpUrl | None = Field(default=None)
    s: HttpUrl | None = Field(default=None)


class PhotoMobile(BaseModel, frozen=True):
    """携帯向け写真URL情報を保持するクラス。

    Attributes:
        l (HttpUrl | None): 写真Lサイズ。
        s (HttpUrl | None): 写真Sサイズ。
    """

    l: HttpUrl | None = Field(default=None)
    s: HttpUrl | None = Field(default=None)


class Photo(BaseModel, frozen=True):
    """写真URL情報を保持するクラス。

    Attributes:
        pc (PhotoPc | None): PC向け写真URL。
        mobile (PhotoMobile | None): 携帯向け写真URL。
    """

    pc: PhotoPc | None = Field(default=None)
    mobile: PhotoMobile | None = Field(default=None)


class CouponUrls(BaseModel, frozen=True):
    """クーポンURL情報を保持するクラス。

    Attributes:
        pc (HttpUrl | None): PC向けクーポンURL。
        sp (HttpUrl | None): スマートフォン向けクーポンURL。
    """

    pc: HttpUrl | None = Field(default=None)
    sp: HttpUrl | None = Field(default=None)


class Shop(BaseModel, frozen=True):
    """お店データを保持するクラス。

    Attributes:
        id (str | None): お店ID。
        name (str | None): お店名。
        logo_image (HttpUrl | None): ロゴ画像URL。
        name_kana (str | None): お店名かな。
        address (str | None): 住所。
        station_name (str | None): 最寄駅名。
        ktai_coupon (int | None): 携帯クーポン有無。
        large_service_area (LargeServiceArea | None): 大サービスエリア。
        service_area (ServiceArea | None): サービスエリア。
        large_area (LargeArea | None): 大エリア。
        middle_area (MiddleArea | None): 中エリア。
        small_area (SmallArea | None): 小エリア。
        lat (float | None): 緯度。
        lng (float | None): 経度。
        genre (Genre | None): ジャンル。
        sub_genre (SubGenre | None): サブジャンル。
        budget (Budget | None): 予算。
        budget_memo (str | None): 予算備考。
        catch (str | None): キャッチコピー。
        capacity (int | None): 総席数。
        access (str | None): 交通アクセス。
        mobile_access (str | None): 携帯用交通アクセス。
        urls (Urls | None): お店URL。
        photo (Photo | None): 写真URL。
        open (str | None): 営業時間。
        close (str | None): 定休日。
        party_capacity (int | None): 最大宴会収容人数。
        wifi (str | None): Wi-Fi。
        wedding (str | None): ウェディング・二次会。
        course (str | None): コース。
        free_drink (str | None): 飲み放題。
        free_food (str | None): 食べ放題。
        private_room (str | None): 個室。
        horigotatsu (str | None): 掘りごたつ。
        tatami (str | None): 座敷。
        card (str | None): カード決済OK。
        non_smoking (str | None): 禁煙席。
        charter (str | None): 貸切可。
        ktai (str | None): 携帯電話OK。
        parking (str | None): 駐車場。
        barrier_free (str | None): バリアフリー。
        other_memo (str | None): その他設備。
        sommelier (str | None): ソムリエ。
        open_air (str | None): オープンエア。
        show (str | None): ライブ・ショー。
        equipment (str | None): エンタメ設備。
        karaoke (str | None): カラオケ。
        band (str | None): バンド演奏可。
        tv (str | None): TV・プロジェクター。
        english (str | None): 英語メニュー。
        pet (str | None): ペット。
        child (int | str | None): お子様連れ。
        lunch (str | None): ランチ。
        midnight (str | None): 23時以降も営業。
        midnight_meal (str | None): 23時以降食事OK。
        shop_detail_memo (str | None): お店詳細備考。
        coupon_urls (CouponUrls | None): クーポンURL。
    """

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
    child: Any | None = Field(default=None)
    lunch: str | None = Field(default=None)
    midnight: str | None = Field(default=None)
    midnight_meal: str | None = Field(default=None)
    shop_detail_memo: str | None = Field(default=None)
    coupon_urls: CouponUrls | None = Field(default=None)

    @model_validator(mode="before")
    @classmethod
    def check_empty_values(cls, data: dict[str, Any]) -> dict[str, Any]:
        """空の値をNoneに変換します。

        Args:
            data (dict[str, Any]): 変換前のデータ。

        Returns:
            dict[str, Any]: 変換後のデータ。
        """
        return {key: (value if bool(value) else None) for key, value in data.items()}

    def meters_to_point(self, lat: float, lng: float) -> int:
        """指定された座標からお店までの距離（メートル）を計算します。

        Args:
            lat (float): 基準地点の緯度。
            lng (float): 基準地点の経度。

        Returns:
            int: 基準地点からお店までの距離（メートル）。緯度または経度が不明な場合は sys.maxsize を返します。
        """
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
