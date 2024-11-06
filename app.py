from shiny import App, ui, reactive, render
from engine import *


def format_values(values, n):
    formatted_rows = []
    for row in values:
        formatted_row = " ".join(
            f"{val:<{n}}" for val in row
        )  # Pad each cell to width n
        formatted_rows.append(formatted_row)
    return "<pre>" + "<br>".join(formatted_rows) + "</pre>"


app_ui = ui.page_fluid(
    ui.head_content(ui.include_js("app_py.js")),
    ui.tags.head(
        ui.tags.style(".container-fluid {  max-width: 500px;}", type="text/css")
    ),
    ui.h2("Gap Challenge Solver"),
    ui.h6("Type 1, 2, 3, 4 or 5 for shapes"),
    ui.h6("Computer shortcuts: Enter to submit, ~/` to clear"),
    ui.input_select(
        "mode", "Number of rows/columns", choices=["3", "4", "5"], selected="3"
    ),
    # Input grid with numeric inputs
    ui.h5("Values:"),
    ui.tags.div(
        ui.input_text("shape11", "", value=None),
        ui.input_text("shape12", "", value=None),
        ui.input_text("shape13", "", value=None),
        ui.panel_conditional(
            "input.mode!='3'", ui.input_text("shape14", "", value=None)
        ),
        ui.panel_conditional(
            "input.mode=='5'", ui.input_text("shape15", "", value=None)
        ),
        style="display: flex; gap: 10px;",
    ),
    ui.div(
        ui.input_text("shape21", "", value=None),
        ui.input_text("shape22", "", value=None),
        ui.input_text("shape23", "", value=None),
        ui.panel_conditional(
            "input.mode!='3'", ui.input_text("shape24", "", value=None)
        ),
        ui.panel_conditional(
            "input.mode=='5'", ui.input_text("shape25", "", value=None)
        ),
        style="display: flex; gap: 10px;",
    ),
    ui.div(
        ui.input_text("shape31", "", value=None),
        ui.input_text("shape32", "", value=None),
        ui.input_text("shape33", "", value=None),
        ui.panel_conditional(
            "input.mode!='3'", ui.input_text("shape34", "", value=None)
        ),
        ui.panel_conditional(
            "input.mode=='5'", ui.input_text("shape35", "", value=None)
        ),
        style="display: flex; gap: 10px;",
    ),
    ui.panel_conditional(
        "input.mode!='3'",
        ui.div(
            ui.input_text("shape41", "", value=None),
            ui.input_text("shape42", "", value=None),
            ui.input_text("shape43", "", value=None),
            ui.input_text("shape44", "", value=None),
            ui.panel_conditional(
                "input.mode=='5'", ui.input_text("shape45", "", value=None)
            ),
            style="display: flex; gap: 10px;",
        ),
    ),
    ui.panel_conditional(
        "input.mode=='5'",
        ui.div(
            ui.input_text("shape51", "", value=None),
            ui.input_text("shape52", "", value=None),
            ui.input_text("shape53", "", value=None),
            ui.input_text("shape54", "", value=None),
            ui.input_text("shape55", "", value=None),
            style="display: flex; gap: 10px;",
        ),
    ),
    ui.div(
        ui.input_action_button("submit", "Submit"),
        ui.input_action_button("clear", "Clear"),
        style="display: flex; gap: 10px;",
    ),
    ui.output_ui(id="logger"),
)


def server(input, output, session):
    log = reactive.value("")

    def clear():
        log.set("")
        boxes = get_boxes(int(input.mode()))

        def clear_box(box):

            ui.update_text("shape" + box, value="")

        for box in boxes:
            clear_box(box)

    def submit():
        n = int(input.mode())
        boxes = get_boxes(n)

        def get_value(box):
            return getattr(input, f"shape{box}")()

        values = []
        for i in range(1, n + 1):
            row_boxes = boxes[(i - 1) * n : (i - 1) * n + n]
            row = list(map(get_value, row_boxes))
            values.append(row)  # Append the row to form a 2D array
        try:
            values = solver(values)
            log.set("")
            # TODO: use ui.update_text to update the grid with definite values
            for i in range(n):
                for j in range(n):
                    box_id = f"shape{boxes[i * n + j]}"
                    cell_value = values[i][j]
                    # Update only if the cell has a definite value (single character)
                    if len(cell_value) == 1:
                        ui.update_text(box_id, value=cell_value)
        except ValueError as e:
            # log.set(str(e) + "<br>" + "<br>".join(str(row) for row in values))
            log.set(str(e) + "<br><br>" + format_values(values, n))

    @reactive.effect
    @reactive.event(input.key)
    def key():
        if input.key() == "Enter":  # organise inputs into an array
            submit()
        elif input.key() == "`":  # clear input when ` or ~ is pressed
            clear()

    @reactive.effect
    @reactive.event(input.clear)
    def button_clear():
        clear()

    @reactive.effect
    @reactive.event(input.submit)
    def button_submit():
        submit()

    @output
    @render.ui
    def logger():
        return ui.HTML(log())


app = App(app_ui, server, debug=True)
