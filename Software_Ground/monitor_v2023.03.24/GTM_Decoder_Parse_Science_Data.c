#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "GTM_Decoder_Parse_Science_Data.h"
#include "GTM_Decoder_Function.h"
#include "GTM_Decoder_CRC_Check.h"

int parse_science_data(int InputFilePointer) {
    size_t actual_binary_buffer_size;
    int output_file_pointer;
    size_t sd_header_location;
    size_t old_sd_header_location;
    size_t full = 0;
    size_t broken = 0;
    uint8_t CRC_next_packet, CRC_calculate;

    // initializing pps and finetime counter
    event_buffer->pps_counter = 0;
    event_buffer->fine_counter = 0;

    // moving pointer inside bin_infile base on InputFilePointer
    fseek(bin_infile, InputFilePointer, SEEK_SET);

    // recording how many bytes in binary_buffer
    actual_binary_buffer_size = fread(binary_buffer, 1, max_binary_buffer_size, bin_infile);
    
    // updating file pointer by InputFilePointer and actual_binary_buffer_size
    output_file_pointer = InputFilePointer + (int)actual_binary_buffer_size;

    // skip (actual_binary_buffer_size == 0) to avoid error in find_next_sd_header()
    if ((int)actual_binary_buffer_size == 0) {
        return output_file_pointer;
    }
    else {
        ///// ↓↓↓ need checking!!!
        // finding first SD header
        sd_header_location = find_next_sd_header(binary_buffer, -SD_HEADER_SIZE, actual_binary_buffer_size);
        if (sd_header_location != 0) {
            log_message("Binary file doesn't start with science data header, first science data header is at byte %zu", (size_t)ftell(bin_infile) - actual_binary_buffer_size + sd_header_location);
            
            // moving pointer inside bin_infile base on sd_header_location
            fseek(bin_infile, sd_header_location - actual_binary_buffer_size, SEEK_CUR);

            // updating how many bytes in binary_buffer
            actual_binary_buffer_size = fread(binary_buffer, 1, max_binary_buffer_size, bin_infile);
        }
    }

    while (1) {
        log_message("load new chunk");

        // leaving when encountering below weird conditions
        if (actual_binary_buffer_size <= SD_HEADER_SIZE) {
            break;
        }
        if (!is_sd_header(binary_buffer)) {
            log_error("Bin file doesn't start with sd header");
        }

        // initializing the position of sd_header_location
        sd_header_location = 0;

        // parsing data in binary_buffer
        while (sd_header_location < actual_binary_buffer_size) {

            // if the packet is not continueous, reset related parameter
            if (!continuous_packet) {
                log_message("Non contiuous occurs around bytes %zu", (size_t)ftell(bin_infile) - actual_binary_buffer_size + sd_header_location);
                got_first_sync_data = 0;
            }

            // finding next SD header
            old_sd_header_location = sd_header_location;
            sd_header_location = find_next_sd_header(binary_buffer, sd_header_location, actual_binary_buffer_size);

            // no next sd header is found or the remaining buffer isn't large enough to contain a science packet
            if (sd_header_location == (size_t)-1) { 
                if (actual_binary_buffer_size == max_binary_buffer_size) {
                    // no next sd header and this is not the last buffer, load next buffer, don't parse the packet
                    break;
                }
                else {
                    // it's the last buffer but can't find next packet
                    if (old_sd_header_location + SD_HEADER_SIZE + SCIENCE_DATA_SIZE < actual_binary_buffer_size) {
                        log_message("Can't find next sd header while this isn't the last packet, discard data after");
                        break;
                    }
                    // it's the last buffer and this is the last packet
                    else {
                        parse_sd_header(binary_buffer + old_sd_header_location);
                        // parse_science_packet(binary_buffer + old_sd_header_location + SD_HEADER_SIZE, actual_binary_buffer_size - old_sd_header_location - SD_HEADER_SIZE);
                        parse_science_packet(binary_buffer + old_sd_header_location + SD_HEADER_SIZE, SCIENCE_DATA_SIZE);
                        full++;
                        break;
                    }
                }
            }

            // parse and check the sequence count
            parse_sd_header(binary_buffer + old_sd_header_location);
            if (sd_header_location - old_sd_header_location == SCIENCE_DATA_SIZE + SD_HEADER_SIZE) {
                // check CRC byte
                memcpy(&CRC_next_packet, binary_buffer + sd_header_location + 2, 1);
                CRC_calculate = calc_CRC_8_ATM_rev(binary_buffer + old_sd_header_location, SCIENCE_DATA_SIZE + SD_HEADER_SIZE);
                if (CRC_next_packet != CRC_calculate) {
                    log_message("Wrong CRC, calculate value: %02X, value from next packet: %02X", CRC_calculate, CRC_next_packet);
                    continuous_packet = 0;
                }

                parse_science_packet(binary_buffer + old_sd_header_location + SD_HEADER_SIZE, SCIENCE_DATA_SIZE);
                full++;
            }
            else {
                // packet smaller than expected
                if (sd_header_location - old_sd_header_location < SCIENCE_DATA_SIZE + SD_HEADER_SIZE) {
                    log_message("Packet size %zu bytes smaller than expected", sd_header_location - old_sd_header_location);
                    parse_science_packet(binary_buffer + old_sd_header_location + SD_HEADER_SIZE, sd_header_location - old_sd_header_location - SD_HEADER_SIZE);
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
        // if (actual_binary_buffer_size < max_binary_buffer_size) {
        //     break;
        // }
        // // offset position indicator of input file stream based on previous sd header position
        // fseek(bin_infile, old_sd_header_location - actual_binary_buffer_size, SEEK_CUR);
        // actual_binary_buffer_size = read_from_file(binary_buffer, bin_infile, max_binary_buffer_size);
    }
    log_message("packet summary: full = %zu, broken = %zu", full, broken);
    
    got_first_sync_data = 0;
    free_got_first_sd_header();
    ///// ↑↑↑ need checking!!!

    // returning new file pointer to main funciton
    return output_file_pointer;
}