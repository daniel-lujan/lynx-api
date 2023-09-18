from typing import Iterable, Sized, SupportsIndex, Union

import numpy as np


class Node:
    def __init__(
            self,
            point : SupportsIndex,
            depth : int,
            left : "Node" = None,
            right : "Node" = None) -> None:

        self.point = point
        self.left = left
        self.right = right
        self.depth = depth
    
    def __repr__(self) -> str:
        return f"""Node (\n  point = {self.point},\n  depth = {self.depth},\n  left = {"Node" if self.left else None},\n  right = {"Node" if self.right else None},\n)"""

class KDTree:
    def __init__(
            self,
            points : Iterable[SupportsIndex]) -> None:
        if len(points) == 0:
            raise ValueError("Points must not be empty")
        
        self.root = self.__build(points)
    
    def __build(
            self,
            points : Iterable[SupportsIndex],
            depth : int = 0
            ) -> Node:
        
        if len(points) == 0:
            return None
        
        axis = depth % len(points[0])
        sorted_points = sorted(points, key=lambda point: point[axis])
        median = len(points) // 2
        mp = sorted_points[median]

        return Node(
            mp,
            depth,
            left = self.__build(sorted_points[:median], depth + 1),
            right = self.__build(sorted_points[median + 1:], depth + 1))

    @staticmethod
    def __recursive_search(
            point: SupportsIndex,
            node: Node,
            depth: int = 0):

        if node is None:
            return None

        if np.array_equal(point, node.point):
            return node

        axis = depth % len(point)

        if point[axis] < node.point[axis]:
            found = KDTree.__recursive_search(
                point,
                node.left,
                depth + 1)
        else:
            found = KDTree.__recursive_search(
                point,
                node.right,
                depth + 1)
        
        return found

    def search(
            self,
            point : Union[SupportsIndex, Sized]) -> Node:
        
        if len(point) != len(self.root.point):
            raise ValueError(f"Point must have {len(self.root.point)} dimensions")
        
        return self.__recursive_search(point, self.root)
    
    @staticmethod
    def distance_sqr(a: Iterable, b: Iterable) -> float:
        return sum((x1 - x2) ** 2 for x1, x2 in zip(a, b))

    @staticmethod
    def distance(a: Iterable, b: Iterable) -> float:
        return np.sqrt(sum((x1 - x2) ** 2 for x1, x2 in zip(a, b)))

    def nearest_neighbor(self, target: SupportsIndex) -> Node:
        k = len(target)
        best : Node = None
        def search(node: Node, depth: int = 0):
            nonlocal best
            
            if node is None:
                return
            
            distance = KDTree.distance_sqr(node.point, target)
            best_distance = KDTree.distance_sqr(best.point, target) if best is not None else float('inf')
            
            if distance < best_distance and not all(node.point == target):
                best = node
            
            axis = depth % k
            diff = target[axis] - node.point[axis]
            if diff <= 0:
                close, away = node.left, node.right
            else:
                close, away = node.right, node.left
            
            search(close, depth + 1)
            if diff**2 < best_distance:
                search(away, depth + 1)
        
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
        