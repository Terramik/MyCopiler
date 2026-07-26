from .Utils import *


__all__ = ('rename_and_collect',)


"""
Модуль собирает все имена и переименовывает, чтобы они не перекрывали встроенные имена из си(и делает их глобальными).
"""


all_forbidden_words = {
    # base
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double',
    'else', 'enum', 'extern', 'float', 'for', 'goto', 'while', 'if', 'int', 'long',
    'register', 'return', 'short', 'signed', 'sizeof', 'static', 'struct', 'switch',
    'typedef', 'union', 'unsigned', 'void', 'volatile', 'inline', 'restrict', '_Alignas',
    '_Alignof', '_Atomic', '_Generic', '_Noreturn', '_Static_assert', '_Thread_local',
    'constexpr', 'nullptr', 'typeof', 'typeof_unqual', '_Complex', '_Imaginary',
    '__cplusplus', '__STDC__', '__VA_ARGS__', '_Pragma',
    # stdbool.h
    'bool', 'true', 'false', '_Bool', '__bool_true_false_are_defined ',
    # stdio.h
    'fclose', 'fopen', 'freopen', 'remove', 'tmpfile', 'clearerr', 'feof',
    'ferror', 'fflush', 'fgetpos', 'fgetc', 'fgets', 'ftell', 'fseek', 'fsetpos',
    'fread', 'fwrite', 'getc', 'getchar', 'gets', 'printf', 'vprintf', 'fprintf',
    'vfprintf', 'sprintf', 'snprintf', 'vsprintf', 'perror', 'putc', 'putchar',
    'scanf', 'vscanf', 'fscanf', 'vfscanf', 'sscanf', 'vsscanf', 'setbuf',
    'setvbuf', 'tmpnam', 'ungetc', 'puts', 'EOF', 'BUFSIZ', 'FILENAME_MAX',
    'FOPEN_MAX', '_IOFBF', '_IOLBF', '_IONBF', 'L_tmpnam', 'NULL', 'SEEK_CUR',
    'SEEK_END', 'SEEK_SET', 'TMP_MAX', 'stdin', 'stdout', 'stderr', 'fputc', 'getwchar',
    'putwchar', 'fgetws', 'fputws',
    # stdint.h
    'int_least8_t', 'int_least16_t', 'int_least32_t', 'int_least64_t', 'INT_LEAST8_MAX',
    'INT_LEAST16_MAX', 'INT_LEAST32_MAX', 'INT_LputcEAST64_MAX', 'INT_LEAST8_MIN', 'INT_LEAST16_MIN',
    'INT_LEAST32_MIN', 'INT_LEAST64_MIN', 'uint_least8_t', 'uint_least16_t', 'uint_least32_t',
    'uint_least64_t', 'UINT_LEAST8_MAX', 'UINT_LEAST16_MAX', 'UINT_LEAST32_MAX',
    'UINT_LEAST64_MAX', 'int_fast8_t', 'int_fast16_t', 'int_fast32_t', 'int_fast64_t',
    'INT_FAST8_MAX', 'INT_FAST16_MAX', 'INT_FAST32_MAX', 'INT_FAST64_MAX', 'INT_FAST8_MIN',
    'INT_FAST16_MIN', 'INT_FAST32_MIN', 'INT_FAST64_MIN', 'uint_fast8_t', 'uint_fast16_t',
    'uint_fast32_t', 'uint_fast64_t', 'UINT_FAST8_MAX', 'UINT_FAST16_MAX', 'UINT_FAST32_MAX',
    'UINT_FAST64_MAX', 'int8_t', 'int16_t', 'int32_t', 'int64_t', 'INT8_MAX', 'INT16_MAX',
    'INT32_MAX', 'INT64_MAX', 'INT8_MIN', 'INT16_MIN', 'INT32_MIN', 'INT64_MIN', 'uint8_t',
    'uint16_t', 'uint32_t', 'uint64_t', 'UINT8_MAX', 'UINT16_MAX', 'UINT32_MAX', 'UINT64_MAX'
    # stdlib.h
    'abort', 'abs', 'atexit', 'atof', 'atoi', 'atol', 'atoll', 'aligned_alloc', 'bsearch',
    'calloc', 'div', 'exit', 'free', 'getenv', 'labs', 'ldiv', 'llabs', 'lldiv', 'malloc',
    'mblen', 'mbstowcs', 'mbtowc', 'qsort', 'rand', 'realloc', 'srand', 'strtod', 'strtof',
    'strtol', 'strtold', 'strtoll', 'strtoul', 'strtoull', 'system', 'wcstombs', 'wctomb',
    '_Exit', 'at_quick_exit', 'quick_exit', 'NULL', 'EXIT_FAILURE', 'EXIT_SUCCESS',
    'RAND_MAX', 'MB_CUR_MAX', 'size_t', 'wchar_t', 'div_t', 'ldiv_t', 'lldiv_t',
    # наш assert и дебагинг
    'our_assert_f', 'our_assert', 'DEBUG_CODE', 'RELEASE_CODE',
    # для строк
    'c_str_to_slise', 'str_t',
    # для наших замыканий
    'env', '_env',
    # для main
    'not_very_main',
    # для нашего std
    'vars_initializer_io', 'vars_initializer_mem',  'vars_initializer_time',
    'vars_initializer_math', 'vars_initializer_rand', 'vars_initializer_testing',

}


