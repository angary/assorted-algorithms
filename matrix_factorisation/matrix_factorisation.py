"""
Meaning of variables
m0: Original matrix to be factorised
m1: Matrix on left side of matrix multiplication
m2: Matrix on right side of matrix multiplication
m3: Product of m1 and m2
 k: Number of latent features, think (num hidden layers in neural net) - 1
"""
from random import random

Matrix = list[list[float]]

MAX_ITERATION = 1_00_000
MIN_ERROR = 0.001
LEARN_RATE = 0.01


def factorise(m0: Matrix, k: int) -> tuple[Matrix, Matrix]:
    """
    Given an (m x n) matrix, factorise the matrix into two (m x k) and (k x n)
    matrices
    """
    # Initialise factors
    rows, cols = len(m0), len(m0[0])
    m1 = [[random()] * k for _ in range(rows)]
    m2 = [[random()] * cols for _ in range(k)]

    # Continue adjusting the variables in factor matrices
    for iteration in range(MAX_ITERATION):
        gradient_descent(m0, m1, m2)
        estimate_matrix = matrix_multiply(m1, m2)
        if mean_square_error(m0, estimate_matrix) < MIN_ERROR:
            break
    print(f"{iteration = }")
    m3 = matrix_multiply(m1, m2)
    print("Mean Square Error: ", mean_square_error(m3, m0))
    return (m1, m2)


def gradient_descent(m0: Matrix, m1: Matrix, m2: Matrix) -> None:
    """
    Given the final matrix, adjust the values of the factor matrices through 
    gradient descent
    """
    for i in range(len(m1)):
        for j in range(len(m2[0])):

            # Find error
            dot_product = sum([m1[i][k] * m2[k][j] for k in range(len(m2))])
            error = (m0[i][j] - dot_product)
            error *= abs(error)

            # Adjust values in two matrices
            for k in range(len(m2)):
                m1_descent = LEARN_RATE * (2 * error * m2[k][j])
                m2_descent = LEARN_RATE * (2 * error * m1[i][k])
                m1[i][k] += m1_descent
                m2[k][j] += m2_descent


def matrix_multiply(a: Matrix, b: Matrix) -> Matrix:
    """
    Given two matrixes, return their product
    """
    product = [[0] * len(b[0]) for _ in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            product[i][j] = sum([a[i][k] * b[k][j] for k in range(len(b))])
    return product


def mean_square_error(a: Matrix, b: Matrix) -> float:
    """
    Given two matrices, return the mean squared error between them
    """
    square_error = 0
    for i in range(len(a)):
        for j in range(len(a[0])):
            square_error += (a[i][j] - b[i][j]) ** 2
    values = len(a) * len(b[0])
    return square_error / values
