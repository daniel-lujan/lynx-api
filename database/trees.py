from database.data import motels
from kdtree import KDTree
from utils.calc import motel_to_point

motels_tree = KDTree(
    [motel_to_point(motel) for motel in motels], ignore_first_axis=True
)
