def is_solved(values: list[list[str]]) -> bool:
    """
    Check if the puzzle is completely solved.

    This function evaluates a 2D list representing the puzzle grid,
    where each cell contains either a single definite value or multiple 
    possible values. It returns True if every cell in the grid has a 
    single definite value, indicating that the puzzle is solved.

    :param values: A 2D list where each element is a string representing 
                   possible values for a cell in the puzzle grid.
    :return: True if all cells have a single definite value, False otherwise.
    :raises ValueError: If any cell has no possible values.
    """
    for row in values:
        for cell in row:
            if len(cell) == 0:  # Check if the cell is empty
                raise ValueError("No solution found: a cell has no possible values")
            if len(cell) != 1:  # Check if the cell has a definite value
                return False
    return True



# Helper functions to find unique values.
def find_unique_values(
    vals: list,  # A 2D list of strings representing possible values for each cell in the puzzle grid
    rows: int,  # The number of rows (and columns) in the grid
    changed: bool  # A boolean indicating whether any changes have been made to the list
) -> tuple:
    """
    Find unique values in rows and columns.

    This function takes a 2D list of strings representing possible values for
    each cell in a puzzle grid, and returns a modified version of the list with
    unique values identified. It also returns a boolean indicating whether any
    changes were made to the list.

    Args:
        vals (list): A 2D list of strings representing possible values for each cell
                     in the puzzle grid.
        rows (int): The number of rows (and columns) in the grid.
        changed (bool): A boolean indicating whether any changes have been made to the list.

    Returns:
        tuple: A tuple containing the modified list and a boolean indicating
               whether any changes were made.
    """
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


def solver(initial_values: list[list[str]]) -> list[list[str]]:
    """
    Solves a puzzle grid by applying constraints and recursive backtracking.

    Args:
        initial_values (list[list[str]]): A 2D list of strings, where each string
                                          represents possible values for a cell
                                          in the grid.

    Returns:
        list[list[str]]: A 2D list of strings, where each string contains a
                         definite value indicating the solved state of the
                         puzzle.

    Raises:
        ValueError: If no solution is found for the puzzle.
    """
    vals: list[list[str]] = initial_values
    rows: int = len(vals)
    possible_val: str = "".join(str(i) for i in range(1, rows + 1))

    for i in range(rows):
        for j in range(rows):
            if vals[i][j] == "":
                vals[i][j] = possible_val

    changed: bool = True
    while changed:
        changed = False

        # Apply the constraint that each row and column must contain each value
        # only once
        for i in range(rows):
            for j in range(rows):
                if len(vals[i][j]) == 1:
                    definite_value: str = vals[i][j]

                    # Remove the definite value from the other cells in the row
                    for col in range(rows):
                        if col != j and definite_value in vals[i][col]:
                            vals[i][col] = vals[i][col].replace(definite_value, "")
                            changed = True

                    # Remove the definite value from the other cells in the column
                    for row in range(rows):
                        if row != i and definite_value in vals[row][j]:
                            vals[row][j] = vals[row][j].replace(definite_value, "")
                            changed = True

        # Apply the constraint that each cell must contain a value that is not
        # already present in its row or column
        if changed:
            continue

        vals, changed = find_unique_values(vals, rows, changed)

    if is_solved(vals):
        return vals

    # If no solution has been found, try each possible value in each cell and
    # recursively call the solver on the modified grid
    for i in range(rows):
        for j in range(rows):
            if len(vals[i][j]) > 1:
                for possible_value in vals[i][j]:
                    vals_copy: list[list[str]] = [row[:] for row in vals]
                    vals_copy[i][j] = possible_value
                    try:
                        vals = solver(vals_copy)                     
                        return vals
                    except ValueError:
                        continue
                raise ValueError("No solution found: a cell has no possible values")

    raise ValueError("No solution found: a cell has no possible values")
