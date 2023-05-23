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
