from matrix_factorisation import factorise

def main():
    rows = int(input("Enter number of rows: "))
    print("Enter matrix, row by row, space seperated values")
    matrix = []
    for _ in range(rows):
        matrix.append((list(map(int, input().split()))))

    latent_features = int(input("Enter number of latent features: "))

    factor1, factor2 = factorise(matrix, latent_features)

    print(factor1)
    print(factor2)

if __name__ == "__main__":
    main()
