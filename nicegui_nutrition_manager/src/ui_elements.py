from nicegui import ui
from .playwright_scraping import get_search_result, get_nutrition_detail
from .utils import extract_float_numbers, calculating_calories

SITE_TITLE = "Nutrition Manager"


def page_layout_consumbles() -> None:
    with ui.header(elevated=True).style('background-color: #333333').classes('items-center justify-between'):
        ui.label(SITE_TITLE).classes("text-xl text-center")


class InputControl:
    def __init__(self):
        with ui.column().classes('self-center transition-all'):
            with ui.row() \
                    .props('autofocus outlined rounded item-aligned input-class="ml-3"') \
                    .classes('self-center mt-5 transition-all'):
                self.inp_search_menu = ui.input(placeholder="Search Menu") \
                    .props('autofocus rounded item-aligned input-class="ml-3"') \
                    .classes('self-center transition-all')
                self.btn_search_menu = ui.button("Search", on_click=self.scraping_menu_list)

            self.dpd_result_menu = ui.select(options=[],
                                             on_change=self.scraping_individual_item) \
                .props('autofocus outlined rounded item-aligned input-class="ml-3"') \
                .classes('w-96 self-center mt-5 transition-all')
            self.lbl_result_menu = ui.label(text="") \
                .props('autofocus item-aligned') \
                .classes('self-center')
            with ui.row().classes('w-70 self-center mt-5 transition-all'):
                self.num_inp_quantity = ui.number(label="Quantity", value=1.0, on_change=self.calculating_pfc_from_quantity) \
                    .props('autofocus item-aligned input-class="ml-3"') \
                    .classes('w-40 self-center mt-5 transition-all')
                self.num_inp_serving_amount = ui.number(label="Amouont", format='%.2f', suffix="g") \
                    .props('autofocus item-aligned input-class="ml-3"') \
                    .classes('w-40 self-center mt-5 transition-all')
            with ui.row().classes('w-110 self-center mt-5 transition-all'):
                self.num_inp_protein = ui.number(label="Protein", format='%.2f', suffix="g")
                self.num_inp_fat = ui.number(label="Fat", format='%.2f', suffix="g")
                self.num_inp_carb = ui.number(label="Carb", format='%.2f', suffix="g")
            self.lbl_calories = ui.label(text="Calories: 0")
            self.btn_add_to_collection = ui.button("Add to Collection") \
                .props('autofocus rounded item-aligned input-class="ml-3"') \
                .classes('self-center transition-all')
            self.df_collection = ...
            self.btn_save_to_db = ui.button("Save to DB") \
                .props('autofocus rounded item-aligned input-class="ml-3"') \
                .classes('self-center transition-all')

            # variables for non-ui elements
            self._set_pfc = ()
            self.loading_spinner = ui.spinner(size='lg').classes('w-96 self-center mt-24 transition-all')
            self.loading_spinner.visible = False

    async def scraping_menu_list(self):
        search_result = await get_search_result(self.inp_search_menu.value)
        self.dpd_result_menu.options = search_result
        self.dpd_result_menu.update()
        # print(search_result)

        ui.notify("Search Completed", type='positive', timeout=1000)

    async def scraping_individual_item(self):
        food_detail = await get_nutrition_detail(self.dpd_result_menu.value)
        self.lbl_result_menu.text = f"{food_detail.title} / {food_detail.serving_amount} / {food_detail.serving_name}"

        # serving_unit_float = extract_float_numbers(food_detail.serving_name)

        self.num_inp_protein.value = food_detail.protein
        self.num_inp_fat.value = food_detail.fat
        self.num_inp_carb.value = food_detail.carb
        self.num_inp_serving_amount.value = food_detail.serving_amount
        self._set_pfc = (food_detail.protein, food_detail.fat, food_detail.carb, food_detail.serving_amount)

        self.lbl_calories.text = f"Calories: {calculating_calories(self.num_inp_protein.value, self.num_inp_fat.value, self.num_inp_carb.value)}"
        self.lbl_calories.update()

    def calculating_pfc_from_quantity(self):
        self.num_inp_protein.value = float(self.num_inp_quantity.value) * self._set_pfc[0]
        self.num_inp_fat.value = self.num_inp_quantity.value * self._set_pfc[1]
        self.num_inp_carb.value = self.num_inp_quantity.value * self._set_pfc[2]
        self.num_inp_serving_amount.value = self.num_inp_quantity.value * self._set_pfc[3]
        self.lbl_calories.text = f"Calories: {calculating_calories(self.num_inp_protein.value, self.num_inp_fat.value, self.num_inp_carb.value)}"
        self.lbl_calories.update()


    def scraping_menu_list_labels(self):
        ...
