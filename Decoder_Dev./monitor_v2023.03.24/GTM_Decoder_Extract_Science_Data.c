#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "GTM_Decoder_Extract_Science_Data.h"
#include "GTM_Decoder_Function.h"

int extract_science_data(int InputFilePointer) {
    unsigned char *nspo_data_buffer;
    size_t actual_binary_buffer_size;
    int output_file_pointer;
    int nspo_data_buffer_counter;
    size_t location;
    size_t chunk_start = 0;
    long long int nspo_packet_counter = 0;
    
    // dynamic memory allocation for each 1127 bytes Science data (with 16 bytes header and 1 byte tail)
    nspo_data_buffer = (unsigned char *)malloc(NSPO_DATA_SIZE);
    if (!nspo_data_buffer) {
        log_error("fail to create NSPO data buffer");
    }

    // recording how many bytes in binary_buffer
    actual_binary_buffer_size = fread(binary_buffer, 1, max_binary_buffer_size, bin_infile+InputFilePointer);

    // updating file pointer by InputFilePointer and actual_binary_buffer_size
    output_file_pointer = InputFilePointer + (int)actual_binary_buffer_size;
    
    while (1) {
        log_message("load new chunk");

        // initializing the position of nspo_data_buffer_counter
        nspo_data_buffer_counter = 0;

        // parsing data in binary_buffer
        for (location=0; location < actual_binary_buffer_size; location++) {
            memcpy(nspo_data_buffer+nspo_data_buffer_counter, binary_buffer+InputFilePointer+location, 1);
            nspo_data_buffer_counter++;

            // checking SD header
            if (nspo_data_buffer_counter == NSPO_HEADER_SIZE) {
                // if anything is wrong, shifting 1 byte to re-surching SD header
                if (!is_nspo_header(nspo_data_buffer)) {
                    log_message("Not NSPO header, location = %zu", chunk_start+location);
                    nspo_data_buffer_counter--;
                    pop_bytes(nspo_data_buffer, 1, NSPO_HEADER_SIZE);
                }
            }

            // Science data (all 1127 bytes data are loaded into nspo_data_buffer)
            if (nspo_data_buffer_counter == NSPO_DATA_SIZE) {
                for (int i=NSPO_HEADER_SIZE; i < NSPO_DATA_SIZE-NSPO_TAIL_SIZE; i++) {
                    fprintf(raw_extract_outfile, "%c", nspo_data_buffer[i]);
                }
                nspo_data_buffer_counter = 0;
                nspo_packet_counter++;
            }
        }
        break;
    }

    log_message("extract total %lli nspo packets", nspo_packet_counter);

    // releaseing dynamic memory allocation for each 1127 bytes Science data (with 16 bytes header and 1 byte tail)
    free(nspo_data_buffer);

    // returning new file pointer to main funciton
    return output_file_pointer;
}