from utils import object_distance
from random import random, randint
import copy
from numpy import exp
from numpy.random import rand


class Board:
    def __init__(self, body_list, height, width, bounds, step_size, temp):
        self.body_list = body_list
        self.width = width
        self.height = height
        self.total_dist = 0
        self.bounds = bounds
        self.step_size = step_size
        self.temp = temp
        self.centroid = None

    def getCentre(self):
        x = [component.pos[0] for component in self.body_list]
        y = [component.pos[1] for component in self.body_list]
        centroid = [sum(x) / len(self.body_list), sum(y) / len(self.body_list)]
        self.centroid = centroid

    def updateAll_DistToCentroid(self):
        for component in self.body_list:
            component.dist_to_centroid = object_distance(
                component.x, component.y, self.centroid[0], self.centroid[1]
            )
            self.total_dist += component.dist_to_centroid

    def weight_randomChoice(self):
        randomInt = random.choices(
            range(len(self.body_list)),
            weights=list(map(lambda d: d.dist_to_centroid, self.body_list)),
            k=1,
        )
        return self.body_list.pop(randomInt[0])

    def update(self, i, n_components=None):
        tempBoard = copy.deepcopy(self)
        # tempBoard.sortByCentroid(centroid)
        if n_components != None:
            done = []
            for n in range(randint(0, n_components)):
                #   tempBoard.body_list[n].update_position(tempBoard.bounds, tempBoard.step_size, centroid)
                component = tempBoard.weight_randomChoice()
                component.update_position(
                    tempBoard.bounds, tempBoard.step_size, tempBoard
                )
                done.append(component)
            # print("Retrieving popped components {}".format(len(done)))
            for component in done:
                tempBoard.body_list.append(component)

        else:
            for n in range(len(tempBoard.body_list)):
                component = tempBoard.body_list[n]
                component.update_position(
                    tempBoard.bounds, tempBoard.step_size, tempBoard
                )

        # difference between candidate and current point evaluation
        diff = tempBoard.total_dist - self.total_dist
        # print("Difference for this iteration - %s is %s" %(i, diff))
        # calculate temperature for current epoch
        t = self.temp / float(i + 1)
        # calculate metropolis acceptance criterion
        metropolis = exp(-diff / t)
        # check if we should keep the new point
        # print("Violtaion {}".format(tempBoard.rule_violation()))
        if diff < 0 and rand() < metropolis and not tempBoard.rule_violation():
            # store the new current point
            self.body_list = copy.deepcopy(tempBoard.body_list)
            self.total_dist = tempBoard.total_dist

    def rule_violation(self):
        for temp_component in self.body_list:
            if self.outOfBounds(temp_component):  # Check excess board
                return True
            if temp_component.hasOverlap(self.body_list) != None:
                # print("Detecting overlaps")
                return True
        return False

    def outOfBounds(self, temp_component):
        if (
            temp_component.x + temp_component.width / 2 > self.width
            or temp_component.y + temp_component.height / 2 > self.height
            or temp_component.x - temp_component.width / 2 < 0
            or temp_component.y - temp_component.height / 2 < 0
        ):
            return True
        else:
            return False

    def resolve_overlap(self):
        self.getCentre()
        self.updateAll_DistToCentroid()
        for obj in self.body_list:
            obj.resolve_overlap(self)

    def overlap_resolve_helper(self, obj, sub, x_buffer, y_buffer):
        if obj.x < sub.x:
            sub.x = sub.x + (x_buffer - (sub.x - obj.x))
            self.centroid[0] += (x_buffer - (sub.x - obj.x)) / len(self.body_list)
        else:
            sub.x = sub.x - (x_buffer - (obj.x - sub.x))
            self.centroid[0] += -(x_buffer - (obj.x - sub.x))

        if obj.y < sub.y:
            sub.y = sub.y + (y_buffer - (sub.y - obj.y))
            self.centroid[1] += (y_buffer - (sub.y - obj.y)) / len(self.body_list)
        else:
            sub.y = sub.y - (y_buffer - (obj.y - sub.y))
            self.centroid[1] += -(y_buffer - (obj.y - sub.y)) / len(self.body_list)

        sub.update_distToCentroid(self)

    def draw(self, ax):
        # print("{} - {} = {}".format(self.prev_score, self.score, self.prev_score-self.score))
        for component in self.body_list:
            component.draw(ax)
