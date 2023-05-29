

PROTEIN = 4
FAT = 9
CARB = 4

DEFAULT_REST_SEC = 10
PORT = 18082
MAXIMUM_CALORIES = 1800
MENU_CATEGORY = {
    1: "Fruit and vegetable",
    2: "Starchy food",
    3: "Dairy",
    4: "Protein",
    5: "Fat and Junk",
    6: "Supplement",
}

DIMENSIONAL_PRODUCT_TABLE = "dim_nutrition_menu"
FACT_PRODUCT_TABLE = "fct_nutrition_menu"

collection_header = [
    {"name": "nutrition_name", "label": "Name", "field": "menu_name"},
    {"name": "nutrition_amount", "label": "Amount", "field": "quantity"},
    {"name": "nutrition_amount", "label": "p", "field": "protein"},
    {"name": "nutrition_amount", "label": "f", "field": "fat"},
    {"name": "nutrition_amount", "label": "c", "field": "carb"},
    {"name": "calories", "label": "Calories", "field": "calories", "required": True,
     "sortable": True,
     "align": "left"}]


def calculating_calories(p: float, f: float, c: float) -> float:
    return p * PROTEIN + f * FAT + c * CARB


def extract_float_numbers(input_string):
    numbers = []
    current_number = ''
    for char in input_string:
        if char.isdigit() or char == '.':
            current_number += char
        elif current_number != '':
            numbers.append(current_number)
            current_number = ''
    if current_number != '':
        numbers.append(current_number)
    return numbers


def pbase_col_options(result, col_name: str):
    lst = []
    for r in result:
        dct = {
            r.id: getattr(r, col_name)
        }
        lst.append(dct)
    return lst


def updating_dict_options(lst: list, index_column: str, column_name: str) -> dict:
    dct = {item[index_column]: item[column_name] for item in lst}
    return dct


