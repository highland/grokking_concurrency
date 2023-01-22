#!/usr/bin/env python3
""" Multiply two matrices sequentially """

import random
from typing import List

Row = List[int]
Matrix = List[Row]


def matrix_multiply(matrix_a: Matrix, matrix_b: Matrix) -> Matrix:
    """ Multiply two matrices as a sequential calculation """
    num_rows_a = len(matrix_a)
    num_cols_a = len(matrix_a[0])
    num_rows_b = len(matrix_b)
    num_cols_b = len(matrix_b[0])
    if num_cols_a != num_rows_b:
        raise ArithmeticError(
            f"Invalid dimensions; Cannot multiply "
            f"{num_rows_a}x{num_cols_a}*{num_rows_b}x{num_cols_b}"
        )
    # for clarity:
    num_rows_c = num_rows_a
    num_cols_c = num_cols_b
    
    return [[
        sum([matrix_a[row][n] * matrix_b[n][col] for n in range(num_cols_a)])
        for col in range(num_cols_c)]
        for row in range(num_rows_c)]


if __name__ == "__main__":
    cols = 3
    rows = 2
    A = [[random.randint(0, 10) for i in range(cols)] for j in range(rows)]
    print(f"matrix A: {A}")
    B = [[random.randint(0, 10) for i in range(rows)] for j in range(cols)]
    print(f"matrix B: {B}")
    C = matrix_multiply(A, B)
    print(f"matrix C: {C}")
