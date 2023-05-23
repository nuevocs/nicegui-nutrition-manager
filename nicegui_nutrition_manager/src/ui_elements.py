from nicegui import ui
from .playwright_scraping import get_search_result, get_nutrition_detail
from .utils import extract_float_numbers, calculating_calories, MENU_CATEGORY, DIMENSIONAL_PRODUCT_TABLE
from .db.schema_dtclass import DimProduct
from .db.supabase_func import insert_as_dict_supabase

SITE_TITLE = "Nutrition Manager"
new_line = '\n'


def page_layout_elements() -> None:
    with ui.header(elevated=True).style('background-color: #333333').classes('items-center justify-between'):
        ui.label(SITE_TITLE).classes("text-xl text-center")
        ui.button(on_click=lambda: right_drawer.toggle()).props('flat color=white icon=menu')
    with ui.right_drawer(fixed=False).style('background-color: #fcfcfc; width:"350"').props(
            'bordered mini-to-overlay width="250" show-if-above="False"') as right_drawer:
        with ui.column():
            ui.label('MENU').classes("text-xl text-gray-600/75 text-center")
            ui.link('Main', "/")
            ui.link('fact', "fact")


class InputControl:
    def __init__(self):

        # dialogue
        with ui.dialog() as self.dialog, ui.card():
            self.dialog_label = ui.label(text="Save to DB")
            ui.button("OK", on_click=self.save_record_to_db)

        # manual entry dialog

        with ui.dialog() as self.manual_entry_dialog, ui.card():
            self.manual_entry_inp_menu_name = ui.input(placeholder="Menu Name")
            self.manual_entry_num_inp_serving_amount = ui.number(label="Amount", format='%.2f', suffix="g")
            self.manual_entry_num_inp_protein = ui.number(label="Protein", format='%.2f', suffix="g")
            self.manual_entry_num_inp_fat = ui.number(label="Fat", format='%.2f', suffix="g")
            self.manual_entry_num_inp_carb = ui.number(label="Carb", format='%.2f', suffix="g")
            ui.button("Confirm", on_click=self.update_ui_values)

        with ui.column().classes('self-center transition-all'):
            with ui.row():
                self.lbl_nutrition_category = ui.label("Nutrition Category") \
                    .props('autofocus outlined rounded item-aligned input-class="ml-3"') \
                    .classes('self-center transition-all')
                self.dpd_nutrition_category = ui.select(options=MENU_CATEGORY) \
                    .props('autofocus  item-aligned input-class="ml-3"') \
                    .classes('w-64 self-center transition-all')

            self.tgl_manual_entry = ui.switch("Manual Entry", value=False, on_change=self.manual_visibility) \
                .props('autofocus outlined rounded item-aligned input-class="ml-3"') \
                .classes('self-center transition-all')
            self.inp_manual_entry = ui.input(placeholder="Manual Entry Field") \
                .props('autofocus outlined rounded item-aligned input-class="ml-3"') \
                .classes('w-96 self-center transition-all') \
                .bind_visibility_from(self.tgl_manual_entry, "value")
            with ui.column() as self.scraping_field:
                with ui.row() \
                        .props('autofocus outlined rounded item-aligned input-class="ml-3"') \
                        .classes('self-center transition-all') as self.search_rows:
                    self.inp_search_menu = ui.input(placeholder="Search Menu") \
                        .props('autofocus outlined rounded item-aligned input-class="ml-3"') \
                        .classes('w-96 self-center transition-all')
                    self.btn_search_menu = ui.button("Search", on_click=self.scraping_menu_list) \
                        .props('autofocus item-aligned input-class="ml-3"') \
                        .classes('w-46 self-center transition-all h-16')

                self.dpd_result_menu = ui.select(options=[],
                                                 on_change=self.scraping_individual_item) \
                    .props('autofocus outlined rounded item-aligned input-class="ml-3"') \
                    .classes('w-96 self-center mt-5 transition-all')
                self.lbl_result_menu = ui.label(text="") \
                    .props('autofocus item-aligned') \
                    .classes('self-center')

            with ui.row().classes('w-70 self-center mt-5 transition-all'):
                # self.num_inp_quantity = ui.number(label="Quantity", value=1.0,
                #                                   on_change=self.calculating_pfc_from_quantity) \
                #     .props('autofocus item-aligned input-class="ml-3"') \
                #     .classes('w-40 self-center mt-5 transition-all')
                self.num_inp_serving_amount = ui.number(label="Amouont", format='%.2f', suffix="g") \
                    .props('autofocus item-aligned input-class="ml-3"') \
                    .classes('w-40 self-center mt-5 transition-all')
            with ui.row().classes('w-110 self-center mt-5 transition-all'):
                self.num_inp_protein = ui.number(label="Protein", format='%.2f', suffix="g")
                self.num_inp_fat = ui.number(label="Fat", format='%.2f', suffix="g")
                self.num_inp_carb = ui.number(label="Carb", format='%.2f', suffix="g")
            self.lbl_calories = ui.label(text="Calories: 0")
            # self.btn_add_to_collection = ui.button("Add to Collection") \
            #     .props('autofocus rounded item-aligned input-class="ml-3"') \
            #     .classes('self-center transition-all')
            # self.df_collection = ...
            # self.btn_save_to_db = ui.button("Save to DB", on_click=self.save_record_to_db) \
            with ui.row().classes('w-110 self-center mt-5 transition-all'):
                self.btn_save_to_db = ui.button("Save to DB", on_click=self.opening_dialog) \
                    .props('autofocus rounded item-aligned input-class="ml-3"') \
                    .classes('self-center transition-all')
                self.btn_recalculate_calories = ui.button("Recalculate Calories", on_click=self.recalculated_calories)  \
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
        self.inp_manual_entry.value = food_detail.title
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
        _calories = calculating_calories(self.num_inp_protein.value, self.num_inp_fat.value, self.num_inp_carb.value)
        self.lbl_calories.text = f"Calories: {_calories:.2f}"
        self.lbl_calories.update()

    def opening_dialog(self):
        self.dialog.open()
        self.dialog_label.text = f"{self.inp_manual_entry.value} {new_line} {calculating_calories(self.num_inp_protein.value, self.num_inp_fat.value, self.num_inp_carb.value)} cal"
        self.dialog_label.update()

    def opening_manual_entry_dialog(self):
        self.manual_entry_dialog.open()

    def recalculated_calories(self):
        self.lbl_calories.text = f"Calories: {calculating_calories(self.num_inp_protein.value, self.num_inp_fat.value, self.num_inp_carb.value)}"
        self.lbl_calories.update()

    def update_ui_values(self):
        self.inp_manual_entry.value = self.manual_entry_inp_menu_name.value
        self.num_inp_serving_amount.value = self.manual_entry_num_inp_serving_amount.value
        self.num_inp_protein.value = self.manual_entry_num_inp_protein.value
        self.num_inp_fat.value = self.manual_entry_num_inp_fat.value
        self.num_inp_carb.value = self.manual_entry_num_inp_carb.value

        self._set_pfc = (
        self.num_inp_protein.value, self.num_inp_fat.value, self.num_inp_carb.value, self.num_inp_serving_amount.value)
        self.lbl_calories.text = f"Calories: {calculating_calories(self.num_inp_protein.value, self.num_inp_fat.value, self.num_inp_carb.value)}"
        self.lbl_calories.update()

        self.manual_entry_dialog.close()

    def save_record_to_db(self):
        dim_item = DimProduct(
            menu_name=self.inp_manual_entry.value,
            menu_category=self.dpd_nutrition_category.value,
            serving_amount=self.num_inp_serving_amount.value,
            protein=self.num_inp_protein.value,
            fat=self.num_inp_fat.value,
            carbohydrate=self.num_inp_carb.value,
            calories=calculating_calories(self.num_inp_protein.value, self.num_inp_fat.value, self.num_inp_carb.value),
        )
        print(dim_item)
        insert_as_dict_supabase(DIMENSIONAL_PRODUCT_TABLE, dim_item)
        self.dialog.close()

    def scraping_menu_list_labels(self):
        ...

    def manual_visibility(self):
        if self.tgl_manual_entry.value is False:
            # self.search_rows.visible = True
            self.scraping_field.visible = True
        else:
            self.scraping_field.visible = False
            self.opening_manual_entry_dialog()
            # self.search_rows.visible = False


