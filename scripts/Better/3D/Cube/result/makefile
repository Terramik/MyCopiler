
CC       = gcc
CFLAGS   = -IC:\Coding\Python\Two\Test\TheLanguage\test\V6\Main\TransferToC\STDModules\realization\include -O2 # -g # -Wall -Wextra
LDFLAGS  = -mconsole
TARGET   = program.exe

SOURCES := C:/Coding/Python/Two/Test/TheLanguage/test/V6/scripts/Better/3D/Cube/result/src/3D/Cube/maind787bc4e0f224d09b7e2a199e2892663.c \
C:/Coding/Python/Two/Test/TheLanguage/test/V6/scripts/Better/3D/Cube/result/src/3D/Cube/defines.c \
C:/Coding/Python/Two/Test/TheLanguage/test/V6/scripts/Better/3D/Cube/result/src/Math/Quaternions.c \
C:/Coding/Python/Two/Test/TheLanguage/test/V6/scripts/Better/3D/Cube/result/src/Math/Matrices.c
    
SOURCES += src/main.c

SOURCES += C:\Coding\Python\Two\Test\TheLanguage\test\V6\Main\TransferToC\STDModules\realization\src\io_our.c
SOURCES += C:\Coding\Python\Two\Test\TheLanguage\test\V6\Main\TransferToC\STDModules\realization\src\testing_our.c
SOURCES += C:\Coding\Python\Two\Test\TheLanguage\test\V6\Main\TransferToC\STDModules\realization\src\time_our.c
SOURCES += C:\Coding\Python\Two\Test\TheLanguage\test\V6\Main\TransferToC\STDModules\realization\src\math_our.c
SOURCES += C:\Coding\Python\Two\Test\TheLanguage\test\V6\Main\TransferToC\STDModules\realization\src\mem_our.c


$(TARGET): $(SOURCES)
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)

clean:
	rm -f $(TARGET)

.PHONY: all clean

