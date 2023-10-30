import os
from datetime import datetime

from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.models import Model
from pynamodb.attributes import UTCDateTimeAttribute, NumberAttribute, UnicodeAttribute


class UrlPathIndex(GlobalSecondaryIndex):
    class Meta:
        projection = AllProjection()

    url_path = UnicodeAttribute(hash_key=True)


class UrlModel(Model):
    """
    A model with an index
    """

    class Meta:
        table_name = os.getenv("URL_TABLE", "url_table")
        region = os.getenv("REGION", "us-east-1")

    url_id = NumberAttribute(hash_key=True)
    url_path = UnicodeAttribute()
    url_title = UnicodeAttribute(null=True)
    created_at = UTCDateTimeAttribute(null=False, default=datetime.now())

    url_path_index = UrlPathIndex()

    def to_dict(self):
        """
        Retrieves the model as a dictionary
        :return:
        """
        _dict_data = {
            "id": self.url_id,
            "path": self.url_path,
            "title": self.url_title,
        }
        return _dict_data
