// recover.c 
""" 
Program for recovering JPEGs from a memory card. 
Based on Problem Set 4 in CS50.
If the program is not yet compiled, run the following from the command line:
    make recover 
When the program is compiled, run from the command line like so: 
    ./recover <card.raw> 
Replacing <card.raw> with the name of the memory card from which to recover JPEG images. 
The program will write any JPEG files found in memory to a new folder, recovered_images, in the directory where the script is stored. 
""" 
#include <stdint.h> 
#include <stdio.h> 
#include <stdlib.h> 
#include <string.h> 
#include <sys/stat.h> 

typedef uint8_t BYTE; 

int main(int argc, char *argv[]){

    //Accept a single command-line argment 
    if (argc != 2){
        printf("Usage: ./recover <CARD>\n");
        return 1; 
    }
    // Ensure command line argument points to a readable file 
    FILE *card = fopen(argv[1], "r");
    if (card == NULL){
        printf("Forensic image cannot be opened for reading\n");
        fclose(card);
        return 1; 
    }

    // Create a buffer of 512 BYTEs (jpeg standard size) for reading in recovered images 
    BYTE buffer[512]; 
    // Create an empty array for filenames 
    char filename[1024];
    // Initialize a counter for formatting filenames in increments 
    int filecounter = 0; 
    // Initialize an empty filepointer for JPEGs 
    FILE *jpeg = NULL; 

    // Define a sub-directory for storing images and create it if it doesn't exist already 
    const char *subdir = "recovered_images"; 
    // Initialize an empty variable for storing directory metadata 
    struct stat st = {0}; 
    // check if subdirectory is valid
    if (stat(subdir, &st) == -1){
        if (mkdir(subdir, 0755) == -1){
            perror("mkdir");
            fclose(card);
            return 1; 
        }
    }
    // Read card data into buffer in chunks of 512 BYTEs so long as any data left in card to read 
    while (fread(buffer, 1, 512, card) == 512){
        // check if at start of new JPEG based on typical signatures 
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0){
                // Check if loop on first JPEG (no JPEG file has been opened previously)
                if (filecounter == 0){
                    // Create filename based on loop iteration 
                    sprintf(filename, "%s/%03i.jpg", subdir, filecounter);
                    // Open a new JPEG file for writing with this filename
                    jpeg = fopen(filename, "w"); 
                    // Ensure jpeg filepointer is valid 
                    if (jpeg != NULL){
                        fwrite(buffer, 1, 512, jpeg); 
                    }
                    // Increment filecounter for next filename format 
                    filecounter++; 
                }
                // If not first JPEG
                else{
                    // Close the previous jpeg file 
                    fclose(jpeg); 
                    // Format filename 
                    sprintf(filename, "%s/%03i.jpg", subdir, filecounter);
                    // Open new jpeg file for writing
                    jpeg = fopen(filename, "w");
                    // Ensure jpeg filepointer is valid 
                    if (jpeg  != NULL){
                        // Write contents of buffer into the file 
                        fwrite(buffer, 1, 512, jpeg); 
                    }
                    // Increment filecounter for next filename 
                    filecounter++; 
                }
            }
            // Else if not start of new JPEG 
            else{
                // If a valid JPEG file is open already, continue writing to it 
                if (jpeg != NULL){
                    fwrite(buffer, 1, 512, jpeg); 
                }
            }
    }
    // Close any files that remain open after loop terminates 
    fclose(jpeg);
    fclose(card); 

    // Return 0 for successful execution 
    return 0; 
}