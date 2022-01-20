from enum import Enum


class STATE(Enum):
    CREATED = "created"
    DRAFTED = "drafted"
    VALIDATED = "validated"
    PUBLISHED = "published"

    @staticmethod
    def from_string(str_state: str):
        return {
            "created": STATE.CREATED,
            "drafted": STATE.DRAFTED,
            "validated": STATE.VALIDATED,
            "published": STATE.PUBLISHED,
        }[str_state]


# TODO: use full mime type, i.e text/csv for value
# this could come in handy later for content negotiation
class FILE_TYPE(Enum):
    CSV = "text/csv"
    CSVW = "application/json"  # TODO - check this
    TTL = "text/ttl"

    @staticmethod
    def from_string(str_state: str):
        return {
            "text/csv": FILE_TYPE.CSV,
            "application/json": FILE_TYPE.CSVW,
            "text/ttl": FILE_TYPE.TTL,
        }[str_state]
