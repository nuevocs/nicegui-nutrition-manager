from nicegui import ui

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
                self.btn_search_menu = ui.button("Search")
            self.dpd_result_menu = ui.select(["Menu Item 1", "Menu Item 2", "Menu Item 3"]) \
                .props('autofocus outlined rounded item-aligned input-class="ml-3"') \
                .classes('w-96 self-center mt-5 transition-all')
            self.lbl_result_menu = ui.label("Menu Item 1") \
                .props('autofocus item-aligned') \
                .classes('self-center')
            self.num_inp_quantity = ui.number(label="qty") \
                .props('autofocus outlined rounded item-aligned input-class="ml-3"') \
                .classes('w-96 self-center mt-5 transition-all')
            with ui.row().classes('w-110 self-center mt-5 transition-all'):
                self.num_inp_protein = ui.number(label="protein")
                self.num_inp_fat = ui.number(label="fat")
                self.num_inp_carb = ui.number(label="carb")
            self.lbl_calories = ui.label("Calories: 0")
            self.btn_add_to_collection = ui.button("Add to Collection") \
                .props('autofocus rounded item-aligned input-class="ml-3"') \
                .classes('self-center transition-all')
            self.df_collection = ...
            self.btn_save_to_db = ui.button("Save to DB") \
                .props('autofocus rounded item-aligned input-class="ml-3"') \
                .classes('self-center transition-all')
