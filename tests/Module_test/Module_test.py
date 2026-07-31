import pytest
from .Simple import *
from pathlib import Path
from ...Definitions import TypesShortener as types
from ...Main.Modules import make_modules


def ch(type: Type) -> CheckType:
    return CheckTypeSimple(type)


CLS = ClassDescriptorManager()
def CLS_obj(id_: int) -> CheckType: return CheckTypeClassInstance(CLS.elem(id_))
def CLS_obj_p(id_: int) -> CheckType: return CheckTypeClassInstance(CLS.elem(id_), [Type.ModifierPointer()])
def CLS_obj_array(id_: int, length: int) -> CheckType: return CheckTypeClassInstance(CLS.elem(id_), [Type.ModifierArray(length)])
def CLS_itself(id_: int) -> CheckType: return CheckTypeClassItself(CLS.elem(id_))


@pytest.mark.parametrize('main_path, data, expected_module', [
    # 1. простейший тест с импортом псевдонима
    pytest.param(
        'the_dir/main.mylang',
        {
            'the_dir/main.mylang': '''
            from ../the_typedef import typedef;
            
            def main() {
                var the_var typedef;
            }
            ''',
            'the_dir/the_typedef.mylang': '''
            
            alias typedef int64;
            
            export typedef;
            '''
        },
        CheckModule(
            Module.Types.Main,
            CheckControlCodeBlock([
                    CheckControlImport(
                        '../the_typedef', [
                            ('typedef', 'typedef')
                        ]
                    ),
                    CheckControlFunctionDefinition(
                        'main', [], [], None,
                        CheckControlCodeBlock([
                            CheckControlExpression(
                                CheckTokenOperatorVariableDefinition(
                                    'the_var', ch(types.int64)
                                )
                            ),
                        ])
                    ),
            ]),
            CheckScope(
                Scope.Types.Global,
                typedefs={'typedef'},
                functions={'main'},
                children=[
                    CheckScope(
                        Scope.Types.Function,
                        variables={'the_var'}
                    )
                ]
            ),
            [
                CheckModule.CheckImportData('typedef', CheckControlTypedef('typedef', ch(types.int64))),
            ],
            [],
            [
                CheckModule(
                    Module.Types.Usual,
                    CheckControlCodeBlock([
                        CheckControlTypedef(
                            'typedef', ch(types.int64)
                        ),
                        CheckControlExport([
                            ('typedef', 'typedef')
                        ])
                    ]),
                    CheckScope(
                        Scope.Types.Global,
                        typedefs={'typedef'}
                    ),
                    [], [
                        CheckModule.CheckExportData('typedef', CheckControlTypedef('typedef', ch(types.int64))),
                    ], []
                ),
            ],
        ),
        id='1'
    ),
    # 2. алиасы для импортов и экспортов
    pytest.param(
        'dir/main/main.mylang',
        {
            'dir/main/main.mylang': '''
            from ../../utils/globals import glob as g;
            
            def main() {
                g = 10;
            }
            ''',
            'dir/utils/globals.mylang': '''
            
            var the_globulus int64;
        
            export the_globulus as glob;
            '''
        },
        CheckModule(
            Module.Types.Main,
            CheckControlCodeBlock([
                    CheckControlImport(
                        '.../utils/globals', [
                            ('glob', 'g')
                        ]
                    ),
                    CheckControlFunctionDefinition(
                        'main', [], [], [],
                        CheckControlCodeBlock([
                            CheckControlExpression(
                                CheckTokenOperatorAssignment(
                                    CheckTokenVariableAccess(
                                        'g', ch(types.int64)
                                    ),
                                    CheckTokenLiteral('10', ch(types.int64)),
                                    ch(types.int64)
                                )
                            ),
                        ])
                    ),
            ]),
            CheckScope(
                Scope.Types.Global,
                variables={'g'},
                functions={'main'},
                children=[
                    CheckScope(
                        Scope.Types.Function
                    )
                ]
            ),
            [
                CheckModule.CheckImportData('glob', CheckTokenOperatorVariableDefinition('g', ch(types.int64))),
            ],
            [],
            [
                CheckModule(
                    Module.Types.Usual,
                    CheckControlCodeBlock([
                        CheckControlExpression(
                            CheckTokenOperatorVariableDefinition(
                                'the_globulus', ch(types.int64)
                            )
                        ),
                        CheckControlExport([
                            ('the_globulus', 'glob')
                        ])
                    ]),
                    CheckScope(
                        Scope.Types.Global,
                        variables={'the_globulus'}
                    ),
                    [], [
                        CheckModule.CheckExportData('glob', CheckTokenOperatorVariableDefinition('the_globulus', ch(types.int64))),
                    ], []
                ),
            ],
        ),
        id='2'
    ),
    # 3. импорт из стандартной библиотеки
    pytest.param(
        'dir/blop.mylang',
        {
            'dir/blop.mylang': '''
            from std/io import print_s;
            
            def main() {
                print_s("Hello, World!");
            }
            
            '''
        },
        CheckModule(
            Module.Types.Main,
            CheckControlCodeBlock([
                CheckControlImport(
                    'std/io', [
                        ('print_s', 'print_s')
                    ]
                ),
                CheckControlFunctionDefinition(
                    'main', [], [], [],
                    CheckControlCodeBlock([
                        CheckControlExpression(
                            CheckTokenOperatorFunctionCall(
                                CheckTokenVariableAccess(
                                    'print_s', ch(types.func([types.str], []))
                                ),
                                [
                                    CheckTokenLiteral(
                                        'Hello, World!', ch(types.str)
                                    )
                                ],
                                None
                            )
                        ),
                    ])
                ),
            ]),
            CheckScope(
                Scope.Types.Global,
                variables={'print_s'},
                functions={'main'},
                children=[
                    CheckScope(
                        Scope.Types.Function
                    )
                ]
            ),
            [
                CheckModule.CheckImportData(
                    'print_s', CheckTokenOperatorVariableDefinition('print_s', ch(types.func([types.str], [])))
                ),
            ],
            [],
            [
                CheckModule.std(std.io)
            ],
        ),
        id='3'
    ),
    # 4. импорт и экспорт всего
    pytest.param(
        'blob/a.mylang',
        {
            'blob/a.mylang': '''
            from ../b import all;
            
            def main() {
                c = d();
            }
            ''',
            'blob/b.mylang': '''
            
            var c bool;
            
            def d() -> (bool) {
                return true;
            }
            
            export all;
            '''
        },
        CheckModule(
            Module.Types.Main,
            CheckControlCodeBlock([
                CheckControlImport(
                    '../b', [], True
                ),
                CheckControlFunctionDefinition(
                    'main', [], [], [],
                    CheckControlCodeBlock([
                        CheckControlExpression(
                            CheckTokenOperatorAssignment(
                                CheckTokenVariableAccess(
                                    'c', ch(types.bool)
                                ),
                                CheckTokenOperatorFunctionCall(
                                    CheckTokenVariableAccess(
                                        'd', ch(types.func([], [types.bool]))
                                    ),
                                    [],
                                    ch(types.bool)
                                ),
                                ch(types.bool)
                            )
                        ),
                    ])
                ),
            ]),
            CheckScope(
                Scope.Types.Global,
                variables={'c', 'd'},
                functions={'main'},
                children=[
                    CheckScope(
                        Scope.Types.Function
                    )
                ]
            ),
            [
                CheckModule.CheckImportData(
                    'c', CheckTokenOperatorVariableDefinition('c', ch(types.bool))
                ),
                CheckModule.CheckImportData(
                    'd', CheckTokenOperatorVariableDefinition('d', ch(types.func([], [types.bool])))
                ),
            ],
            [],
            [
                CheckModule(
                    Module.Types.Usual,
                    CheckControlCodeBlock([
                        CheckControlExpression(
                            CheckTokenOperatorVariableDefinition(
                                'c', ch(types.bool)
                            )
                        ),
                        CheckControlFunctionDefinition(
                            'd', [], [ch(types.bool)], [],
                            CheckControlCodeBlock([
                                CheckControlReturn([
                                    CheckTokenLiteral(
                                        'true', ch(types.bool)
                                    )
                                ])
                            ])
                        ),
                        CheckControlExport([], True)
                    ]),
                    CheckScope(
                        Scope.Types.Global,
                        variables={'c'},
                        functions={'d'},
                        children=[
                            CheckScope(
                                Scope.Types.Function
                            )
                        ]
                    ),
                    [], [
                        CheckModule.CheckExportData('c', CheckTokenOperatorVariableDefinition('c', ch(types.bool))),
                        CheckModule.CheckExportData('d', CheckTokenOperatorVariableDefinition('d', ch(types.func([], [types.bool]))))
                    ],
                    []
                )
            ],
        ),
        id='4'
    ),
    # 5. импорт модуля
    pytest.param(
        'blob/main.mylang',
        {
            'blob/main.mylang': '''
            from ../cls import MyClass;
        
            def main() {
                var obj MyClass;
                var objp (MyClass.MyClassPth);
            }
            ''',
            'blob/cls.mylang': '''
        
            class MyClass{
                {
                    x float64;
                    y float64;
                }
                
                alias MyClassPth (MyClass*);
            }
            
            export MyClass;
            '''
        },
        CheckModule(
            Module.Types.Main,
            CheckControlCodeBlock([
                CheckControlImport(
                    '../cls', [
                        ('MyClass', 'MyClass')
                    ]
                ),
                CheckControlFunctionDefinition(
                    'main', [], [], [],
                    CheckControlCodeBlock([
                        CheckControlExpression(
                            CheckTokenOperatorVariableDefinition(
                                'obj', CLS_obj(5)
                            )
                        ),
                        CheckControlExpression(
                            CheckTokenOperatorVariableDefinition(
                                'objp', CLS_obj_p(5)
                            )
                        )
                    ])
                )
            ]),
            CheckScope(
                Scope.Types.Global,
                variables={'MyClass'},
                functions={'main'},
                children=[
                    CheckScope(
                        Scope.Types.Function,
                        variables={'obj', 'objp'}
                    )
                ]
            ),
            [
                CheckModule.CheckImportData(
                    'MyClass', CheckTokenOperatorVariableDefinition('MyClass', CLS_itself(5))
                )
            ], [], [
                CheckModule(
                    Module.Types.Usual,
                    CheckControlCodeBlock([
                        CLS.assign(5, CheckControlClass(
                            'MyClass', [
                                CheckTokenOperatorVariableDefinition('x', ch(types.float64)),
                                CheckTokenOperatorVariableDefinition('y', ch(types.float64))
                            ],
                            CheckControlCodeBlock([
                                CheckControlTypedef(
                                    'MyClassPth', CLS_obj_p(5)
                                )
                            ])
                        )),
                        CheckControlExport(
                            [('MyClass', 'MyClass')]
                        )
                    ]),
                    CheckScope(
                        Scope.Types.Global,
                        classes={'MyClass'},
                        children=[
                            CheckScope(
                                Scope.Types.Class,
                                functions={'__init__'},
                                typedefs={'MyClassPth'},
                                children=[
                                    CheckScope(
                                        Scope.Types.Function,
                                        variables={'self'}
                                    )
                                ]
                            )
                        ]
                    ), [], [
                        CheckModule.CheckExportData('MyClass', CheckTokenOperatorVariableDefinition('MyClass', CLS_itself(5)))
                    ],
                    []
                )
            ]
        ),
        id='5'
    )
])
def test(tmp_path: Path, main_path, data: dict[str, str], expected_module: CheckModule):
    for path, code in data.items():
        path = tmp_path / path
        path.parent.mkdir(exist_ok=True, parents=True)
        path.write_text(code)

    module = make_modules(tmp_path / main_path)
    expected_module.is_match(module)














