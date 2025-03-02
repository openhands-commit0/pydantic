"""The types module contains custom types used by pydantic."""
from __future__ import annotations as _annotations
import base64
import dataclasses as _dataclasses
import re
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING, Any, Callable, ClassVar, Dict, FrozenSet, Generic, Hashable, Iterator, List, Pattern, Set, TypeVar, Union, cast, get_args, get_origin
from uuid import UUID
import annotated_types
from annotated_types import BaseMetadata, MaxLen, MinLen
from pydantic_core import CoreSchema, PydanticCustomError, core_schema
from typing_extensions import Annotated, Literal, Protocol, TypeAlias, TypeAliasType, deprecated
from ._internal import _core_utils, _fields, _internal_dataclass, _typing_extra, _utils, _validators
from ._migration import getattr_migration
from .annotated_handlers import GetCoreSchemaHandler, GetJsonSchemaHandler
from .errors import PydanticUserError
from .json_schema import JsonSchemaValue
from .warnings import PydanticDeprecatedSince20
__all__ = ('Strict', 'StrictStr', 'conbytes', 'conlist', 'conset', 'confrozenset', 'constr', 'ImportString', 'conint', 'PositiveInt', 'NegativeInt', 'NonNegativeInt', 'NonPositiveInt', 'confloat', 'PositiveFloat', 'NegativeFloat', 'NonNegativeFloat', 'NonPositiveFloat', 'FiniteFloat', 'condecimal', 'UUID1', 'UUID3', 'UUID4', 'UUID5', 'FilePath', 'DirectoryPath', 'NewPath', 'Json', 'Secret', 'SecretStr', 'SecretBytes', 'StrictBool', 'StrictBytes', 'StrictInt', 'StrictFloat', 'PaymentCardNumber', 'ByteSize', 'PastDate', 'FutureDate', 'PastDatetime', 'FutureDatetime', 'condate', 'AwareDatetime', 'NaiveDatetime', 'AllowInfNan', 'EncoderProtocol', 'EncodedBytes', 'EncodedStr', 'Base64Encoder', 'Base64Bytes', 'Base64Str', 'Base64UrlBytes', 'Base64UrlStr', 'GetPydanticSchema', 'StringConstraints', 'Tag', 'Discriminator', 'JsonValue', 'OnErrorOmit', 'FailFast')
T = TypeVar('T')

@_dataclasses.dataclass
class Strict(_fields.PydanticMetadata, BaseMetadata):
    """Usage docs: https://docs.pydantic.dev/2.8/concepts/strict_mode/#strict-mode-with-annotated-strict

    A field metadata class to indicate that a field should be validated in strict mode.

    Attributes:
        strict: Whether to validate the field in strict mode.

    Example:
        ```python
        from typing_extensions import Annotated

        from pydantic.types import Strict

        StrictBool = Annotated[bool, Strict()]
        ```
    """
    strict: bool = True

    def __hash__(self) -> int:
        return hash(self.strict)
StrictBool = Annotated[bool, Strict()]
'A boolean that must be either ``True`` or ``False``.'

def conint(*, strict: bool | None=None, gt: int | None=None, ge: int | None=None, lt: int | None=None, le: int | None=None, multiple_of: int | None=None) -> type[int]:
    """
    !!! warning "Discouraged"
        This function is **discouraged** in favor of using
        [`Annotated`](https://docs.python.org/3/library/typing.html#typing.Annotated) with
        [`Field`][pydantic.fields.Field] instead.

        This function will be **deprecated** in Pydantic 3.0.

        The reason is that `conint` returns a type, which doesn't play well with static analysis tools.

        === ":x: Don't do this"
            ```py
            from pydantic import BaseModel, conint

            class Foo(BaseModel):
                bar: conint(strict=True, gt=0)
            ```

        === ":white_check_mark: Do this"
            ```py
            from typing_extensions import Annotated

            from pydantic import BaseModel, Field

            class Foo(BaseModel):
                bar: Annotated[int, Field(strict=True, gt=0)]
            ```

    A wrapper around `int` that allows for additional constraints.

    Args:
        strict: Whether to validate the integer in strict mode. Defaults to `None`.
        gt: The value must be greater than this.
        ge: The value must be greater than or equal to this.
        lt: The value must be less than this.
        le: The value must be less than or equal to this.
        multiple_of: The value must be a multiple of this.

    Returns:
        The wrapped integer type.

    ```py
    from pydantic import BaseModel, ValidationError, conint

    class ConstrainedExample(BaseModel):
        constrained_int: conint(gt=1)

    m = ConstrainedExample(constrained_int=2)
    print(repr(m))
    #> ConstrainedExample(constrained_int=2)

    try:
        ConstrainedExample(constrained_int=0)
    except ValidationError as e:
        print(e.errors())
        '''
        [
            {
                'type': 'greater_than',
                'loc': ('constrained_int',),
                'msg': 'Input should be greater than 1',
                'input': 0,
                'ctx': {'gt': 1},
                'url': 'https://errors.pydantic.dev/2/v/greater_than',
            }
        ]
        '''
    ```

    """
    pass
PositiveInt = Annotated[int, annotated_types.Gt(0)]
"An integer that must be greater than zero.\n\n```py\nfrom pydantic import BaseModel, PositiveInt, ValidationError\n\nclass Model(BaseModel):\n    positive_int: PositiveInt\n\nm = Model(positive_int=1)\nprint(repr(m))\n#> Model(positive_int=1)\n\ntry:\n    Model(positive_int=-1)\nexcept ValidationError as e:\n    print(e.errors())\n    '''\n    [\n        {\n            'type': 'greater_than',\n            'loc': ('positive_int',),\n            'msg': 'Input should be greater than 0',\n            'input': -1,\n            'ctx': {'gt': 0},\n            'url': 'https://errors.pydantic.dev/2/v/greater_than',\n        }\n    ]\n    '''\n```\n"
NegativeInt = Annotated[int, annotated_types.Lt(0)]
"An integer that must be less than zero.\n\n```py\nfrom pydantic import BaseModel, NegativeInt, ValidationError\n\nclass Model(BaseModel):\n    negative_int: NegativeInt\n\nm = Model(negative_int=-1)\nprint(repr(m))\n#> Model(negative_int=-1)\n\ntry:\n    Model(negative_int=1)\nexcept ValidationError as e:\n    print(e.errors())\n    '''\n    [\n        {\n            'type': 'less_than',\n            'loc': ('negative_int',),\n            'msg': 'Input should be less than 0',\n            'input': 1,\n            'ctx': {'lt': 0},\n            'url': 'https://errors.pydantic.dev/2/v/less_than',\n        }\n    ]\n    '''\n```\n"
NonPositiveInt = Annotated[int, annotated_types.Le(0)]
"An integer that must be less than or equal to zero.\n\n```py\nfrom pydantic import BaseModel, NonPositiveInt, ValidationError\n\nclass Model(BaseModel):\n    non_positive_int: NonPositiveInt\n\nm = Model(non_positive_int=0)\nprint(repr(m))\n#> Model(non_positive_int=0)\n\ntry:\n    Model(non_positive_int=1)\nexcept ValidationError as e:\n    print(e.errors())\n    '''\n    [\n        {\n            'type': 'less_than_equal',\n            'loc': ('non_positive_int',),\n            'msg': 'Input should be less than or equal to 0',\n            'input': 1,\n            'ctx': {'le': 0},\n            'url': 'https://errors.pydantic.dev/2/v/less_than_equal',\n        }\n    ]\n    '''\n```\n"
NonNegativeInt = Annotated[int, annotated_types.Ge(0)]
"An integer that must be greater than or equal to zero.\n\n```py\nfrom pydantic import BaseModel, NonNegativeInt, ValidationError\n\nclass Model(BaseModel):\n    non_negative_int: NonNegativeInt\n\nm = Model(non_negative_int=0)\nprint(repr(m))\n#> Model(non_negative_int=0)\n\ntry:\n    Model(non_negative_int=-1)\nexcept ValidationError as e:\n    print(e.errors())\n    '''\n    [\n        {\n            'type': 'greater_than_equal',\n            'loc': ('non_negative_int',),\n            'msg': 'Input should be greater than or equal to 0',\n            'input': -1,\n            'ctx': {'ge': 0},\n            'url': 'https://errors.pydantic.dev/2/v/greater_than_equal',\n        }\n    ]\n    '''\n```\n"
StrictInt = Annotated[int, Strict()]
"An integer that must be validated in strict mode.\n\n```py\nfrom pydantic import BaseModel, StrictInt, ValidationError\n\nclass StrictIntModel(BaseModel):\n    strict_int: StrictInt\n\ntry:\n    StrictIntModel(strict_int=3.14159)\nexcept ValidationError as e:\n    print(e)\n    '''\n    1 validation error for StrictIntModel\n    strict_int\n      Input should be a valid integer [type=int_type, input_value=3.14159, input_type=float]\n    '''\n```\n"

@_dataclasses.dataclass
class AllowInfNan(_fields.PydanticMetadata):
    """A field metadata class to indicate that a field should allow ``-inf``, ``inf``, and ``nan``."""
    allow_inf_nan: bool = True

    def __hash__(self) -> int:
        return hash(self.allow_inf_nan)

