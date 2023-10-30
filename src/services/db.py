from typing import Optional

from src.data.model.url import UrlModel


def save_url(url_id: int, url_path: str, url_title: str):
    """
    Save new url
    :param url_id:
    :param url_path:
    :param url_title:
    :return:
    """
    url_model = UrlModel()
    url_model.url_id = url_id
    url_model.url_path = url_path
    url_model.url_title = url_title
    url_model.save()


def get_url(url_id: int) -> Optional[UrlModel]:
    """
    Get url
    :param url_id:
    :return:
    """
    try:
        return UrlModel.get(hash_key=url_id)
    except UrlModel.DoesNotExist:
        return None


def get_url_by_path(url_path: str) -> list:
    """
    Get url
    :param url_path:
    :return:
    """
    try:
        return list(UrlModel.url_path_index.query(hash_key=url_path))
    except UrlModel.DoesNotExist:
        return []
