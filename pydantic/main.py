"""Logic for creating models."""
from __future__ import annotations as _annotations
import operator
import sys
import types
import typing
import warnings
from copy import copy, deepcopy
from typing import TYPE_CHECKING, Any, Callable, ClassVar, Dict, Generator, Literal, Set, Tuple, TypeVar, Union, cast, overload
import pydantic_core
import typing_extensions
from pydantic_core import PydanticUndefined
from typing_extensions import Self, TypeAlias, Unpack
from ._internal import _config, _decorators, _fields, _forward_ref, _generics, _mock_val_ser, _model_construction, _repr, _typing_extra, _utils
from ._migration import getattr_migration
from .aliases import AliasChoices, AliasPath
from .annotated_handlers import GetCoreSchemaHandler, GetJsonSchemaHandler
from .config import ConfigDict
from .errors import PydanticUndefinedAnnotation, PydanticUserError
from .json_schema import DEFAULT_REF_TEMPLATE, GenerateJsonSchema, JsonSchemaMode, JsonSchemaValue, model_json_schema
from .plugin._schema_validator import PluggableSchemaValidator
from .warnings import PydanticDeprecatedSince20
ModelT = TypeVar('ModelT', bound='BaseModel')
TupleGenerator = Generator[Tuple[str, Any], None, None]
IncEx: TypeAlias = Union[Set[int], Set[str], Dict[int, Any], Dict[str, Any], None]
if TYPE_CHECKING:
    from inspect import Signature
    from pathlib import Path
    from pydantic_core import CoreSchema, SchemaSerializer, SchemaValidator
    from ._internal._utils import AbstractSetIntStr, MappingIntStrAny
    from .deprecated.parse import Protocol as DeprecatedParseProtocol
    from .fields import ComputedFieldInfo, FieldInfo, ModelPrivateAttr
    from .fields import PrivateAttr as _PrivateAttr
else:
    DeprecationWarning = PydanticDeprecatedSince20
__all__ = ('BaseModel', 'create_model')
_object_setattr = _model_construction.object_setattr

