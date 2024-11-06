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
