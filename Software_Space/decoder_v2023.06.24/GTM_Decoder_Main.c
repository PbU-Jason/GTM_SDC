#include <stdlib.h>

#include "GTM_Decoder_Function.h"
#include "GTM_Decoder_Extract_Science_Data.h"
#include "GTM_Decoder_Parse_Science_Data.h"
#include "GTM_Decoder_Parse_TMTC_Data.h"

int decoder(char *FileName, int DecodeMode, int ExtractMode, int ExportMode, int InitailFilePointer) {
    char *output_file_path ;
    const char *file_end = ".bin";
    int new_file_pointer;

    output_file_path = str_remove(FileName, file_end); // FileName - .bin

    decode_mode  = DecodeMode;  // 1 = Science Data; 2 = TMTC Data # ; 3 = Consider Both Together
    extract_mode = ExtractMode; // 0 = Don't Need to Extract NSPO Header; 1 = Need to Extract NSPO Header
    export_mode  = ExportMode;  // 1 = Raw Science Data; 2 = Pipeline Science Data; 3 = Consider Both Together

    check_endianness();
    create_all_buffer();
    open_all_file(FileName, output_file_path);
    switch (decode_mode) {
        case 1:
            if (extract_mode) {
                log_message("start extracting science data");
                new_file_pointer = extract_science_data(InitailFilePointer);
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
                new_file_pointer = parse_science_data(InitailFilePointer);
            }
            break;
        case 2:
            log_message("start decoding telemetry data");
            new_file_pointer = parse_tmtc_data(InitailFilePointer);
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