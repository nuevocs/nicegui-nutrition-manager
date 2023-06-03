from nicegui import ui
from .playwright_scraping import get_search_result, get_nutrition_detail
from .utils import extract_float_numbers, calculating_calories, MENU_CATEGORY, DIMENSIONAL_PRODUCT_TABLE, \
    updating_dict_options, collection_header, FACT_PRODUCT_TABLE
from .db.schema_dtclass import DimProduct, FctProduct, Collection, current_date_jst, last_week_date_jst
from .db.supabase_func import insert_as_dict_supabase, select_filtered, select_all, select_filtered_gte
from dataclasses import asdict
import pandas as pd

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
            ui.link('data', "data")


def nutrition_records_content() -> pd.DataFrame:
    today = current_date_jst()
    one_week_prior = last_week_date_jst()

    fct_data = select_filtered_gte("fct_nutrition_menu", "date, menu_id, quantity", "date", one_week_prior)
    dim_data = select_all("dim_nutrition_menu", "id, menu_name, menu_category, protein, fat, carbohydrate, "
                                                "calories")

    fct_data = pd.DataFrame(fct_data)
    dim_data = pd.DataFrame(dim_data)
    df_merged = pd.merge(fct_data, dim_data, left_on='menu_id', right_on='id')
    df_merged = df_merged.drop(['menu_id', 'id'], axis=1)
    df_merged['protein'] = df_merged['protein'] * df_merged['quantity']
    df_merged['fat'] = df_merged['fat'] * df_merged['quantity']
    df_merged['carbohydrate'] = df_merged['carbohydrate'] * df_merged['quantity']
    df_merged['calories'] = df_merged['calories'] * df_merged['quantity']

    group_by = df_merged.drop(['quantity', 'menu_category'], axis=1)
    group_by = group_by.groupby('date').sum(numeric_only=True)
    return group_by
    # print(group_by)


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
                self.btn_recalculate_calories = ui.button("Recalculate Calories", on_click=self.recalculated_calories) \
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

        self.lbl_calories.text = f"Calories: {calculating_calories(self.num_inp_protein.value, self.num_inp_fat.value, self.num_inp_carb.value):.2f}"
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
            self.num_inp_protein.value, self.num_inp_fat.value, self.num_inp_carb.value,
            self.num_inp_serving_amount.value)
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
        # print(dim_item)
        insert_as_dict_supabase(DIMENSIONAL_PRODUCT_TABLE, dim_item)
        ui.notify("Saved to DB", type='positive', timeout=1000)
        self.inp_manual_entry.value = ""
        self.dpd_result_menu.options = []
        self.dpd_result_menu.value = ""
        self.dpd_result_menu.update()
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
        with ui.column() \
                .props('autofocus outlined rounded item-aligned input-class="ml-3"') \
                .classes('self-center transition-all'):
            self.selected_category = ui.select(options=MENU_CATEGORY,
                                               on_change=self.query_menu_based_upon_selected_category)
            self.selected_menu = ui.select(options=[], on_change=self.query_menu_pfc)
            self.quantity = ui.number(label="Quantity", value=1.0,
                                      on_change=self.calculating_calories_based_upon_quantity)
            self.calories = ui.label(text="Calories: 0")
            self.add_to_collection = ui.button("Add to Collection", on_click=self.add_to_collection)
            self.collections = ...
            self.save_to_db = ui.button("Save to DB", on_click=self.save_to_db_fct)
            self._calories = 0
            self._micronutrients = ()
            self.collection = ui.table(columns=collection_header, rows=[])
            self._db_collection = []

    def query_menu_based_upon_selected_category(self) -> dict:
        """
        This method queries the menu db based on the selected category.
        :return: dictionary of the menu list
        """
        self.selected_menu.value = None
        self.selected_menu.update()

        filtered_data = select_filtered("dim_nutrition_menu", "id, menu_name", "menu_category",
                                        self.selected_category.value)
        x = updating_dict_options(filtered_data, "id", "menu_name")
        self.selected_menu.options = x
        self.selected_menu.update()

    def query_menu_pfc(self) -> tuple:
        """
        This method queries the menu pfc based on the selected menu.
        :return: tuple of the pfc
        """
        if self.selected_menu.value is None:
            ...
        else:
            selected_menu_micronutrients = select_filtered("dim_nutrition_menu", "id, menu_name, protein, fat, \
                                                                                 carbohydrate, \
                                                                                 calories", "id",
                                                           self.selected_menu.value)
            print(selected_menu_micronutrients)
            self._micronutrients = (selected_menu_micronutrients[0]['menu_name'],
                                    selected_menu_micronutrients[0]['protein'],
                                    selected_menu_micronutrients[0]['fat'],
                                    selected_menu_micronutrients[0]['carbohydrate'],
                                    selected_menu_micronutrients[0]['calories'],
                                    )
            print(self._micronutrients)
            self.calories.text = f"Calories: {selected_menu_micronutrients[0]['calories']:.2f}"
            self._calories = selected_menu_micronutrients[0]['calories']
            self.calories.update()

    def calculating_calories_based_upon_quantity(self) -> float:
        """
        This method calculates the calories based on the quantity.
        :return: float
        """
        calories_text = float(self.quantity.value) * self._calories
        self.calories.text = f"Calories: {calories_text:.2f}"
        self.calories.update()

    def add_to_collection(self):

        fct_data = FctProduct(
            menu_id=self.selected_menu.value,
            quantity=self.quantity.value,
            date=current_date_jst(),
        )
        print(fct_data)

        protein_data = self._micronutrients[1] * self.quantity.value
        fat_data = self._micronutrients[2] * self.quantity.value
        carb_data = self._micronutrients[3] * self.quantity.value
        calories_data = self._micronutrients[4] * self.quantity.value

        col = Collection(
            menu_name=self._micronutrients[0],
            quantity=self.quantity.value,
            protein=f"{protein_data:.2f} {' ✅' if protein_data > 10 else ' 😅'}",
            fat=f"{fat_data:.2f} {' ✅' if fat_data < 10 else ' ❌'}",
            carb=f"{carb_data:.2f} {' ✅' if carb_data < 100 else ' 😅'}",
            calories=f"{calories_data:.2f} {' ✅' if calories_data < 500 else ' ❌'}",
        )
        self.collection.rows.append(asdict(col))
        self.collection.update()
        self._db_collection.append(fct_data)

    def save_to_db_fct(self):
        # print(self._db_collection)
        for r in self._db_collection:
            insert_as_dict_supabase(FACT_PRODUCT_TABLE, r)

        self.collection.rows.clear()
        self.collection.update()
        ui.notify("Saved to DB", type='positive', timeout=1000)


class DataVisual:

    def __init__(self, df: pd.DataFrame):
        # self.df = None
        self.chart_calories_by_date = ui.chart({
            'title': False,
            'chart': {'type': 'column'},
            'xAxis': {'categories': df.index.tolist()},
            'series': [
                {'name': 'Calories', 'data': df["calories"].tolist()},
            ],
        }).classes('w-full h-64')
        self.chart_pfc_by_date = ui.chart({
            'title': False,
            'chart': {'type': 'bar'},
            'xAxis': {'categories': df.index.tolist()},
            'series': [
                {'name': 'Protein', 'data': df["protein"].tolist()},
                {'name': 'Fat', 'data': df["fat"].tolist()},
                {'name': 'Carb', 'data': df["carbohydrate"].tolist()},
            ],
        }).classes('w-full h-64')
