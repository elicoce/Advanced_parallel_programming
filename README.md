# Advanced and Parallel Programming Final Project

This repository contains two distinct assignments developed as part of the final project for the 'Advanced and Parallel Programming' course.

### Repository Structure

- `c_code/`: Contains the C implementation of a Mandelbrot fractal image generator.
- `python_code/`: Contains the Python implementation of a postfix expression evaluator with support for variables, conditionals, loops, and subroutines.
- `README.md`: This file, providing an overview of the project.



### C : Mandelbrot Fractal Generator

This program generates a grayscale Mandelbrot fractal image in NetPBM (PGM) format. The code is modular and split across several files:

- `main.c`: Entry point of the program.
- `mandelbrot.c` / `mandelbrot.h`: Contains the logic for computing the Mandelbrot set.
- `pgm.c` / `pgm.h`: Handles image creation and saving in PGM format.
- `Makefile`: Used to compile the project.

The computation of the Mandelbrot set is parallelized using OpenMP to improve performance on multicore systems.

### How to Compile 

    cd c_code
    make
    ./mandelbrot

### Python: Expression evaluator

This program implements a system to build and evaluate mathematical and logical expressions written in postfix notation (Reverse Polish Notation). The implementation uses class hierarchies to avoid code duplication and improve extensibility.
This project explores object-oriented programming, expression parsing, and stack-based evaluation.  


### How to Run

    cd python_code
    python3 expressions.py

  

