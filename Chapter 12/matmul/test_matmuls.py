from matmul_sequential import matrix_multiply as sequential_mm
from matmul_concurrent import matrix_multiply as concurrent_mm


matrixA = [[4, 8], [9, 6], [5, 9], [4, 4]]
matrixB = [[9, 9, 4, 7], [3, 7, 7, 6]]

expected = [[60, 92, 72, 76], [99, 123, 78, 99], [72, 108, 83, 89], [48, 64, 44, 52]]


def test_sequential():
    actual = sequential_mm(matrixA, matrixB)
    assert actual == expected
    
def test_concurrent():
    actual = concurrent_mm(matrixA, matrixB)
    assert actual == expected