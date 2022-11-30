#!/usr/bin/env python3
"""Multiply two matrices sequentially"""

from typing import List

Row = List[int]
Matrix = List[Row]

def matrix_multiply(matrix_a: Matrix, matrix_b: Matrix) -> Matrix:
    num_rows_a = len(matrix_a)
    num_cols_a = len(matrix_a[0])
    num_rows_b = len(matrix_b)
    num_cols_b = len(matrix_b[0])
    if num_cols_a != num_rows_b:
        raise ArithmeticError(
            f"Invalid dimensions; Cannot multiply "
            f"{num_rows_a}x{num_cols_a}*{num_rows_b}x{num_cols_b}"
        )
    solution_matrix = [[0] * num_cols_b for _ in range(num_rows_a)]
    for i in range(num_rows_a):         # for each row in matrix_a
        for j in range(num_cols_b):     # for each col in matrix_b
            for k in range(num_cols_a): # for each col in matrix a
                solution_matrix[i][j] += matrix_a[i][k] * matrix_b[k][j]
    return solution_matrix
