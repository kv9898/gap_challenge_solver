from shiny import App, ui, reactive, render


def get_boxes(rows: int) -> list:
    boxes = [str(i) + str(j) for i in range(1, rows + 1) for j in range(1, rows + 1)]
    return boxes


def solver(values: list, rows: int) -> list:
    # Step 1: Define the set of all possible values based on `rows`
    possible_values = "".join(str(i) for i in range(1, rows + 1))

    # Step 2: Fill empty cells with the full range of possible values
    for i in range(rows):
        for j in range(rows):
            if values[i][j] == "":  # Assuming empty cells are represented by an empty string
                values[i][j] = possible_values

    # Step 3: Define a loop that continues until no changes are made
    made_changes = True
    while made_changes:
        made_changes = False  # Reset the flag for each pass

        # Iterate over each cell to narrow down possible values by row and column constraints
        for i in range(rows):
            for j in range(rows):
                if len(values[i][j]) == 1:
                    # This cell already has a definite value, so remove it from others in the same row and column
                    definite_value = values[i][j]

                    # Remove this value from other cells in the same row
                    for col in range(rows):
                        if col != j and definite_value in values[i][col]:
                            values[i][col] = values[i][col].replace(definite_value, "")
                            made_changes = True  # Set flag if any change was made

                    # Remove this value from other cells in the same column
                    for row in range(rows):
                        if row != i and definite_value in values[row][j]:
                            values[row][j] = values[row][j].replace(definite_value, "")
                            made_changes = True  # Set flag if any change was made

    return values

app_ui = ui.page_fluid(
    ui.head_content(ui.include_js("app_py.js")),
    ui.h2("AON Gap Challenge Solver (Generalized)"),
    ui.h5("Type 1, 2, 3, 4 or 5 for shapes"),
    ui.h5("Enter to submit, ~/` to clear"),
    ui.input_select(
        "mode", "Number of rows/columns", choices=["3", "4", "5"], selected="3"
    ),
    # Input grid with numeric inputs
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
    ui.output_text("logger"),
)


def server(input, output, session):
    log = reactive.value("")

    @reactive.effect
    @reactive.event(input.keyid)
    def _():
        if input.keyid() == 13:  # organise inputs into an array
            n = int(input.mode())
            boxes = get_boxes(n)

            def get_value(box):
                return getattr(input, f"shape{box}")()

            values = []
            for i in range(1, n + 1):
                row_boxes = boxes[(i - 1) * n : (i - 1) * n + n]
                row = list(map(get_value, row_boxes))
                values.append(row)  # Append the row to form a 2D array
            values = solver(values, n)
            log.set(values)
            # TODO: use ui.update_text to update the grid with definite values
            for i in range(n):
                for j in range(n):
                    box_id = f"shape{boxes[i * n + j]}"
                    cell_value = values[i][j]
                    # Update only if the cell has a definite value (single character)
                    if len(cell_value) == 1:
                        ui.update_text(box_id, value=cell_value)
        elif input.keyid() == 96:  # clear input when ` or ~ is pressed
            boxes = get_boxes(int(input.mode()))

            def clear_box(box):
                ui.update_text("shape" + box, value="")

            for box in boxes:
                clear_box(box)

    @output
    @render.text
    def logger():
        return log()

app = App(app_ui, server)
