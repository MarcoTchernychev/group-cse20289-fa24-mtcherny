CC=		gcc
CFLAGS=	-Wall --std=c99
LD=		gcc
LDFLAGS=-lpthread
LIBS=	-lm
SOURCE= $(wildcard *.c)
OBJECTS=$(SOURCE:.c=.o)
TARGET= redextract

all: $(TARGETS)

redextract-debug: CFLAGS += -g
redextract-debug: $(TARGET)
	valgrind --leak-check=full --track-origins=yes ./$(TARGET) $(ARGS)

$(TARGET): $(OBJECTS)
	$(LD) $(LDFLAGS) -o $@ $^ $(LIBS)

%.o: %.c
	$(CC) -c $(CFLAGS) -o $@ $^

clean:
	rm -f $(TARGET) *.o
