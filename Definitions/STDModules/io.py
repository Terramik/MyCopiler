from .Utils import *


expr = []
realization = {}
header = '''
#include <stdio.h>

static inline bool parse_int(str_t str, size_t* ip, int* res) {
    long int val = 0;
    size_t i = *ip;
    uint8_t ch = str.start[i];
    while (i < str._0 && ch >= '0' && ch <= '9')
    {
        val = val * 10 + (ch - '0');
        if ( val > INT_MAX )
            return false;
        i++;
        ch = str.start[i];
    }
    if ( i == *ip ) 
        return false;
    *ip = i;
    *res = val;
    return true;
}


static inline bool print_iter(str_t str, bool* format_used, bool* format_mode, size_t* i, uint8_t* ch) {
    *ch = str.start[*i];
    
    if ( *ch == '%' ) {
        if ( *format_mode ) {
            if ( *i >= 1 && str.start[*i-1] == '%' ) {
                *format_mode = false;
                putchar('%');
            } else {
                printf("unexpected symbol; '%%' can only appear right after '%%'");
                abort();
            }
        } else {
            *format_mode = true;
        }
        (*i)++;
    } else {
        if ( !*format_mode ) {
            putchar(*ch);
            (*i)++;
        } else {
            if ( *format_used ) {
                printf("only 1 format on print__");
                abort();
            }
            
            return true;
        }
    }
    return false;
}
'''

module = Module(
    Module.Types.Standard, Path('io'),
    ControlCodeBlock([
        IOStream := make_cls(
            'IOStream', expr, realization,
            '''
            FILE* file;
            '''
        ),

        make_v('stdin', types.class_instance(IOStream), expr, realization, '''
            (IOStream_ourinstance){stdin};
        '''),

        make_v('stdout', types.class_instance(IOStream), expr, realization, '''
            (IOStream_ourinstance){stdout};
        '''),

        make_v('stderr', types.class_instance(IOStream), expr, realization, '''
            (IOStream_ourinstance){stderr};
        '''),

        # make_f('print_b', [
        #     ('format', types.str), ('b', types.bool),
        # ], [], expr, realization, '''
        # printf(format.start, b ? "true" : "false");
        # '''),
        #
        # make_f('print_c', [
        #     ('format', types.str), ('c', types.char),
        # ], [], expr, realization, '''
        # printf(format.start, c);
        # '''),
        #
        # make_f('print_s', [
        #     ('format', types.str),
        # ], [], expr, realization, '''
        # printf(format.start);
        # '''),

    ], zero_origin),
    export_=expr
)

IOStreamInst = types.class_instance(IOStream)
IOStreamInstP = types.class_instance(IOStream).add_modifier(Type.ModifierPointer())

make_cls_f(IOStream, '__init__', [
    ('self', IOStreamInst)
], [
    IOStreamInst
], expr, realization, '''
printf("Use \\"open\\" for creating IOStream instances");
abort();
''')


make_cls_f(IOStream, 'open', [
    ('path', types.str),
    ('mode', types.str)
], [
    IOStreamInst
], expr, realization, '''
return (IOStream_ourinstance){
    fopen((char*)(path.start), (char*)(mode.start))
};
''')

make_cls_f(IOStream, '__del__', [
    ('self', IOStreamInst)
], [], expr, realization, '''
fclose(self.file);
''')

make_cls_f(IOStream, 'is_eof', [
    ('stream', IOStreamInstP)
], [
    types.bool
], expr, realization, '''
return feof(stream->file) != 0;
''')

make_cls_f(IOStream, 'is_err', [
    ('stream', IOStreamInstP)
], [
    types.bool
], expr, realization, '''
return stream->file != NULL && ferror(stream->file) != 0;
''')

make_cls_f(IOStream, 'good', [
    ('stream', IOStreamInstP)
], [
    types.bool
], expr, realization, '''
return (feof(stream->file) == 0) && (ferror(stream->file) == 0);
''')


make_cls_f(IOStream, 'getc', [
    ('stream', IOStreamInstP)
], [
    types.char
], expr, realization, '''
return fgetc(stream->file);
''')


