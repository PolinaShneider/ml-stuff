import numpy as np

first = [0, 0, 0, 0]
second = [0, 1, 1, 1]
third = [0, 1, 0, 1]
fourth = [1, 0, 1, 0]
fifth = [1, 0, 0, 0]
data = [fifth, second, third, fourth, fifth]

max_similarity = 0
[i, j] = [-1, -1]













for x_idx, x_val in enumerate(data):
    for y_idx, y_val in enumerate(data):
        if x_idx == y_idx:
            continue
        dot_product = np.dot(x_val, y_val)
        if dot_product > max_similarity:
            max_similarity = dot_product
            [i, j] = [x_idx, y_idx]

print(max_similarity, data[i], data[j])