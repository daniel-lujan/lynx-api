from typing import Iterable, Sized, Union

from schemas.constants import ALLOWED_MUSIC_GENRES, PERSON_CHARACTERISTICS


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
    form_data = form_data.copy()

    point = [form_data.pop("_id")]

    del form_data["name"]
    del form_data["age"]
    del form_data["gender"]
    del form_data["mapPoint"]

    point.extend(one_hot_encode(form_data.pop("favMusicGenres"), ALLOWED_MUSIC_GENRES))
    point.extend(
        one_hot_encode(form_data.pop("mostImportantAttr"), PERSON_CHARACTERISTICS)
    )

    point.extend(v for v in form_data.values())

    print(point)

    return point


def motel_to_point(data: dict) -> list:
    return [data["name"], data["location"]["lat"], data["location"]["lng"]]
