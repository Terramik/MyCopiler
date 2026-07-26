from ...Definitions.Scopes import *
from ...Definitions.Tokens import *
from .AddImplicitDel import add_implicit_del
from .AddDelToTemporaryObjects import add_del_to_temporary_objects
from .ReplaceAccessToClassFieldsFromInstancesToDirectAccess import replace_access_to_class_fields_from_instances_to_direct_access
from .ReplaceClassInstanceCastToExplicitMethodUse import replace_class_instance_cast_to_explicit_method_use
from .ExpandDeInitializers import expand_deinitializers

__all__ = ('post_analyze_transforms',)


def post_analyze_transforms(code: ControlCodeBlock, scope: Scope):
    """Должен запускаться по окончанию анализа"""
    replace_class_instance_cast_to_explicit_method_use(code, scope)
    add_implicit_del(code, scope)
    add_del_to_temporary_objects(code, scope)
    replace_access_to_class_fields_from_instances_to_direct_access(code, scope)
    expand_deinitializers(code, scope)


# def transform(code: ControlCodeBlock, scope: Scope):
#     turn_some_lenof_to_constants(code, scope).
