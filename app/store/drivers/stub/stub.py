import json
from os import listdir
from pathlib import Path
import shutil
from typing import List
import uuid
        
from app.store.base import BaseStore

stub_data_path = Path(Path(__file__).parent / "data")
pristine_dir = Path(stub_data_path / "resources"  / "pristine")
temporary_dir = Path(stub_data_path / "resources" / "temporary")


def path_from_id(id: str) -> (Path):
    """
    Find a (hard coded, local file representation) of a resource by id, confirm
    it exists then return a Path object to it. 
    """
    resource_path = Path(temporary_dir / f"{id}.json")
    if not resource_path.exists():
        raise FileExistsError(f'Unable to find expected resource at path {resource_path}')
    return resource_path

        
class StubStore(BaseStore):
    """
    The StubStore implements very basic (largely hardcoded) functionality as
    expected by the final store implementation of this api service.
    
    The StubStore is for development purposes ONLY and should be replaced
    and removed in due course.
    """

    def setup(self):
        """
        Generic setup method to allow for the use of more
        complex database solutions.
        """

        # Copy ./pristine over into ./temporary
        # This resets our stubbed store to pristine.
        if Path(temporary_dir).exists():
            shutil.rmtree(temporary_dir)
        shutil.copytree(pristine_dir, temporary_dir)

    def create_resource(self, graph_identifier: str):
        """
        Creates a new metadata record, populating the graph_identifier
        field.
        """
        id = str(uuid.uuid4())
        with open(Path(temporary_dir / f'{id}.json'), "w") as f:
            json.dump({"id": id, "graph_identifier": graph_identifier}, f)
        return id
        
    def get_resource(self, id: str) -> (dict):
        """
        Returns a dictionary representation of the metadata we are holding
        about a single resource, using the id of the resource to select it
        """
        resource_path = path_from_id(id)
        with open(resource_path) as f:
            data = json.load(f)
        
        return data
    
    def list_resources(self, **kwargs) -> (List[dict]):
        """
        Returns a list of resources.
        Keyword args allow filtering of what's being returned.
        """
        
        # Load everything from disk
        resource_files = [Path(temporary_dir / f) for f in listdir(temporary_dir) if Path(temporary_dir / f).exists()]
        all_data = []
        for rf in resource_files:
            with open(rf) as f:
                all_data.append(json.load(f))
                
        # Now use the kwargs to filter
        if kwargs:
            for k, v in kwargs.items():
                all_data = [x for x in all_data if k in x.keys()]
                all_data = [x for x in all_data if x[k] == v]
                
        return all_data

    def upsert_resource_field(self, id: str, field: str, value: object):
        """
        Given a resource id, allows upsert of a single field
        """
        data = self.get_resource(id)
        data[field] = value
        with open(path_from_id(id), "w") as f:
            json.dump(data, f)

    def get_resource_field(self, id: int, field: str) -> (object):
        """
        Given a resource id, acquires the value of a single field
        """
        data = self.get_resource(id)
        return data[field]
    
        