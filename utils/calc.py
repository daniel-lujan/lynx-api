from typing import Iterable, Sized, Union

from schemas.constants import ALLOWED_MUSIC_GENRES


def one_hot_encode(data: list, categories: Union[Sized, Iterable]) -> list:
    """One-hot encode a list of data.

    Args:
        data (list): List of data to be encoded.
        categories (Iterable): Iterable of categories to be encoded.

    Returns:
        list: List of one-hot encoded data.
    """
    encoded_data = [0] * len(categories)

    for i, category in enumerate(categories):
        if category in data:
            encoded_data[i] = 1

    return encoded_data


def form_to_point(form_data: dict) -> list:
    point = []

    point.append(form_data["_id"])
    point.append(one_hot_encode(form_data["favMusicGenres"], ALLOWED_MUSIC_GENRES))
    point.append(form_data["moviesTaste"])
    # ...

    return point