class FactInputControl:
    """
    This class is for the input control of the fact table.
    There will be multiple number inputs, text inputs, and dropdowns.
    - Number inputs: quantity
    - Dropdowns: title(menu), category
    - Labels: calories, which actively changes based on the number inputs of quantity
    - Dataframe: collection of the input data
    - Buttons: add to collection, save to db
    Flow:
    1. User selects the category from the dropdown
    2. User selects the menu from the dropdown
    3. User inputs the quantity
    4. User clicks the add button
    """

    def __init__(self):
        self.selected_category = ui.select(options=[], on_change=self.query_menu_based_upon_selected_category)
        self.selected_menu = ui.select(options=[], on_change=self.query_menu_pfc)
        self.quantity = ui.number(label="Quantity", value=1.0, on_change=self.calculating_calories_based_upon_quantity)
        self.calories = ui.label(text="Calories: 0")
        self.add_to_collection = ui.button("Add to Collection")
        self.collections = ...
        self.save_to_db = ui.button("Save to DB")

    def query_menu_based_upon_selected_category(self) -> dict:
        """
        This method queries the menu db based on the selected category.
        :return: dictionary of the menu list
        """
        ...

    def query_menu_pfc(self) -> tuple:
        """
        This method queries the menu pfc based on the selected menu.
        :return: tuple of the pfc
        """
        ...

    def calculating_calories_based_upon_quantity(self) -> float:
        """
        This method calculates the calories based on the quantity.
        :return: float
        """
        ...
