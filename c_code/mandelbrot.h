// ELISA COCEANI SM3201340

#ifndef MANDELBROT_H
#define MANDELBROT_H


// Funzione per l'allocazione della matrice per immagazzinare i risuktati della funzione sucessiva
int** create_matrix(int nrows, int ncols);

// Funzione che calcola l'appartenenza di un punto all'inzieme di Mandelbrot
void mandelbrot_points(int **matrix, int nrows, int ncols, int M);

#endif
