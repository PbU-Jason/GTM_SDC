#include <stdlib.h>

#include "GTM_Decoder_Function.h"
#include "GTM_Decoder_Extract_Science_Data.h"
#include "GTM_Decoder_Parse_Science_Data.h"
#include "GTM_Decoder_Parse_TMTC_Data.h"
#include "GTM_Decoder_Parse_Both_TMTC_Science_Data.h"


char *input_file_path  = NULL;
char *output_file_path = NULL;
const char *file_end   = ".bin";

int decoder(char *FileName, int DecodeMode, int ExtractMode, int ExportMode, int HitMode, int GainMode) {
    check_endianness();

    input_file_path  = FileName;
    output_file_path = str_remove(FileName, file_end); // FileName - .bin

    decode_mode  = DecodeMode;  // 1 = Science Data; 2 = TMTC Data; 3 = Consider Both Together
    extract_mode = ExtractMode; // 0 = Don't Need to Extract NSPO Header; 1 = Need to Extract NSPO Header
    export_mode  = ExportMode;  // 1 = Raw Science Data; 2 = Pipeline Science Data
    hit_mode     = HitMode;     // 1 = Hit Science Data; 2 = NoHit Science Data
    gain_mode    = GainMode;    // 1 = High Gain Science Data; 2 = Low Gain Science Data

    create_all_buffer();
    open_all_file(input_file_path, output_file_path);
    switch (decode_mode) {
        case 1:
            if (extract_mode) {
                log_message("start extracting science data");
                extract_science_data();
                close_all_file();
                extract_mode = 0;
                input_file_path = str_append(output_file_path, "_extracted.bin");
                output_file_path = str_append(output_file_path, "_extracted");
                open_all_file(input_file_path, output_file_path);
                log_message("start decoding science data");
                parse_science_data();
            }
            else {
                log_message("start decoding science data");
                parse_science_data();
            }
            break;
        case 2:
            log_message("start decoding telemetry data");
            parse_tmtc_data();
            break;
        case 3:
            log_message("start decoding telemetry and science data simultaneously");
            parse_both_tmtc_science_data();
            break;
        default:
            log_error("unknown decode mode");
            break;
    }
    close_all_file();
    destroy_all_buffer();

    return 0;
}