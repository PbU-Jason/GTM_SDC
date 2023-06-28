#include "GTM_Decoder_Function.h"
#include "GTM_Decoder_Parse_TMTC_Data.h"



int parse_tmtc_data(int input_file_pointer) {
    size_t input_binary_buffer_size;
    int output_file_pointer;

    unsigned char *tmtc_144_byte_buffer; // 144 bytes is the length of a single packet from TASA
    int tmtc_144_byte_buffer_counter = 0;

    /// step_1_read_data ///

    // move file pointer inside input_binary_file base on input_file_pointer
    fseek(input_binary_file, input_file_pointer, SEEK_SET);

    // record data from input_binary_file to input_binary_buffer and also how many bytes in input_binary_buffer
    input_binary_buffer_size = fread(input_binary_buffer, 1, max_input_binary_buffer_size, input_binary_file);

    // update file pointer by input_file_pointer and input_binary_buffer_size
    output_file_pointer = input_file_pointer + (int)input_binary_buffer_size;

    /// step_1_read_data_end ///

    /// step_2_parse_data ///

    // dynamic memory allocation for tmtc_144_byte_buffer
    tmtc_144_byte_buffer = (unsigned char *)malloc(TMTC_PACKET_HEADER_SIZE+TMTC_PACKET_DATA_FIELD_SIZE);

    // parse data in input_binary_buffer
    for (size_t i = 0; i < input_binary_buffer_size; i++) {

        // copy memory from input_binary_buffer to tmtc_144_byte_buffer
        memcpy(tmtc_144_byte_buffer+tmtc_144_byte_buffer_counter, input_binary_buffer+i, 1);
        tmtc_144_byte_buffer_counter++;

        // check tmtc header from TASA
        if (tmtc_144_byte_buffer_counter == TMTC_PACKET_HEADER_SIZE) {
            if (!is_tmtc_gicd_header(tmtc_144_byte_buffer)) { 
                log_error("Please check tmtc header defined by GICD!");
            }
        }

        // parse tmtc data (all 144 bytes data are loaded into tmtc_144_byte_buffer)
        if (tmtc_144_byte_buffer_counter == TMTC_PACKET_HEADER_SIZE+TMTC_PACKET_DATA_FIELD_SIZE) {

            // check 128 bytes tmtc head
            if (tmtc_144_byte_buffer_counter == sizeof(tmtc_buffer->head)) {
                if (!is_tmtc_icd_head(tmtc_144_byte_buffer)) { 
                    log_error("Please check tmtc head defined by ICD!");
                }
            }

            // check 128 bytes tmtc tail
            if (tmtc_144_byte_buffer_counter == sizeof(tmtc_buffer->tail)) {
                if (!is_tmtc_icd_tail(tmtc_144_byte_buffer)) { 
                    log_error("Please check tmtc tail defined by ICD!");
                }
            }

            // if all data is healthy, parse it out
            write_tmtc_raw_all(tmtc_144_byte_buffer); // print each byte for checking
            parse_tmtc_packet(tmtc_144_byte_buffer);

            // reset tmtc_144_byte_buffer_counter
            tmtc_144_byte_buffer_counter = 0;
        }
    }

    // release dynamic memory allocation for tmtc_144_byte_buffer
    free(tmtc_144_byte_buffer);

    /// step_2_parse_data_end ///
    
    // destroy input_binary_buffer independently
    free(input_binary_buffer);
    
    // return updated file pointer to main funciton
    return output_file_pointer;
}