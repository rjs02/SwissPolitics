.PHONY: all

all: projection

projection: main.cpp
	$(CXX) -I /mnt/c/dev/lib/eigen-3.4.0 $< -o $@ 

.PHONY: run
run: projection
	./$<

.PHONY: clean
clean:
	$(RM) projection