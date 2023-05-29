from nicegui import ui
from src.ui_elements import page_layout_elements, InputControl, FactInputControl, DataVisual, nutrition_records_content


@ui.page('/')
async def main_content():
    page_layout_elements()
    main = InputControl()


@ui.page('/data')
async def data():
    page_layout_elements()
    data_visual = DataVisual(nutrition_records_content())


@ui.page('/fact')
async def fact():
    page_layout_elements()
    fct = FactInputControl()


ui.run()
