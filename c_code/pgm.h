// ELISA COCEANI SM3201340

#ifndef PGM_H
#define PGM_H

#include <stdio.h>
#include <stdlib.h>

// Struttura per rappresentare l'immagine in formato pmg
typedef struct{
    int width;
    int heigth;
    unsigned char *pixels; 
}pgmImage;


// Dimensionamento del'immagine
pgmImage create_image(int nrows, int ncols);


// Riempimento dell'immagine
void write_colors(pgmImage * image, int **matrix, int M);


// Mappare il file in memoria
void save_image( char *filename, pgmImage * image);


// Liberare la memoria allocata per l'immagine
int close_image(pgmImage *image);

#endif
