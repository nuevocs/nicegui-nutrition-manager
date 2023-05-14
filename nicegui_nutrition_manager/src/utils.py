PROTEIN = 4
FAT = 9
CARB = 4


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