class BaseModel(metaclass=_model_construction.ModelMetaclass):
    """Usage docs: https://docs.pydantic.dev/2.8/concepts/models/

    A base class for creating Pydantic models.

    Attributes:
        __class_vars__: The names of classvars defined on the model.
        __private_attributes__: Metadata about the private attributes of the model.
        __signature__: The signature for instantiating the model.

        __pydantic_complete__: Whether model building is completed, or if there are still undefined fields.
        __pydantic_core_schema__: The pydantic-core schema used to build the SchemaValidator and SchemaSerializer.
        __pydantic_custom_init__: Whether the model has a custom `__init__` function.
        __pydantic_decorators__: Metadata containing the decorators defined on the model.
            This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
        __pydantic_generic_metadata__: Metadata for generic models; contains data used for a similar purpose to
            __args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these.
        __pydantic_parent_namespace__: Parent namespace of the model, used for automatic rebuilding of models.
        __pydantic_post_init__: The name of the post-init method for the model, if defined.
        __pydantic_root_model__: Whether the model is a `RootModel`.
        __pydantic_serializer__: The pydantic-core SchemaSerializer used to dump instances of the model.
        __pydantic_validator__: The pydantic-core SchemaValidator used to validate instances of the model.

        __pydantic_extra__: An instance attribute with the values of extra fields from validation when
            `model_config['extra'] == 'allow'`.
        __pydantic_fields_set__: An instance attribute with the names of fields explicitly set.
        __pydantic_private__: Instance attribute with the values of private attributes set on the model instance.
    """
    if TYPE_CHECKING:
        model_config: ClassVar[ConfigDict]
        '\n        Configuration for the model, should be a dictionary conforming to [`ConfigDict`][pydantic.config.ConfigDict].\n        '
        model_fields: ClassVar[dict[str, FieldInfo]]
        '\n        Metadata about the fields defined on the model,\n        mapping of field names to [`FieldInfo`][pydantic.fields.FieldInfo].\n\n        This replaces `Model.__fields__` from Pydantic V1.\n        '
        model_computed_fields: ClassVar[dict[str, ComputedFieldInfo]]
        'A dictionary of computed field names and their corresponding `ComputedFieldInfo` objects.'
        __class_vars__: ClassVar[set[str]]
        __private_attributes__: ClassVar[dict[str, ModelPrivateAttr]]
        __signature__: ClassVar[Signature]
        __pydantic_complete__: ClassVar[bool]
        __pydantic_core_schema__: ClassVar[CoreSchema]
        __pydantic_custom_init__: ClassVar[bool]
        __pydantic_decorators__: ClassVar[_decorators.DecoratorInfos]
        __pydantic_generic_metadata__: ClassVar[_generics.PydanticGenericMetadata]
        __pydantic_parent_namespace__: ClassVar[dict[str, Any] | None]
        __pydantic_post_init__: ClassVar[None | Literal['model_post_init']]
        __pydantic_root_model__: ClassVar[bool]
        __pydantic_serializer__: ClassVar[SchemaSerializer]
        __pydantic_validator__: ClassVar[SchemaValidator | PluggableSchemaValidator]
        __pydantic_extra__: dict[str, Any] | None = _PrivateAttr()
        __pydantic_fields_set__: set[str] = _PrivateAttr()
        __pydantic_private__: dict[str, Any] | None = _PrivateAttr()
    else:
        model_fields = {}
        model_computed_fields = {}
        __pydantic_decorators__ = _decorators.DecoratorInfos()
        __pydantic_parent_namespace__ = None
        __pydantic_core_schema__ = _mock_val_ser.MockCoreSchema('Pydantic models should inherit from BaseModel, BaseModel cannot be instantiated directly', code='base-model-instantiated')
        __pydantic_validator__ = _mock_val_ser.MockValSer('Pydantic models should inherit from BaseModel, BaseModel cannot be instantiated directly', val_or_ser='validator', code='base-model-instantiated')
        __pydantic_serializer__ = _mock_val_ser.MockValSer('Pydantic models should inherit from BaseModel, BaseModel cannot be instantiated directly', val_or_ser='serializer', code='base-model-instantiated')
    __slots__ = ('__dict__', '__pydantic_fields_set__', '__pydantic_extra__', '__pydantic_private__')
    model_config = ConfigDict()
    __pydantic_complete__ = False
    __pydantic_root_model__ = False

    def __init__(self, /, **data: Any) -> None:
        """Create a new model by parsing and validating input data from keyword arguments.

        Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
        validated to form a valid model.

        `self` is explicitly positional-only to allow `self` as a field name.
        """
        __tracebackhide__ = True
        self.__pydantic_validator__.validate_python(data, self_instance=self)
    __init__.__pydantic_base_init__ = True

    @property
    def model_extra(self) -> dict[str, Any] | None:
        """Get extra fields set during validation.

        Returns:
            A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`.
        """
        pass

    @property
    def model_fields_set(self) -> set[str]:
        """Returns the set of fields that have been explicitly set on this model instance.

        Returns:
            A set of strings representing the fields that have been set,
                i.e. that were not filled from defaults.
        """
        pass

    @classmethod
    def model_construct(cls, _fields_set: set[str] | None=None, **values: Any) -> Self:
        """Creates a new instance of the `Model` class with validated data.

        Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
        Default values are respected, but no other validation is performed.

        !!! note
            `model_construct()` generally respects the `model_config.extra` setting on the provided model.
            That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
            and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
            Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
            an error if extra values are passed, but they will be ignored.

        Args:
            _fields_set: The set of field names accepted for the Model instance.
            values: Trusted or pre-validated data dictionary.

        Returns:
            A new instance of the `Model` class with validated data.
        """
        pass

    def model_copy(self, *, update: dict[str, Any] | None=None, deep: bool=False) -> Self:
        """Usage docs: https://docs.pydantic.dev/2.8/concepts/serialization/#model_copy

        Returns a copy of the model.

        Args:
            update: Values to change/add in the new model. Note: the data is not validated
                before creating the new model. You should trust this data.
            deep: Set to `True` to make a deep copy of the model.

        Returns:
            New model instance.
        """
        pass

    def model_dump(self, *, mode: Literal['json', 'python'] | str='python', include: IncEx=None, exclude: IncEx=None, context: Any | None=None, by_alias: bool=False, exclude_unset: bool=False, exclude_defaults: bool=False, exclude_none: bool=False, round_trip: bool=False, warnings: bool | Literal['none', 'warn', 'error']=True, serialize_as_any: bool=False) -> dict[str, Any]:
        """Usage docs: https://docs.pydantic.dev/2.8/concepts/serialization/#modelmodel_dump

        Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

        Args:
            mode: The mode in which `to_python` should run.
                If mode is 'json', the output will only contain JSON serializable types.
                If mode is 'python', the output may contain non-JSON-serializable Python objects.
            include: A set of fields to include in the output.
            exclude: A set of fields to exclude from the output.
            context: Additional context to pass to the serializer.
            by_alias: Whether to use the field's alias in the dictionary key if defined.
            exclude_unset: Whether to exclude fields that have not been explicitly set.
            exclude_defaults: Whether to exclude fields that are set to their default value.
            exclude_none: Whether to exclude fields that have a value of `None`.
            round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
            warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
                "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
            serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

        Returns:
            A dictionary representation of the model.
        """
        pass

    def model_dump_json(self, *, indent: int | None=None, include: IncEx=None, exclude: IncEx=None, context: Any | None=None, by_alias: bool=False, exclude_unset: bool=False, exclude_defaults: bool=False, exclude_none: bool=False, round_trip: bool=False, warnings: bool | Literal['none', 'warn', 'error']=True, serialize_as_any: bool=False) -> str:
        """Usage docs: https://docs.pydantic.dev/2.8/concepts/serialization/#modelmodel_dump_json

        Generates a JSON representation of the model using Pydantic's `to_json` method.

        Args:
            indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
            include: Field(s) to include in the JSON output.
            exclude: Field(s) to exclude from the JSON output.
            context: Additional context to pass to the serializer.
            by_alias: Whether to serialize using field aliases.
            exclude_unset: Whether to exclude fields that have not been explicitly set.
            exclude_defaults: Whether to exclude fields that are set to their default value.
            exclude_none: Whether to exclude fields that have a value of `None`.
            round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
            warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
                "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
            serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

        Returns:
            A JSON string representation of the model.
        """
        pass

    @classmethod
    def model_json_schema(cls, by_alias: bool=True, ref_template: str=DEFAULT_REF_TEMPLATE, schema_generator: type[GenerateJsonSchema]=GenerateJsonSchema, mode: JsonSchemaMode='validation') -> dict[str, Any]:
        """Generates a JSON schema for a model class.

        Args:
            by_alias: Whether to use attribute aliases or not.
            ref_template: The reference template.
            schema_generator: To override the logic used to generate the JSON schema, as a subclass of
                `GenerateJsonSchema` with your desired modifications
            mode: The mode in which to generate the schema.

        Returns:
            The JSON schema for the given model class.
        """
        pass

    @classmethod
    def model_parametrized_name(cls, params: tuple[type[Any], ...]) -> str:
        """Compute the class name for parametrizations of generic classes.

        This method can be overridden to achieve a custom naming scheme for generic BaseModels.

        Args:
            params: Tuple of types of the class. Given a generic class
                `Model` with 2 type variables and a concrete model `Model[str, int]`,
                the value `(str, int)` would be passed to `params`.

        Returns:
            String representing the new class where `params` are passed to `cls` as type variables.

        Raises:
            TypeError: Raised when trying to generate concrete names for non-generic models.
        """
        pass

    def model_post_init(self, __context: Any) -> None:
        """Override this method to perform additional initialization after `__init__` and `model_construct`.
        This is useful if you want to do some validation that requires the entire model to be initialized.
        """
        pass

    @classmethod
    def model_rebuild(cls, *, force: bool=False, raise_errors: bool=True, _parent_namespace_depth: int=2, _types_namespace: dict[str, Any] | None=None) -> bool | None:
        """Try to rebuild the pydantic-core schema for the model.

        This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
        the initial attempt to build the schema, and automatic rebuilding fails.

        Args:
            force: Whether to force the rebuilding of the model schema, defaults to `False`.
            raise_errors: Whether to raise errors, defaults to `True`.
            _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
            _types_namespace: The types namespace, defaults to `None`.

        Returns:
            Returns `None` if the schema is already "complete" and rebuilding was not required.
            If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
        """
        pass

    @classmethod
    def model_validate(cls, obj: Any, *, strict: bool | None=None, from_attributes: bool | None=None, context: Any | None=None) -> Self:
        """Validate a pydantic model instance.

        Args:
            obj: The object to validate.
            strict: Whether to enforce types strictly.
            from_attributes: Whether to extract data from object attributes.
            context: Additional context to pass to the validator.

        Raises:
            ValidationError: If the object could not be validated.

        Returns:
            The validated model instance.
        """
        pass

    @classmethod
    def model_validate_json(cls, json_data: str | bytes | bytearray, *, strict: bool | None=None, context: Any | None=None) -> Self:
        """Usage docs: https://docs.pydantic.dev/2.8/concepts/json/#json-parsing

        Validate the given JSON data against the Pydantic model.

        Args:
            json_data: The JSON data to validate.
            strict: Whether to enforce types strictly.
            context: Extra variables to pass to the validator.

        Returns:
            The validated Pydantic model.

        Raises:
            ValueError: If `json_data` is not a JSON string.
        """
        pass

    @classmethod
    def model_validate_strings(cls, obj: Any, *, strict: bool | None=None, context: Any | None=None) -> Self:
        """Validate the given object with string data against the Pydantic model.

        Args:
            obj: The object containing string data to validate.
            strict: Whether to enforce types strictly.
            context: Extra variables to pass to the validator.

        Returns:
            The validated Pydantic model.
        """
        pass

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[BaseModel], handler: GetCoreSchemaHandler, /) -> CoreSchema:
        """Hook into generating the model's CoreSchema.

        Args:
            source: The class we are generating a schema for.
                This will generally be the same as the `cls` argument if this is a classmethod.
            handler: A callable that calls into Pydantic's internal CoreSchema generation logic.

        Returns:
            A `pydantic-core` `CoreSchema`.
        """
        schema = cls.__dict__.get('__pydantic_core_schema__')
        if schema is not None and (not isinstance(schema, _mock_val_ser.MockCoreSchema)):
            if not cls.__pydantic_generic_metadata__['origin']:
                return cls.__pydantic_core_schema__
        return handler(source)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler, /) -> JsonSchemaValue:
        """Hook into generating the model's JSON schema.

        Args:
            core_schema: A `pydantic-core` CoreSchema.
                You can ignore this argument and call the handler with a new CoreSchema,
                wrap this CoreSchema (`{'type': 'nullable', 'schema': current_schema}`),
                or just call the handler with the original schema.
            handler: Call into Pydantic's internal JSON schema generation.
                This will raise a `pydantic.errors.PydanticInvalidForJsonSchema` if JSON schema
                generation fails.
                Since this gets called by `BaseModel.model_json_schema` you can override the
                `schema_generator` argument to that function to change JSON schema generation globally
                for a type.

        Returns:
            A JSON schema, as a Python object.
        """
        return handler(core_schema)

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        """This is intended to behave just like `__init_subclass__`, but is called by `ModelMetaclass`
        only after the class is actually fully initialized. In particular, attributes like `model_fields` will
        be present when this is called.

        This is necessary because `__init_subclass__` will always be called by `type.__new__`,
        and it would require a prohibitively large refactor to the `ModelMetaclass` to ensure that
        `type.__new__` was called in such a manner that the class would already be sufficiently initialized.

        This will receive the same `kwargs` that would be passed to the standard `__init_subclass__`, namely,
        any kwargs passed to the class definition that aren't used internally by pydantic.

        Args:
            **kwargs: Any keyword arguments passed to the class definition that aren't used internally
                by pydantic.
        """
        pass

    def __class_getitem__(cls, typevar_values: type[Any] | tuple[type[Any], ...]) -> type[BaseModel] | _forward_ref.PydanticRecursiveRef:
        cached = _generics.get_cached_generic_type_early(cls, typevar_values)
        if cached is not None:
            return cached
        if cls is BaseModel:
            raise TypeError('Type parameters should be placed on typing.Generic, not BaseModel')
        if not hasattr(cls, '__parameters__'):
            raise TypeError(f'{cls} cannot be parametrized because it does not inherit from typing.Generic')
        if not cls.__pydantic_generic_metadata__['parameters'] and typing.Generic not in cls.__bases__:
            raise TypeError(f'{cls} is not a generic class')
        if not isinstance(typevar_values, tuple):
            typevar_values = (typevar_values,)
        _generics.check_parameters_count(cls, typevar_values)
        typevars_map: dict[_typing_extra.TypeVarType, type[Any]] = dict(zip(cls.__pydantic_generic_metadata__['parameters'], typevar_values))
        if _utils.all_identical(typevars_map.keys(), typevars_map.values()) and typevars_map:
            submodel = cls
            _generics.set_cached_generic_type(cls, typevar_values, submodel)
        else:
            parent_args = cls.__pydantic_generic_metadata__['args']
            if not parent_args:
                args = typevar_values
            else:
                args = tuple((_generics.replace_types(arg, typevars_map) for arg in parent_args))
            origin = cls.__pydantic_generic_metadata__['origin'] or cls
            model_name = origin.model_parametrized_name(args)
            params = tuple({param: None for param in _generics.iter_contained_typevars(typevars_map.values())})
            with _generics.generic_recursion_self_type(origin, args) as maybe_self_type:
                if maybe_self_type is not None:
                    return maybe_self_type
                cached = _generics.get_cached_generic_type_late(cls, typevar_values, origin, args)
                if cached is not None:
                    return cached
                try:
                    origin.model_rebuild(_parent_namespace_depth=3)
                except PydanticUndefinedAnnotation:
                    pass
                submodel = _generics.create_generic_submodel(model_name, origin, args, params)
                _generics.set_cached_generic_type(cls, typevar_values, submodel, origin, args)
        return submodel

    def __copy__(self) -> Self:
        """Returns a shallow copy of the model."""
        cls = type(self)
        m = cls.__new__(cls)
        _object_setattr(m, '__dict__', copy(self.__dict__))
        _object_setattr(m, '__pydantic_extra__', copy(self.__pydantic_extra__))
        _object_setattr(m, '__pydantic_fields_set__', copy(self.__pydantic_fields_set__))
        if not hasattr(self, '__pydantic_private__') or self.__pydantic_private__ is None:
            _object_setattr(m, '__pydantic_private__', None)
        else:
            _object_setattr(m, '__pydantic_private__', {k: v for k, v in self.__pydantic_private__.items() if v is not PydanticUndefined})
        return m

    def __deepcopy__(self, memo: dict[int, Any] | None=None) -> Self:
        """Returns a deep copy of the model."""
        cls = type(self)
        m = cls.__new__(cls)
        _object_setattr(m, '__dict__', deepcopy(self.__dict__, memo=memo))
        _object_setattr(m, '__pydantic_extra__', deepcopy(self.__pydantic_extra__, memo=memo))
        _object_setattr(m, '__pydantic_fields_set__', copy(self.__pydantic_fields_set__))
        if not hasattr(self, '__pydantic_private__') or self.__pydantic_private__ is None:
            _object_setattr(m, '__pydantic_private__', None)
        else:
            _object_setattr(m, '__pydantic_private__', deepcopy({k: v for k, v in self.__pydantic_private__.items() if v is not PydanticUndefined}, memo=memo))
        return m
    if not TYPE_CHECKING:

        def __getattr__(self, item: str) -> Any:
            private_attributes = object.__getattribute__(self, '__private_attributes__')
            if item in private_attributes:
                attribute = private_attributes[item]
                if hasattr(attribute, '__get__'):
                    return attribute.__get__(self, type(self))
                try:
                    return self.__pydantic_private__[item]
                except KeyError as exc:
                    raise AttributeError(f'{type(self).__name__!r} object has no attribute {item!r}') from exc
            else:
                try:
                    pydantic_extra = object.__getattribute__(self, '__pydantic_extra__')
                except AttributeError:
                    pydantic_extra = None
                if pydantic_extra:
                    try:
                        return pydantic_extra[item]
                    except KeyError as exc:
                        raise AttributeError(f'{type(self).__name__!r} object has no attribute {item!r}') from exc
                elif hasattr(self.__class__, item):
                    return super().__getattribute__(item)
                else:
                    raise AttributeError(f'{type(self).__name__!r} object has no attribute {item!r}')

        def __setattr__(self, name: str, value: Any) -> None:
            if name in self.__class_vars__:
                raise AttributeError(f'{name!r} is a ClassVar of `{self.__class__.__name__}` and cannot be set on an instance. If you want to set a value on the class, use `{self.__class__.__name__}.{name} = value`.')
            elif not _fields.is_valid_field_name(name):
                if self.__pydantic_private__ is None or name not in self.__private_attributes__:
                    _object_setattr(self, name, value)
                else:
                    attribute = self.__private_attributes__[name]
                    if hasattr(attribute, '__set__'):
                        attribute.__set__(self, value)
                    else:
                        self.__pydantic_private__[name] = value
                return
            self._check_frozen(name, value)
            attr = getattr(self.__class__, name, None)
            if isinstance(attr, property):
                attr.__set__(self, value)
            elif self.model_config.get('validate_assignment', None):
                self.__pydantic_validator__.validate_assignment(self, name, value)
            elif self.model_config.get('extra') != 'allow' and name not in self.model_fields:
                raise ValueError(f'"{self.__class__.__name__}" object has no field "{name}"')
            elif self.model_config.get('extra') == 'allow' and name not in self.model_fields:
                if self.model_extra and name in self.model_extra:
                    self.__pydantic_extra__[name] = value
                else:
                    try:
                        getattr(self, name)
                    except AttributeError:
                        self.__pydantic_extra__[name] = value
                    else:
                        _object_setattr(self, name, value)
            else:
                self.__dict__[name] = value
                self.__pydantic_fields_set__.add(name)

        def __delattr__(self, item: str) -> Any:
            if item in self.__private_attributes__:
                attribute = self.__private_attributes__[item]
                if hasattr(attribute, '__delete__'):
                    attribute.__delete__(self)
                    return
                try:
                    del self.__pydantic_private__[item]
                    return
                except KeyError as exc:
                    raise AttributeError(f'{type(self).__name__!r} object has no attribute {item!r}') from exc
            self._check_frozen(item, None)
            if item in self.model_fields:
                object.__delattr__(self, item)
            elif self.__pydantic_extra__ is not None and item in self.__pydantic_extra__:
                del self.__pydantic_extra__[item]
            else:
                try:
                    object.__delattr__(self, item)
                except AttributeError:
                    raise AttributeError(f'{type(self).__name__!r} object has no attribute {item!r}')

    def __getstate__(self) -> dict[Any, Any]:
        private = self.__pydantic_private__
        if private:
            private = {k: v for k, v in private.items() if v is not PydanticUndefined}
        return {'__dict__': self.__dict__, '__pydantic_extra__': self.__pydantic_extra__, '__pydantic_fields_set__': self.__pydantic_fields_set__, '__pydantic_private__': private}

    def __setstate__(self, state: dict[Any, Any]) -> None:
        _object_setattr(self, '__pydantic_fields_set__', state.get('__pydantic_fields_set__', {}))
        _object_setattr(self, '__pydantic_extra__', state.get('__pydantic_extra__', {}))
        _object_setattr(self, '__pydantic_private__', state.get('__pydantic_private__', {}))
        _object_setattr(self, '__dict__', state.get('__dict__', {}))
    if not TYPE_CHECKING:

        def __eq__(self, other: Any) -> bool:
            if isinstance(other, BaseModel):
                self_type = self.__pydantic_generic_metadata__['origin'] or self.__class__
                other_type = other.__pydantic_generic_metadata__['origin'] or other.__class__
                if not (self_type == other_type and getattr(self, '__pydantic_private__', None) == getattr(other, '__pydantic_private__', None) and (self.__pydantic_extra__ == other.__pydantic_extra__)):
                    return False
                if self.__dict__ == other.__dict__:
                    return True
                model_fields = type(self).model_fields.keys()
                if self.__dict__.keys() <= model_fields and other.__dict__.keys() <= model_fields:
                    return False
                getter = operator.itemgetter(*model_fields) if model_fields else lambda _: _utils._SENTINEL
                try:
                    return getter(self.__dict__) == getter(other.__dict__)
                except KeyError:
                    self_fields_proxy = _utils.SafeGetItemProxy(self.__dict__)
                    other_fields_proxy = _utils.SafeGetItemProxy(other.__dict__)
                    return getter(self_fields_proxy) == getter(other_fields_proxy)
            else:
                return NotImplemented
    if TYPE_CHECKING:

        def __init_subclass__(cls, **kwargs: Unpack[ConfigDict]):
            """This signature is included purely to help type-checkers check arguments to class declaration, which
            provides a way to conveniently set model_config key/value pairs.

            ```py
            from pydantic import BaseModel

            class MyModel(BaseModel, extra='allow'):
                ...
            ```

            However, this may be deceiving, since the _actual_ calls to `__init_subclass__` will not receive any
            of the config arguments, and will only receive any keyword arguments passed during class initialization
            that are _not_ expected keys in ConfigDict. (This is due to the way `ModelMetaclass.__new__` works.)

            Args:
                **kwargs: Keyword arguments passed to the class definition, which set model_config

            Note:
                You may want to override `__pydantic_init_subclass__` instead, which behaves similarly but is called
                *after* the class is fully initialized.
            """

    def __iter__(self) -> TupleGenerator:
        """So `dict(model)` works."""
        yield from [(k, v) for k, v in self.__dict__.items() if not k.startswith('_')]
        extra = self.__pydantic_extra__
        if extra:
            yield from extra.items()

    def __repr__(self) -> str:
        return f'{self.__repr_name__()}({self.__repr_str__(', ')})'

    def __repr_args__(self) -> _repr.ReprArgs:
        for k, v in self.__dict__.items():
            field = self.model_fields.get(k)
            if field and field.repr:
                yield (k, v)
        try:
            pydantic_extra = object.__getattribute__(self, '__pydantic_extra__')
        except AttributeError:
            pydantic_extra = None
        if pydantic_extra is not None:
            yield from ((k, v) for k, v in pydantic_extra.items())
        yield from ((k, getattr(self, k)) for k, v in self.model_computed_fields.items() if v.repr)
    __repr_name__ = _repr.Representation.__repr_name__
    __repr_str__ = _repr.Representation.__repr_str__
    __pretty__ = _repr.Representation.__pretty__
    __rich_repr__ = _repr.Representation.__rich_repr__

    def __str__(self) -> str:
        return self.__repr_str__(' ')

    @property
    @typing_extensions.deprecated('The `__fields__` attribute is deprecated, use `model_fields` instead.', category=None)
    def __fields__(self) -> dict[str, FieldInfo]:
        warnings.warn('The `__fields__` attribute is deprecated, use `model_fields` instead.', category=PydanticDeprecatedSince20)
        return self.model_fields

    @property
    @typing_extensions.deprecated('The `__fields_set__` attribute is deprecated, use `model_fields_set` instead.', category=None)
    def __fields_set__(self) -> set[str]:
        warnings.warn('The `__fields_set__` attribute is deprecated, use `model_fields_set` instead.', category=PydanticDeprecatedSince20)
        return self.__pydantic_fields_set__

    @typing_extensions.deprecated('The `copy` method is deprecated; use `model_copy` instead. See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.', category=None)
    def copy(self, *, include: AbstractSetIntStr | MappingIntStrAny | None=None, exclude: AbstractSetIntStr | MappingIntStrAny | None=None, update: Dict[str, Any] | None=None, deep: bool=False) -> Self:
        """Returns a copy of the model.

        !!! warning "Deprecated"
            This method is now deprecated; use `model_copy` instead.

        If you need `include` or `exclude`, use:

        ```py
        data = self.model_dump(include=include, exclude=exclude, round_trip=True)
        data = {**data, **(update or {})}
        copied = self.model_validate(data)
        ```

        Args:
            include: Optional set or mapping specifying which fields to include in the copied model.
            exclude: Optional set or mapping specifying which fields to exclude in the copied model.
            update: Optional dictionary of field-value pairs to override field values in the copied model.
            deep: If True, the values of fields that are Pydantic models will be deep-copied.

        Returns:
            A copy of the model with included, excluded and updated fields as specified.
        """
        pass

