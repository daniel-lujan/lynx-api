from time import time
from typing import Iterable
from unittest import TestCase

from numpy.random import randint

from kdtree import KDTree


class bc:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class TestKDTree(TestCase):
    def test_NNS(
        self,
        n_repeats: int = 100,
        test_dimensions: Iterable[int] = range(2, 50),
        test_points: int = 20,
        bound: int = 1000,
    ):
        for dim in test_dimensions:
            print(
                f"{bc.OKCYAN}{bc.BOLD}Testing {dim} dimensions{bc.ENDC}... ",
                end="",
                flush=True,
            )
            t = time()
            for _ in range(n_repeats):
                points = randint(-bound, bound, (20, dim))
                tree = KDTree(points)
                for _ in range(test_points):
                    point = randint(-bound, bound, dim)
                    actual_nearest = min(points, key=lambda x: sum((x - point) ** 2))
                    nearest = tree.nearest_neighbor(point)

                    self.assertAlmostEqual(
                        sum((actual_nearest - point) ** 2),
                        tree.distance_sqr(nearest.point, point),
                        places=5,
                        msg=f"{bc.FAIL}{bc.BOLD}Test failed{bc.ENDC}, {nearest.point} != {actual_nearest}, point = {point}",
                    )

            print(
                f"{bc.OKGREEN}{bc.BOLD}Test passed in ⏱️ {round(time()-t, 4)}s{bc.ENDC}"
            )
