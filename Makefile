CC = gcc
CFLAGS = -Wall 
OBJS = reportData.o 

all: $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o program
	cc -fPIC -shared -o libfun.so reportData.c

reportData.o: reportData.c
	$(CC) $(CFLAGS) -c reportData.c

clean:
	rm -f *~ *.o program libfun.so
 