def create_model(model_name: str, /, *, __config__: ConfigDict | None=None, __doc__: str | None=None, __base__: type[ModelT] | tuple[type[ModelT], ...] | None=None, __module__: str | None=None, __validators__: dict[str, Callable[..., Any]] | None=None, __cls_kwargs__: dict[str, Any] | None=None, __slots__: tuple[str, ...] | None=None, **field_definitions: Any) -> type[ModelT]:
    """Usage docs: https://docs.pydantic.dev/2.8/concepts/models/#dynamic-model-creation

    Dynamically creates and returns a new Pydantic model, in other words, `create_model` dynamically creates a
    subclass of [`BaseModel`][pydantic.BaseModel].

    Args:
        model_name: The name of the newly created model.
        __config__: The configuration of the new model.
        __doc__: The docstring of the new model.
        __base__: The base class or classes for the new model.
        __module__: The name of the module that the model belongs to;
            if `None`, the value is taken from `sys._getframe(1)`
        __validators__: A dictionary of methods that validate fields. The keys are the names of the validation methods to
            be added to the model, and the values are the validation methods themselves. You can read more about functional
            validators [here](https://docs.pydantic.dev/2.8/concepts/validators/#field-validators).
        __cls_kwargs__: A dictionary of keyword arguments for class creation, such as `metaclass`.
        __slots__: Deprecated. Should not be passed to `create_model`.
        **field_definitions: Attributes of the new model. They should be passed in the format:
            `<name>=(<type>, <default value>)`, `<name>=(<type>, <FieldInfo>)`, or `typing.Annotated[<type>, <FieldInfo>]`.
            Any additional metadata in `typing.Annotated[<type>, <FieldInfo>, ...]` will be ignored.

    Returns:
        The new [model][pydantic.BaseModel].

    Raises:
        PydanticUserError: If `__base__` and `__config__` are both passed.
    """
    pass
__getattr__ = getattr_migration(__name__)