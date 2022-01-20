import datetime
from genericpath import exists
import json
from os import listdir
from pathlib import Path
import shutil
from typing import List

from app.store.base import BaseStore
from app.models.metadata import Metadata


class StubStore(BaseStore):
    """
    The StubStore implements very basic Store using read and wrties to local
    to provide persistance.

    The StubeStore will also reset to defaults (whatevers in ./data/pristine)
    upon instantiation.

    The StubStore is for decouplwd development purposes ONLY and should be
    replaced and removed in due course.
    """

    def setup(
        self,
        data_root: Path = Path(Path(__file__).parent.parent.parent / "stub_data"),
    ):
        """
        If not otherwise specified the folder for storing the stubbed
        data will be app/stub_data
        """
        data_root.mkdir(parents=True, exist_ok=True)
        self.data_root = data_root

    def path_from_id(self, id: str) -> (Path):
        """
        Find the path to some json representing a metadata recvord by id, confirm
        it exists then return a Path object to it.
        """
        resource_path = Path(self.data_root / f"{id}.json")
        if not resource_path.exists():
            raise FileExistsError(
                f"Unable to find expected resource at path {resource_path}"
            )
        return resource_path

    def create_resource(self, graph_identifier: str):
        """
        Creates a new metadata record, populating the graph_identifier
        field.
        """
        metadata_record = Metadata(graph_identifier)
        with open(Path(self.data_root / f"{metadata_record.id}.json"), "w") as f:
            json.dump(metadata_record.as_dict(), f)
        return metadata_record.id

    def get_resource(self, **kwargs) -> (dict):
        """
        Returns a single Metadata object, based on the keyword
        filters provided.
        """
        metadata_records: List[Metadata] = self.list_resources(**kwargs)
        assert (
            len(metadata_records) == 1
        ), f"Expecting one record for {kwargs}, got {len(metadata_records)}"
        return metadata_records[0]

    def list_resources(self, **kwargs) -> (List[Metadata]):
        """
        Returns a list of resources.
        Keyword args allow filtering of what's being returned.
        """

        # Load everything from disk
        resource_files = [
            Path(self.data_root / f)
            for f in listdir(self.data_root)
            if Path(self.data_root / f).exists()
        ]
        all_metadata_records = []
        for rf in resource_files:
            with open(rf) as f:
                all_metadata_records.append(json.load(f))

        # Now use the kwargs to filter
        if kwargs:
            for k, v in kwargs.items():
                all_metadata_records = [
                    x for x in all_metadata_records if k in x.keys()
                ]
                all_metadata_records = [x for x in all_metadata_records if x[k] == v]

        return [Metadata.from_dict(x) for x in all_metadata_records]

    def upsert_resource_field(self, id: str, field: str, value: object):
        """
        Given a resource id, allows upsert of a single field
        """
        metadata: Metadata = self.get_resource(id=id)
        metadata_dict = metadata.as_dict()
        metadata_dict[field] = value
        with open(Path(self.data_root / f'{id}.json'), "w") as f:
            json.dump(metadata_dict, f)

    def get_resource_field(self, id: int, field: str) -> (object):
        """
        Given a resource id, acquires the value of a single field
        """
        data = self.get_resource(id=id)
        return data[field]
