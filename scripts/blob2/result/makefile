
CC       = gcc
CFLAGS   = -IC:\Coding\Python\Two\Test\TheLanguage\test\V6\Main\TransferToC\STDModules\realization\include -O2 # -g # -Wall -Wextra
LDFLAGS  = -mconsole
TARGET   = program.exe

SOURCES := C:/Coding/Python/Two/Test/TheLanguage/test/V6/scripts/blob2/result/src/maind25dbbb164cb48b29586a2053bc1aa7e.c
    
SOURCES += src/main.c

SOURCES += C:\Coding\Python\Two\Test\TheLanguage\test\V6\Main\TransferToC\STDModules\realization\src\io_our.c


$(TARGET): $(SOURCES)
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)

clean:
	rm -f $(TARGET)

.PHONY: all clean

