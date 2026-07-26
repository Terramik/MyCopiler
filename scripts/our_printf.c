#include <stdio.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>



typedef struct {
    uint8_t* start;
    size_t size;
} str_t;


str_t str_to_str(char* str, size_t len) {
    return (str_t){
        (uint8_t*)str, len
    };
}


bool parse_int(str_t str, size_t* ip, int* res) {
    long int val = 0;
    size_t i = *ip;
    uint8_t ch = str.start[i];
    while (i < str.size && ch >= '0' && ch <= '9')
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


#define ON_ERROR(indx) printf("Bad" # indx); abort();


static inline bool iter(str_t str, bool* format_used, bool* format_mode, size_t* i, uint8_t* ch) {
    *ch = str.start[*i];
    
    if ( *ch == '%' ) {
        if ( *format_mode ) {
            if ( *i >= 1 && str.start[*i-1] == '%' ) {
                *format_mode = false;
                putchar('%');
            } else {
                ON_ERROR(1)
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
                ON_ERROR(2)
            }
            
            return true;
        }
    }

    return false;
}


void print_f(str_t str, double f) {

    int mod_min = INT_MIN;
    int mod_decimal = INT_MIN;

    bool format_used = false;
    bool format_mode = false;

    uint8_t ch;
    size_t i = 0;
    while (i < str.size) {
        if (
            iter(str, &format_used, &format_mode, &i, &ch)
        ) {
            if ( ch == 'f' ) {
                
                if ( mod_min == INT_MIN && mod_decimal == INT_MIN ) {
                    printf("%f", f);
                } else if ( mod_decimal == INT_MIN ) {
                    printf("%*f", mod_min, f);
                } else if ( mod_min == INT_MIN ) {
                    printf("%.*f", mod_decimal, f);
                } else {
                    printf("%*.*f", mod_min, mod_decimal, f);
                }

                format_mode = false;
                format_used = true;
                i++;

            } else if ( mod_decimal == INT_MIN && ch == '.' ) {
                i++;
                if ( !parse_int(str, &i, &mod_decimal) ) { ON_ERROR(3) }
            } else if ( mod_min == INT_MIN ) {
                if ( !parse_int(str, &i, &mod_min) ) { ON_ERROR(4) }
            }  else {
                ON_ERROR(5)
            }
        }
    }
    if ( format_mode || !format_used ) {
        ON_ERROR(6)
    }
}



int main() {
    print_f(str_to_str("-%f-\n", 5), 1300.0031);
    print_f(str_to_str("%%-%10f-%%\n", 11), 10101);
    print_f(str_to_str("[%12.3f]", 8), 10.3);
    print_f(str_to_str("[%5.0f]\n", 8), 555);
    print_f(str_to_str("%.3f\n", 5), 1.123456);
    return 0;
}





