#include "GTM_Decoder_Function.h"
#include "GTM_Decoder_Parse_TMTC_Data.h"
#include "GTM_Decoder_Parse_Science_Data.h"



int decoder(char *file_name, int decode_mode, int export_mode, int initail_file_pointer) {

    // decode_mode: 1 = tmtc data; 2 = science data
    // export_mode: 1 = raw science decoded data; 2 = pipeline science decoded data; 3 = both

    int new_file_pointer;
    
    check_endianness();
    initailize_sync_data_flag(); // for continuously decode
    create_basic_buffer();
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
            new_file_pointer = parse_science_data(initail_file_pointer, file_name);
            
            break;
    }

    close_all_file();
    destroy_basic_buffer();

    return new_file_pointer;
}