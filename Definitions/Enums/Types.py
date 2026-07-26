from enum import Enum


class BaseTypes(Enum):
    bool = 'bool'
    int64 = 'int64'
    int32 = 'int32'
    int16 = 'int16'
    int8 = 'int8'
    uint64 = 'uint64'
    uint32 = 'uint32'
    uint16 = 'uint16'
    uint8 = 'uint8'
    float64 = 'float64'
    float32 = 'float32'


class BaseTypesTypes:
    Boolean = (
        BaseTypes.bool,
    )
    Numeric = (
        BaseTypes.bool,
        BaseTypes.int8,
        BaseTypes.int16,
        BaseTypes.int32,
        BaseTypes.int64,
        BaseTypes.uint8,
        BaseTypes.uint16,
        BaseTypes.uint32,
        BaseTypes.uint64,
        BaseTypes.float32,
        BaseTypes.float64,
    )
    Floating = (
        BaseTypes.float32,
        BaseTypes.float64,
    )
    Integer = (
        BaseTypes.bool,
        BaseTypes.int8,
        BaseTypes.int16,
        BaseTypes.int32,
        BaseTypes.int64,
        BaseTypes.uint8,
        BaseTypes.uint16,
        BaseTypes.uint32,
        BaseTypes.uint64,
    )
    Unsigned = (
        BaseTypes.bool,
        BaseTypes.uint8,
        BaseTypes.uint16,
        BaseTypes.uint32,
        BaseTypes.uint64,
    )
    Signed = (
        BaseTypes.int8,
        BaseTypes.int16,
        BaseTypes.int32,
        BaseTypes.int64,
    )