make_cls_f(IOStream, 'getl', [
    ('stream', IOStreamInstP),
    ('buf', types.str)
], [
    types.uint64
], expr, realization, '''
FILE* file = stream->file;
uint64_t i = 0;
while (i < buf._0 && (feof(stream->file) == 0) && (ferror(stream->file) == 0)) {
    uint8_t chr = fgetc(file);
    buf.start[i] = chr;
    if (chr == '\\n') break;
    i++;
}
return i;
''')


make_cls_f(IOStream, 'gets', [
    ('stream', IOStreamInstP),
    ('buf', types.str)
], [
    types.uint64
], expr, realization, '''
FILE* file = stream->file;
uint64_t i = 0; 
while (i < buf._0 && (feof(stream->file) == 0) && (ferror(stream->file) == 0)) {
    uint8_t chr = fgetc(file);
    buf.start[i] = chr;
    i++;
}
return i;
''')


make_cls_f(IOStream, 'putc', [
    ('stream', IOStreamInstP),
    ('ch', types.char)
], [], expr, realization, '''
fputc(ch, stream->file);
''')


make_cls_f(IOStream, 'puts', [
    ('stream', IOStreamInstP),
    ('str', types.str)
], [
    types.uint64
], expr, realization, '''
uint64_t i = 0;
while (i < str._0 && (feof(stream->file) == 0) && (ferror(stream->file) == 0)) {
    fputc(str.start[i], stream->file);
    i++;
}
return i;
''')


make_cls_f(IOStream, 'pos', [
    ('stream', IOStreamInstP)
], [
    types.int64
], expr, realization, '''
return ftell(stream->file);
''')


make_cls_f(IOStream, 'gotos', [
    ('stream', IOStreamInstP),
    ('pos', types.int64)
], [], expr, realization, '''
fseek(stream->file, pos, SEEK_SET);
''')

make_cls_f(IOStream, 'jump', [
    ('stream', IOStreamInstP),
    ('pos', types.int64)
], [], expr, realization, '''
fseek(stream->file, pos, SEEK_CUR);
''')

make_cls_f(IOStream, 'gotoe', [
    ('stream', IOStreamInstP),
    ('pos', types.int64)
], [], expr, realization, '''
fseek(stream->file, pos, SEEK_END);
''')


make_cls_f(IOStream, 'flush', [
    ('stream', IOStreamInstP)
], [], expr, realization, '''
fflush(stream->file);
''')


make_cls_f(IOStream, 'print_i', [
    ('stream', IOStreamInstP),
    ('format', types.str),
    ('i', types.int64)
], [], expr, realization, '''
int mod_min = INT_MIN;

bool format_used = false;
bool format_mode = false;

size_t i_ = 0;
while (i_ < format._0) {
    uint8_t ch = format.start[i_];

    if (
        print_iter(format, &format_used, &format_mode, &i_, &ch)
    ) {
        if ( ch == 'i' ) {
            if ( mod_min == INT_MIN ) {
                fprintf(stream->file, "%lld", i);
            } else {
                fprintf(stream->file, "%*lld", mod_min, i);
            }

            format_mode = false;
            format_used = true;
            i_++;

        } else if ( mod_min == INT_MIN ) {
            if ( !parse_int(format, &i_, &mod_min) ) { 
                printf("minimal size parse failed");
                abort();
            }
        }  else {
            printf("unexpected symbol: quantifier parts were expected");
            abort();
        }
    }
}
if ( !format_used ) { printf("no quantifier found"); abort(); }
if ( format_mode ) { printf("quantifier was not finished"); }
''')


