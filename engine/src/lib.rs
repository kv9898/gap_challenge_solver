use pyo3::prelude::*;

/// A Python module implemented in Rust.
#[pymodule]
fn engine(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(solve_grid, m)?)?;
    Ok(())
}

type Grid = Vec<Vec<String>>;

#[pyfunction]
fn solve_grid(mut grid: Grid) -> PyResult<Vec<Vec<String>>> {
    if solver(&mut grid) {
        Ok(grid)
    } else {
        Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
            "No solution found",
        ))
    }
}

// Main solver logic
fn solver(vals: &mut Grid) -> bool {
    let rows = vals.len();
    let possible_vals = (1..=rows)
        .map(|i| i.to_string())
        .collect::<Vec<_>>()
        .join("");

    // Initialize empty cells
    for row in vals.iter_mut() {
        for cell in row.iter_mut() {
            if cell.is_empty() {
                *cell = possible_vals.clone();
            }
        }
    }

    let mut changed = true;
    while changed {
        changed = false;

        for i in 0..rows {
            for j in 0..rows {
                if vals[i][j].len() == 1 {
                    let val = vals[i][j].clone();

                    // Row elimination
                    for col in 0..rows {
                        if col != j && vals[i][col].contains(&val) {
                            vals[i][col] = vals[i][col].replace(&val, "");
                            changed = true;
                        }
                    }

                    // Column elimination
                    for row in 0..rows {
                        if row != i && vals[row][j].contains(&val) {
                            vals[row][j] = vals[row][j].replace(&val, "");
                            changed = true;
                        }
                    }
                }
            }
        }

        if !changed {
            changed = find_unique_values(vals);
        }
    }

    if is_solved(vals) {
        return true;
    }

    // Backtracking
    for i in 0..rows {
        for j in 0..rows {
            if vals[i][j].len() > 1 {
                for ch in vals[i][j].chars() {
                    let mut vals_copy = vals.clone();
                    vals_copy[i][j] = ch.to_string();

                    if solver(&mut vals_copy) {
                        *vals = vals_copy;
                        return true;
                    }
                }
                return false;
            }
        }
    }

    false
}

fn is_solved(grid: &Grid) -> bool {
    for row in grid {
        for cell in row {
            if cell.is_empty() {
                return false;
            }
            if cell.len() != 1 {
                return false;
            }
        }
    }
    true
}

fn find_unique_values(vals: &mut Grid) -> bool {
    let rows = vals.len();
    for i in 0..rows {
        // Rows
        let row_vals: String = vals[i].concat();
        for j in 0..rows {
            if vals[i][j].len() > 1 {
                for ch in vals[i][j].chars() {
                    if row_vals.matches(ch).count() == 1 {
                        vals[i][j] = ch.to_string();
                        return true;
                    }
                }
            }
        }

        // Columns
        let mut col_vals = String::new();
        for row in 0..rows {
            col_vals.push_str(&vals[row][i]);
        }

        for j in 0..rows {
            if vals[j][i].len() > 1 {
                for ch in vals[j][i].chars() {
                    if col_vals.matches(ch).count() == 1 {
                        vals[j][i] = ch.to_string();
                        return true;
                    }
                }
            }
        }
    }

    false
}
