import numpy as np
from matrix_factorisation import factorise

def main():
    rows = int(input("Enter number of rows: "))
    print("Enter matrix, row by row, space seperated values")
    m = [list(map(float, input().split())) for _ in range(rows)]

    latent_features = int(input("Enter number of latent features: "))
    factor1, factor2 = factorise(m, latent_features)

    print("\n1st factor")
    print(np.array(factor1))
    print("\n2nd factor")
    print(np.array(factor2))
    print("\nResult")
    print(np.matmul(factor1, factor2))


if __name__ == "__main__":
    main()