def confloat(*, strict: bool | None=None, gt: float | None=None, ge: float | None=None, lt: float | None=None, le: float | None=None, multiple_of: float | None=None, allow_inf_nan: bool | None=None) -> type[float]:
    """
    !!! warning "Discouraged"
        This function is **discouraged** in favor of using
        [`Annotated`](https://docs.python.org/3/library/typing.html#typing.Annotated) with
        [`Field`][pydantic.fields.Field] instead.

        This function will be **deprecated** in Pydantic 3.0.

        The reason is that `confloat` returns a type, which doesn't play well with static analysis tools.

        === ":x: Don't do this"
            ```py
            from pydantic import BaseModel, confloat

            class Foo(BaseModel):
                bar: confloat(strict=True, gt=0)
            ```

        === ":white_check_mark: Do this"
            ```py
            from typing_extensions import Annotated

            from pydantic import BaseModel, Field

            class Foo(BaseModel):
                bar: Annotated[float, Field(strict=True, gt=0)]
            ```

    A wrapper around `float` that allows for additional constraints.

    Args:
        strict: Whether to validate the float in strict mode.
        gt: The value must be greater than this.
        ge: The value must be greater than or equal to this.
        lt: The value must be less than this.
        le: The value must be less than or equal to this.
        multiple_of: The value must be a multiple of this.
        allow_inf_nan: Whether to allow `-inf`, `inf`, and `nan`.

    Returns:
        The wrapped float type.

    ```py
    from pydantic import BaseModel, ValidationError, confloat

    class ConstrainedExample(BaseModel):
        constrained_float: confloat(gt=1.0)

    m = ConstrainedExample(constrained_float=1.1)
    print(repr(m))
    #> ConstrainedExample(constrained_float=1.1)

    try:
        ConstrainedExample(constrained_float=0.9)
    except ValidationError as e:
        print(e.errors())
        '''
        [
            {
                'type': 'greater_than',
                'loc': ('constrained_float',),
                'msg': 'Input should be greater than 1',
                'input': 0.9,
                'ctx': {'gt': 1.0},
                'url': 'https://errors.pydantic.dev/2/v/greater_than',
            }
        ]
        '''
    ```
    """
    pass
PositiveFloat = Annotated[float, annotated_types.Gt(0)]
"A float that must be greater than zero.\n\n```py\nfrom pydantic import BaseModel, PositiveFloat, ValidationError\n\nclass Model(BaseModel):\n    positive_float: PositiveFloat\n\nm = Model(positive_float=1.0)\nprint(repr(m))\n#> Model(positive_float=1.0)\n\ntry:\n    Model(positive_float=-1.0)\nexcept ValidationError as e:\n    print(e.errors())\n    '''\n    [\n        {\n            'type': 'greater_than',\n            'loc': ('positive_float',),\n            'msg': 'Input should be greater than 0',\n            'input': -1.0,\n            'ctx': {'gt': 0.0},\n            'url': 'https://errors.pydantic.dev/2/v/greater_than',\n        }\n    ]\n    '''\n```\n"
NegativeFloat = Annotated[float, annotated_types.Lt(0)]
"A float that must be less than zero.\n\n```py\nfrom pydantic import BaseModel, NegativeFloat, ValidationError\n\nclass Model(BaseModel):\n    negative_float: NegativeFloat\n\nm = Model(negative_float=-1.0)\nprint(repr(m))\n#> Model(negative_float=-1.0)\n\ntry:\n    Model(negative_float=1.0)\nexcept ValidationError as e:\n    print(e.errors())\n    '''\n    [\n        {\n            'type': 'less_than',\n            'loc': ('negative_float',),\n            'msg': 'Input should be less than 0',\n            'input': 1.0,\n            'ctx': {'lt': 0.0},\n            'url': 'https://errors.pydantic.dev/2/v/less_than',\n        }\n    ]\n    '''\n```\n"
NonPositiveFloat = Annotated[float, annotated_types.Le(0)]
"A float that must be less than or equal to zero.\n\n```py\nfrom pydantic import BaseModel, NonPositiveFloat, ValidationError\n\nclass Model(BaseModel):\n    non_positive_float: NonPositiveFloat\n\nm = Model(non_positive_float=0.0)\nprint(repr(m))\n#> Model(non_positive_float=0.0)\n\ntry:\n    Model(non_positive_float=1.0)\nexcept ValidationError as e:\n    print(e.errors())\n    '''\n    [\n        {\n            'type': 'less_than_equal',\n            'loc': ('non_positive_float',),\n            'msg': 'Input should be less than or equal to 0',\n            'input': 1.0,\n            'ctx': {'le': 0.0},\n            'url': 'https://errors.pydantic.dev/2/v/less_than_equal',\n        }\n    ]\n    '''\n```\n"
NonNegativeFloat = Annotated[float, annotated_types.Ge(0)]
"A float that must be greater than or equal to zero.\n\n```py\nfrom pydantic import BaseModel, NonNegativeFloat, ValidationError\n\nclass Model(BaseModel):\n    non_negative_float: NonNegativeFloat\n\nm = Model(non_negative_float=0.0)\nprint(repr(m))\n#> Model(non_negative_float=0.0)\n\ntry:\n    Model(non_negative_float=-1.0)\nexcept ValidationError as e:\n    print(e.errors())\n    '''\n    [\n        {\n            'type': 'greater_than_equal',\n            'loc': ('non_negative_float',),\n            'msg': 'Input should be greater than or equal to 0',\n            'input': -1.0,\n            'ctx': {'ge': 0.0},\n            'url': 'https://errors.pydantic.dev/2/v/greater_than_equal',\n        }\n    ]\n    '''\n```\n"
StrictFloat = Annotated[float, Strict(True)]
"A float that must be validated in strict mode.\n\n```py\nfrom pydantic import BaseModel, StrictFloat, ValidationError\n\nclass StrictFloatModel(BaseModel):\n    strict_float: StrictFloat\n\ntry:\n    StrictFloatModel(strict_float='1.0')\nexcept ValidationError as e:\n    print(e)\n    '''\n    1 validation error for StrictFloatModel\n    strict_float\n      Input should be a valid number [type=float_type, input_value='1.0', input_type=str]\n    '''\n```\n"
FiniteFloat = Annotated[float, AllowInfNan(False)]
'A float that must be finite (not ``-inf``, ``inf``, or ``nan``).\n\n```py\nfrom pydantic import BaseModel, FiniteFloat\n\nclass Model(BaseModel):\n    finite: FiniteFloat\n\nm = Model(finite=1.0)\nprint(m)\n#> finite=1.0\n```\n'

def conbytes(*, min_length: int | None=None, max_length: int | None=None, strict: bool | None=None) -> type[bytes]:
    """A wrapper around `bytes` that allows for additional constraints.

    Args:
        min_length: The minimum length of the bytes.
        max_length: The maximum length of the bytes.
        strict: Whether to validate the bytes in strict mode.

    Returns:
        The wrapped bytes type.
    """
    pass
StrictBytes = Annotated[bytes, Strict()]
'A bytes that must be validated in strict mode.'

@_dataclasses.dataclass(frozen=True)
class StringConstraints(annotated_types.GroupedMetadata):
    """Usage docs: https://docs.pydantic.dev/2.8/concepts/fields/#string-constraints

    Apply constraints to `str` types.

    Attributes:
        strip_whitespace: Whether to remove leading and trailing whitespace.
        to_upper: Whether to convert the string to uppercase.
        to_lower: Whether to convert the string to lowercase.
        strict: Whether to validate the string in strict mode.
        min_length: The minimum length of the string.
        max_length: The maximum length of the string.
        pattern: A regex pattern that the string must match.
    """
    strip_whitespace: bool | None = None
    to_upper: bool | None = None
    to_lower: bool | None = None
    strict: bool | None = None
    min_length: int | None = None
    max_length: int | None = None
    pattern: str | Pattern[str] | None = None

    def __iter__(self) -> Iterator[BaseMetadata]:
        if self.min_length is not None:
            yield MinLen(self.min_length)
        if self.max_length is not None:
            yield MaxLen(self.max_length)
        if self.strict is not None:
            yield Strict(self.strict)
        if self.strip_whitespace is not None or self.pattern is not None or self.to_lower is not None or (self.to_upper is not None):
            yield _fields.pydantic_general_metadata(strip_whitespace=self.strip_whitespace, to_upper=self.to_upper, to_lower=self.to_lower, pattern=self.pattern)

def constr(*, strip_whitespace: bool | None=None, to_upper: bool | None=None, to_lower: bool | None=None, strict: bool | None=None, min_length: int | None=None, max_length: int | None=None, pattern: str | Pattern[str] | None=None) -> type[str]:
    """
    !!! warning "Discouraged"
        This function is **discouraged** in favor of using
        [`Annotated`](https://docs.python.org/3/library/typing.html#typing.Annotated) with
        [`StringConstraints`][pydantic.types.StringConstraints] instead.

        This function will be **deprecated** in Pydantic 3.0.

        The reason is that `constr` returns a type, which doesn't play well with static analysis tools.

        === ":x: Don't do this"
            ```py
            from pydantic import BaseModel, constr

            class Foo(BaseModel):
                bar: constr(strip_whitespace=True, to_upper=True, pattern=r'^[A-Z]+$')
            ```

        === ":white_check_mark: Do this"
            ```py
            from typing_extensions import Annotated

            from pydantic import BaseModel, StringConstraints

            class Foo(BaseModel):
                bar: Annotated[str, StringConstraints(strip_whitespace=True, to_upper=True, pattern=r'^[A-Z]+$')]
            ```

    A wrapper around `str` that allows for additional constraints.

    ```py
    from pydantic import BaseModel, constr

    class Foo(BaseModel):
        bar: constr(strip_whitespace=True, to_upper=True, pattern=r'^[A-Z]+$')


    foo = Foo(bar='  hello  ')
    print(foo)
    #> bar='HELLO'
    ```

    Args:
        strip_whitespace: Whether to remove leading and trailing whitespace.
        to_upper: Whether to turn all characters to uppercase.
        to_lower: Whether to turn all characters to lowercase.
        strict: Whether to validate the string in strict mode.
        min_length: The minimum length of the string.
        max_length: The maximum length of the string.
        pattern: A regex pattern to validate the string against.

    Returns:
        The wrapped string type.
    """
    pass
