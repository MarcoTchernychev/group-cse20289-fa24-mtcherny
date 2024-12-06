CC=		gcc
CFLAGS=	
LD=		gcc
LDFLAGS= 
LIBS= -lzmq 
SOURCE= $(wildcard *.c)
OBJECTS=$(SOURCE:.c=.o)
TARGET= client

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(LD) $(LDFLAGS) -o $@ $^ $(LIBS)

%.o: %.c
	$(CC) -c $(CFLAGS) -o $@ $^

clean:
	rm -f $(TARGET) *.o
