import numpy as np
import random


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def ReLU(x):
    return x * (x > 0)

def tan(x):
    return np.tanh(x)

class NeuralNetwork:

    def __init__(self, layer_sizes):
        """
        Neural Network initialization.
        Given layer_sizes as an input, you have to design a Fully Cected Neural Network architecture here.
        :param layer_sizes: A list containing neuron numbers in each layers. For example [3, 10, 2] means that there are
        3 neurons in the input layer, 10 neurons in the hidden layer, and 2 neurons in the output layer.
        """
        input_vector_size = layer_sizes[0]
        hidden_vector_size1 = layer_sizes[1]
        output_vector_size = layer_sizes[2]

        # Weights and bayas of hidden layer 1
        self.w1 = np.random.rand(hidden_vector_size1, input_vector_size)
        self.b1 = np.random.rand(hidden_vector_size1, 1)

        # Weights of output layer
        self.w2 = np.random.rand(output_vector_size, hidden_vector_size1)
        self.b2 = np.random.rand(output_vector_size, 1)

    def activation(self, x):
        """
        The activation function of our neural network, e.g., Sigmoid, ReLU.
        :param x: Vector of a layer in our network.
        :return: Vector after applying activation function.
        """
        #return sigmoid(x)
        #return ReLU(x)
        return tan(x)

    def forward(self, x):
        """
        Receives input vector as a parameter and calculates the output vector based on weights and biases.
        :param x: Input vector which is a numpy array.
        :return: Output vector
        """
        # output of hidden layer1
        z1 = self.w1.dot(x)
        z1 = np.add(z1, self.b1)
        a1 = self.activation(z1)

        # output
        z2 = self.w2.dot(a1)
        z2 = np.add(z2, self.b2)
        output = self.activation(z2)

        return output




