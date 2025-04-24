CC= gcc
STATIC= True
SHARED_EXT= dll
HEADERS = ${wildcard *.h}

ifeq "${STATIC}" "True"
CFLAGS= -fopenmp -O3 -Wall -pedantic -std=c17
else
CFLAGS= -fPIC -fopenmp -O3 -Wall -pedantic -std=c17
endif

all: main

ifeq  "${STATIC}" "True"
main: main.o lib/libbst.a 
	${CC} ${CFLAGS} -o $@ $< -L./lib -lbst -lm
else
main: main.o lib/libbst.${SHARED_EXT}
	${CC} ${CFLAGS} -o $@ $< -L./lib -lbst -lm
	
endif


lib/libbst.a: mandelbrot.o pgm.o
	mkdir -p lib
	ar rs $@ $^

lib/libbst.${SHARED_EXT}: mandelbrot.o pgm.o
	{CC} ${CFLAGS} -o $@ -shared $< -lm

%.o: %.c ${HEADERS}
	${CC} ${CFLAGS} -c $<

.PHONY: clean clean-all
clean:
	rm -f *.o
	rm -rf lib/*.a lib/*.${SHARED_EXT}
	rmdir -p lib
	rm main