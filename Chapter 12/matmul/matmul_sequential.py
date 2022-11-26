#!/usr/bin/env python3
"""Multiply two matrices sequentially"""

import random
from typing import List

ROWS = 4
COLS = 2


def matrix_multiply(matrix_a: List[List[int]], matrix_b: List[List[int]]) -> List[List[int]]:
    num_rows_a = len(matrix_a)
    num_cols_a = len(matrix_a[0])
    num_rows_b = len(matrix_b)
    num_cols_b = len(matrix_b[0])
    if num_cols_a != num_rows_b:
        raise ArithmeticError(
            f"Invalid dimensions; Cannot multiply "
            f"{num_rows_a}x{num_cols_a}*{num_rows_b}x{num_cols_b}"
        )
    matrix_c = [[0] * num_cols_b for i in range(num_rows_a)]
    for i in range(num_rows_a):
        for j in range(num_cols_b):
            for k in range(num_cols_a):
                matrix_c[i][j] += matrix_a[i][k] * matrix_b[k][j]
    return matrix_c


if __name__ == "__main__":
    matrixA = [[random.randint(0, 10) for i in range(COLS)] for j in range(ROWS)]
    matrixB = [[random.randint(0, 10) for i in range(ROWS)] for j in range(COLS)]
    matrixC = matrix_multiply(matrixA, matrixB)
    print(matrixC)
