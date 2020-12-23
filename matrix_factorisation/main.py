from matrix_factorisation import AdamFactorisation

rows = int(input("Enter number of rows: "))
print("Enter matrix, row by row, space separated values")
matrix = []
for _ in range(rows):
    matrix.append((list(map(int, input().split()))))

latent_features = int(input("Enter number of latent features: "))

factoriser = AdamFactorisation(matrix, latent_features)

factor1, factor2 = factoriser.factorise()

print(factor1)
print(factor2)
