
CC       = gcc
CFLAGS   = -IC:/Coding/Python/Two/Test/TheLanguage/test2/Main/TransferToC/STDModules/realization/include -O2 # -g # -Wall -Wextra
LDFLAGS  = -mconsole
TARGET   = program.exe

SOURCES := C:/Coding/Python/Two/Test/TheLanguage/test2/scripts/result/src/Matrices.c \
C:/Coding/Python/Two/Test/TheLanguage/test2/scripts/result/src/Vectors.c
    
SOURCES += src/main.c

SOURCES += C:/Coding/Python/Two/Test/TheLanguage/test2/Main/TransferToC/STDModules/realization/src/io_our.c
SOURCES += C:/Coding/Python/Two/Test/TheLanguage/test2/Main/TransferToC/STDModules/realization/src/mem_our.c
SOURCES += C:/Coding/Python/Two/Test/TheLanguage/test2/Main/TransferToC/STDModules/realization/src/math_our.c
SOURCES += C:/Coding/Python/Two/Test/TheLanguage/test2/Main/TransferToC/STDModules/realization/src/testing_our.c


$(TARGET): $(SOURCES)
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)

clean:
	rm -f $(TARGET)

.PHONY: all clean

