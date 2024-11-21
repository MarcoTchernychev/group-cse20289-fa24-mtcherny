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
	valgrind ./$(TARGET)

$(TARGET): $(OBJECTS)
	$(LD) $(LDFLAGS) -o $@ $^ $(LIBS)

%.o: %.c
	$(CC) -c $(CFLAGS) -o $@ $^

clean:
	rm -f $(TARGET) *.o

#old code:
#redextract: packet.c packet.h pcap-read.c pcap-read.h pcap-process.c pcap-process.h main.c
	#gcc packet.c pcap-process.c pcap-read.c main.c -Wall --std=c99 -lpthread -lm -o redextract
