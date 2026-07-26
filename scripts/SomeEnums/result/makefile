
CC       = gcc
CFLAGS   = -IC:\Coding\Python\Two\Test\TheLanguage\test\V5\Main\TransferToC\STDModules\realization\include -O2 # -g # -Wall -Wextra
LDFLAGS  = -mconsole
TARGET   = program.exe

SOURCES := $(wildcard src/*.c)

SOURCES += C:\Coding\Python\Two\Test\TheLanguage\test\V5\Main\TransferToC\STDModules\realization\src\io_our.c


$(EXTRA_SOURCES)

HEADERS := $(wildcard include/*.h)

all: $(TARGET)

$(TARGET): $(SOURCES) $(HEADERS)
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)

clean:
	rm -f $(TARGET)

.PHONY: all clean

