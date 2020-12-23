"""
Code is just here for educational purposes
"""
from random import random
from math import sqrt

MIN_ERROR = 1e-3

class AdamFactorisation():

    def __init__(self, matrix, latent_features):
        """
        Initialise variables
        """
        # Initialise variables based off inputs
        self.matrix = matrix
        self.latent_features = latent_features

        # Initialise factor matrices
        rows = len(matrix)
        cols = len(matrix[0])
        self.factor1 = [[random()] * latent_features for _ in range(rows)]
        self.factor2 = [[random()] * cols for _ in range(latent_features)]

        # Initialise variables used for adam optimisation
        self.v1 = 0
        self.m1 = 0
        self.v2 = 0
        self.m2 = 0
    
    def factorise(self, epoch=1000, learn_rate=0.1, beta1=0.9, beta2=0.99, epsilon=1e-8):
        """
        Given the parameters for adam optimisation, factorise the matrix through
        gradient descent
        """
        for t in range(1, epoch + 1):
            
            square_error = 0

            for i in range(len(self.factor1)):
                for j in range(len(self.factor2[0])):

                    # Find error
                    dot_product = 0
                    for k in range(len(self.factor2)):
                        dot_product += self.factor1[i][k] * self.factor2[k][j]
                    error = (self.matrix[i][j] - dot_product)
                    square_error += error ** 2

                    # Apply gradient descent along factor1's row and factor2's col
                    for k in range(len(self.factor2)):

                        # Find the gradient for both factors
                        grad1 = -2 * error * self.factor2[k][j]
                        grad2 = -2 * error * self.factor1[i][k]

                        # Update momentum and variance for both factors to be 
                        # exponential weighted average
                        self.m1 = beta1 * self.m1 + (1 - beta1) * grad1
                        self.v1 = beta2 * self.v1 + (1 - beta2) * (grad1 ** 2)
                        self.m2 = beta1 * self.m2 + (1 - beta1) * grad2
                        self.v2 = beta2 * self.v2 + (1 - beta2) * (grad2 ** 2)

                        # Bias correction for both factors
                        m1_hat = self.m1 / (1 - beta1 ** t)
                        v1_hat = self.v1 / (1 - beta2 ** t)
                        m2_hat = self.m2 / (1 - beta1 ** t)
                        v2_hat = self.v2 / (1 - beta2 ** t)

                        # Apply grad descent
                        self.factor1[i][k] -= learn_rate * (m1_hat / (sqrt(v1_hat + epsilon)))
                        self.factor2[k][j] -= learn_rate * (m2_hat / (sqrt(v2_hat + epsilon)))
            
            mean_error = square_error / (len(self.factor1) * len(self.factor2[0]))
            if mean_error < MIN_ERROR:
                print("Final iteration: ", t)
                print("Mean error: ", mean_error)
                break

        # Return both factors
        return (self.factor1, self.factor2)
