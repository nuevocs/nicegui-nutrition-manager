from dataclasses import dataclass
import datetime

jst_no_tz = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None) + datetime.timedelta(hours=9)


@dataclass
class DimProduct:
    menu_name: str
    menu_category: int
    serving_amount: float = 1
    protein: float = 0
    fat: float = 0
    carbohydrate: float = 0
    calories: float = 0
    date: str = jst_no_tz.strftime('%Y-%m-%d')


@dataclass
class FctProduct:
    menu_id: int
    quantity: float
    # menu_name: str
    date: str = jst_no_tz.strftime('%Y-%m-%d')


@dataclass
class Collection:
    menu_name: str
    protein: str
    fat: str
    carb: str
    calories: str
    quantity: float
