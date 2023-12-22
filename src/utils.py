import math


def rotate(component):
    component.width, component.height = component.height, component.width


def object_distance(obj_1_x, obj_1_y, obj_2_x, obj_2_y):
    X = obj_1_x - obj_2_x
    Y = obj_1_y - obj_2_y
    return math.sqrt(pow(X, 2) + pow(Y, 2))
