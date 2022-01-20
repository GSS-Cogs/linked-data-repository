from datetime import datetime
from pathlib import Path
from typing import NamedTuple, Optional, List, Union
import uuid

from .constants import STATE, FILE_TYPE


class Representation(NamedTuple):
    """
    A class representing a single representation of the
    data in question. Typical representations would be:
    csvw, ttl, json-ld etc.
    """

    state: STATE
    file_type: FILE_TYPE
    path: Optional[Path] = None
    date_created: Optional[datetime] = None
    last_modified: Optional[datetime] = None

    def is_rdf(self) -> (bool):
        """
        Is this file an RDF representation?
        """
        return self.file_type.value in ["ttl"]

    def to_json(self) -> (dict):
        """
        format this class as a dictionary
        """
        return {
            "state": self.state.value,
            "file_type": self.file_type.value,
            "path": self.path.absolute() if self.path else "",
            "date_created": self.date_created.strftime("%m/%d/%Y, %H:%M:%S"),
            "last_modified": self.last_modified.strftime("%m/%d/%Y, %H:%M:%S"),
        }

    @staticmethod
    def from_dict(d: dict):
        return Representation(
            state=STATE.from_string(d["state"]),
            file_type=FILE_TYPE.from_string(d["format"]),
            path=d["path"],
            date_created=d["date_created"],
            last_modified=d["last_modified"],
        )

    @staticmethod
    def new(
        file_type: str,
        path: Path,
        state: STATE = STATE.CREATED,
        date_created: datetime = datetime.utcnow(),
        last_modified: datetime = datetime.utcnow(),
    ):
        """
        Create a new Representation with appropriate values
        """

        return Representation(
            state=state,
            file_type=FILE_TYPE.from_string(file_type),
            path=path,
            date_created=date_created,
            last_modified=last_modified,
        )


class Metadata:
    """
    Simple metadata model representing a single record
    of metadata about a single iteration of a data resource.

    Note: "record of metadata" is the conceptual hold all here, a single
    data resource could simultaneously be represented in several different
    formats: csv, csvw, ttl, n-triples, json-ld, excel (maybe) etc etc.

    The various representations of that single base thing are tracked
    by self.representatons[]
    """

    def __init__(
        self,
        graph_identifier: str,
        date_created: datetime = None,
        last_modified: datetime = None,
    ):
        self.id = str(uuid.uuid4())
        self.graph_identifier: str = graph_identifier
        self.date_created: datetime = (
            datetime.utcnow() if not date_created else date_created
        )
        self.last_modified: datetime = (
            datetime.utcnow() if not last_modified else last_modified
        )
        self.representations: List[Representation] = []

    @staticmethod
    def from_dict(d: dict):
        """
        Create a metadata class (and associated Representaton classes)
        from a single dictionary input
        """
        m = Metadata(d["graph_identifier"])

    def add_representation(self, format: str, path: Union[str, Path]):
        """
        Adds a new format representation of this data
        """
        if not isinstance(path, Path):
            path = Path(path)

        if not path.exists():
            raise FileNotFoundError(
                f"File {path.absolute()} not found when "
                f"attempting to upload {format} representation to {self.id}"
            )

        if format not in [x.value for x in FILE_TYPE]:
            raise ValueError(f"File format {format} is not supported")

        if self._find_format(format):
            raise ValueError(f"Aborting, format {format} representation already exists")

        self.representations.append(Representation.new(format, path))

    def as_dict(self) -> (dict):
        """
        Create a simple dict representation of this metadata record.
        """
        return {
            "id": self.id,
            "date_created": self.date_created.strftime("%m/%d/%Y, %H:%M:%S"),
            "last_modified": self.last_modified.strftime("%m/%d/%Y, %H:%M:%S"),
            "representations": [x.to_json() for x in self.representations],
            "graph_identifier": self.graph_identifier,
        }

    def _find_format(self, file_type: FILE_TYPE) -> (Union[Representation, None]):
        """
        Returns a representation of the requested type or None
        where such a representation has not been created.
        """
        matched_files = [
            x for x in self.representations if x.file_type.value == file_type
        ]
        assert (
            len(matched_files) < 2
        ), f"We should only have one representation of each file type, got {len(matched_files)}"
        return matched_files[0] if len(matched_files) == 1 else None
