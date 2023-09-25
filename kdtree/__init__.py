from typing import Iterable, Sized, SupportsIndex, Union

import numpy as np


class Node:
    def __init__(
        self,
        point: SupportsIndex,
        depth: int,
        left: "Node" = None,
        right: "Node" = None,
    ) -> None:
        self.point = point
        self.left = left
        self.right = right
        self.depth = depth

    def __repr__(self) -> str:
        return f"""Node (\n  point = {self.point},\n  depth = {self.depth},\n  left = {"Node" if self.left else None},\n  right = {"Node" if self.right else None},\n)"""


class KDTree:
    def __init__(
        self, points: Iterable[SupportsIndex], ignore_first_axis: bool = False
    ) -> None:
        if len(points) == 0:
            raise ValueError("Points must not be empty")

        if ignore_first_axis:
            self.dimensions = len(points[0]) - 1
        else:
            self.dimensions = len(points[0])
        self.ignore_first_axis = ignore_first_axis
        self.root = self.__build(points)

    def __build(self, points: Iterable[SupportsIndex], depth: int = 0) -> Node:
        if len(points) == 0:
            return None

        axis = self.__get_axis(depth)
        sorted_points = sorted(points, key=lambda point: point[axis])
        median = len(points) // 2
        mp = sorted_points[median]

        return Node(
            mp,
            depth,
            left=self.__build(sorted_points[:median], depth + 1),
            right=self.__build(sorted_points[median + 1 :], depth + 1),
        )

    def __get_axis(self, depth: int) -> int:
        if self.ignore_first_axis:
            return (depth % self.dimensions) + 1
        else:
            return depth % self.dimensions

    @staticmethod
    def __recursive_search(point: SupportsIndex, node: Node, depth: int = 0):
        if node is None:
            return None

        if np.array_equal(point, node.point):
            return node

        axis = node.depth % len(point)

        if point[axis] < node.point[axis]:
            found = KDTree.__recursive_search(point, node.left, depth + 1)
        else:
            found = KDTree.__recursive_search(point, node.right, depth + 1)

        return found

    def search(self, point: Union[SupportsIndex, Sized]) -> Node:
        if len(point) != len(self.root.point):
            raise ValueError(f"Point must have {len(self.root.point)} dimensions")

        return self.__recursive_search(point, self.root)

    def distance_sqr(self, a: Iterable, b: Iterable) -> float:
        if self.ignore_first_axis:
            return np.sum(np.square(np.subtract(a[1:], b[1:])))
        else:
            return np.sum(np.square(a - b))

    def distance(self, a: Iterable, b: Iterable) -> float:
        return np.sqrt(self.distance_sqr(a, b))

    def check_equal(self, a: Iterable, b: Iterable) -> bool:
        if self.ignore_first_axis:
            return np.array_equal(a[1:], b[1:])
        else:
            return np.array_equal(a, b)

    def nearest_neighbor(self, query: SupportsIndex) -> Node:
        best: Node = None
        best_distance = float("inf")

        def search(node: Node):
            nonlocal best, best_distance

            if node is None:
                return

            distance = self.distance_sqr(node.point, query)

            if distance < best_distance and not self.check_equal(node.point, query):
                best = node
            
            best_distance = self.distance_sqr(best.point, query)

            axis = self.__get_axis(node.depth)
            diff = query[axis] - node.point[axis]
            if diff <= 0:
                close, away = node.left, node.right
            else:
                close, away = node.right, node.left

            search(close)
            if diff**2 < best_distance:
                search(away)

        search(self.root)
        return best

    def __repr__(self) -> str:
        string = "KDTree (\n"

        def get_repr(node, depth=0):
            nonlocal string
            if node is None:
                return
            string += "    " * depth + str(node.point) + "\n"
            get_repr(node.left, depth + 1)
            get_repr(node.right, depth + 1)

        get_repr(self.root)
        return string + ")"