make_cls_f(IOStream, 'print_u', [
    ('stream', IOStreamInstP),
    ('format', types.str),
    ('u', types.uint64)
], [], expr, realization, '''
int mod_min = INT_MIN;

bool format_used = false;
bool format_mode = false;

size_t i = 0;
while (i < format._0) {
    uint8_t ch = format.start[i];
    
    if (
        print_iter(format, &format_used, &format_mode, &i, &ch)
    ) {
        if ( ch == 'u' ) {
            if ( mod_min == INT_MIN ) {
                fprintf(stream->file, "%llu", u);
            } else {
                fprintf(stream->file, "%*llu", mod_min, u);
            }

            format_mode = false;
            format_used = true;
            i++;

        } else if ( mod_min == INT_MIN ) {
            if ( !parse_int(format, &i, &mod_min) ) { 
                printf("minimal size parse failed");
                abort();
            }
        }  else {
            printf("unexpected symbol: quantifier parts were expected");
            abort();
        }
    }
}
if ( !format_used ) { printf("no quantifier found"); abort(); }
if ( format_mode ) { printf("quantifier was not finished"); }
''')

make_cls_f(IOStream, 'print_f', [
    ('stream', IOStreamInstP),
    ('format', types.str),
    ('f', types.float64)
], [], expr, realization, '''
int mod_min = INT_MIN;
int mod_decimal = INT_MIN;

bool format_used = false;
bool format_mode = false;

size_t i = 0;
while (i < format._0) {
    uint8_t ch = format.start[i];
    
    if (
        print_iter(format, &format_used, &format_mode, &i, &ch)
    ) {
        if ( ch == 'f' ) {
            
            if ( mod_min == INT_MIN && mod_decimal == INT_MIN ) {
                fprintf(stream->file, "%f", f);
            } else if ( mod_decimal == INT_MIN ) {
                fprintf(stream->file, "%*f", mod_min, f);
            } else if ( mod_min == INT_MIN ) {
                fprintf(stream->file, "%.*f", mod_decimal, f);
            } else {
                fprintf(stream->file, "%*.*f", mod_min, mod_decimal, f);
            }

            format_mode = false;
            format_used = true;
            i++;

        } else if ( mod_decimal == INT_MIN && ch == '.' ) {
            i++;
            if ( !parse_int(format, &i, &mod_decimal) ) { 
                printf("the number of decimals parse failed");
                abort();
            }
        } else if ( mod_min == INT_MIN ) {
            if ( !parse_int(format, &i, &mod_min) ) { 
                printf("minimal size parse failed");
                abort();
            }
        }  else {
            printf("unexpected symbol: quantifier parts were expected");
            abort();
        }
    }
}
if ( !format_used ) { printf("no quantifier found"); abort(); }
if ( format_mode ) { printf("quantifier was not finished"); }
''')


make_cls_f(IOStream, 'print_b', [
    ('stream', IOStreamInstP),
    ('format', types.str),
    ('b', types.bool)
], [], expr, realization, '''
bool is_full = false;

bool format_used = false;
bool format_mode = false;

size_t i = 0;
while (i < format._0) {
    uint8_t ch = format.start[i];
    
    if (
        print_iter(format, &format_used, &format_mode, &i, &ch)
    ) {
        if ( ch == 'b' ) {

            if ( is_full ) {
                fprintf(stream->file, "%s", (b) ? "true" : "false");
            } else {
                fprintf(stream->file, "%1u", b);
            }

            format_mode = false;
            format_used = true;
            i++;

        } else if ( !is_full && ch == 't' ) {
            is_full = true;
            i++;
        } else {
            printf("unexpected symbol: quantifier parts were expected");
            abort();
        }
    }
}
if ( !format_used ) { printf("no quantifier found"); abort(); }
if ( format_mode ) { printf("quantifier was not finished"); }
''')


make_cls_f(IOStream, 'print_c', [
    ('stream', IOStreamInstP),
    ('format', types.str),
    ('c', types.uint8)
], [], expr, realization, '''
bool format_used = false;
bool format_mode = false;

size_t i = 0;
while (i < format._0) {
    uint8_t ch = format.start[i];

    if (
        print_iter(format, &format_used, &format_mode, &i, &ch)
    ) {
        if ( ch == 'c' ) {
            fprintf(stream->file, "%c", c);

            format_mode = false;
            format_used = true;
            i++;
        } else {
            printf("unexpected symbol: quantifier parts were expected");
            abort();
        }
    }
}
if ( !format_used ) { printf("no quantifier found"); abort(); }
if ( format_mode ) { printf("quantifier was not finished"); }
''')




'''


'''
