#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "GTM_Decoder_Extract_Science_Data.h"
#include "GTM_Decoder_Function.h"

void extract_science_data(void) {
    unsigned char *nspo_data_buffer = NULL;
    int nspo_data_buffer_counter = 0;
    size_t actual_binary_buffer_size = 0;
    size_t chunk_start = 0;
    size_t location;
    long long int nspo_packet_counter = 0;
    int i;

    nspo_data_buffer = (unsigned char *)malloc(NSPO_DATA_SIZE);
    if (!nspo_data_buffer) {
        log_error("fail to create NSPO data buffer");
    }

    actual_binary_buffer_size = read_from_file(binary_buffer, bin_infile, max_binary_buffer_size);
    // loop through buffer
    while (1) {
        log_message("load new chunk");
        location = 0;
        while (location < actual_binary_buffer_size) {
            memcpy(nspo_data_buffer + nspo_data_buffer_counter, binary_buffer + location, 1);
            nspo_data_buffer_counter++;

            if (nspo_data_buffer_counter == NSPO_HEADER_SIZE) {
                if (!is_nspo_header(nspo_data_buffer)) { // is not nspo header
                    log_message("Not NSPO header, location = %zu", chunk_start + location);
                    // exit(1);
                    nspo_data_buffer_counter--;
                    // discard the first byte in the buffer
                    pop_bytes(nspo_data_buffer, 1, NSPO_HEADER_SIZE);
                }
            }
            if (nspo_data_buffer_counter == NSPO_DATA_SIZE) { // all nspo data is loaded into buffer
                for (i = NSPO_HEADER_SIZE; i < NSPO_DATA_SIZE - NSPO_TAIL_SIZE; ++i) {
                    fprintf(raw_extract_outfile, "%c", nspo_data_buffer[i]);
                }
                nspo_data_buffer_counter = 0;
                nspo_packet_counter++;
            }

            location++;
        }

        if (actual_binary_buffer_size < max_binary_buffer_size) {
            break;
        }
        chunk_start += actual_binary_buffer_size;
        actual_binary_buffer_size = read_from_file(binary_buffer, bin_infile, max_binary_buffer_size);
    }

    log_message("extract total %lli nspo packets", nspo_packet_counter);
    free(nspo_data_buffer);
}