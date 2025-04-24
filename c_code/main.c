// ELISA COCEANI SM3201340

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include "mandelbrot.h"
#include "pgm.h"

int main(int argc, char *argv[]){

    /* Gli input da inserire da linea di comando sono, oltre a il file main.c da compilare: 
    - il nome del file in cui viene salvata l'immagine in formato pgm
    - il numero massimo di iterazioni M 
    - il numero di righe nrows che rappresenta l'altezza dell'immagine
    */

   // Controllo che il numero di input sia corretto
    
    if (argc != 4) {
        fprintf(stderr, "Input da inserire: <nomefile> <M> <nrows>\n");
        exit(EXIT_FAILURE);
    }

    // Dichiarazione delle variabili

    char *filename = argv[1];
    int M = atoi(argv[2]);
    int nrows = atoi(argv[3]);
    // è stato scelto di definire il numero di colonne ncols di tipo intero in quanto questa variabile rappresenta anche la larghezza dell'immagine
    int ncols = (int)(1.5 * nrows); 

    // Controllo che il nome del file termini con .pgm, altrimenti viene aggiunto 
    if (strstr(filename, ".pgm") == NULL) {
        char new_filename[256];
        snprintf(new_filename, sizeof(new_filename), "%s.pgm", filename);
        filename = new_filename;
    }

    // Controllo del dominio degli input numerici
    if ( M < 0 || nrows < 0){
        fprintf(stderr, "Errore nell'inserimento dei dati\n");
        exit(EXIT_FAILURE);
    }

    // Iniziallizzazione una matrice delle dimensioni cercate
    int ** matrix= create_matrix(nrows,ncols); 

    // Calcolo dei punto dell'insieme di mandelbrot
    mandelbrot_points(matrix, nrows,ncols, M);
    
    // Creazione dell'immagine
    pgmImage image=create_image(nrows,ncols);

    // L'immagine viene riempita
    write_colors(&image,matrix, M);

    // Salvataggio dell'immagine in memoria 
    save_image(filename, &image);

    // Liberare la memoria allocata per la matrice
    for (int i = 0; i < nrows; i++) {
        free(matrix[i]);
    }
    free(matrix);

    // Chiusura dell'immagine e liberazione delle risorse allocate
    close_image(&image);
    printf("Completata la creazione dell'immagine '%s' \n", filename);

    return 0;
}