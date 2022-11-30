#!/usr/bin/env python3
""" Multiply two matrices concurrently """

from typing import List
from concurrent.futures import ProcessPoolExecutor, wait, Executor, Future

Row = List[int]
Column = List[int]
Matrix = List[Row]


def matrix_multiply(matrix_a: Matrix, matrix_b: Matrix) -> Matrix:
    """ Multiply two matrices,
            calculating each column of the solution concurrently. """
    num_rows_a = len(matrix_a)
    num_cols_a = len(matrix_a[0])
    num_rows_b = len(matrix_b)
    num_cols_b = len(matrix_b[0])
    if num_cols_a != num_rows_b:
        raise ArithmeticError(
            f"Invalid dimensions; Cannot multiply "
            f"{num_rows_a}x{num_cols_a}*{num_rows_b}x{num_cols_b}"
        )

    pool: Executor = ProcessPoolExecutor()
    futures: List[Future[Row]] = []

    for row_index in range(num_rows_a):
        futures.append(pool.submit(worker, matrix_a, matrix_b, row_index))

    wait(futures)
    solution_matrix = [future.result() for future in futures]

    return solution_matrix


def worker(matrix_a: Matrix, matrix_b: Matrix, row_idx: int) -> Column:
    """ Creates 1 column of the solution_matrix """
    num_cols_a = len(matrix_a[0])
    num_cols_b = len(matrix_b[0])

    result_col = [0] * num_cols_b
    for j in range(num_cols_b):     # for each col in matrix_b
        for k in range(num_cols_a):  # for each col in matrix a
            result_col[j] += matrix_a[row_idx][k] * matrix_b[k][j]
    return result_col
