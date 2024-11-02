from shiny import App, ui, reactive, render


def get_boxes(rows: int) -> list:
    boxes = [str(i) + str(j) for i in range(1, rows + 1) for j in range(1, rows + 1)]
    return boxes


def is_solved(values: list) -> bool:
    for row in values:
        for cell in row:
            if len(cell) == 0:  # Check if the cell is empty
                raise ValueError("No solution found: a cell has no possible values")
            if len(cell) != 1:  # Check if the cell has a definite value
                return False
    return True


# Helper functions to find unique values.
def find_unique_values(vals, rows, changed):
    for i in range(rows):
        # Check rows
        row_vals = "".join([val for val in vals[i]])
        for j in range(rows):
            if len(vals[i][j]) > 1:
                for char in vals[i][j]:
                    if row_vals.count(char) == 1:
                        vals[i][j] = char
                        changed = True
                        return vals, changed

        # Check columns
        col_vals = "".join([vals[row][i] for row in range(rows)])
        for j in range(rows):
            if len(vals[j][i]) > 1:
                for char in vals[j][i]:
                    if col_vals.count(char) == 1:
                        vals[j][i] = char
                        changed = True
                        return vals, changed

    return vals, changed


def solver(initial_values: list) -> list:
    vals = initial_values
    rows = len(vals)
    # Step 1: Define the set of all possible values based on `rows`
    possible_val = "".join(str(i) for i in range(1, rows + 1))

    # Step 2: Fill empty cells with the full range of possible values
    for i in range(rows):
        for j in range(rows):
            if (
                vals[i][j] == ""
            ):  # Assuming empty cells are represented by an empty string
                vals[i][j] = possible_val

    # Step 3: Iteratively apply constraints until no more changes
    changed = True
    while changed:
        changed = False  # Track if any changes were made in this pass

        # Step 4: Loop through each cell and remove possibilities based on definite values in the row and column
        for i in range(rows):
            for j in range(rows):
                if len(vals[i][j]) == 1:
                    # This cell has a definite value, so remove it from others in the same row and column
                    definite_value = vals[i][j]

                    # Remove this value from other cells in the same row
                    for col in range(rows):
                        if col != j and definite_value in vals[i][col]:
                            vals[i][col] = vals[i][col].replace(definite_value, "")
                            changed = True  # Mark that a change was made

                    # Remove this value from other cells in the same column
                    for row in range(rows):
                        if row != i and definite_value in vals[row][j]:
                            vals[row][j] = vals[row][j].replace(definite_value, "")
                            changed = True  # Mark that a change was made
        if changed == True:
            next

        # Step 5: After standard elimination, find unique values
        vals, changed = find_unique_values(vals, rows, changed)

    if is_solved(vals):
        return vals

    # TODO: Step 5 try all possible values in the first non-definite cell and recurse
    for i in range(rows):
        for j in range(rows):
            if len(vals[i][j]) > 1:
                for possible_value in vals[i][j]:
                    # Create a copy of the current state
                    vals_copy = [row[:] for row in vals]
                    # Try this possible value
                    vals_copy[i][j] = possible_value
                    try:
                        # Recursively solve with this value
                        vals = solver(vals_copy)
                        # If a solution is found, return it
                        return vals
                    except ValueError:
                        # If this path fails, try the next possible value
                        continue
                # If no possible values work, raise an error for backtracking
                raise ValueError("No solution found: a cell has no possible values")

    # Step 6 if no solution is found, raise an error
    raise ValueError("No solution found: a cell has no possible values")


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
        ui.tags.style(
            ".container-fluid {  max-width: 500px;}",
            type="text/css"
        )
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
