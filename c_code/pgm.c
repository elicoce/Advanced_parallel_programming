// ELISA COCEANI SM3201340

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <string.h>
#include <fcntl.h>
#include <omp.h>
#include <math.h>

#include "pgm.h"


// Creazione  dell'immagine
pgmImage create_image( int nrows, int ncols){ 
    /* Input:
    nrows = numero di righe e altezza dell'immagine
    ncols = numero di colonne e larghezza dell'immagine

    La funzione restitiusce un oggetto di tipo pgmImage della dimensione specificata.
    */
    pgmImage image;
    image.heigth= nrows; 
    image.width= ncols;

    // Allocazione dinamica per l'array di pixel
    image.pixels = malloc(image.width * image.heigth * sizeof(unsigned char));
    
    // Check per vedere se l'immagine è stata creata con successo
    if (image.pixels == NULL) {
        fprintf(stderr, "Errore: Allocazione di memoria fallita.\n");
        exit(EXIT_FAILURE);
    }

    return image;
}


// Colorazione dell'immagine
void write_colors( pgmImage * image, int **matrix, int M){ 
/* Input:
- * image = puntatore alla struttura dell'immagine 
- ** matrix = puntatore alla matrice contenente il numero di iterazioni per ogni punto 
- M = numero massimo di iterazioni

Per ogni punto appartenente alla matrice, il pixel corrispondente viene colorato di bianco (255) se questo è nell'insieme di Mandelbrot, 
viene colorato di una sfumatura di grigio altrimenti.

*/
#pragma omp parallel for collapse(2)
    for ( int i=0 ; i< image->heigth; i++){
        for ( int j=0; j< image->width; j++){
            
            int index= i*image->width +j;
            image->pixels[index] =(unsigned char) 255 * ( log(matrix[i][j])/ log(M));
        }
    }
}


// Salvataggio dell'immagine in formato pgm
void save_image( char *filename, pgmImage * image){ 
    /* Input:
    - *filename= puntatore al nome del file inserito in input
    - * image = puntatore alla struttura dell'immagine da salvare

    Questa funzione definisce l'intestazione dell'immagine in formato .pgm ed effettua la mappatura in memoria utilizzando mmap.
    Vengono poi effettuate una copia dei dati dell'immagine nell'area mappata e la sincronizzazine della memoria mappata con il file. 
    Infine viene effettuato il deallocamento della memoria mappata e chiuso il file.
    */

    // Apertura del file 
    FILE * fd= fopen(filename, "w+");
    if (fd ==NULL){
        fprintf( stderr, "Errore nell'apertura del file %s\n", filename);
        exit(EXIT_FAILURE);
    }

    // Intestazione del file
    char header[100];
    int header_length= snprintf( header, sizeof(header), "P5\n%d %d\n255\n", image->width, image->heigth);
    fwrite(header,1,header_length,fd);
    
    // Troncamento del file alla dimensione desiderata
    size_t size= header_length + (image->width * image->heigth);

    if (ftruncate(fileno(fd), size) == -1) {
        fprintf(stderr, "Errore nel troncare il file\n");
        fclose(fd);
        exit(EXIT_FAILURE);
    }


    // Mappatura in memoria 
    char *mapped_data= mmap(0,size, PROT_READ | PROT_WRITE, MAP_SHARED,fileno(fd), 0); 
    // In caso di errore il programma termina con un messaggio di errore
    if ( mapped_data==MAP_FAILED){
        perror( "Errore nella mappatura in memoria\n");
        fclose(fd);
        exit(EXIT_FAILURE);
    }

    // Copia dei dati dell'immagine nell'area mappata
    memcpy(mapped_data + header_length, image ->pixels, image->width * image->heigth);

    // Mi assicuro che la sincronizzazione della memoria mappata con il file sia avvenuta con successo
    if ( msync(mapped_data, size, MS_SYNC)==-1){
        fprintf(stderr, "Errore nella sincronizzazione della memoria\n");
        fclose(fd);
        exit(EXIT_FAILURE);
    }

    // Deallocazione dlela memoria mappata
    munmap(image->pixels, size);

    fclose(fd);
}


// Funzione per liberare la memoria allocata
int close_image (pgmImage * image){ 
    if ( image == NULL){
        return -1; 
    }

    free(image->pixels); 
    return 0;
} 

