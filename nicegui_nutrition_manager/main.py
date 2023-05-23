from nicegui import ui
from src.ui_elements import page_layout_elements, InputControl, FactInputControl



@ui.page('/')
async def main_content():
    page_layout_elements()
    main = InputControl()



@ui.page('/fact')
async def fact():
    page_layout_elements()
    fct = FactInputControl()


ui.run()
