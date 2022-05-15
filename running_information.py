import matplotlib.pyplot as plt
import numpy as np

low = []
high = []
average = []

def draw():
    x = [i for i in range(1,len(low)+1)]

    plt.plot(x,high,label="best score")
    plt.plot(x,average,label="average score")
    plt.plot(x,low,label="low score")

    plt.legend()
    plt.show()