StrictStr = Annotated[str, Strict()]
'A string that must be validated in strict mode.'
HashableItemType = TypeVar('HashableItemType', bound=Hashable)

def conset(item_type: type[HashableItemType], *, min_length: int | None=None, max_length: int | None=None) -> type[set[HashableItemType]]:
    """A wrapper around `typing.Set` that allows for additional constraints.

    Args:
        item_type: The type of the items in the set.
        min_length: The minimum length of the set.
        max_length: The maximum length of the set.

    Returns:
        The wrapped set type.
    """
    pass

def confrozenset(item_type: type[HashableItemType], *, min_length: int | None=None, max_length: int | None=None) -> type[frozenset[HashableItemType]]:
    """A wrapper around `typing.FrozenSet` that allows for additional constraints.

    Args:
        item_type: The type of the items in the frozenset.
        min_length: The minimum length of the frozenset.
        max_length: The maximum length of the frozenset.

    Returns:
        The wrapped frozenset type.
    """
    pass
AnyItemType = TypeVar('AnyItemType')

def conlist(item_type: type[AnyItemType], *, min_length: int | None=None, max_length: int | None=None, unique_items: bool | None=None) -> type[list[AnyItemType]]:
    """A wrapper around typing.List that adds validation.

    Args:
        item_type: The type of the items in the list.
        min_length: The minimum length of the list. Defaults to None.
        max_length: The maximum length of the list. Defaults to None.
        unique_items: Whether the items in the list must be unique. Defaults to None.
            !!! warning Deprecated
                The `unique_items` parameter is deprecated, use `Set` instead.
                See [this issue](https://github.com/pydantic/pydantic-core/issues/296) for more details.

    Returns:
        The wrapped list type.
    """
    pass
AnyType = TypeVar('AnyType')
if TYPE_CHECKING:
    ImportString = Annotated[AnyType, ...]
