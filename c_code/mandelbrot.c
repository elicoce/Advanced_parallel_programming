// ELISA COCEANI SM3201340

#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <math.h>
#include <omp.h>
#include "mandelbrot.h"

// Funzione per l'allocazione della matrice per immagazzinare i risultati della funzione sucessiva

int ** create_matrix (int nrows, int ncols){
    /* Input:
    nrows = numero di righe 
    ncols = numero di colonne 

    La funzione restitiusce un puntatore a una matrice di dimensione nrows * ncols.
    Alloca dinamicamente una matirce bidimensionale di interi.
    */
    int ** matrix= (int**)malloc(nrows *sizeof(int*));

    for (int i = 0; i < nrows; i++) {
        matrix[i] = (int*)malloc(ncols * sizeof(int));
    }
    
    // Se l'allocazione non è avvenuta con successo vine stampato un messaggio di errore
    if ( matrix==NULL){
        fprintf(stderr,"Errore nell'allocazione della matrice\n");
        exit(EXIT_FAILURE);
    }
    return matrix;
}


//Funzione che calcola l'appartenenza del punti all'insieme di mandelbrot 

void mandelbrot_points( int **matrix, int nrows, int ncols, int M){
    /*Input: 
    real= parte reale 
    imag= imag parte immaginaria 
    M= numero massimo di iterazioni 

    Restitiusce il numero di iterazioni n tale che |f^n(c)| <= 2.0;
    viene restitiuto M se il punto appartiene all'insieme di Mandelbrot.
    */

#pragma omp parallel for collapse(2)
    for (int i=0; i<nrows; i++){
        for ( int j=0; j<ncols; j++){

            // ad ogni iterazione viene definito un punto nell'insieme complesso 
            float real = -2.0 + 3.0 * j / (ncols-1);
            float imag = -1.0 + 2.0 * i / (nrows-1);

            float complex c = real + imag * I;

            // si iniziano le iterazioni per dichiarare se il punto appartiene o meno all'insieme di Mandelbrot
            float complex z = 0.0 + 0.0 * I;
            int iter=0; //numero di iterazioni completate, inizializzato a zero

            while (cabs(z) < 2.0 && iter < M){  // raggio = 2
                z = cpow(z,2.0) + c;
                iter ++;
            }
            
            // Il numero di iteraizoni calcolato viene memorizzato nella matrice 
            matrix[i][j] = iter;
        
        }
    }
    
    
}
