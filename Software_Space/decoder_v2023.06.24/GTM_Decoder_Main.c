#include "GTM_Decoder_Function.h"
#include "GTM_Decoder_Parse_TMTC_Data.h"
#include "GTM_Decoder_Parse_Science_Data.h"



int decoder(char *file_name, int decode_mode, int export_mode, int initail_file_pointer) {

    // decode_mode: 1 = tmtc data; 2 = science data
    // export_mode: 1 = raw science decoded data; 2 = pipeline science decoded data; 3 = both

    int new_file_pointer;
    
    check_endianness();
    create_all_buffer();
    open_all_file(file_name);

    switch (decode_mode) {

        // decode tmtc data
        case 1:
            log_message("Start decoding tmtc data");
            new_file_pointer = parse_tmtc_data(initail_file_pointer);
            break;

        // decode science data
        case 2:
            log_message("Start decoding science data");

            // initialize some setting about time in science data to continously decoding
            sync_data_buffer_master_counter = 0;
            sync_data_buffer_slave_counter  = 0;
            missing_sync_data_master        = 0;
            missing_sync_data_slave         = 0;
            got_first_sync_data_master      = 0;
            got_first_sync_data_slave       = 0;
            new_file_pointer = parse_science_data(initail_file_pointer);
            
            break;
    }

    close_all_file();
    destroy_all_buffer();

    return new_file_pointer;
}