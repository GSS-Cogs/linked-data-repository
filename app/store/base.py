from abc import ABCMeta, abstractmethod
from enum import Enum
from pathlib import Path
from typing import List, Union

class MetadataKeys(Enum):
    """
    Simple Enum for in-use metadata record field names.
    """
    csv_path = "csv_path"
    csvw_path = "csvw_path"
    rdf_path = "ttl_path"
    
    
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
        self.meta_keys = MetadataKeys
        
    @abstractmethod
    def setup(self):
        """
        Generic setup method to allow for the use of more
        complex database solutions.
        """
        pass

    @abstractmethod
    def create_resource(self, graph_identifier: str) -> (str):
        """
        Creates a new metadata resource record. Returns a unique identifier for
        the created record.
        """
        pass
    
    @abstractmethod
    def get_resource(self, resource_id: str) -> (dict):
        """
        Returns a dictionary representation of the metadata we are holding
        about a single resource, using the id of the resource to select it
        """
        pass
    
    @abstractmethod
    def list_resources(self, **kwargs) -> (List[dict]):
        """
        Returns a list of resources.
        Keyword args allow filtering of what's being returned.
        """
        pass

    @abstractmethod
    def upsert_resource_field(self, resource_id: int, field: str, value: str):
        """
        Given a resource id, allows upsert of a single field
        """
        pass

    @abstractmethod
    def get_resource_field(self, resource_id: int, field: str) -> (object):
        """
        Given a resource id, acquires value of a single field
        """
        pass

    # ------------------------------------------------------------------------
    # Note: All following methods are wrappers and associated functionality, none
    # of this should ever never need to be overwritten.
    # DO add more as needed, we want to keep the data logic our of the app proper.
    
    @staticmethod
    def ensure_path(maybe_path: Union[str, Path]):
        if not isinstance(maybe_path, Path):
            maybe_path = Path(maybe_path)
            assert maybe_path.exists()
        return maybe_path
    
    def set_csv(self, resource_id: str, csv_path: Union[Path, str]):
        csv_path = self.ensure_path(csv_path)
        self.upsert_resource_field(resource_id, self.meta_keys.csv_path.value, csv_path)
        
    def get_csv_path(self, resource_id: str) -> (Path):
        return self.get_resource_field(resource_id, self.meta_keys.csv_path.value)
        
    def set_csvw(self, resource_id: str, csvw_path: str):
        csvw_path = self.ensure_path(csvw_path)
        self.upsert_resource_field(resource_id, self.meta_keys.csvw_path.value, csvw_path)
     
    def get_csvw_path(self, resource_id: str) -> (Path):
        return self.get_resource_field(resource_id, self.meta_keys.csvw_path.value)
           
    def set_rdf(self, resource_id: str, rdf_path: str):
        rdf_path = self.ensure_path(rdf_path)
        self.upsert_resource_field(resource_id, self.meta_keys.rdf_path.value, rdf_path)
       
    def get_rdf_path(self, resource_id: str) -> (Path):
        return self.get_resource_field(resource_id, self.meta_keys.rdf_path.value)
         