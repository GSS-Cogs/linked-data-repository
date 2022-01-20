from abc import ABCMeta, abstractmethod
from enum import Enum
from pathlib import Path
from typing import List, Union

from app.models.metadata import Metadata


class BaseStore(metaclass=ABCMeta):
    """
    Abstract class defining the api data Store.

    The "resource" we make reference to throughout this abstract is a
    single database entry/record holding metadata relevant to a single instance
    of an defined data "resource" and its various representations.

    Note: this is _not_ synonymous with version, as some versions will fail
    to upload, or just not be published or signed off. All versions start as a
    resource record accessible via the Store class (via whatever database solution
    is powering Store) - but - not all resource records will become published versions
    of something.

    Examples:

    1.) A codelist: is a resource and you could use its resource record
    to access its csv, csvw and rdf representations.

    2.) A dataset is also a resource and you could use its resource record
    to access its csv, csvw and rdf representations.
    """

    def __init__(self):
        pass

    @abstractmethod
    def setup(self, *args, **kwargs):
        """
        Generic setup method to allow for the use of more
        complex database solutions.
        """
        pass

    @abstractmethod
    def create_resource(self, graph_identifier: str) -> (str):
        """
        Creates a new metadata resource record. Returns a metadata_record_id
        """
        pass

    @abstractmethod
    def get_resource(self, **kwargs) -> (Metadata):
        """
        Returns a dictionary representation of the metadata we are holding
        about a single resource, using the id of the resource to select it
        """
        pass

    @abstractmethod
    def list_resources(self, **kwargs) -> (List[Metadata]):
        """
        Returns a list of resources.
        Keyword args allow filtering of what's being returned.
        """
        pass

    @abstractmethod
    def upsert_resource_field(self, metadata_record_id: int, field: str, value: str):
        """
        Given a resource id, allows upsert of a single field
        """
        pass

    @abstractmethod
    def get_resource_field(self, metadata_record_id: int, field: str) -> (object):
        """
        Given a resource id, acquires value of a single field
        """
        pass
