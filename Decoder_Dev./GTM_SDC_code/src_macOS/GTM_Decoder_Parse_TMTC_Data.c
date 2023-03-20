#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "GTM_Decoder_Parse_TMTC_Data.h"
#include "GTM_Decoder_Function.h"

// the code is designed for little endian computers (like x86_64) !!
void parse_tmtc_data(void)
{
    unsigned char *tmtc_data_buffer;
    size_t actual_binary_buffer_size = 0;
    size_t location;
    int tmtc_data_buffer_counter;

    tmtc_data_buffer = (unsigned char *)malloc(TMTC_DATA_SIZE);
    if (!tmtc_data_buffer)
    {
        log_error("fail to create tmtc data buffer");
    }

    actual_binary_buffer_size = read_from_file(binary_buffer, bin_infile, max_binary_buffer_size);
    // loop through buffer
    while (1)
    {
        log_message("load new chunk");

        tmtc_data_buffer_counter = 0;
        for (location = 0; location < actual_binary_buffer_size; location++)
        {
            memcpy(tmtc_data_buffer + tmtc_data_buffer_counter, binary_buffer + location, 1);
            tmtc_data_buffer_counter++;
            if (tmtc_data_buffer_counter == 2)
            { // tmtc header
                if (!is_tmtc_header(tmtc_data_buffer))
                { // is not tmtc header
                    tmtc_data_buffer[0] = tmtc_data_buffer[1];
                    tmtc_data_buffer_counter = 1;
                }
            }
            if (tmtc_data_buffer_counter == TMTC_DATA_SIZE)
            { // all tmtc data is loaded into buffer
                if (!is_tmtc_tail(tmtc_data_buffer + TMTC_DATA_SIZE - 2))
                { // is not tmtc tail
                    log_message("tmtc tail missing!!");
                }
                else
                { // tmtc data is all fine
                    parse_tmtc_packet(tmtc_data_buffer);
                }
                tmtc_data_buffer_counter = 0;
            }
        }

        if (actual_binary_buffer_size < max_binary_buffer_size)
        {
            break;
        }
        actual_binary_buffer_size = read_from_file(binary_buffer, bin_infile, max_binary_buffer_size);
    }

    free(tmtc_data_buffer);
}
