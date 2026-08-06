
#include "../include/base.h"

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

    IOStreaminstance __init__g(void* _par){
        
printf("Use \"open\" for creating IOStream instances");
abort();

    }
    IOStreaminstance openg(str_t path, str_t mode,void* _par){
        
return (IOStreaminstance){
    fopen((char*)(path.start), (char*)(mode.start))
};

    }
    void __del__g(IOStreaminstance self,void* _par){
        
fclose(self.file);

    }
    bool is_eofg(IOStreaminstancep stream,void* _par){
        
return feof(stream->file) != 0;

    }
    bool is_errg(IOStreaminstancep stream,void* _par){
        
return stream->file != NULL && ferror(stream->file) != 0;

    }
    bool goodg(IOStreaminstancep stream,void* _par){
        
return (feof(stream->file) == 0) && (ferror(stream->file) == 0);

    }
    uint8_t getcg(IOStreaminstancep stream,void* _par){
        
return fgetc(stream->file);

    }
    uint64_t getlg(IOStreaminstancep stream, str_t buf,void* _par){
        
FILE* file = stream->file;
uint64_t i = 0;
while (i < buf._0 && (feof(stream->file) == 0) && (ferror(stream->file) == 0)) {
    uint8_t chr = fgetc(file);
    buf.start[i] = chr;
    if (chr == '\n') break;
    i++;
}
return i;

    }
    uint64_t getsg(IOStreaminstancep stream, str_t buf,void* _par){
        
FILE* file = stream->file;
uint64_t i = 0; 
while (i < buf._0 && (feof(stream->file) == 0) && (ferror(stream->file) == 0)) {
    uint8_t chr = fgetc(file);
    buf.start[i] = chr;
    i++;
}
return i;

    }
    void putcg(IOStreaminstancep stream, uint8_t ch,void* _par){
        
fputc(ch, stream->file);

    }
    uint64_t putsg(IOStreaminstancep stream, str_t str,void* _par){
        
uint64_t i = 0;
while (i < str._0 && (feof(stream->file) == 0) && (ferror(stream->file) == 0)) {
    fputc(str.start[i], stream->file);
    i++;
}
return i;

    }
    int64_t posg(IOStreaminstancep stream,void* _par){
        
return ftell(stream->file);

    }
    void gotosg(IOStreaminstancep stream, int64_t pos,void* _par){
        
fseek(stream->file, pos, SEEK_SET);

    }
    void jumpg(IOStreaminstancep stream, int64_t pos,void* _par){
        
fseek(stream->file, pos, SEEK_CUR);

    }
    void gotoeg(IOStreaminstancep stream, int64_t pos,void* _par){
        
fseek(stream->file, pos, SEEK_END);

    }
    void flushg(IOStreaminstancep stream,void* _par){
        
fflush(stream->file);

    }
    void print_ig(IOStreaminstancep stream, str_t format, int64_t i,void* _par){
        
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

    }
    void print_ug(IOStreaminstancep stream, str_t format, uint64_t u,void* _par){
        
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

    }
    void print_fg(IOStreaminstancep stream, str_t format, double f,void* _par){
        
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

    }
    void print_bg(IOStreaminstancep stream, str_t format, bool b,void* _par){
        
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

    }
    void print_cg(IOStreaminstancep stream, str_t format, uint8_t c,void* _par){
        
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

    }IOStreamtype IOStream;
IOStreaminstance stdin_our;
IOStreaminstance stdout_our;
IOStreaminstance stderr_our;
void vars_initializer_io(){
    IOStream = (IOStreamtype){
        .__init__ = __init__g,.open = openg,.__del__ = __del__g,.is_eof = is_eofg,.is_err = is_errg,.good = goodg,.getc = getcg,.getl = getlg,.gets = getsg,.putc = putcg,.puts = putsg,.pos = posg,.gotos = gotosg,.jump = jumpg,.gotoe = gotoeg,.flush = flushg,.print_i = print_ig,.print_u = print_ug,.print_f = print_fg,.print_b = print_bg,.print_c = print_cg
    };

    stdin_our = 
            (IOStreaminstance){stdin};
        ;
stdout_our = 
            (IOStreaminstance){stdout};
        ;
stderr_our = 
            (IOStreaminstance){stderr};
        ;
}