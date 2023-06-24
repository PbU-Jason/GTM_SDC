#include <stdlib.h>

#include "GTM_Decoder_Function.h"
#include "GTM_Decoder_Extract_Science_Data.h"
#include "GTM_Decoder_Parse_Science_Data.h"
#include "GTM_Decoder_Parse_TMTC_Data.h"

int decoder(char *file_name, int decode_mode, int export_mode, int initail_file_pointer) {

    // decode_mode: 1 = tmtc data; 2 = science data
    // export_mode: 1 = raw science decoded data; 2 = pipeline science decoded data

    int new_file_pointer;
    
    check_endianness();
    create_all_buffer();
    open_all_file(file_name, output_file_path);
    switch (decode_mode) {
        case 1:
            if (extract_mode) {
                log_message("start extracting science data");
                new_file_pointer = extract_science_data(initail_file_pointer);
            }
            else {
                log_message("start decoding science data");
                // initialize some setting about sd time to continously decoding
                sync_data_buffer_master_counter = 0;
                sync_data_buffer_slave_counter  = 0;
                missing_sync_data_master        = 0;
                missing_sync_data_slave         = 0;
                got_first_sync_data_master      = 0;
                got_first_sync_data_slave       = 0;
                new_file_pointer = parse_science_data(initail_file_pointer);
            }
            break;
        case 2:
            log_message("start decoding telemetry data");
            new_file_pointer = parse_tmtc_data(initail_file_pointer);
            break;
        case 3:
            log_message("start decoding telemetry and science data simultaneously");
            // parse_both_tmtc_science_data();
            break;
        default:
            log_error("unknown decode mode");
            break;
    }
    close_all_file();
    destroy_all_buffer();

    return new_file_pointer;
}