class ItExpr(IteratorExpression):
    def __init__(self, all_names: set[str]):
        self.all_names = all_names

    def on_var_def(self, node: TokenOperatorVariableDefinition, parent: TypeExpressionParent):
        # переименовываем объявления переменной
        if node.name in self.all_names:
            node.name = get_unique_name(self.all_names, f'{node.name}_')
        else:
            self.all_names.add(node.name)


class ItCont(IteratorControl):
    def __init__(self, exp: ItExpr):
        self.all_names = exp.all_names
        self.exp = exp

    def on_expr(self, exp: TokenOperatorWvalueABC | TokenOperatorRvalueABC, parent: ControlABC):
        self.exp(exp, parent)

    def on_func_def(self, func_def: ControlFunctionDefinition):
        # это костыль, но мне нужно main в собственное пользование
        if func_def.name == 'main':
            func_def.name = 'not_very_main'
            func_def.var.name = func_def.name
        else:
        # переименовываем функции
            if func_def.name in self.all_names:
                func_def.name = get_unique_name(self.all_names, f'{func_def.name}_')
                func_def.var.name = func_def.name
            else:
                self.all_names.add(func_def.name)
        # аргументы тоже
        for arg in func_def.parameters:
            self.exp(arg, func_def)
        super().on_func_def(func_def)

    # просто класс
    def on_class(self, cls: ControlClass):
        if cls.name in self.all_names:
            cls.name = get_unique_name(self.all_names, f'{cls.name}_')
            cls.class_var.name = cls.name
        else:
            self.all_names.add(cls.name)

        super().on_class(cls)


class ItModule(IteratorModule):
    def __init__(self, all_names: set[str]):
        self.all_names = all_names
        self.it_control = ItCont(ItExpr(self.all_names))

    def on_module(self, module: Module):
        super().on_module(module)
        if not module.is_std:
            # импортируемые имена
            for imp in module.import_:
                if isinstance(imp.thing, TokenOperatorVariableDefinition):
                    self.it_control.exp(imp.thing, module)
            # всё остальное
            self.it_control(module.code)


def rename_and_collect(modules: Module | list[Module], data: DataContainer):
    """
    Переименовывает все переменные так, чтобы они не затмевали встроенные имена си,
    делает их уникальными на всб программу и собирает их.
    """
    data.all_names = data.all_names.union(all_forbidden_words)
    it_module = ItModule(data.all_names)
    it_module.many_modules(modules)
