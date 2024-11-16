from shiny import App, ui, reactive, render
import base64
from pathlib import Path
from engine import *
from cv import detect_shapes


def format_values(values: list[list[str]], n: int) -> str:
    """
    Format a 2D list of values into a string with HTML preformatted text for error messages.

    :param values: A 2D list where each element is a string representing a value in the grid.
    :param n: The width to pad each cell in the formatted output.
    :return: A formatted string with each row joined by '<br>' and each cell
             padded to width 'n', wrapped in HTML <pre> tags.
    """
    formatted_rows = []
    for row in values:
        formatted_row = " ".join(
            f"{val:<{n}}" for val in row
        )  # Pad each cell to width n
        formatted_rows.append(formatted_row)
    return "<pre>" + "<br>".join(formatted_rows) + "</pre>"


def is_value(value: str, rows: int) -> bool:
    """
    Check if a string is a valid value in the grid.

    Args:
        value (str): The string to check.
        rows (int): The number of rows in the grid.

    Returns:
        bool: True if the string is a valid value, False otherwise.
    """
    return value in [str(i) for i in range(1, rows + 1)] or value == ""


app_ui = ui.page_fluid(
    # Load JavaScript code from app_py.js
    ui.head_content(ui.include_js("app_py.js")),
    ui.tags.head(
        # Set max-width to 500px for the whole page
        ui.tags.style(".container-fluid {  max-width: 500px;}", type="text/css")
    ),
    # Title and instructions
    ui.h2("Gap Challenge Solver"),
    ui.h6("Type 1, 2, 3, 4 or 5 for shapes"),
    ui.h6("Computer shortcuts: Enter to submit, ~/` to clear"),
    # Select number of rows/columns
    ui.input_select(
        "mode", "Number of rows/columns:", choices=["3", "4", "5"], selected="3"
    ),
    # Input grid with numeric inputs
    ui.h5("Values:"),
    ui.tags.div(
        # Create the input fields for the grid, depending on the number of rows/columns
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
    # Submit and clear buttons
    ui.div(
        ui.input_action_button("submit", "Submit"),
        ui.input_action_button("clear", "Clear"),
        ui.input_action_button("change", "To Practice"),
        style="display: flex; gap: 10px;",
    ),
    # The output of the solver will be displayed here
    ui.output_ui(id="logger"),
)


def server(input, output, session):

    log = reactive.value("")
    AON = reactive.value(True)

    def clear():
        """
        Clear the input grid and log output when the 'Clear' button is clicked or shortcut is pressed.
        """

        log.set("")
        boxes = get_boxes(int(input.mode()))

        def clear_box(box):

            ui.update_text("shape" + box, value="")

        for box in boxes:
            clear_box(box)

    def submit():
        n = int(input.mode())
        boxes = get_boxes(n)

        def get_value(box: str) -> str:
            """
            Get the value of a box in the grid, or raise a ValueError if the value is invalid.

            Args:
                box (str): The ID of the box, e.g. "11".
            Returns:
                str: The value of the box, or an empty string if not provided.
            Raises:
                ValueError: If the value is invalid.
            """
            value = getattr(input, f"shape{box}")()
            if is_value(value, n):
                return value
            else:
                raise ValueError(f"Invalid value for box ({", ".join(box)}): {value}")

        values = []
        try:
            for i in range(1, n + 1):
                row_boxes = boxes[(i - 1) * n : (i - 1) * n + n]
                row = list(map(get_value, row_boxes))
                values.append(row)  # Append the row to form a 2D array
        except ValueError as e:  # Dealing of invalid input
            log.set(str(e))
            return
        try:
            values = solver(values)
            log.set("")
            # use ui.update_text to update the grid with definite values
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
    @reactive.event(input.paste_image)
    def paste_image():
        # Remove the base64 header (e.g., "data:image/png;base64,")
        base64_data = input.paste_image().split(",")[1]

        # Decode the base64 data and convert it into an image
        image_data = base64.b64decode(base64_data)

        detected = detect_shapes(image_data, int(input.mode()), AON())

        # Print the detected shapes in input boxes
        for i in range(len(detected)):
            for j in range(len(detected[i])):
                box_id = (
                    f"shape{get_boxes(int(input.mode()))[i * len(detected[i]) + j]}"
                )
                ui.update_text(box_id, value=detected[i][j])

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

    @reactive.effect
    @reactive.event(input.change)
    def button_change():
        if AON():
            AON.set(False)
            ui.update_action_button(id="change", label="To AON")
            log.set("Detecting patterns from the practice site...")
        else:
            AON.set(True)
            ui.update_action_button(id="change", label="To Practice")
            log.set("Detecting patterns from the AON site...")

    @output
    @render.ui
    def logger():
        return ui.HTML(log())


app = App(app_ui, server, static_assets=Path(__file__).parent / "www")
