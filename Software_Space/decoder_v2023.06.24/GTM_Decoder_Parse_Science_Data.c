#include "GTM_Decoder_Function.h"
#include "GTM_Decoder_Parse_Science_Data.h"



int parse_science_data(int input_file_pointer) {
    size_t input_binary_buffer_size;
    int output_file_pointer;

    unsigned char *science_icd_binary_buffer; // for science data without TATS added info
    int science_icd_binary_buffer_counter = 0;
    unsigned char *scienc_1279_byte_buffer; // 1279 bytes is the length of a single packet from TASA
    int science_1279_byte_buffer_counter = 0;

    size_t science_icd_binary_buffer_size;
    size_t sd_header_location;
    size_t old_sd_header_location;
    size_t full = 0;
    size_t broken = 0;

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

    // dynamic memory allocation for scienc_1279_byte_buffer
    scienc_1279_byte_buffer = (unsigned char *)malloc(SCIENCE_ATTACHED_SYNCHRO_MARKER_SIZE+SCIENCE_TRANSFER_FRAME_SIZE+SCIENCE_REED_SOLOMON_CHECK_SYMBOLS_SIZE);

    // extract data in input_binary_buffer
    for (size_t i = 0; i < input_binary_buffer_size; i++) {

        // copy memory of real science data from input_binary_buffer to science_1105_byte_buffer
        memcpy(scienc_1279_byte_buffer+science_1279_byte_buffer_counter, input_binary_buffer+i, 1);
        science_1279_byte_buffer_counter++;

        // check science marker from TASA
        if (science_1279_byte_buffer_counter == SCIENCE_ATTACHED_SYNCHRO_MARKER_SIZE) {
            if (!is_science_gicd_marker(scienc_1279_byte_buffer)) { 
                log_error("Please check science marker defined by GICD!");
            }
        }

        // extract science data (all 1279 bytes data are loaded into scienc_1279_byte_buffer)
        if (science_1279_byte_buffer_counter == SCIENCE_ATTACHED_SYNCHRO_MARKER_SIZE+SCIENCE_TRANSFER_FRAME_SIZE+SCIENCE_REED_SOLOMON_CHECK_SYMBOLS_SIZE) {
            memcpy(science_icd_binary_buffer+science_icd_binary_buffer_counter, \
            scienc_1279_byte_buffer+SCIENCE_ATTACHED_SYNCHRO_MARKER_SIZE+SCIENCE_PRIMARY_HEADER_SIZE, SCIENCE_TRANSFER_FRAME_DATA_FIELD_SIZE);
            science_icd_binary_buffer_counter+=SCIENCE_TRANSFER_FRAME_DATA_FIELD_SIZE;

            // reset science_1279_byte_buffer_counter
            science_1279_byte_buffer_counter = 0;
        }
    }

    // release dynamic memory allocation for scienc_1279_byte_buffer
    free(scienc_1279_byte_buffer);

    /// step_2_extract_data ///

    // destroy input_binary_buffer independently
    free(input_binary_buffer);

    /// step_3_parse_data ///

    // parse data in input_binary_buffer
    for (size_t i = 0; i < strlen(science_icd_binary_buffer); i++) {

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











    /// step_3_parse_data ///

    // skip (input_binary_buffer_size == 0) to avoid error in find_next_sd_header()
    if ((int)input_binary_buffer_size == 0) {
        return output_file_pointer;
    }
    else {
        ///// ↓↓↓ need checking!!!
        // finding first SD header
        sd_header_location = find_next_sd_header(input_binary_buffer, -SCIENCE_HEADER_SIZE, input_binary_buffer_size);
        if (sd_header_location != 0) {
            log_message("Binary file doesn't start with science data header, first science data header is at byte %zu", (size_t)ftell(input_binary) - input_binary_buffer_size + sd_header_location);
            
            // moving pointer inside input_binary base on sd_header_location
            fseek(input_binary, sd_header_location - input_binary_buffer_size, SEEK_CUR);

            // updating how many bytes in input_binary_buffer
            input_binary_buffer_size = fread(input_binary_buffer, 1, max_input_binary_buffer_size, input_binary);
        }
    }

    while (1) {
        log_message("load new chunk");

        // leaving when encountering below weird conditions
        if (input_binary_buffer_size <= SCIENCE_HEADER_SIZE) {
            break;
        }
        if (!is_sd_header(input_binary_buffer)) {
            log_error("Bin file doesn't start with sd header");
        }

        // initializing the position of sd_header_location
        sd_header_location = 0;

        // parsing data in input_binary_buffer
        while (sd_header_location < input_binary_buffer_size) {

            // if the packet is not continueous, reset related parameter
            if (!continuous_packet) {
                log_message("Non contiuous occurs around bytes %zu", (size_t)ftell(input_binary) - input_binary_buffer_size + sd_header_location);
                got_first_sync_data = 0;
            }

            // finding next SD header
            old_sd_header_location = sd_header_location;
            sd_header_location = find_next_sd_header(input_binary_buffer, sd_header_location, input_binary_buffer_size);

            // no next sd header is found or the remaining buffer isn't large enough to contain a science packet
            if (sd_header_location == (size_t)-1) { 
                if (input_binary_buffer_size == max_input_binary_buffer_size) {
                    // no next sd header and this is not the last buffer, load next buffer, don't parse the packet
                    break;
                }
                else {
                    // it's the last buffer but can't find next packet
                    if (old_sd_header_location + SCIENCE_HEADER_SIZE + SCIENCE_DATA_SIZE < input_binary_buffer_size) {
                        log_message("Can't find next sd header while this isn't the last packet, discard data after");
                        break;
                    }
                    // it's the last buffer and this is the last packet
                    else {
                        parse_sd_header(input_binary_buffer + old_sd_header_location);
                        // parse_science_packet(input_binary_buffer + old_sd_header_location + SCIENCE_HEADER_SIZE, input_binary_buffer_size - old_sd_header_location - SCIENCE_HEADER_SIZE);
                        parse_science_packet(input_binary_buffer + old_sd_header_location + SCIENCE_HEADER_SIZE, SCIENCE_DATA_SIZE);
                        full++;
                        break;
                    }
                }
            }

            // parse and check the sequence count
            parse_sd_header(input_binary_buffer + old_sd_header_location);
            if (sd_header_location - old_sd_header_location == SCIENCE_DATA_SIZE + SCIENCE_HEADER_SIZE) {
                // check CRC byte
                memcpy(&CRC_next_packet, input_binary_buffer + sd_header_location + 2, 1);
                CRC_calculate = calc_CRC_8_ATM_rev(input_binary_buffer + old_sd_header_location, SCIENCE_DATA_SIZE + SCIENCE_HEADER_SIZE);
                if (CRC_next_packet != CRC_calculate) {
                    log_message("Wrong CRC, calculate value: %02X, value from next packet: %02X", CRC_calculate, CRC_next_packet);
                    continuous_packet = 0;
                }

                parse_science_packet(input_binary_buffer + old_sd_header_location + SCIENCE_HEADER_SIZE, SCIENCE_DATA_SIZE);
                full++;
            }
            else {
                // packet smaller than expected
                if (sd_header_location - old_sd_header_location < SCIENCE_DATA_SIZE + SCIENCE_HEADER_SIZE) {
                    log_message("Packet size %zu bytes smaller than expected", sd_header_location - old_sd_header_location);
                    parse_science_packet(input_binary_buffer + old_sd_header_location + SCIENCE_HEADER_SIZE, sd_header_location - old_sd_header_location - SCIENCE_HEADER_SIZE);
                }
                // if packet larger than expected, don't parse the packet
                else {
                    log_message("Packet size %zu bytes larger than expected", sd_header_location - old_sd_header_location);
                }
                continuous_packet = 0;
                broken++;
            }
        }
        break;
    }
    log_message("packet summary: full = %zu, broken = %zu", full, broken);
    
    got_first_sync_data = 0;
    free_got_first_sd_header();
    ///// ↑↑↑ need checking!!!

    /// step_3_parse_data_end ///

    // destroy science_icd_binary_buffer independently
    free(science_icd_binary_buffer);

    // return updated file pointer to main funciton
    return output_file_pointer;
}