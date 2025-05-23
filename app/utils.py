from enum import IntEnum, StrEnum


class UpdateTypes(StrEnum):
    VOID = "void"
    AUTO_PILOT_PATH = "auto_pilot_path"
    MANUAL = "manual"


class Errors(IntEnum):
    OK = 0
    DRONE_NOT_FOUND = 1
    TIMEOUT = 2
