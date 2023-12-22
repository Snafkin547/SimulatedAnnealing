from utils import object_distance
from random import randint
import matplotlib.pyplot as plt


class Component:
    def __init__(self, x, y, width, height, r, g, b):
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
        self.width = width
        self.height = height
        self.r = r
        self.g = g
        self.b = b

        self.dist_to_centroid = 0

    def draw(self, ax):
        r, g, b = self.r / 255, self.g / 255, self.b / 255  # Normalize colors
        x = self.x
        y = self.y
        x_lower_lim = x - self.width / 2
        y_lower_lim = y - self.height / 2
        ax.add_patch(
            plt.Rectangle((x_lower_lim, y_lower_lim), self.width, self.height, color=(r, g, b))
        )

    def resolve_overlap(self, field):
        for _component in field.body_list:
            if self != _component:
                if self.isOverlap(_component):
                    x_buffer = self.width / 2 + _component.width / 2
                    y_buffer = self.height / 2 + _component.height / 2
                    if self.dist_to_centroid < _component.dist_to_centroid:
                        field.overlap_resolve_helper(self, _component, x_buffer, y_buffer)
                    else:
                        field.overlap_resolve_helper(_component, self, x_buffer, y_buffer)

                    _component.resolve_overlap(field)  # Recurse till no overlap

    def hasOverlap(self, body_list):
        for _component in body_list:
            if self != _component:
                if self.isOverlap(_component):
                    return _component
        return None

    def isOverlap(self, _component):
        return (
            abs(_component.x - self.x) < (self.width + _component.width) / 2
            and abs(_component.y - self.y) < (self.height + _component.height) / 2
        )

    def update_position(self, bounds, step_size, field):
        if field.centroid[0] - self.x > 0:
            x_dir = 1
        else:
            x_dir = -1

        if field.centroid[1] - self.y > 0:
            y_dir = 1
        else:
            y_dir = -1

        x_move = randint(bounds[0], bounds[1]) * step_size * x_dir
        y_move = randint(bounds[0], bounds[1]) * step_size * y_dir
        self.x = self.x + x_move  # X direction
        self.y = self.y + y_move  # Y direction
        self.pos = (self.x, self.y)
        field.centroid[0] += x_move / len(field.body_list)
        field.centroid[1] += y_move / len(field.body_list)
        self.update_distToCentroid(field)

    def update_distToCentroid(self, field):
        # print("Prev{}".format(field.total_dist))
        field.total_dist -= self.dist_to_centroid
        self.dist_to_centroid = object_distance(
            self.x, self.y, field.centroid[0], field.centroid[1]
        )
        field.total_dist += self.dist_to_centroid
        # print("Aft{}".format(field.total_dist))
