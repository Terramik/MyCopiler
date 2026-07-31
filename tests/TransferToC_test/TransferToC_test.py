import pytest
from .Simple import *



@pytest.mark.parametrize('enter_path, data, expected_stdout', [
    # ---- IOStream функции ----
    pytest.param(
        'main.mylang',
        {
            'main.mylang': r'''
        from std/io import stdout;
        def main() -> () {
            stdout.putc('H');
            stdout.putc('i');
            stdout.putc('!');
            stdout.puts(" Hello");
            stdout.puts(" World\n");
            stdout.print_i("int: %i\n", -123);
            stdout.print_u("uint: %u\n", 456);
            stdout.print_f("float: %f\n", 3.1415);
            stdout.print_b("bool true: %b, ", true);
            stdout.print_b("bool false: %tb\n", false);
            # stdout.print_c("char: %c\n", 'A');
            # stdout.print_s("string: %s\n", "test");
        }
        ''',
        },
        "Hi! Hello World\nint: -123\nuint: 456\nfloat: 3.141500\nbool true: 1, bool false: false\n",
        id='1'
    ),
    # ---- Арифметические операции ----
    pytest.param(
        'main.mylang',
        {
            'main.mylang': r'''
            from std/io import stdout;
            def main() -> () {
                var a int64 = 10;
                var b int64 = 3;
                stdout.print_i("a+b=%i\n", a+b);
                stdout.print_i("a-b=%i\n", a-b);
                stdout.print_i("a*b=%i\n", a*b);
                stdout.print_i("a/b=%i\n", a/b);
                stdout.print_i("a%%b=%i\n", a%b);
                stdout.print_i("-a=%i\n", -a);
                var x float64 = 7.5;
                var y float64 = 2.0;
                stdout.print_f("x+y=%f\n", x+y);
                stdout.print_f("x-y=%f\n", x-y);
                stdout.print_f("x*y=%f\n", x*y);
                stdout.print_f("x/y=%f\n", x/y);
                var c uint64 = 0b1010;
                var d uint64 = 0b1100;
                stdout.print_u("c&d=%u\n", c & d);
                stdout.print_u("c|d=%u\n", c | d);
                stdout.print_u("c^d=%u\n", c ^ d);
                stdout.print_u("~c=%u\n", ~c);
                stdout.print_u("c<<2=%u\n", c << 2);
                stdout.print_u("c>>1=%u\n", c >> 1);
            }
            ''',
        },
        "a+b=13\na-b=7\na*b=30\na/b=3\na%b=1\n-a=-10\nx+y=9.500000\nx-y=5.500000\nx*y=15.000000\nx/y=3.750000\nc&d=8\nc|d=14\nc^d=6\n~c=18446744073709551605\nc<<2=40\nc>>1=5\n",
        id='2'
    ),
    # ---- Логические и сравнивающие операции, цепочки сравнений ----
    pytest.param(
        'main.mylang',
        {
            'main.mylang': r'''
            from std/io import stdout;
            def main() -> () {
                var a int64 = 5;
                var b int64 = 10;
                var c int64 = 5;
                stdout.print_b("a==b: %b\n", a == b);
                stdout.print_b("a!=b: %b\n", a != b);
                stdout.print_b("a<b: %b\n", a < b);
                stdout.print_b("a<=c: %b\n", a <= c);
                stdout.print_b("b>a: %b\n", b > a);
                stdout.print_b("b>=c: %b\n", b >= c);
                stdout.print_b("true and false: %b\n", true and false);
                stdout.print_b("true or false: %b\n", true or false);
                stdout.print_b("not true: %b\n", not true);
                stdout.print_b("not false: %b\n", not false);
                
                var x int64 = 2;
                var y int64 = 3;
                var z int64 = 4;
                stdout.print_b("x<y<z: %b\n", x < y < z);   # true
                stdout.print_b("x<y==z: %b\n", x < y == z); # false
                stdout.print_b("x<y<z and y<z: %b\n", x < y < z and y < z); # true
            }
            ''',
        },
        "a==b: 0\na!=b: 1\na<b: 1\na<=c: 1\nb>a: 1\nb>=c: 1\ntrue and false: 0\ntrue or false: 1\nnot true: 0\nnot false: 1\nx<y<z: 1\nx<y==z: 0\nx<y<z and y<z: 1\n",
        id='3'
    ),
    # ---- Условная конструкция ----
    pytest.param(
        'main.mylang',
        {
            'main.mylang': r'''
            from std/io import stdout;
            def main() -> () {
                var x int64 = 10;
                if x < 5 {
                    stdout.puts("if\n");
                } elif x == 10 {
                    stdout.puts("elif\n");
                } else {
                    stdout.puts("else\n");
                }
                if x == 10 {
                    stdout.puts("if2\n");
                }
                if false {
                    stdout.puts("if3\n");
                } elif false {
                    stdout.puts("elif3\n");
                } else {
                    stdout.puts("else3\n");
                }
            }
            ''',
        },
        "elif\nif2\nelse3\n",
        id='4'
    ),
    # ---- Циклы (while, break, continue) ----
    pytest.param(
        'main.mylang',
        {
            'main.mylang': r'''
            from std/io import stdout;
            def main() -> () {
                var i int64 = 0;
                while i < 5 {
                    i = i + 1;
                    if i == 3 { continue; }
                    stdout.print_i("%i", i);
                }
                stdout.puts("\n");
                i = 0;
                while true {
                    i = i + 1;
                    if i == 5 { break; }
                    stdout.print_i("%i", i);
                }
                stdout.puts("\n");
                
                var j int64 = 0;
                while i < 10 {
                    i = i + 1;
                    while j < 2 {
                        j = j + 1;
                        stdout.print_i("%i", j);
                    }
                }
                stdout.puts("\n");
            }
            ''',
        },
        "1245\n1234\n12\n",
        id='5'
    ),
    # ---- Функции (параметры, возврат, рекурсия, глобальные переменные) ----
    pytest.param(
        'main.mylang',
        {
            'main.mylang': r'''
            from std/io import stdout;
            
            var glob int64 = 100;
            
            def add(a int64, b int64) -> (int64) {
                return a + b;
            }
            def mul(a int64, b int64) -> (int64) {
                return a * b;
            }
            def fact(n int64) -> (int64) {
                if n <= 1 { return 1; }
                return n * fact(n - 1);
            }
            def swap(a int64, b int64) -> (int64, int64) {
                return b, a;
            }
            
            def main() -> () {
                var x int64 = 5;
                var y int64 = 7;
                stdout.print_i("add(5,7)=%i\n", add(x, y));
                stdout.print_i("mul(5,7)=%i\n", mul(x, y));
                stdout.print_i("fact(5)=%i\n", fact(5));
                stdout.print_i("glob=%i\n", glob);
                
                def inner() -> (int64) {
                    return glob + 1;
                }
                stdout.print_i("inner()=%i\n", inner());
                
                var a int64, var b int64 = swap(10, 20);
                stdout.print_i("swap(10,20) -> %i, ", a);
                stdout.print_i("%i\n", b);
            }
            ''',
        },
        "add(5,7)=12\nmul(5,7)=35\nfact(5)=120\nglob=100\ninner()=101\nswap(10,20) -> 20, 10\n",
        id='6'
    ),
    # ---- Множественный результат и массовое присваивание ----
    pytest.param(
        'main.mylang',
        {
            'main.mylang': r'''
            from std/io import stdout;
            def f() -> (int64, int64, int64) {
                return 1, 2, 3;
            }
            def print3(a int64, b int64, c int64) {
                stdout.print_i("%i ", a);
                stdout.print_i("%i ", b);
                stdout.print_i("%i\n", c);
            }
            def main() -> () {
                var a int64; var b int64; var c int64;
                a, b, c = f();
                print3(a, b, c);
                a, b = 10, 20;
                c, b = 30, 40;
                print3(a, b, c);
                
                var x int64; var y int64; var z int64;
                x, y, z, a = 100, f();
                print3(x, y, z);
            }
            ''',
        },
        "1 2 3\n10 40 30\n100 1 2\n",
        id='7'
    ),
    # ---- Массивы (одномерные, многомерные, создание, индексация, присваивание, lenof) ----
    pytest.param(
        'main.mylang',
        {
            'main.mylang': r'''
            from std/io import stdout;
            def print3(a int64, b int64, c int64) {
                stdout.print_i("%i ", a);
                stdout.print_i("%i ", b);
                stdout.print_i("%i\n", c);
            }
            def main() -> () {
                var arr1 int64[3] = [1, 2, 3];
                print3(arr1[0], arr1[1], arr1[2]);
                arr1[1] = 10;
                print3(arr1[0], arr1[1], arr1[2]);
                var arr2 int64[3][2] = [[1,2,3],[4,5,6]];
                print3(arr2[0][0], arr2[0][1], arr2[0][2]);
                print3(arr2[1][0], arr2[1][1], arr2[1][2]);
                arr2[1][1] = 100;
                stdout.print_i("%i\n", arr2[1][1]);
                stdout.print_i("lenof arr1 = %i\n", lenof arr1);
                stdout.print_i("lenof arr2[0] = %i\n", lenof (arr2[0]));
                
                var arr3 float64[3] = [1, 2.5, 3];
                stdout.print_f("%f ", arr3[0]);
                stdout.print_f("%f ", arr3[1]);
                stdout.print_f("%f\n", arr3[2]);
            }
            ''',
        },
        "1 2 3\n1 10 3\n1 2 3\n4 5 6\n100\nlenof arr1 = 3\nlenof arr2[0] = 3\n1.000000 2.500000 3.000000\n",
        id='8'
    ),
    # ---- Указатели (взятие адреса, разыменование, изменение, указатель на функцию) ----
    pytest.param(
        'main.mylang',
        {
            'main.mylang': r'''
            from std/io import stdout;
            def add(a int64, b int64) -> (int64) {
                return a + b;
            }
            def main() -> () {
                var x int64 = 42;
                var ptr int64* = x&;
                stdout.print_i("*ptr = %i\n", ptr*);
                ptr* = 100;
                stdout.print_i("x = %i\n", x);
                var y int64 = 200;
                var ptr2 (int64*) = y&;
                ptr = ptr2;
                stdout.print_i("*ptr = %i\n", ptr*);
        
                var fptr func(int64,int64)->(int64) = add;
                var res int64 = fptr(3, 4);
                stdout.print_i("fptr(3,4) = %i\n", res);
        
                var fptr2 func(int64,int64)->(int64) = add;
                stdout.print_i("fptr2(5,6) = %i\n", fptr2(5,6));
        
                var pp int64** = ptr2&;
                stdout.print_i("**pp = %i\n", pp**);
            }
            ''',
        },
        "*ptr = 42\nx = 100\n*ptr = 200\nfptr(3,4) = 7\nfptr2(5,6) = 11\n**pp = 200\n",
        id='9'
    ),
    # ---- Срезы (создание из массива, среза, указателя, индексация, присваивание) ----
    pytest.param(
        'main.mylang',
        {
            'main.mylang': r'''
            from std/io import stdout;
            def main() -> () {
                var arr int64[5] = [10, 20, 30, 40, 50];
                var sl1 int64[] = arr[1:2];   # [20,30]
                stdout.print_i("%i ", sl1[0]);
                stdout.print_i("%i\n", sl1[1]);
                sl1[0] = 99;
                stdout.print_i("%i ", sl1[0]);
                stdout.print_i("%i\n", sl1[1]);
                
                var sl2 int64[] = sl1[1:1];   # [30]
                stdout.print_i("%i\n", sl2[0]);
                
                var ptr (int64*) = (arr[0])&;
                var sl3 int64[] = ptr[2:2];   # [30,40]
                
                stdout.print_i("lenof sl1 = %i\n", lenof sl1);
                stdout.print_i("lenof sl2 = %i\n", lenof sl2);
                
                sl1[1] = 999;
                stdout.print_i("%i ", sl1[0]);
                stdout.print_i("%i\n", sl1[1]);
                
                var mat int64[3][3] = [[1,2,3],[4,5,6],[7,8,9]];
                var slmat int64[,] = mat[:2,2];
                stdout.print_i("%i ", slmat[0][0]);
                stdout.print_i("%i\n", slmat[0][1]);
                stdout.print_i("%i ", slmat[1][0]);
                stdout.print_i("%i\n", slmat[1][1]);
            }
            ''',
        },
        "20 30\n99 30\n30\nlenof sl1 = 2\nlenof sl2 = 1\n99 999\n1 2\n3 4\n",
        id="10"
    ),
])
def test(tmp_path: Path, enter_path, data: dict[str, str], expected_stdout: str):
    for path, code in data.items():
        path = tmp_path / path
        path.parent.mkdir(exist_ok=True, parents=True)
        path.write_text(code)
    res_path = tmp_path / 'program'
    transfer(tmp_path / enter_path, res_path)
    res = execute(res_path)
    assert res.returncode == 0
    assert res.stdout == expected_stdout


