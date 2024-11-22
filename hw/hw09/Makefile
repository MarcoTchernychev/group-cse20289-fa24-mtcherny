CC=		gcc
CFLAGS=	-Wall --std=c99
LD=		gcc
LDFLAGS=-lpthread
LIBS=	-lm
SOURCE= $(wildcard *.c)
OBJECTS=$(SOURCE:.c=.o)
TARGET= redextract
DEBUGTARGET= redextract-debug

all: $(TARGETS)

$(DEBUGTARGET): CFLAGS += -g
$(DEBUGTARGET): $(OBJECTS)
	$(LD) $(LDFLAGS) -o $@ $^ $(LIBS)

$(TARGET): $(OBJECTS)
	$(LD) $(LDFLAGS) -o $@ $^ $(LIBS)

%.o: %.c
	$(CC) -c $(CFLAGS) -o $@ $^

clean:
	rm -f $(TARGET) $(DEBUGTARGET) *.o
