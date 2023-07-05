#include "GTM_Decoder_Function.h"
#include "GTM_Decoder_Parse_Science_Data.h"



int parse_science_data(int input_file_pointer, char *input_file_path) {
    size_t input_binary_buffer_size;
    int output_file_pointer;

    // due to inconsistent length of science data from TASA and real science data
    // we have to create more complicated temporary buffer to save memory and simplify logic
    // and also have better to destroy input_binary_buffer independently 

    unsigned char *science_icd_binary_buffer; // for science data without TASA added info
    size_t science_icd_binary_buffer_size = 0;
    unsigned char *science_1279_byte_buffer; // 1279 bytes = the length of a single packet from TASA
    int science_1279_byte_buffer_counter = 0;

    unsigned char *scienc_1110_byte_buffer; // 1110 bytes = the length of a single packet real science data
    int science_1110_byte_buffer_counter = 0;

    char *science_extract_output_path;
    FILE *science_extract_output_file;

    /// step_1_read_data ///

    // move file pointer inside input_binary_file base on input_file_pointer
    fseek(input_binary_file, input_file_pointer, SEEK_SET);

    // record data from input_binary_file to input_binary_buffer and also how many bytes in input_binary_buffer
    input_binary_buffer_size = fread(input_binary_buffer, 1, max_input_binary_buffer_size, input_binary_file);

    // update file pointer by input_file_pointer and input_binary_buffer_size
    output_file_pointer = input_file_pointer + (int)input_binary_buffer_size;

    /// step_1_read_data_end ///

    /// step_2_extract_data ///

    // create science_icd_binary_buffer independently
    science_icd_binary_buffer = (unsigned char *)malloc(input_binary_buffer_size);

    // dynamic memory allocation for science_1279_byte_buffer
    science_1279_byte_buffer = (unsigned char *)malloc(SCIENCE_ATTACHED_SYNCHRO_MARKER_SIZE+SCIENCE_TRANSFER_FRAME_SIZE+SCIENCE_REED_SOLOMON_CHECK_SYMBOLS_SIZE);

    // extract data in input_binary_buffer
    for (size_t i = 0; i < input_binary_buffer_size; i++) {

        // copy memory of real science data from input_binary_buffer to science_1279_byte_buffer
        memcpy(science_1279_byte_buffer+science_1279_byte_buffer_counter, input_binary_buffer+i, 1);
        science_1279_byte_buffer_counter++;

        // check science marker from TASA
        if (science_1279_byte_buffer_counter == SCIENCE_ATTACHED_SYNCHRO_MARKER_SIZE) {
            if (!is_science_gicd_marker(science_1279_byte_buffer)) { 
                log_error("Please check science marker defined by GICD!");
            }
        }

        // extract science data (all 1279 bytes data are loaded into science_1279_byte_buffer)
        if (science_1279_byte_buffer_counter == SCIENCE_ATTACHED_SYNCHRO_MARKER_SIZE+SCIENCE_TRANSFER_FRAME_SIZE+SCIENCE_REED_SOLOMON_CHECK_SYMBOLS_SIZE) {            
            memcpy(science_icd_binary_buffer+science_icd_binary_buffer_size, science_1279_byte_buffer+SCIENCE_ATTACHED_SYNCHRO_MARKER_SIZE+SCIENCE_PRIMARY_HEADER_SIZE, SCIENCE_TRANSFER_FRAME_DATA_FIELD_SIZE);
            
            // accumulate SCIENCE_TRANSFER_FRAME_DATA_FIELD_SIZE into science_icd_binary_buffer_size
            science_icd_binary_buffer_size += SCIENCE_TRANSFER_FRAME_DATA_FIELD_SIZE;

            // reset science_1279_byte_buffer_counter
            science_1279_byte_buffer_counter = 0;
        }
    }

    // release dynamic memory allocation for science_1279_byte_buffer
    free(science_1279_byte_buffer);

    /// step_2_extract_data ///

    // destroy input_binary_buffer independently
    free(input_binary_buffer);

    // // check science_icd_binary_buffer by save as file
    // science_extract_output_path = str_append(input_file_path, "_extracted.bin");
    // science_extract_output_file = fopen(science_extract_output_path, "ab");
    // for (size_t i = 0; i < science_icd_binary_buffer_size; i++) {
    //     fprintf(science_extract_output_file, "%c", science_icd_binary_buffer[i]);
    // }
    // free(science_extract_output_path);
    // fclose(science_extract_output_file);

    /// step_3_parse_data ///

    // dynamic memory allocation for scienc_1110_byte_buffer
    scienc_1110_byte_buffer = (unsigned char *)malloc(SCIENCE_HEADER_SIZE+SCIENCE_DATA_SIZE);

    // parse data in science_icd_binary_buffer
    for (size_t i = 0; i < science_icd_binary_buffer_size; i++) {

        // copy memory from science_icd_binary_buffer to scienc_1110_byte_buffer
        memcpy(scienc_1110_byte_buffer+science_1110_byte_buffer_counter, science_icd_binary_buffer+i, 1);
        science_1110_byte_buffer_counter++;

        // check 1110 bytes science head
        if (science_1110_byte_buffer_counter == 2) {
            if (!is_science_icd_head(scienc_1110_byte_buffer)) { 
                log_error("Please check science head defined by ICD!");
            }
        }

        // parse science data (all 1110 bytes data are loaded into science_1110_byte_buffer_counter)
        if (science_1110_byte_buffer_counter == SCIENCE_HEADER_SIZE+SCIENCE_DATA_SIZE) {

            log_message("check 1");

            // if all data is healthy, parse it out
            parse_science_packet(scienc_1110_byte_buffer);

            // reset science_1110_byte_buffer_counter
            science_1110_byte_buffer_counter = 0;
        }
    }

    // release dynamic memory allocation for scienc_1110_byte_buffer
    free(scienc_1110_byte_buffer);

    /// step_3_parse_data_end ///

    // destroy science_icd_binary_buffer independently
    free(science_icd_binary_buffer);

    // return updated file pointer to main funciton
    return output_file_pointer;
}