else:

    class ImportString:
        """A type that can be used to import a type from a string.

        `ImportString` expects a string and loads the Python object importable at that dotted path.
        Attributes of modules may be separated from the module by `:` or `.`, e.g. if `'math:cos'` was provided,
        the resulting field value would be the function`cos`. If a `.` is used and both an attribute and submodule
        are present at the same path, the module will be preferred.

        On model instantiation, pointers will be evaluated and imported. There is
        some nuance to this behavior, demonstrated in the examples below.

        **Good behavior:**
        ```py
        from math import cos

        from pydantic import BaseModel, Field, ImportString, ValidationError


        class ImportThings(BaseModel):
            obj: ImportString


        # A string value will cause an automatic import
        my_cos = ImportThings(obj='math.cos')

        # You can use the imported function as you would expect
        cos_of_0 = my_cos.obj(0)
        assert cos_of_0 == 1


        # A string whose value cannot be imported will raise an error
        try:
            ImportThings(obj='foo.bar')
        except ValidationError as e:
            print(e)
            '''
            1 validation error for ImportThings
            obj
            Invalid python path: No module named 'foo.bar' [type=import_error, input_value='foo.bar', input_type=str]
            '''


        # Actual python objects can be assigned as well
        my_cos = ImportThings(obj=cos)
        my_cos_2 = ImportThings(obj='math.cos')
        my_cos_3 = ImportThings(obj='math:cos')
        assert my_cos == my_cos_2 == my_cos_3


        # You can set default field value either as Python object:
        class ImportThingsDefaultPyObj(BaseModel):
            obj: ImportString = math.cos


        # or as a string value (but only if used with `validate_default=True`)
        class ImportThingsDefaultString(BaseModel):
            obj: ImportString = Field(default='math.cos', validate_default=True)


        my_cos_default1 = ImportThingsDefaultPyObj()
        my_cos_default2 = ImportThingsDefaultString()
        assert my_cos_default1.obj == my_cos_default2.obj == math.cos


        # note: this will not work!
        class ImportThingsMissingValidateDefault(BaseModel):
            obj: ImportString = 'math.cos'

        my_cos_default3 = ImportThingsMissingValidateDefault()
        assert my_cos_default3.obj == 'math.cos'  # just string, not evaluated
        ```

        Serializing an `ImportString` type to json is also possible.

        ```py
        from pydantic import BaseModel, ImportString


        class ImportThings(BaseModel):
            obj: ImportString


        # Create an instance
        m = ImportThings(obj='math.cos')
        print(m)
        #> obj=<built-in function cos>
        print(m.model_dump_json())
        #> {"obj":"math.cos"}
        ```
        """

        @classmethod
        def __class_getitem__(cls, item: AnyType) -> AnyType:
            return Annotated[item, cls()]

        @classmethod
        def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
            serializer = core_schema.plain_serializer_function_ser_schema(cls._serialize, when_used='json')
            if cls is source:
                return core_schema.no_info_plain_validator_function(function=_validators.import_string, serialization=serializer)
            else:
                return core_schema.no_info_before_validator_function(function=_validators.import_string, schema=handler(source), serialization=serializer)

        @classmethod
        def __get_pydantic_json_schema__(cls, cs: CoreSchema, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
            return handler(core_schema.str_schema())

        def __repr__(self) -> str:
            return 'ImportString'

def condecimal(*, strict: bool | None=None, gt: int | Decimal | None=None, ge: int | Decimal | None=None, lt: int | Decimal | None=None, le: int | Decimal | None=None, multiple_of: int | Decimal | None=None, max_digits: int | None=None, decimal_places: int | None=None, allow_inf_nan: bool | None=None) -> type[Decimal]:
    """
    !!! warning "Discouraged"
        This function is **discouraged** in favor of using
        [`Annotated`](https://docs.python.org/3/library/typing.html#typing.Annotated) with
        [`Field`][pydantic.fields.Field] instead.

        This function will be **deprecated** in Pydantic 3.0.

        The reason is that `condecimal` returns a type, which doesn't play well with static analysis tools.

        === ":x: Don't do this"
            ```py
            from pydantic import BaseModel, condecimal

            class Foo(BaseModel):
                bar: condecimal(strict=True, allow_inf_nan=True)
            ```

        === ":white_check_mark: Do this"
            ```py
            from decimal import Decimal

            from typing_extensions import Annotated

            from pydantic import BaseModel, Field

            class Foo(BaseModel):
                bar: Annotated[Decimal, Field(strict=True, allow_inf_nan=True)]
            ```

    A wrapper around Decimal that adds validation.

    Args:
        strict: Whether to validate the value in strict mode. Defaults to `None`.
        gt: The value must be greater than this. Defaults to `None`.
        ge: The value must be greater than or equal to this. Defaults to `None`.
        lt: The value must be less than this. Defaults to `None`.
        le: The value must be less than or equal to this. Defaults to `None`.
        multiple_of: The value must be a multiple of this. Defaults to `None`.
        max_digits: The maximum number of digits. Defaults to `None`.
        decimal_places: The number of decimal places. Defaults to `None`.
        allow_inf_nan: Whether to allow infinity and NaN. Defaults to `None`.

    ```py
    from decimal import Decimal

    from pydantic import BaseModel, ValidationError, condecimal

    class ConstrainedExample(BaseModel):
        constrained_decimal: condecimal(gt=Decimal('1.0'))

    m = ConstrainedExample(constrained_decimal=Decimal('1.1'))
    print(repr(m))
    #> ConstrainedExample(constrained_decimal=Decimal('1.1'))

    try:
        ConstrainedExample(constrained_decimal=Decimal('0.9'))
    except ValidationError as e:
        print(e.errors())
        '''
        [
            {
                'type': 'greater_than',
                'loc': ('constrained_decimal',),
                'msg': 'Input should be greater than 1.0',
                'input': Decimal('0.9'),
                'ctx': {'gt': Decimal('1.0')},
                'url': 'https://errors.pydantic.dev/2/v/greater_than',
            }
        ]
        '''
    ```
    """
    pass

@_dataclasses.dataclass(**_internal_dataclass.slots_true)
class UuidVersion:
    """A field metadata class to indicate a [UUID](https://docs.python.org/3/library/uuid.html) version."""
    uuid_version: Literal[1, 3, 4, 5]

    def __get_pydantic_json_schema__(self, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
        field_schema = handler(core_schema)
        field_schema.pop('anyOf', None)
        field_schema.update(type='string', format=f'uuid{self.uuid_version}')
        return field_schema

    def __get_pydantic_core_schema__(self, source: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        if isinstance(self, source):
            return core_schema.uuid_schema(version=self.uuid_version)
        else:
            schema = handler(source)
            _check_annotated_type(schema['type'], 'uuid', self.__class__.__name__)
            schema['version'] = self.uuid_version
            return schema

    def __hash__(self) -> int:
        return hash(type(self.uuid_version))
UUID1 = Annotated[UUID, UuidVersion(1)]
'A [UUID](https://docs.python.org/3/library/uuid.html) that must be version 1.\n\n```py\nimport uuid\n\nfrom pydantic import UUID1, BaseModel\n\nclass Model(BaseModel):\n    uuid1: UUID1\n\nModel(uuid1=uuid.uuid1())\n```\n'
UUID3 = Annotated[UUID, UuidVersion(3)]
"A [UUID](https://docs.python.org/3/library/uuid.html) that must be version 3.\n\n```py\nimport uuid\n\nfrom pydantic import UUID3, BaseModel\n\nclass Model(BaseModel):\n    uuid3: UUID3\n\nModel(uuid3=uuid.uuid3(uuid.NAMESPACE_DNS, 'pydantic.org'))\n```\n"
UUID4 = Annotated[UUID, UuidVersion(4)]
'A [UUID](https://docs.python.org/3/library/uuid.html) that must be version 4.\n\n```py\nimport uuid\n\nfrom pydantic import UUID4, BaseModel\n\nclass Model(BaseModel):\n    uuid4: UUID4\n\nModel(uuid4=uuid.uuid4())\n```\n'
UUID5 = Annotated[UUID, UuidVersion(5)]
"A [UUID](https://docs.python.org/3/library/uuid.html) that must be version 5.\n\n```py\nimport uuid\n\nfrom pydantic import UUID5, BaseModel\n\nclass Model(BaseModel):\n    uuid5: UUID5\n\nModel(uuid5=uuid.uuid5(uuid.NAMESPACE_DNS, 'pydantic.org'))\n```\n"

@_dataclasses.dataclass
class PathType:
    path_type: Literal['file', 'dir', 'new']

    def __get_pydantic_json_schema__(self, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
        field_schema = handler(core_schema)
        format_conversion = {'file': 'file-path', 'dir': 'directory-path'}
        field_schema.update(format=format_conversion.get(self.path_type, 'path'), type='string')
        return field_schema

    def __get_pydantic_core_schema__(self, source: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        function_lookup = {'file': cast(core_schema.WithInfoValidatorFunction, self.validate_file), 'dir': cast(core_schema.WithInfoValidatorFunction, self.validate_directory), 'new': cast(core_schema.WithInfoValidatorFunction, self.validate_new)}
        return core_schema.with_info_after_validator_function(function_lookup[self.path_type], handler(source))

    def __hash__(self) -> int:
        return hash(type(self.path_type))
FilePath = Annotated[Path, PathType('file')]
"A path that must point to a file.\n\n```py\nfrom pathlib import Path\n\nfrom pydantic import BaseModel, FilePath, ValidationError\n\nclass Model(BaseModel):\n    f: FilePath\n\npath = Path('text.txt')\npath.touch()\nm = Model(f='text.txt')\nprint(m.model_dump())\n#> {'f': PosixPath('text.txt')}\npath.unlink()\n\npath = Path('directory')\npath.mkdir(exist_ok=True)\ntry:\n    Model(f='directory')  # directory\nexcept ValidationError as e:\n    print(e)\n    '''\n    1 validation error for Model\n    f\n      Path does not point to a file [type=path_not_file, input_value='directory', input_type=str]\n    '''\npath.rmdir()\n\ntry:\n    Model(f='not-exists-file')\nexcept ValidationError as e:\n    print(e)\n    '''\n    1 validation error for Model\n    f\n      Path does not point to a file [type=path_not_file, input_value='not-exists-file', input_type=str]\n    '''\n```\n"
DirectoryPath = Annotated[Path, PathType('dir')]
"A path that must point to a directory.\n\n```py\nfrom pathlib import Path\n\nfrom pydantic import BaseModel, DirectoryPath, ValidationError\n\nclass Model(BaseModel):\n    f: DirectoryPath\n\npath = Path('directory/')\npath.mkdir()\nm = Model(f='directory/')\nprint(m.model_dump())\n#> {'f': PosixPath('directory')}\npath.rmdir()\n\npath = Path('file.txt')\npath.touch()\ntry:\n    Model(f='file.txt')  # file\nexcept ValidationError as e:\n    print(e)\n    '''\n    1 validation error for Model\n    f\n      Path does not point to a directory [type=path_not_directory, input_value='file.txt', input_type=str]\n    '''\npath.unlink()\n\ntry:\n    Model(f='not-exists-directory')\nexcept ValidationError as e:\n    print(e)\n    '''\n    1 validation error for Model\n    f\n      Path does not point to a directory [type=path_not_directory, input_value='not-exists-directory', input_type=str]\n    '''\n```\n"
NewPath = Annotated[Path, PathType('new')]
'A path for a new file or directory that must not already exist. The parent directory must already exist.'
if TYPE_CHECKING:
    Json = Annotated[AnyType, ...]
else:

    class Json:
        """A special type wrapper which loads JSON before parsing.

        You can use the `Json` data type to make Pydantic first load a raw JSON string before
        validating the loaded data into the parametrized type:

        ```py
        from typing import Any, List

        from pydantic import BaseModel, Json, ValidationError


        class AnyJsonModel(BaseModel):
            json_obj: Json[Any]


        class ConstrainedJsonModel(BaseModel):
            json_obj: Json[List[int]]


        print(AnyJsonModel(json_obj='{"b": 1}'))
        #> json_obj={'b': 1}
        print(ConstrainedJsonModel(json_obj='[1, 2, 3]'))
        #> json_obj=[1, 2, 3]

        try:
            ConstrainedJsonModel(json_obj=12)
        except ValidationError as e:
            print(e)
            '''
            1 validation error for ConstrainedJsonModel
            json_obj
            JSON input should be string, bytes or bytearray [type=json_type, input_value=12, input_type=int]
            '''

        try:
            ConstrainedJsonModel(json_obj='[a, b]')
        except ValidationError as e:
            print(e)
            '''
            1 validation error for ConstrainedJsonModel
            json_obj
            Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[a, b]', input_type=str]
            '''

        try:
            ConstrainedJsonModel(json_obj='["a", "b"]')
        except ValidationError as e:
            print(e)
            '''
            2 validation errors for ConstrainedJsonModel
            json_obj.0
            Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='a', input_type=str]
            json_obj.1
            Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='b', input_type=str]
            '''
        ```

        When you dump the model using `model_dump` or `model_dump_json`, the dumped value will be the result of validation,
        not the original JSON string. However, you can use the argument `round_trip=True` to get the original JSON string back:

        ```py
        from typing import List

        from pydantic import BaseModel, Json


        class ConstrainedJsonModel(BaseModel):
            json_obj: Json[List[int]]


        print(ConstrainedJsonModel(json_obj='[1, 2, 3]').model_dump_json())
        #> {"json_obj":[1,2,3]}
        print(
            ConstrainedJsonModel(json_obj='[1, 2, 3]').model_dump_json(round_trip=True)
        )
        #> {"json_obj":"[1,2,3]"}
        ```
        """

        @classmethod
        def __class_getitem__(cls, item: AnyType) -> AnyType:
            return Annotated[item, cls()]

        @classmethod
        def __get_pydantic_core_schema__(cls, source: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
            if cls is source:
                return core_schema.json_schema(None)
            else:
                return core_schema.json_schema(handler(source))

        def __repr__(self) -> str:
            return 'Json'

        def __hash__(self) -> int:
            return hash(type(self))

        def __eq__(self, other: Any) -> bool:
            return type(other) == type(self)
SecretType = TypeVar('SecretType')

class _SecretBase(Generic[SecretType]):

    def __init__(self, secret_value: SecretType) -> None:
        self._secret_value: SecretType = secret_value

    def get_secret_value(self) -> SecretType:
        """Get the secret value.

        Returns:
            The secret value.
        """
        pass

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self.get_secret_value() == other.get_secret_value()

    def __hash__(self) -> int:
        return hash(self.get_secret_value())

    def __str__(self) -> str:
        return str(self._display())

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._display()!r})'

class Secret(_SecretBase[SecretType]):
    """A generic base class used for defining a field with sensitive information that you do not want to be visible in logging or tracebacks.

    You may either directly parametrize `Secret` with a type, or subclass from `Secret` with a parametrized type. The benefit of subclassing
    is that you can define a custom `_display` method, which will be used for `repr()` and `str()` methods. The examples below demonstrate both
    ways of using `Secret` to create a new secret type.

    1. Directly parametrizing `Secret` with a type:

    ```py
    from pydantic import BaseModel, Secret

    SecretBool = Secret[bool]

    class Model(BaseModel):
        secret_bool: SecretBool

    m = Model(secret_bool=True)
    print(m.model_dump())
    #> {'secret_bool': Secret('**********')}

    print(m.model_dump_json())
    #> {"secret_bool":"**********"}

    print(m.secret_bool.get_secret_value())
    #> True
    ```

    2. Subclassing from parametrized `Secret`:

    ```py
    from datetime import date

    from pydantic import BaseModel, Secret

    class SecretDate(Secret[date]):
        def _display(self) -> str:
            return '****/**/**'

    class Model(BaseModel):
        secret_date: SecretDate

    m = Model(secret_date=date(2022, 1, 1))
    print(m.model_dump())
    #> {'secret_date': SecretDate('****/**/**')}

    print(m.model_dump_json())
    #> {"secret_date":"****/**/**"}

    print(m.secret_date.get_secret_value())
    #> 2022-01-01
    ```

    The value returned by the `_display` method will be used for `repr()` and `str()`.
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        inner_type = None
        origin_type = get_origin(source)
        if origin_type is not None:
            inner_type = get_args(source)[0]
        else:
            bases = getattr(cls, '__orig_bases__', getattr(cls, '__bases__', []))
            for base in bases:
                if get_origin(base) is Secret:
                    inner_type = get_args(base)[0]
            if bases == [] or inner_type is None:
                raise TypeError(f"Can't get secret type from {cls.__name__}. Please use Secret[<type>], or subclass from Secret[<type>] instead.")
        inner_schema = handler.generate_schema(inner_type)

        def validate_secret_value(value, handler) -> Secret[SecretType]:
            if isinstance(value, Secret):
                value = value.get_secret_value()
            validated_inner = handler(value)
            return cls(validated_inner)

        def serialize(value: Secret[SecretType], info: core_schema.SerializationInfo) -> str | Secret[SecretType]:
            if info.mode == 'json':
                return str(value)
            else:
                return value
        return core_schema.json_or_python_schema(python_schema=core_schema.no_info_wrap_validator_function(validate_secret_value, inner_schema), json_schema=core_schema.no_info_after_validator_function(lambda x: cls(x), inner_schema), serialization=core_schema.plain_serializer_function_ser_schema(serialize, info_arg=True, when_used='always'))

class _SecretField(_SecretBase[SecretType]):
    _inner_schema: ClassVar[CoreSchema]
    _error_kind: ClassVar[str]

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:

        def serialize(value: _SecretField[SecretType], info: core_schema.SerializationInfo) -> str | _SecretField[SecretType]:
            if info.mode == 'json':
                return _secret_display(value.get_secret_value())
            else:
                return value

        def get_json_schema(_core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
            json_schema = handler(cls._inner_schema)
            _utils.update_not_none(json_schema, type='string', writeOnly=True, format='password')
            return json_schema
        json_schema = core_schema.no_info_after_validator_function(source, cls._inner_schema)

        def get_secret_schema(strict: bool) -> CoreSchema:
            return core_schema.json_or_python_schema(python_schema=core_schema.union_schema([core_schema.is_instance_schema(source), json_schema], custom_error_type=cls._error_kind, strict=strict), json_schema=json_schema, serialization=core_schema.plain_serializer_function_ser_schema(serialize, info_arg=True, return_schema=core_schema.str_schema(), when_used='json'))
        return core_schema.lax_or_strict_schema(lax_schema=get_secret_schema(strict=False), strict_schema=get_secret_schema(strict=True), metadata={'pydantic_js_functions': [get_json_schema]})

class SecretStr(_SecretField[str]):
    """A string used for storing sensitive information that you do not want to be visible in logging or tracebacks.

    When the secret value is nonempty, it is displayed as `'**********'` instead of the underlying value in
    calls to `repr()` and `str()`. If the value _is_ empty, it is displayed as `''`.

    ```py
    from pydantic import BaseModel, SecretStr

    class User(BaseModel):
        username: str
        password: SecretStr

    user = User(username='scolvin', password='password1')

    print(user)
    #> username='scolvin' password=SecretStr('**********')
    print(user.password.get_secret_value())
    #> password1
    print((SecretStr('password'), SecretStr('')))
    #> (SecretStr('**********'), SecretStr(''))
    ```
    """
    _inner_schema: ClassVar[CoreSchema] = core_schema.str_schema()
    _error_kind: ClassVar[str] = 'string_type'

    def __len__(self) -> int:
        return len(self._secret_value)

class SecretBytes(_SecretField[bytes]):
    """A bytes used for storing sensitive information that you do not want to be visible in logging or tracebacks.

    It displays `b'**********'` instead of the string value on `repr()` and `str()` calls.
    When the secret value is nonempty, it is displayed as `b'**********'` instead of the underlying value in
    calls to `repr()` and `str()`. If the value _is_ empty, it is displayed as `b''`.

    ```py
    from pydantic import BaseModel, SecretBytes

    class User(BaseModel):
        username: str
        password: SecretBytes

    user = User(username='scolvin', password=b'password1')
    #> username='scolvin' password=SecretBytes(b'**********')
    print(user.password.get_secret_value())
    #> b'password1'
    print((SecretBytes(b'password'), SecretBytes(b'')))
    #> (SecretBytes(b'**********'), SecretBytes(b''))
    ```
    """
    _inner_schema: ClassVar[CoreSchema] = core_schema.bytes_schema()
    _error_kind: ClassVar[str] = 'bytes_type'

    def __len__(self) -> int:
        return len(self._secret_value)

class PaymentCardBrand(str, Enum):
    amex = 'American Express'
    mastercard = 'Mastercard'
    visa = 'Visa'
    other = 'other'

    def __str__(self) -> str:
        return self.value

@deprecated('The `PaymentCardNumber` class is deprecated, use `pydantic_extra_types` instead. See https://docs.pydantic.dev/latest/api/pydantic_extra_types_payment/#pydantic_extra_types.payment.PaymentCardNumber.', category=PydanticDeprecatedSince20)
class PaymentCardNumber(str):
    """Based on: https://en.wikipedia.org/wiki/Payment_card_number."""
    strip_whitespace: ClassVar[bool] = True
    min_length: ClassVar[int] = 12
    max_length: ClassVar[int] = 19
    bin: str
    last4: str
    brand: PaymentCardBrand

    def __init__(self, card_number: str):
        self.validate_digits(card_number)
        card_number = self.validate_luhn_check_digit(card_number)
        self.bin = card_number[:6]
        self.last4 = card_number[-4:]
        self.brand = self.validate_brand(card_number)

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(cls.validate, core_schema.str_schema(min_length=cls.min_length, max_length=cls.max_length, strip_whitespace=cls.strip_whitespace))

    @classmethod
    def validate(cls, input_value: str, /, _: core_schema.ValidationInfo) -> PaymentCardNumber:
        """Validate the card number and return a `PaymentCardNumber` instance."""
        pass

    @property
    def masked(self) -> str:
        """Mask all but the last 4 digits of the card number.

        Returns:
            A masked card number string.
        """
        pass

    @classmethod
    def validate_digits(cls, card_number: str) -> None:
        """Validate that the card number is all digits."""
        pass

    @classmethod
    def validate_luhn_check_digit(cls, card_number: str) -> str:
        """Based on: https://en.wikipedia.org/wiki/Luhn_algorithm."""
        pass

    @staticmethod
    def validate_brand(card_number: str) -> PaymentCardBrand:
        """Validate length based on BIN for major brands:
        https://en.wikipedia.org/wiki/Payment_card_number#Issuer_identification_number_(IIN).
        """
        pass

class ByteSize(int):
    """Converts a string representing a number of bytes with units (such as `'1KB'` or `'11.5MiB'`) into an integer.

    You can use the `ByteSize` data type to (case-insensitively) convert a string representation of a number of bytes into
    an integer, and also to print out human-readable strings representing a number of bytes.

    In conformance with [IEC 80000-13 Standard](https://en.wikipedia.org/wiki/ISO/IEC_80000) we interpret `'1KB'` to mean 1000 bytes,
    and `'1KiB'` to mean 1024 bytes. In general, including a middle `'i'` will cause the unit to be interpreted as a power of 2,
    rather than a power of 10 (so, for example, `'1 MB'` is treated as `1_000_000` bytes, whereas `'1 MiB'` is treated as `1_048_576` bytes).

    !!! info
        Note that `1b` will be parsed as "1 byte" and not "1 bit".

    ```py
    from pydantic import BaseModel, ByteSize

    class MyModel(BaseModel):
        size: ByteSize

    print(MyModel(size=52000).size)
    #> 52000
    print(MyModel(size='3000 KiB').size)
    #> 3072000

    m = MyModel(size='50 PB')
    print(m.size.human_readable())
    #> 44.4PiB
    print(m.size.human_readable(decimal=True))
    #> 50.0PB
    print(m.size.human_readable(separator=' '))
    #> 44.4 PiB

    print(m.size.to('TiB'))
    #> 45474.73508864641
    ```
    """
    byte_sizes = {'b': 1, 'kb': 10 ** 3, 'mb': 10 ** 6, 'gb': 10 ** 9, 'tb': 10 ** 12, 'pb': 10 ** 15, 'eb': 10 ** 18, 'kib': 2 ** 10, 'mib': 2 ** 20, 'gib': 2 ** 30, 'tib': 2 ** 40, 'pib': 2 ** 50, 'eib': 2 ** 60, 'bit': 1 / 8, 'kbit': 10 ** 3 / 8, 'mbit': 10 ** 6 / 8, 'gbit': 10 ** 9 / 8, 'tbit': 10 ** 12 / 8, 'pbit': 10 ** 15 / 8, 'ebit': 10 ** 18 / 8, 'kibit': 2 ** 10 / 8, 'mibit': 2 ** 20 / 8, 'gibit': 2 ** 30 / 8, 'tibit': 2 ** 40 / 8, 'pibit': 2 ** 50 / 8, 'eibit': 2 ** 60 / 8}
    byte_sizes.update({k.lower()[0]: v for k, v in byte_sizes.items() if 'i' not in k})
    byte_string_pattern = '^\\s*(\\d*\\.?\\d+)\\s*(\\w+)?'
    byte_string_re = re.compile(byte_string_pattern, re.IGNORECASE)

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(function=cls._validate, schema=core_schema.union_schema([core_schema.str_schema(pattern=cls.byte_string_pattern), core_schema.int_schema(ge=0)], custom_error_type='byte_size', custom_error_message='could not parse value and unit from byte string'), serialization=core_schema.plain_serializer_function_ser_schema(int, return_schema=core_schema.int_schema(ge=0)))

    def human_readable(self, decimal: bool=False, separator: str='') -> str:
        """Converts a byte size to a human readable string.

        Args:
            decimal: If True, use decimal units (e.g. 1000 bytes per KB). If False, use binary units
                (e.g. 1024 bytes per KiB).
            separator: A string used to split the value and unit. Defaults to an empty string ('').

        Returns:
            A human readable string representation of the byte size.
        """
        pass

    def to(self, unit: str) -> float:
        """Converts a byte size to another unit, including both byte and bit units.

        Args:
            unit: The unit to convert to. Must be one of the following: B, KB, MB, GB, TB, PB, EB,
                KiB, MiB, GiB, TiB, PiB, EiB (byte units) and
                bit, kbit, mbit, gbit, tbit, pbit, ebit,
                kibit, mibit, gibit, tibit, pibit, eibit (bit units).

        Returns:
            The byte size in the new unit.
        """
        pass
if TYPE_CHECKING:
    PastDate = Annotated[date, ...]
    FutureDate = Annotated[date, ...]
else:

    class PastDate:
        """A date in the past."""

        @classmethod
        def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
            if cls is source:
                return core_schema.date_schema(now_op='past')
            else:
                schema = handler(source)
                _check_annotated_type(schema['type'], 'date', cls.__name__)
                schema['now_op'] = 'past'
                return schema

        def __repr__(self) -> str:
            return 'PastDate'

    class FutureDate:
        """A date in the future."""

        @classmethod
        def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
            if cls is source:
                return core_schema.date_schema(now_op='future')
            else:
                schema = handler(source)
                _check_annotated_type(schema['type'], 'date', cls.__name__)
                schema['now_op'] = 'future'
                return schema

        def __repr__(self) -> str:
            return 'FutureDate'

def condate(*, strict: bool | None=None, gt: date | None=None, ge: date | None=None, lt: date | None=None, le: date | None=None) -> type[date]:
    """A wrapper for date that adds constraints.

    Args:
        strict: Whether to validate the date value in strict mode. Defaults to `None`.
        gt: The value must be greater than this. Defaults to `None`.
        ge: The value must be greater than or equal to this. Defaults to `None`.
        lt: The value must be less than this. Defaults to `None`.
        le: The value must be less than or equal to this. Defaults to `None`.

    Returns:
        A date type with the specified constraints.
    """
    pass
if TYPE_CHECKING:
    AwareDatetime = Annotated[datetime, ...]
    NaiveDatetime = Annotated[datetime, ...]
    PastDatetime = Annotated[datetime, ...]
    FutureDatetime = Annotated[datetime, ...]
else:

    class AwareDatetime:
        """A datetime that requires timezone info."""

        @classmethod
        def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
            if cls is source:
                return core_schema.datetime_schema(tz_constraint='aware')
            else:
                schema = handler(source)
                _check_annotated_type(schema['type'], 'datetime', cls.__name__)
                schema['tz_constraint'] = 'aware'
                return schema

        def __repr__(self) -> str:
            return 'AwareDatetime'

    class NaiveDatetime:
        """A datetime that doesn't require timezone info."""

        @classmethod
        def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
            if cls is source:
                return core_schema.datetime_schema(tz_constraint='naive')
            else:
                schema = handler(source)
                _check_annotated_type(schema['type'], 'datetime', cls.__name__)
                schema['tz_constraint'] = 'naive'
                return schema

        def __repr__(self) -> str:
            return 'NaiveDatetime'

    class PastDatetime:
        """A datetime that must be in the past."""

        @classmethod
        def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
            if cls is source:
                return core_schema.datetime_schema(now_op='past')
            else:
                schema = handler(source)
                _check_annotated_type(schema['type'], 'datetime', cls.__name__)
                schema['now_op'] = 'past'
                return schema

        def __repr__(self) -> str:
            return 'PastDatetime'

    class FutureDatetime:
        """A datetime that must be in the future."""

        @classmethod
        def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
            if cls is source:
                return core_schema.datetime_schema(now_op='future')
            else:
                schema = handler(source)
                _check_annotated_type(schema['type'], 'datetime', cls.__name__)
                schema['now_op'] = 'future'
                return schema

        def __repr__(self) -> str:
            return 'FutureDatetime'

class EncoderProtocol(Protocol):
    """Protocol for encoding and decoding data to and from bytes."""

    @classmethod
    def decode(cls, data: bytes) -> bytes:
        """Decode the data using the encoder.

        Args:
            data: The data to decode.

        Returns:
            The decoded data.
        """
        pass

    @classmethod
    def encode(cls, value: bytes) -> bytes:
        """Encode the data using the encoder.

        Args:
            value: The data to encode.

        Returns:
            The encoded data.
        """
        pass

    @classmethod
    def get_json_format(cls) -> str:
        """Get the JSON format for the encoded data.

        Returns:
            The JSON format for the encoded data.
        """
        pass

class Base64Encoder(EncoderProtocol):
    """Standard (non-URL-safe) Base64 encoder."""

    @classmethod
    def decode(cls, data: bytes) -> bytes:
        """Decode the data from base64 encoded bytes to original bytes data.

        Args:
            data: The data to decode.

        Returns:
            The decoded data.
        """
        pass

    @classmethod
    def encode(cls, value: bytes) -> bytes:
        """Encode the data from bytes to a base64 encoded bytes.

        Args:
            value: The data to encode.

        Returns:
            The encoded data.
        """
        pass

    @classmethod
    def get_json_format(cls) -> Literal['base64']:
        """Get the JSON format for the encoded data.

        Returns:
            The JSON format for the encoded data.
        """
        pass

class Base64UrlEncoder(EncoderProtocol):
    """URL-safe Base64 encoder."""

    @classmethod
    def decode(cls, data: bytes) -> bytes:
        """Decode the data from base64 encoded bytes to original bytes data.

        Args:
            data: The data to decode.

        Returns:
            The decoded data.
        """
        pass

    @classmethod
    def encode(cls, value: bytes) -> bytes:
        """Encode the data from bytes to a base64 encoded bytes.

        Args:
            value: The data to encode.

        Returns:
            The encoded data.
        """
        pass

    @classmethod
    def get_json_format(cls) -> Literal['base64url']:
        """Get the JSON format for the encoded data.

        Returns:
            The JSON format for the encoded data.
        """
        pass

@_dataclasses.dataclass(**_internal_dataclass.slots_true)
class EncodedBytes:
    """A bytes type that is encoded and decoded using the specified encoder.

    `EncodedBytes` needs an encoder that implements `EncoderProtocol` to operate.

    ```py
    from typing_extensions import Annotated

    from pydantic import BaseModel, EncodedBytes, EncoderProtocol, ValidationError

    class MyEncoder(EncoderProtocol):
        @classmethod
        def decode(cls, data: bytes) -> bytes:
            if data == b'**undecodable**':
                raise ValueError('Cannot decode data')
            return data[13:]

        @classmethod
        def encode(cls, value: bytes) -> bytes:
            return b'**encoded**: ' + value

        @classmethod
        def get_json_format(cls) -> str:
            return 'my-encoder'

    MyEncodedBytes = Annotated[bytes, EncodedBytes(encoder=MyEncoder)]

    class Model(BaseModel):
        my_encoded_bytes: MyEncodedBytes

    # Initialize the model with encoded data
    m = Model(my_encoded_bytes=b'**encoded**: some bytes')

    # Access decoded value
    print(m.my_encoded_bytes)
    #> b'some bytes'

    # Serialize into the encoded form
    print(m.model_dump())
    #> {'my_encoded_bytes': b'**encoded**: some bytes'}

    # Validate encoded data
    try:
        Model(my_encoded_bytes=b'**undecodable**')
    except ValidationError as e:
        print(e)
        '''
        1 validation error for Model
        my_encoded_bytes
          Value error, Cannot decode data [type=value_error, input_value=b'**undecodable**', input_type=bytes]
        '''
    ```
    """
    encoder: type[EncoderProtocol]

    def __get_pydantic_json_schema__(self, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
        field_schema = handler(core_schema)
        field_schema.update(type='string', format=self.encoder.get_json_format())
        return field_schema

    def __get_pydantic_core_schema__(self, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(function=self.decode, schema=core_schema.bytes_schema(), serialization=core_schema.plain_serializer_function_ser_schema(function=self.encode))

    def decode(self, data: bytes, _: core_schema.ValidationInfo) -> bytes:
        """Decode the data using the specified encoder.

        Args:
            data: The data to decode.

        Returns:
            The decoded data.
        """
        pass

    def encode(self, value: bytes) -> bytes:
        """Encode the data using the specified encoder.

        Args:
            value: The data to encode.

        Returns:
            The encoded data.
        """
        pass

    def __hash__(self) -> int:
        return hash(self.encoder)

@_dataclasses.dataclass(**_internal_dataclass.slots_true)
class EncodedStr(EncodedBytes):
    """A str type that is encoded and decoded using the specified encoder.

    `EncodedStr` needs an encoder that implements `EncoderProtocol` to operate.

    ```py
    from typing_extensions import Annotated

    from pydantic import BaseModel, EncodedStr, EncoderProtocol, ValidationError

    class MyEncoder(EncoderProtocol):
        @classmethod
        def decode(cls, data: bytes) -> bytes:
            if data == b'**undecodable**':
                raise ValueError('Cannot decode data')
            return data[13:]

        @classmethod
        def encode(cls, value: bytes) -> bytes:
            return b'**encoded**: ' + value

        @classmethod
        def get_json_format(cls) -> str:
            return 'my-encoder'

    MyEncodedStr = Annotated[str, EncodedStr(encoder=MyEncoder)]

    class Model(BaseModel):
        my_encoded_str: MyEncodedStr

    # Initialize the model with encoded data
    m = Model(my_encoded_str='**encoded**: some str')

    # Access decoded value
    print(m.my_encoded_str)
    #> some str

    # Serialize into the encoded form
    print(m.model_dump())
    #> {'my_encoded_str': '**encoded**: some str'}

    # Validate encoded data
    try:
        Model(my_encoded_str='**undecodable**')
    except ValidationError as e:
        print(e)
        '''
        1 validation error for Model
        my_encoded_str
          Value error, Cannot decode data [type=value_error, input_value='**undecodable**', input_type=str]
        '''
    ```
    """

    def __get_pydantic_core_schema__(self, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(function=self.decode_str, schema=super(EncodedStr, self).__get_pydantic_core_schema__(source=source, handler=handler), serialization=core_schema.plain_serializer_function_ser_schema(function=self.encode_str))

    def decode_str(self, data: bytes, _: core_schema.ValidationInfo) -> str:
        """Decode the data using the specified encoder.

        Args:
            data: The data to decode.

        Returns:
            The decoded data.
        """
        pass

    def encode_str(self, value: str) -> str:
        """Encode the data using the specified encoder.

        Args:
            value: The data to encode.

        Returns:
            The encoded data.
        """
        pass

    def __hash__(self) -> int:
        return hash(self.encoder)
Base64Bytes = Annotated[bytes, EncodedBytes(encoder=Base64Encoder)]
"A bytes type that is encoded and decoded using the standard (non-URL-safe) base64 encoder.\n\nNote:\n    Under the hood, `Base64Bytes` use standard library `base64.encodebytes` and `base64.decodebytes` functions.\n\n    As a result, attempting to decode url-safe base64 data using the `Base64Bytes` type may fail or produce an incorrect\n    decoding.\n\n```py\nfrom pydantic import Base64Bytes, BaseModel, ValidationError\n\nclass Model(BaseModel):\n    base64_bytes: Base64Bytes\n\n# Initialize the model with base64 data\nm = Model(base64_bytes=b'VGhpcyBpcyB0aGUgd2F5')\n\n# Access decoded value\nprint(m.base64_bytes)\n#> b'This is the way'\n\n# Serialize into the base64 form\nprint(m.model_dump())\n#> {'base64_bytes': b'VGhpcyBpcyB0aGUgd2F5\n'}\n\n# Validate base64 data\ntry:\n    print(Model(base64_bytes=b'undecodable').base64_bytes)\nexcept ValidationError as e:\n    print(e)\n    '''\n    1 validation error for Model\n    base64_bytes\n      Base64 decoding error: 'Incorrect padding' [type=base64_decode, input_value=b'undecodable', input_type=bytes]\n    '''\n```\n"
Base64Str = Annotated[str, EncodedStr(encoder=Base64Encoder)]
"A str type that is encoded and decoded using the standard (non-URL-safe) base64 encoder.\n\nNote:\n    Under the hood, `Base64Bytes` use standard library `base64.encodebytes` and `base64.decodebytes` functions.\n\n    As a result, attempting to decode url-safe base64 data using the `Base64Str` type may fail or produce an incorrect\n    decoding.\n\n```py\nfrom pydantic import Base64Str, BaseModel, ValidationError\n\nclass Model(BaseModel):\n    base64_str: Base64Str\n\n# Initialize the model with base64 data\nm = Model(base64_str='VGhlc2UgYXJlbid0IHRoZSBkcm9pZHMgeW91J3JlIGxvb2tpbmcgZm9y')\n\n# Access decoded value\nprint(m.base64_str)\n#> These aren't the droids you're looking for\n\n# Serialize into the base64 form\nprint(m.model_dump())\n#> {'base64_str': 'VGhlc2UgYXJlbid0IHRoZSBkcm9pZHMgeW91J3JlIGxvb2tpbmcgZm9y\n'}\n\n# Validate base64 data\ntry:\n    print(Model(base64_str='undecodable').base64_str)\nexcept ValidationError as e:\n    print(e)\n    '''\n    1 validation error for Model\n    base64_str\n      Base64 decoding error: 'Incorrect padding' [type=base64_decode, input_value='undecodable', input_type=str]\n    '''\n```\n"
Base64UrlBytes = Annotated[bytes, EncodedBytes(encoder=Base64UrlEncoder)]
'A bytes type that is encoded and decoded using the URL-safe base64 encoder.\n\nNote:\n    Under the hood, `Base64UrlBytes` use standard library `base64.urlsafe_b64encode` and `base64.urlsafe_b64decode`\n    functions.\n\n    As a result, the `Base64UrlBytes` type can be used to faithfully decode "vanilla" base64 data\n    (using `\'+\'` and `\'/\'`).\n\n```py\nfrom pydantic import Base64UrlBytes, BaseModel\n\nclass Model(BaseModel):\n    base64url_bytes: Base64UrlBytes\n\n# Initialize the model with base64 data\nm = Model(base64url_bytes=b\'SHc_dHc-TXc==\')\nprint(m)\n#> base64url_bytes=b\'Hw?tw>Mw\'\n```\n'
Base64UrlStr = Annotated[str, EncodedStr(encoder=Base64UrlEncoder)]
'A str type that is encoded and decoded using the URL-safe base64 encoder.\n\nNote:\n    Under the hood, `Base64UrlStr` use standard library `base64.urlsafe_b64encode` and `base64.urlsafe_b64decode`\n    functions.\n\n    As a result, the `Base64UrlStr` type can be used to faithfully decode "vanilla" base64 data (using `\'+\'` and `\'/\'`).\n\n```py\nfrom pydantic import Base64UrlStr, BaseModel\n\nclass Model(BaseModel):\n    base64url_str: Base64UrlStr\n\n# Initialize the model with base64 data\nm = Model(base64url_str=\'SHc_dHc-TXc==\')\nprint(m)\n#> base64url_str=\'Hw?tw>Mw\'\n```\n'
__getattr__ = getattr_migration(__name__)

@_dataclasses.dataclass(**_internal_dataclass.slots_true)
class GetPydanticSchema:
    """Usage docs: https://docs.pydantic.dev/2.8/concepts/types/#using-getpydanticschema-to-reduce-boilerplate

    A convenience class for creating an annotation that provides pydantic custom type hooks.

    This class is intended to eliminate the need to create a custom "marker" which defines the
     `__get_pydantic_core_schema__` and `__get_pydantic_json_schema__` custom hook methods.

    For example, to have a field treated by type checkers as `int`, but by pydantic as `Any`, you can do:
    ```python
    from typing import Any

    from typing_extensions import Annotated

    from pydantic import BaseModel, GetPydanticSchema

    HandleAsAny = GetPydanticSchema(lambda _s, h: h(Any))

    class Model(BaseModel):
        x: Annotated[int, HandleAsAny]  # pydantic sees `x: Any`

    print(repr(Model(x='abc').x))
    #> 'abc'
    ```
    """
    get_pydantic_core_schema: Callable[[Any, GetCoreSchemaHandler], CoreSchema] | None = None
    get_pydantic_json_schema: Callable[[Any, GetJsonSchemaHandler], JsonSchemaValue] | None = None
    if not TYPE_CHECKING:

        def __getattr__(self, item: str) -> Any:
            """Use this rather than defining `__get_pydantic_core_schema__` etc. to reduce the number of nested calls."""
            if item == '__get_pydantic_core_schema__' and self.get_pydantic_core_schema:
                return self.get_pydantic_core_schema
            elif item == '__get_pydantic_json_schema__' and self.get_pydantic_json_schema:
                return self.get_pydantic_json_schema
            else:
                return object.__getattribute__(self, item)
    __hash__ = object.__hash__

@_dataclasses.dataclass(**_internal_dataclass.slots_true, frozen=True)
class Tag:
    """Provides a way to specify the expected tag to use for a case of a (callable) discriminated union.

    Also provides a way to label a union case in error messages.

    When using a callable `Discriminator`, attach a `Tag` to each case in the `Union` to specify the tag that
    should be used to identify that case. For example, in the below example, the `Tag` is used to specify that
    if `get_discriminator_value` returns `'apple'`, the input should be validated as an `ApplePie`, and if it
    returns `'pumpkin'`, the input should be validated as a `PumpkinPie`.

    The primary role of the `Tag` here is to map the return value from the callable `Discriminator` function to
    the appropriate member of the `Union` in question.

    ```py
    from typing import Any, Union

    from typing_extensions import Annotated, Literal

    from pydantic import BaseModel, Discriminator, Tag

    class Pie(BaseModel):
        time_to_cook: int
        num_ingredients: int

    class ApplePie(Pie):
        fruit: Literal['apple'] = 'apple'

    class PumpkinPie(Pie):
        filling: Literal['pumpkin'] = 'pumpkin'

    def get_discriminator_value(v: Any) -> str:
        if isinstance(v, dict):
            return v.get('fruit', v.get('filling'))
        return getattr(v, 'fruit', getattr(v, 'filling', None))

    class ThanksgivingDinner(BaseModel):
        dessert: Annotated[
            Union[
                Annotated[ApplePie, Tag('apple')],
                Annotated[PumpkinPie, Tag('pumpkin')],
            ],
            Discriminator(get_discriminator_value),
        ]

    apple_variation = ThanksgivingDinner.model_validate(
        {'dessert': {'fruit': 'apple', 'time_to_cook': 60, 'num_ingredients': 8}}
    )
    print(repr(apple_variation))
    '''
    ThanksgivingDinner(dessert=ApplePie(time_to_cook=60, num_ingredients=8, fruit='apple'))
    '''

    pumpkin_variation = ThanksgivingDinner.model_validate(
        {
            'dessert': {
                'filling': 'pumpkin',
                'time_to_cook': 40,
                'num_ingredients': 6,
            }
        }
    )
    print(repr(pumpkin_variation))
    '''
    ThanksgivingDinner(dessert=PumpkinPie(time_to_cook=40, num_ingredients=6, filling='pumpkin'))
    '''
    ```

    !!! note
        You must specify a `Tag` for every case in a `Tag` that is associated with a
        callable `Discriminator`. Failing to do so will result in a `PydanticUserError` with code
        [`callable-discriminator-no-tag`](../errors/usage_errors.md#callable-discriminator-no-tag).

    See the [Discriminated Unions] concepts docs for more details on how to use `Tag`s.

    [Discriminated Unions]: ../concepts/unions.md#discriminated-unions
    """
    tag: str

    def __get_pydantic_core_schema__(self, source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema:
        schema = handler(source_type)
        metadata = schema.setdefault('metadata', {})
        assert isinstance(metadata, dict)
        metadata[_core_utils.TAGGED_UNION_TAG_KEY] = self.tag
        return schema

@_dataclasses.dataclass(**_internal_dataclass.slots_true, frozen=True)
class Discriminator:
    """Usage docs: https://docs.pydantic.dev/2.8/concepts/unions/#discriminated-unions-with-callable-discriminator

    Provides a way to use a custom callable as the way to extract the value of a union discriminator.

    This allows you to get validation behavior like you'd get from `Field(discriminator=<field_name>)`,
    but without needing to have a single shared field across all the union choices. This also makes it
    possible to handle unions of models and primitive types with discriminated-union-style validation errors.
    Finally, this allows you to use a custom callable as the way to identify which member of a union a value
    belongs to, while still seeing all the performance benefits of a discriminated union.

    Consider this example, which is much more performant with the use of `Discriminator` and thus a `TaggedUnion`
    than it would be as a normal `Union`.

    ```py
    from typing import Any, Union

    from typing_extensions import Annotated, Literal

    from pydantic import BaseModel, Discriminator, Tag

    class Pie(BaseModel):
        time_to_cook: int
        num_ingredients: int

    class ApplePie(Pie):
        fruit: Literal['apple'] = 'apple'

    class PumpkinPie(Pie):
        filling: Literal['pumpkin'] = 'pumpkin'

    def get_discriminator_value(v: Any) -> str:
        if isinstance(v, dict):
            return v.get('fruit', v.get('filling'))
        return getattr(v, 'fruit', getattr(v, 'filling', None))

    class ThanksgivingDinner(BaseModel):
        dessert: Annotated[
            Union[
                Annotated[ApplePie, Tag('apple')],
                Annotated[PumpkinPie, Tag('pumpkin')],
            ],
            Discriminator(get_discriminator_value),
        ]

    apple_variation = ThanksgivingDinner.model_validate(
        {'dessert': {'fruit': 'apple', 'time_to_cook': 60, 'num_ingredients': 8}}
    )
    print(repr(apple_variation))
    '''
    ThanksgivingDinner(dessert=ApplePie(time_to_cook=60, num_ingredients=8, fruit='apple'))
    '''

    pumpkin_variation = ThanksgivingDinner.model_validate(
        {
            'dessert': {
                'filling': 'pumpkin',
                'time_to_cook': 40,
                'num_ingredients': 6,
            }
        }
    )
    print(repr(pumpkin_variation))
    '''
    ThanksgivingDinner(dessert=PumpkinPie(time_to_cook=40, num_ingredients=6, filling='pumpkin'))
    '''
    ```

    See the [Discriminated Unions] concepts docs for more details on how to use `Discriminator`s.

    [Discriminated Unions]: ../concepts/unions.md#discriminated-unions
    """
    discriminator: str | Callable[[Any], Hashable]
    'The callable or field name for discriminating the type in a tagged union.\n\n    A `Callable` discriminator must extract the value of the discriminator from the input.\n    A `str` discriminator must be the name of a field to discriminate against.\n    '
    custom_error_type: str | None = None
    'Type to use in [custom errors](../errors/errors.md#custom-errors) replacing the standard discriminated union\n    validation errors.\n    '
    custom_error_message: str | None = None
    'Message to use in custom errors.'
    custom_error_context: dict[str, int | str | float] | None = None
    'Context to use in custom errors.'

    def __get_pydantic_core_schema__(self, source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema:
        origin = _typing_extra.get_origin(source_type)
        if not origin or not _typing_extra.origin_is_union(origin):
            raise TypeError(f'{type(self).__name__} must be used with a Union type, not {source_type}')
        if isinstance(self.discriminator, str):
            from pydantic import Field
            return handler(Annotated[source_type, Field(discriminator=self.discriminator)])
        else:
            original_schema = handler(source_type)
            return self._convert_schema(original_schema)
_JSON_TYPES = {int, float, str, bool, list, dict, type(None)}

class _AllowAnyJson:

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema:
        python_schema = handler(source_type)
        return core_schema.json_or_python_schema(json_schema=core_schema.any_schema(), python_schema=python_schema)
if TYPE_CHECKING:
    JsonValue: TypeAlias = Union[List['JsonValue'], Dict[str, 'JsonValue'], str, bool, int, float, None]
    "A `JsonValue` is used to represent a value that can be serialized to JSON.\n\n    It may be one of:\n\n    * `List['JsonValue']`\n    * `Dict[str, 'JsonValue']`\n    * `str`\n    * `bool`\n    * `int`\n    * `float`\n    * `None`\n\n    The following example demonstrates how to use `JsonValue` to validate JSON data,\n    and what kind of errors to expect when input data is not json serializable.\n\n    ```py\n    import json\n\n    from pydantic import BaseModel, JsonValue, ValidationError\n\n    class Model(BaseModel):\n        j: JsonValue\n\n    valid_json_data = {'j': {'a': {'b': {'c': 1, 'd': [2, None]}}}}\n    invalid_json_data = {'j': {'a': {'b': ...}}}\n\n    print(repr(Model.model_validate(valid_json_data)))\n    #> Model(j={'a': {'b': {'c': 1, 'd': [2, None]}}})\n    print(repr(Model.model_validate_json(json.dumps(valid_json_data))))\n    #> Model(j={'a': {'b': {'c': 1, 'd': [2, None]}}})\n\n    try:\n        Model.model_validate(invalid_json_data)\n    except ValidationError as e:\n        print(e)\n        '''\n        1 validation error for Model\n        j.dict.a.dict.b\n          input was not a valid JSON value [type=invalid-json-value, input_value=Ellipsis, input_type=ellipsis]\n        '''\n    ```\n    "
else:
    JsonValue = TypeAliasType('JsonValue', Annotated[Union[Annotated[List['JsonValue'], Tag('list')], Annotated[Dict[str, 'JsonValue'], Tag('dict')], Annotated[str, Tag('str')], Annotated[bool, Tag('bool')], Annotated[int, Tag('int')], Annotated[float, Tag('float')], Annotated[None, Tag('NoneType')]], Discriminator(_get_type_name, custom_error_type='invalid-json-value', custom_error_message='input was not a valid JSON value'), _AllowAnyJson])

class _OnErrorOmit:

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.with_default_schema(schema=handler(source_type), on_error='omit')
OnErrorOmit = Annotated[T, _OnErrorOmit]
'\nWhen used as an item in a list, the key type in a dict, optional values of a TypedDict, etc.\nthis annotation omits the item from the iteration if there is any error validating it.\nThat is, instead of a [`ValidationError`][pydantic_core.ValidationError] being propagated up and the entire iterable being discarded\nany invalid items are discarded and the valid ones are returned.\n'

@_dataclasses.dataclass
class FailFast(_fields.PydanticMetadata, BaseMetadata):
    """A `FailFast` annotation can be used to specify that validation should stop at the first error.

    This can be useful when you want to validate a large amount of data and you only need to know if it's valid or not.

    You might want to enable this setting if you want to validate your data faster (basically, if you use this,
    validation will be more performant with the caveat that you get less information).

    ```py
    from typing import List
    from typing_extensions import Annotated
    from pydantic import BaseModel, FailFast, ValidationError

    class Model(BaseModel):
        x: Annotated[List[int], FailFast()]

    # This will raise a single error for the first invalid value and stop validation
    try:
        obj = Model(x=[1, 2, 'a', 4, 5, 'b', 7, 8, 9, 'c'])
    except ValidationError as e:
        print(e)
        '''
        1 validation error for Model
        x.2
          Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='a', input_type=str]
        '''
    ```
    """
    fail_fast: bool = True