#include "GTM_Decoder_Function.h"

#include <stdarg.h> // for va_list, va_start(), va_arg() & va_end()
#include <stdlib.h> // for exit & malloc (also has size_t)
#include <string.h> // for strlen, memcpy, strcat & memcmp (also has size_t)
#include <time.h>   // for mktime & localtime (also has size_t)
#include <math.h>   // for pow



//* define_global_variable *//

/// main ///

int decode_mode = 0;
int export_mode = 0;

int sync_data_buffer_master_counter = 0;
int sync_data_buffer_slave_counter  = 0;
int missing_sync_data_master        = 0; // =1 after sync data with no tail
int missing_sync_data_slave         = 0; 
int got_first_sync_data_master      = 0; // =1 after parsing first sync data
int got_first_sync_data_slave       = 0;

/// main_end ///

/// parse_science_data ///

int continuous_packet = 1;

/// parse_science_data_end ///

/// create_all_buffer ///

// for input binary
size_t max_input_binary_buffer_size = 1174405120; // 1 GB
unsigned char *input_binary_buffer  =  NULL;

// for typedef struct
UTC *utc_buffer       = NULL; // tmtc and science shared
TMTC *tmtc_buffer     = NULL;
Science *event_buffer = NULL;

// for other TASA added header and tail
unsigned char *tasa_tmtc_packet_header_buffer              = NULL;
unsigned char *tasa_science_attached_synchro_marker_buffer = NULL;
unsigned char *tasa_science_primary_header_buffer          = NULL;
unsigned char *tasa_science_transfer_frame_trailer_buffer  = NULL;
unsigned char *tasa_science_reed_solomon_symbols_buffer    = NULL;

/// create_all_buffer_end ///

/// open_all_file ///

FILE *input_binary_file = NULL;

FILE *raw_output_file               = NULL; // tmtc and science shared
FILE *tmtc_master_output_file       = NULL;
FILE *tmtc_slave_output_file        = NULL;
FILE *science_pipeline_output_file  = NULL;

/// open_all_file_end ///

//* define_global_variable_end *//



//* local_variable *//

char tmtc_header_all[] = "Bytes 0;Bytes 1;Bytes 2;Bytes 3;Bytes 4;Bytes 5;Bytes 6;Bytes 7;Bytes 8;Bytes 9;Bytes 10;Bytes 11;Bytes 12;Bytes 13;Bytes 14;Bytes 15;Bytes 16;Bytes 17;Bytes 18;Bytes 19;Bytes 20;Bytes 21;Bytes 22;Bytes 23;Bytes 24;Bytes 25;Bytes 26;Bytes 27;Bytes 28;Bytes 29;Bytes 30;Bytes 31;Bytes 32;Bytes 33;Bytes 34;Bytes 35;Bytes 36;Bytes 37;Bytes 38;Bytes 39;Bytes 40;Bytes 41;Bytes 42;Bytes 43;Bytes 44;Bytes 45;Bytes 46;Bytes 47;Bytes 48;Bytes 49;Bytes 50;Bytes 51;Bytes 52;Bytes 53;Bytes 54;Bytes 55;Bytes 56;Bytes 57;Bytes 58;Bytes 59;Bytes 60;Bytes 61;Bytes 62;Bytes 63;Bytes 64;Bytes 65;Bytes 66;Bytes 67;Bytes 68;Bytes 69;Bytes 70;Bytes 71;Bytes 72;Bytes 73;Bytes 74;Bytes 75;Bytes 76;Bytes 77;Bytes 78;Bytes 79;Bytes 80;Bytes 81;Bytes 82;Bytes 83;Bytes 84;Bytes 85;Bytes 86;Bytes 87;Bytes 88;Bytes 89;Bytes 90;Bytes 91;Bytes 92;Bytes 93;Bytes 94;Bytes 95;Bytes 96;Bytes 97;Bytes 98;Bytes 99;Bytes 100;Bytes 101;Bytes 102;Bytes 103;Bytes 104;Bytes 105;Bytes 106;Bytes 107;Bytes 108;Bytes 109;Bytes 110;Bytes 111;Bytes 112;Bytes 113;Bytes 114;Bytes 115;Bytes 116;Bytes 117;Bytes 118;Bytes 119;Bytes 120;Bytes 121;Bytes 122;Bytes 123;Bytes 124;Bytes 125;Bytes 126;Bytes 127\n";
char tmtc_header_master[] = "Header;GTM ID;Packet Counter;Data Length (MSB);Data Length;UTC Year;UTC Day;UTC Hour;UTC Minute;UTC Second;UTC Subsecond;GTM ID in Lastest PPS Counter;Lastest PPS Counter;Lastest Fine Time Counter Value Between 2 PPSs;Board Temperature#1;Board Temperature#2;CITIROC1 Temperature;CITIROC2 Temperature;CITIROC1 Live Time (Busy);CITIROC2 Live Time (Busy);CITIROC1 Hit Counter#0;CITIROC1 Hit Counter#1;CITIROC1 Hit Counter#2;CITIROC1 Hit Counter#3;CITIROC1 Hit Counter#4;CITIROC1 Hit Counter#5;CITIROC1 Hit Counter#6;CITIROC1 Hit Counter#7;CITIROC1 Hit Counter#8;CITIROC1 Hit Counter#9;CITIROC1 Hit Counter#10;CITIROC1 Hit Counter#11;CITIROC1 Hit Counter#12;CITIROC1 Hit Counter#13;CITIROC1 Hit Counter#14;CITIROC1 Hit Counter#15;CITIROC1 Hit Counter#16;CITIROC1 Hit Counter#17;CITIROC1 Hit Counter#18;CITIROC1 Hit Counter#19;CITIROC1 Hit Counter#20;CITIROC1 Hit Counter#21;CITIROC1 Hit Counter#22;CITIROC1 Hit Counter#23;CITIROC1 Hit Counter#24;CITIROC1 Hit Counter#25;CITIROC1 Hit Counter#26;CITIROC1 Hit Counter#27;CITIROC1 Hit Counter#28;CITIROC1 Hit Counter#29;CITIROC1 Hit Counter#30;CITIROC1 Hit Counter#31;CITIROC2 Hit Counter#0;CITIROC2 Hit Counter#1;CITIROC2 Hit Counter#2;CITIROC2 Hit Counter#3;CITIROC2 Hit Counter#4;CITIROC2 Hit Counter#5;CITIROC2 Hit Counter#6;CITIROC2 Hit Counter#7;CITIROC2 Hit Counter#8;CITIROC2 Hit Counter#9;CITIROC2 Hit Counter#10;CITIROC2 Hit Counter#11;CITIROC2 Hit Counter#12;CITIROC2 Hit Counter#13;CITIROC2 Hit Counter#14;CITIROC2 Hit Counter#15;CITIROC2 Hit Counter#16;CITIROC2 Hit Counter#17;CITIROC2 Hit Counter#18;CITIROC2 Hit Counter#19;CITIROC2 Hit Counter#20;CITIROC2 Hit Counter#21;CITIROC2 Hit Counter#22;CITIROC2 Hit Counter#23;CITIROC2 Hit Counter#24;CITIROC2 Hit Counter#25;CITIROC2 Hit Counter#26;CITIROC2 Hit Counter#27;CITIROC2 Hit Counter#28;CITIROC2 Hit Counter#29;CITIROC2 Hit Counter#30;CITIROC2 Hit Counter#31;CITIROC1 Trigger Counter;CITIROC2 Trigger Counter;Counter Period Setting;HV DAC1;HV DAC2;SPW#A Error Count;SPW#A Last Recv Byte;SPW#B Error Count;SPW#B Last Recv Byte;SPW#A Status;SPW#B Status;Recv Checksum of Last CMD;Calc Checksum of Last CMD;Number of Recv CMDs;Bytes 114;Bytes 115;Bytes 116;Bytes 117;Bytes 118;CITIROC1 Live Time (Buffer+Busy);CITIROC2 Live Time (Buffer+Busy);Checksum;Tail\n";
char tmtc_header_slave[] = "Header;GTM ID;Packet Counter;Data Length (MSB);Data Length;UTC Year;UTC Day;UTC Hour;UTC Minute;UTC Second;UTC Subsecond;GTM ID in Lastest PPS Counter;Lastest PPS Counter;Lastest Fine Time Counter Value Between 2 PPSs;Board Temperature#1;Board Temperature#2;CITIROC1 Temperature;CITIROC2 Temperature;CITIROC1 Live Time (Busy);CITIROC2 Live Time (Busy);CITIROC1 Hit Counter#0;CITIROC1 Hit Counter#1;CITIROC1 Hit Counter#2;CITIROC1 Hit Counter#3;CITIROC1 Hit Counter#4;CITIROC1 Hit Counter#5;CITIROC1 Hit Counter#6;CITIROC1 Hit Counter#7;CITIROC1 Hit Counter#8;CITIROC1 Hit Counter#9;CITIROC1 Hit Counter#10;CITIROC1 Hit Counter#11;CITIROC1 Hit Counter#12;CITIROC1 Hit Counter#13;CITIROC1 Hit Counter#14;CITIROC1 Hit Counter#15;CITIROC1 Hit Counter#16;CITIROC1 Hit Counter#17;CITIROC1 Hit Counter#18;CITIROC1 Hit Counter#19;CITIROC1 Hit Counter#20;CITIROC1 Hit Counter#21;CITIROC1 Hit Counter#22;CITIROC1 Hit Counter#23;CITIROC1 Hit Counter#24;CITIROC1 Hit Counter#25;CITIROC1 Hit Counter#26;CITIROC1 Hit Counter#27;CITIROC1 Hit Counter#28;CITIROC1 Hit Counter#29;CITIROC1 Hit Counter#30;CITIROC1 Hit Counter#31;CITIROC2 Hit Counter#0;CITIROC2 Hit Counter#1;CITIROC2 Hit Counter#2;CITIROC2 Hit Counter#3;CITIROC2 Hit Counter#4;CITIROC2 Hit Counter#5;CITIROC2 Hit Counter#6;CITIROC2 Hit Counter#7;CITIROC2 Hit Counter#8;CITIROC2 Hit Counter#9;CITIROC2 Hit Counter#10;CITIROC2 Hit Counter#11;CITIROC2 Hit Counter#12;CITIROC2 Hit Counter#13;CITIROC2 Hit Counter#14;CITIROC2 Hit Counter#15;CITIROC2 Hit Counter#16;CITIROC2 Hit Counter#17;CITIROC2 Hit Counter#18;CITIROC2 Hit Counter#19;CITIROC2 Hit Counter#20;CITIROC2 Hit Counter#21;CITIROC2 Hit Counter#22;CITIROC2 Hit Counter#23;CITIROC2 Hit Counter#24;CITIROC2 Hit Counter#25;CITIROC2 Hit Counter#26;CITIROC2 Hit Counter#27;CITIROC2 Hit Counter#28;CITIROC2 Hit Counter#29;CITIROC2 Hit Counter#30;CITIROC2 Hit Counter#31;CITIROC1 Trigger Counter;CITIROC2 Trigger Counter;Counter Period Setting;HV DAC1;HV DAC2;Input Current Value;Input Voltage Value;Current Monitor Chip (U22) Temperature;HV Input Current Value;HV Input Voltage Value;Current Monitor Chip (U21) Temperature;Recv Checksum of Last CMD;Calc Checksum of Last CMD;Number of Recv CMDs;Bytes 114;Bytes 115;Bytes 116;Bytes 117;Bytes 118;CITIROC1 Live Time (Buffer+Busy);CITIROC2 Live Time (Buffer+Busy);Checksum;Tail\n";
char science_pipeline_header[] = "Module;PPS;FineTime;CITIROC;Channel;Gain;ADC\n";

int got_first_sd_header = 0;
uint8_t sequence_count = 0;
int got_first_time_info = 0;

//* local_variable_end *//



//* function *//

/// main ///

// checked~
void check_endianness() {
    unsigned char x[2] = {0x00, 0x01}; 
    // use char array to define string
    // x[2] means there are two charaters
    // x stores the address of first charater, which is x[0] (like value)
    // char array decay to char pointer, so they are differnet but similar

    uint16_t *y;

    y = (uint16_t *)x;
    // (uint16_t *) to make two pointer types compatible 
    // for little endian (most of PC), int(hex(*y)) == int(0x0100) == 256
    // for big endian (GTM data), int(hex(*y)) == int(0x0001) == 1
    // this program is designed to decode GTM data to recognized data in most of PC
    
    if (*y == 1) {
        log_error("This program can't be run on big endian system!");
    }
}

// checked~
// not necessary, just see how to write printf in the user's own way
// please refer below link to see ..., va_list, va_start, vprintf and va_end
// https://www.ibm.com/docs/en/zos/2.1.0?topic=functions-vprintf-format-print-data-stdout
void log_error(const char *sentence, ...) {
    // use char pointer to define string
    // sentence stores the address of first charater, which is *sentence
    // second charater is *(sentence + 1)
    // const make string unchangeable

    va_list args;

    va_start(args, sentence);
    printf("Error: "); vprintf(sentence, args); printf("\n");
    va_end(args);
    exit(1); // abnormal exit
}

// checked~
void create_all_buffer() {

    // dynamically allocate a single large block of memory with the specified size

    input_binary_buffer = (unsigned char *)malloc(max_input_binary_buffer_size);
    
    utc_buffer = (UTC *)malloc(sizeof(UTC));
    tmtc_buffer = (TMTC *)malloc(sizeof(TMTC));
    event_buffer = (Science *)malloc(sizeof(Science));

    tasa_tmtc_packet_header_buffer = (unsigned char *)malloc(TMTC_PACKET_HEADER_SIZE);
    tasa_science_attached_synchro_marker_buffer = (unsigned char *)malloc(SCIENCE_ATTACHED_SYNCHRO_MARKER_SIZE);
    tasa_science_primary_header_buffer = (unsigned char *)malloc(SCIENCE_PRIMARY_HEADER_SIZE);
    tasa_science_transfer_frame_trailer_buffer = (unsigned char *)malloc(SCIENCE_TRANSFER_FRAME_TRAILER_SIZE);
    tasa_science_reed_solomon_symbols_buffer = (unsigned char *)malloc(SCIENCE_REED_SOLOMON_CHECK_SYMBOLS_SIZE);
}

// checked~
void open_all_file(char *input_file_path) {
    char *raw_output_path = NULL; // tmtc and science shared
    char *tmtc_master_output_path = NULL;
    char *tmtc_slave_output_path = NULL;
    char *science_pipeline_output_path = NULL;
    
    // open input file
    input_binary_file = fopen(input_file_path, "rb");
    log_message("Successfully load input file");

    // open output file
    switch (decode_mode) {

        // decode tmtc data
        case 1:
            // tmtc with master + slave
            raw_output_path = str_append(input_file_path, "_tmtc_all.csv");
            raw_output_file = fopen(raw_output_path, "a");
            if (ftell(raw_output_file) == 0) {
                fputs(tmtc_header_all, raw_output_file);
            }
            free(raw_output_path);

            // tmtc only with master
            tmtc_master_output_path = str_append(input_file_path, "_tmtc_master.csv");
            tmtc_master_output_file = fopen(tmtc_master_output_path, "a");
            if (ftell(tmtc_master_output_file) == 0) {
                fputs(tmtc_header_master, tmtc_master_output_file);
            }
            free(tmtc_master_output_path);

            // tmtc only with slave
            tmtc_slave_output_path = str_append(input_file_path, "_tmtc_slave.csv");
            tmtc_slave_output_file = fopen(tmtc_slave_output_path, "a");
            if (ftell(tmtc_slave_output_file) == 0) {
                fputs(tmtc_header_slave, tmtc_slave_output_file);
            }
            free(tmtc_slave_output_path);
            break;

        // decode science data
        case 2:
            if (export_mode == 1) {
                raw_output_path = str_append(input_file_path, "_science_raw.txt");
                raw_output_file = fopen(raw_output_path, "a");
                free(raw_output_path);
            }
            else if (export_mode == 2) {
                science_pipeline_output_path = str_append(input_file_path, "_science_pipeline.csv");
                science_pipeline_output_file = fopen(science_pipeline_output_path, "a");
                if (ftell(science_pipeline_output_file) == 0) {
                    fputs(science_pipeline_header, science_pipeline_output_file);
                }
                free(science_pipeline_output_path);
            }
            else if (export_mode == 3) {
                raw_output_path = str_append(input_file_path, "_science_raw.txt");
                raw_output_file = fopen(raw_output_path, "a");
                free(raw_output_path);

                science_pipeline_output_path = str_append(input_file_path, "_science_pipeline.csv");
                science_pipeline_output_file = fopen(science_pipeline_output_path, "a");
                if (ftell(science_pipeline_output_file) == 0) {
                    fputs(science_pipeline_header, science_pipeline_output_file);
                }
                free(science_pipeline_output_path);
            }
            else{
                log_error("Unknown export mode!");
            }
            break;
        
        default:
            log_error("Unknown decode mode!");
            break;
        }
}

// checked~
// similar with log_error, but no exit
void log_message(const char *sentence, ...) {
    va_list args;

    va_start(args, sentence);
    printf("Message: "); vprintf(sentence, args); printf("\n");
    va_end(args);
}

// checked~
char *str_append(char *pre_fix, char *post_fix) {
    char *new;
    size_t size_prefix, size_postfix;

    size_prefix = strlen(pre_fix); // not count \0
    size_postfix = strlen(post_fix);
    new = (char *)malloc((size_prefix + size_postfix + 1) * sizeof(char)); // +1 to keep \0 place

    memcpy(new, pre_fix, size_prefix + 1); // again, +1 to keep \0 place
    strcat(new, post_fix); // automatically repalce \0 of pre_fix and add \0 after post_fix
    
    return new;
}

// checked~
void close_all_file() {

    // close input file
    fclose(input_binary_file);

    // close output file
    switch (decode_mode) {
        
        // decode tmtc data
        case 1:
            fclose(raw_output_file);
            fclose(tmtc_master_output_file);
            fclose(tmtc_slave_output_file);
            break;
        
        // decode science data
        case 2:
            if (export_mode == 1) {
                fclose(raw_output_file);
            }
            else if (export_mode == 2) {
                fclose(science_pipeline_output_file);
            }
            else if (export_mode == 3) {
                fclose(raw_output_file);
                fclose(science_pipeline_output_file);
            }
            else {
                log_error("Unknown export mode!");
            }
            break;

        default:
            log_error("Unknown decode mode!");
            break;
    }
    log_message("close all file");
}

// checked~
void destroy_all_buffer() {
    free(input_binary_buffer);

    free(utc_buffer);
    free(tmtc_buffer);
    free(event_buffer);

    free(tasa_tmtc_packet_header_buffer);
    free(tasa_science_attached_synchro_marker_buffer);
    free(tasa_science_primary_header_buffer);
    free(tasa_science_transfer_frame_trailer_buffer);
    free(tasa_science_reed_solomon_symbols_buffer);
}

/// main_end ///

/// parse_tmtc_data ///

int is_tmtc_header(unsigned char *Target) {
    static unsigned char ref[2] = {0x55, 0xAA};

    if (!memcmp(ref, Target, 2)) {
        return 1;
    }

    return 0;
}

int is_tmtc_tail(unsigned char *Targrt) {
    static unsigned char ref[2] = {0xFB, 0xF2};

    if (!memcmp(ref, Targrt, 2))
    {
        return 1;
    }
    return 0;
}

void parse_tmtc_packet(unsigned char *Target) {
    int i;
    int j;

    // header
    memcpy(tmtc_buffer->head, Target, 2);

    // GTM module
    j = (*(Target + 2) == 0x02) ? 0 : 1;
    memcpy(&(tmtc_buffer->gtm_id), Target + 2, 1);

    // packet counter
    memcpy(&(tmtc_buffer->packet_counter), Target + 3, 2);
    big2little_endian(&(tmtc_buffer->packet_counter), 2);

    // data length
    memcpy(&(tmtc_buffer->data_length_msb), Target + 5, 1);
    memcpy(&(tmtc_buffer->data_length_120_byte), Target + 6, 1);

    // UTC
    parse_utc_time_tmtc(Target + 7);

    // pps_counter
    tmtc_buffer->gtm_id_in_pps_counter = ((*(Target + 15) & 0x80) == 0x80) ? 1 : 0; // extract GTM ID
    *(Target + 15) = *(Target + 15) & 0x7F; // mask GTM ID
    memcpy(&(tmtc_buffer->pps_counter), Target + 15, 2);
    big2little_endian(&(tmtc_buffer->pps_counter), 2);
    // fine counter
    memcpy(&(tmtc_buffer->fine_time_counter), Target + 17, 3); // (fine_counter[0] << 16) | (fine_counter[1] << 8) | fine_counter[2] to recover

    // board temp (int8_t)
    memcpy(&(tmtc_buffer->board_temp_1), Target + 20, 1);
    memcpy(&(tmtc_buffer->board_temp_2), Target + 21, 1);

    // citiroc temp (definition in ICD is Little-Endian!)
    if ((*(Target + 24) & 0x80) == 0x80) {
        tmtc_buffer->citiroc_1_temp[0] = 0xC0 | ((*(Target + 24) & 0x7E) >> 1);
    }
    else {
        tmtc_buffer->citiroc_1_temp[0] = 0x00 | ((*(Target + 24) & 0x7E) >> 1);
    }
    memcpy(&(tmtc_buffer->citiroc_1_temp[1]), Target + 22, 1);

    if ((*(Target + 25) & 0x80) == 0x80) {
        tmtc_buffer->citiroc_2_temp[0] = 0xC0 | ((*(Target + 25) & 0x7E) >> 1);
    }
    else {
        tmtc_buffer->citiroc_2_temp[0] = 0x00 | ((*(Target + 25) & 0x7E) >> 1);
    }
    memcpy(&(tmtc_buffer->citiroc_2_temp[1]), Target + 23, 1);

    // citiroc livetime // see fine counter
    memcpy(&(tmtc_buffer->citiroc_1_livetime_busy), Target + 26, 3); 
    memcpy(&(tmtc_buffer->citiroc_2_livetime_busy), Target + 29, 3);
    // citiroc hit
    for (i = 0; i < 32; ++i) {
        memcpy(&(tmtc_buffer->citiroc_1_hit[i]), Target + 32 + i, 1);
        memcpy(&(tmtc_buffer->citiroc_2_hit[i]), Target + 64 + i, 1);
    }
    // citiroc trigger
    memcpy(&(tmtc_buffer->citiroc_1_trigger_counter), Target + 96, 2);
    big2little_endian(&(tmtc_buffer->citiroc_1_trigger_counter), 2);
    memcpy(&(tmtc_buffer->citiroc_2_trigger_counter), Target + 98, 2);
    big2little_endian(&(tmtc_buffer->citiroc_2_trigger_counter), 2);

    // counter period
    memcpy(&(tmtc_buffer->counter_period), Target + 100, 1);

    // hv dac
    memcpy(&(tmtc_buffer->hv_dac_1), Target + 101, 1);
    memcpy(&(tmtc_buffer->hv_dac_2), Target + 102, 1);

    if (j == 0) {
        // for master
        // spw stuff
        memcpy(&(tmtc_buffer->spw_a_error_count), Target + 103, 1);
        memcpy(&(tmtc_buffer->spw_a_last_recv_byte), Target + 104, 1);
        memcpy(&(tmtc_buffer->spw_b_error_count), Target + 105, 1);
        memcpy(&(tmtc_buffer->spw_b_last_recv_byte), Target + 106, 1);
        memcpy(&(tmtc_buffer->spw_a_status), Target + 107, 2);
        big2little_endian(&(tmtc_buffer->spw_a_status), 2);
        memcpy(&(tmtc_buffer->spw_b_status), Target + 109, 2);
        big2little_endian(&(tmtc_buffer->spw_b_status), 2);
    }
    else if (j == 1) {
        // for slave
        // spw v & i monitoring
        memcpy(&(tmtc_buffer->input_i), Target + 103, 1);
        memcpy(&(tmtc_buffer->input_v), Target + 104, 1);
        memcpy(&(tmtc_buffer->input_i_v), Target + 105, 1);
        memcpy(&(tmtc_buffer->i_monitor_u22_temp), Target + 106, 1);
        memcpy(&(tmtc_buffer->hv_input_i), Target + 107, 1);
        memcpy(&(tmtc_buffer->hv_input_v), Target + 108, 1);
        memcpy(&(tmtc_buffer->hv_input_i_v), Target + 109, 1);
        memcpy(&(tmtc_buffer->i_monitor_u21_temp), Target + 110, 1);
    }
    else {
        log_error("unknown module!");
    }

    // checksum
    memcpy(&(tmtc_buffer->cmd_recv_checksum), Target + 111, 1);
    memcpy(&(tmtc_buffer->cmd_calc_checksum), Target + 112, 1);
    // recv num
    memcpy(&(tmtc_buffer->cmd_recv_number), Target + 113, 1);

    // tmtc empty
    memcpy(&(tmtc_buffer->tmtc_empty), Target + 114, 5);

    // citiroc livetime // see fine counter
    memcpy(&(tmtc_buffer->citiroc_1_livetime_buffer_busy), Target + 119, 3); 
    memcpy(&(tmtc_buffer->citiroc_2_livetime_buffer_busy), Target + 122, 3);

    // checksum
    memcpy(&(tmtc_buffer->checksum), Target + 125, 1);

    // tail
    memcpy(tmtc_buffer->tail, Target + 126, 2);

    write_tmtc_buffer_all(Target);
    if (j == 0) {
        write_tmtc_buffer_master();
    }
    else if (j == 1) {
        write_tmtc_buffer_slave();
    }
    else {
        log_error("unknown module!");
    }
}

void parse_utc_time_tmtc(unsigned char *Target) {
    // year
    memcpy(&(time_buffer->year), Target, 2);
    big2little_endian(&(time_buffer->year), 2);
    // day
    memcpy(&(time_buffer->day), Target + 2, 2);
    big2little_endian(&(time_buffer->day), 2);
    // hour
    memcpy(&(time_buffer->hour), Target + 4, 1);
    // minute
    memcpy(&(time_buffer->minute), Target + 5, 1);
    // sec
    memcpy(&(time_buffer->sec), Target + 6, 1);
    // sub sec (ms)
    memcpy(&(time_buffer->sub_sec), Target + 7, 1);

    return;
}

void write_tmtc_buffer_all(unsigned char *Target) { 
    int i;
    unsigned char byte[1];

    for (i = 0; i < 127; i++) {
        memcpy(&(byte[0]), Target + i, 1);
        fprintf(raw_output_file, "%d;", byte[0]);
    }
    memcpy(&(byte[0]), Target + 127, 1);
    fprintf(raw_output_file, "%d\n", byte[0]);
}

void write_tmtc_buffer_master(void) {
    int i;
    int fine_counter = 0;
    int citiroc1_livetime_busy = 0;
    int citiroc2_livetime_busy = 0;
    int citiroc1_livetime_buffer_busy = 0;
    int citiroc2_livetime_buffer_busy = 0;

    int16_t citiroc1_temp = 0;
    int16_t citiroc2_temp = 0;

    // recover 3 bytes
    fine_counter = (tmtc_buffer->fine_time_counter[0] << 16) | (tmtc_buffer->fine_time_counter[1] << 8) | tmtc_buffer->fine_time_counter[2];
    citiroc1_livetime_busy = (tmtc_buffer->citiroc_1_livetime_busy[0] << 16) | (tmtc_buffer->citiroc_1_livetime_busy[1] << 8) | tmtc_buffer->citiroc_1_livetime_busy[2];
    citiroc2_livetime_busy = (tmtc_buffer->citiroc_2_livetime_busy[0] << 16) | (tmtc_buffer->citiroc_2_livetime_busy[1] << 8) | tmtc_buffer->citiroc_2_livetime_busy[2];
    citiroc1_livetime_buffer_busy = (tmtc_buffer->citiroc_1_livetime_buffer_busy[0] << 16) | (tmtc_buffer->citiroc_1_livetime_buffer_busy[1] << 8) | tmtc_buffer->citiroc_1_livetime_buffer_busy[2];
    citiroc2_livetime_buffer_busy = (tmtc_buffer->citiroc_2_livetime_buffer_busy[0] << 16) | (tmtc_buffer->citiroc_2_livetime_buffer_busy[1] << 8) | tmtc_buffer->citiroc_2_livetime_buffer_busy[2];

    // recover 2 bytes, consider sign (don't need to transfer Endian)
    citiroc1_temp = (tmtc_buffer->citiroc_1_temp[0] << 8) |  tmtc_buffer->citiroc_1_temp[1];
    citiroc2_temp = (tmtc_buffer->citiroc_2_temp[0] << 8) |  tmtc_buffer->citiroc_2_temp[1];

    fprintf(tmtc_master_output_file, "%X%X", tmtc_buffer->head[0], tmtc_buffer->head[1]); // head
    fprintf(tmtc_master_output_file, \
    ";%u;%u;%u;%u; \
    %u;%u;%u;%u;%u;%u; \
    %i;%u;%i; \
    %i;%i;%i;%i;%i;%i", \
    tmtc_buffer->gtm_id, tmtc_buffer->packet_counter, tmtc_buffer->data_length_msb, tmtc_buffer->data_length_120_byte, \
    time_buffer->year, time_buffer->day, time_buffer->hour, time_buffer->minute, time_buffer->sec, time_buffer->sub_sec, \
    tmtc_buffer->gtm_id_in_pps_counter, tmtc_buffer->pps_counter, fine_counter, \
    tmtc_buffer->board_temp_1, tmtc_buffer->board_temp_2, citiroc1_temp, citiroc2_temp, citiroc1_livetime_busy, citiroc2_livetime_busy);    
    for (i = 0; i < 32; ++i) {
        fprintf(tmtc_master_output_file, ";%u", tmtc_buffer->citiroc_1_hit[i]);
    }
    for (i = 0; i < 32; ++i) {
        fprintf(tmtc_master_output_file, ";%u", tmtc_buffer->citiroc_2_hit[i]);
    }
    fprintf(tmtc_master_output_file, \
    ";%u;%u;%u;%u;%u;\
    %X;%X;%X;%X;%X;%X;\
    %u;%u;%u", \
    tmtc_buffer->citiroc_1_trigger_counter, tmtc_buffer->citiroc_2_trigger_counter, tmtc_buffer->counter_period, tmtc_buffer->hv_dac_1, tmtc_buffer->hv_dac_2, \
    tmtc_buffer->spw_a_error_count, tmtc_buffer->spw_a_last_recv_byte, tmtc_buffer->spw_b_error_count, tmtc_buffer->spw_b_last_recv_byte, tmtc_buffer->spw_a_status, tmtc_buffer->spw_b_status, \
    tmtc_buffer->cmd_recv_checksum, tmtc_buffer->cmd_calc_checksum, tmtc_buffer->cmd_recv_number);
    for (i = 0; i < 5; ++i) {
        fprintf(tmtc_master_output_file, ";%u", tmtc_buffer->tmtc_empty[i]);
    }
    fprintf(tmtc_master_output_file, ";%i;%i;%u", citiroc1_livetime_buffer_busy, citiroc2_livetime_buffer_busy, tmtc_buffer->checksum);
    fprintf(tmtc_master_output_file, ";%X%X\n", tmtc_buffer->tail[0], tmtc_buffer->tail[1]); // tail
}

void write_tmtc_buffer_slave(void) {
    int i;
    int fine_counter = 0;
    int citiroc1_livetime_busy = 0;
    int citiroc2_livetime_busy = 0;
    int citiroc1_livetime_buffer_busy = 0;
    int citiroc2_livetime_buffer_busy = 0;

    int16_t citiroc1_temp = 0;
    int16_t citiroc2_temp = 0;

    uint16_t input_i = 0;
    uint16_t input_v = 0;
    uint16_t hv_input_i = 0;
    uint16_t hv_input_v = 0;

    // recover 3 bytes
    fine_counter = (tmtc_buffer->fine_time_counter[0] << 16) | (tmtc_buffer->fine_time_counter[1] << 8) | tmtc_buffer->fine_time_counter[2];
    citiroc1_livetime_busy = (tmtc_buffer->citiroc_1_livetime_busy[0] << 16) | (tmtc_buffer->citiroc_1_livetime_busy[1] << 8) | tmtc_buffer->citiroc_1_livetime_busy[2];
    citiroc2_livetime_busy = (tmtc_buffer->citiroc_2_livetime_busy[0] << 16) | (tmtc_buffer->citiroc_2_livetime_busy[1] << 8) | tmtc_buffer->citiroc_2_livetime_busy[2];
    citiroc1_livetime_buffer_busy = (tmtc_buffer->citiroc_1_livetime_buffer_busy[0] << 16) | (tmtc_buffer->citiroc_1_livetime_buffer_busy[1] << 8) | tmtc_buffer->citiroc_1_livetime_buffer_busy[2];
    citiroc2_livetime_buffer_busy = (tmtc_buffer->citiroc_2_livetime_buffer_busy[0] << 16) | (tmtc_buffer->citiroc_2_livetime_buffer_busy[1] << 8) | tmtc_buffer->citiroc_2_livetime_buffer_busy[2];

    // recover 2 bytes, consider sign (don't need to transfer Endian)
    citiroc1_temp = (tmtc_buffer->citiroc_1_temp[1] << 8) |  tmtc_buffer->citiroc_1_temp[0];
    citiroc2_temp = (tmtc_buffer->citiroc_2_temp[1] << 8) |  tmtc_buffer->citiroc_2_temp[0];

    // recover 2 bytes, unsign
    input_v = ( ((tmtc_buffer->input_i >> 4) << 8) | ((tmtc_buffer->input_i << 4) | (tmtc_buffer->input_i_v >> 4)) );
    input_i = ( ((tmtc_buffer->input_v >> 4) << 8) | ((tmtc_buffer->input_v << 4) | (tmtc_buffer->input_i_v & 0x0F)) );
    hv_input_v = ( ((tmtc_buffer->hv_input_i >> 4) << 8) | ((tmtc_buffer->hv_input_i << 4) | (tmtc_buffer->hv_input_i_v >> 4)) );
    hv_input_i = ( ((tmtc_buffer->hv_input_v >> 4) << 8) | ((tmtc_buffer->hv_input_v << 4) | (tmtc_buffer->hv_input_i_v & 0x0F)) );

    fprintf(tmtc_slave_output_file, "%X%X", tmtc_buffer->head[0], tmtc_buffer->head[1]); // head
    fprintf(tmtc_slave_output_file, \
    ";%u;%u;%u;%u; \
    %u;%u;%u;%u;%u;%u; \
    %i;%u;%i; \
    %i;%i;%i;%i;%i;%i", \
    tmtc_buffer->gtm_id, tmtc_buffer->packet_counter, tmtc_buffer->data_length_msb, tmtc_buffer->data_length_120_byte, \
    time_buffer->year, time_buffer->day, time_buffer->hour, time_buffer->minute, time_buffer->sec, time_buffer->sub_sec, \
    tmtc_buffer->gtm_id_in_pps_counter, tmtc_buffer->pps_counter, fine_counter, \
    tmtc_buffer->board_temp_1, tmtc_buffer->board_temp_2, citiroc1_temp, citiroc2_temp, citiroc1_livetime_busy, citiroc2_livetime_busy);    
    for (i = 0; i < 32; ++i) {
        fprintf(tmtc_slave_output_file, ";%u", tmtc_buffer->citiroc_1_hit[i]);
    }
    for (i = 0; i < 32; ++i) {
        fprintf(tmtc_slave_output_file, ";%u", tmtc_buffer->citiroc_2_hit[i]);
    }
    fprintf(tmtc_slave_output_file, \
    ";%u;%u;%u;%u;%u;\
    %u;%u;%i;%u;%u;%i;\
    %u;%u;%u", \
    tmtc_buffer->citiroc_1_trigger_counter, tmtc_buffer->citiroc_2_trigger_counter, tmtc_buffer->counter_period, tmtc_buffer->hv_dac_1, tmtc_buffer->hv_dac_2, \
    input_v, input_i, tmtc_buffer->i_monitor_u22_temp, hv_input_v, hv_input_i, tmtc_buffer->i_monitor_u21_temp, \
    tmtc_buffer->cmd_recv_checksum, tmtc_buffer->cmd_calc_checksum, tmtc_buffer->cmd_recv_number);    
    for (i = 0; i < 5; ++i) {
        fprintf(tmtc_slave_output_file, ";%u", tmtc_buffer->tmtc_empty[i]);
    }
    fprintf(tmtc_slave_output_file, ";%i;%i;%u", citiroc1_livetime_buffer_busy, citiroc2_livetime_buffer_busy, tmtc_buffer->checksum);
    fprintf(tmtc_slave_output_file, ";%X%X\n", tmtc_buffer->tail[0], tmtc_buffer->tail[1]); // tail
}

/// parse_tmtc_data_end ///

/// parse_science_data ///

int find_next_sd_header(unsigned char *Buffer, size_t CurrentSdHeaderLocation, size_t ActualBufferSize) {
    size_t location;

    // quick check
    location = CurrentSdHeaderLocation + SCIENCE_HEADER_SIZE + SCIENCE_DATA_SIZE;
    if (location <= ActualBufferSize - SCIENCE_HEADER_SIZE) {
        if (is_sd_header(Buffer + location)) {
            return location;
        }
    }
    // remaining buffer isn't large enough to contain a science packet
    else {
        return -1;
    }

    // the remaining buffer is large enough but science header doesn't appear is the correct position, try to find forward from old science data header
    for (location = CurrentSdHeaderLocation + SCIENCE_HEADER_SIZE; location <= ActualBufferSize - SCIENCE_HEADER_SIZE; location++) {
        if (is_sd_header(Buffer + location)) {
            return location;
        }
    }

    // no next sd header is found
    return -1;
}

// since sd header's head has some prob in current test data, reduce some matching pattern
int is_sd_header(unsigned char *Target) {
    static unsigned char target_copy[SCIENCE_HEADER_SIZE];
    static unsigned char ref_master[2] = {0x88, 0x55};
    static unsigned char ref_slave[2] = {0x88, 0xAA};

    // mask the sequence count byte
    memcpy(target_copy, Target, SCIENCE_HEADER_SIZE);
    target_copy[3] = 0x00;

    if (!memcmp(target_copy, ref_master, 2)) {
        event_buffer->gtm_module = 0;
        return 1;
    }
    else if (!memcmp(target_copy, ref_slave, 2)) {
        event_buffer->gtm_module = 1;
        return 1;
    }
    else {
        return 0;
    }
}

// sync data is 3 * 15 bytes, which may be splitted by master/slave switch
// need to deal with sync data by separating it to master and slave cases
void parse_science_packet(unsigned char *Buffer, size_t MaxLocation) {
    int i;
    unsigned char *current_location;

    unsigned char sync_module_buffer = 0x00;

    // parse data based on word (3 bytes)
    for (i = 0; i < MaxLocation / 3; ++i) {
        current_location = Buffer + 3 * i;

        // separate master and slave cases
        if (event_buffer->gtm_module == 0) {

            // always look for sync data header
            if (is_sync_header(current_location)) {
                memcpy(&sync_module_buffer, current_location + 1, 1);
                if ((sync_module_buffer & 0x80) == 0x00) {
                    missing_sync_data_master = 1;
                    sync_data_buffer_master_counter = 0;
                    memcpy(sync_data_buffer_master, current_location, 3);
                    continue;
                }
            }

            if (missing_sync_data_master) {
                sync_data_buffer_master_counter += 3;
                memcpy(&sync_data_buffer_master[sync_data_buffer_master_counter], current_location, 3);
                // the tail of the sync data
                if (sync_data_buffer_master_counter == 42) {
                    if (is_sync_tail(sync_data_buffer_master + 42)) {
                        missing_sync_data_master = 0;
                        got_first_sync_data_master = 1;
                        sync_data_buffer_master_counter += 3;

                        // log_message("update sync_data_buffer_master");
                        parse_sync_data(sync_data_buffer_master);
                    }
                    // if the tail is missing, keep finding the next sync data header
                    else {
                        missing_sync_data_master = 0;
                        got_first_sync_data_master = 0;
                        sync_data_buffer_master_counter = 0;
                    }
                }
            }
            else if (got_first_sync_data_master) {
                parse_event_data(current_location);
            }
        }
        else {

            // always look for sync data header
            if (is_sync_header(current_location)) {
                memcpy(&sync_module_buffer, current_location + 1, 1);
                if ((sync_module_buffer & 0x80) == 0x80) {
                    missing_sync_data_slave = 1;
                    sync_data_buffer_slave_counter = 0;
                    memcpy(sync_data_buffer_slave, current_location, 3);
                    continue;
                }
            }

            if (missing_sync_data_slave) {
                sync_data_buffer_slave_counter += 3;
                memcpy(&sync_data_buffer_slave[sync_data_buffer_slave_counter], current_location, 3);
                // the tail of the sync data
                if (sync_data_buffer_slave_counter == 42) {
                    if (is_sync_tail(sync_data_buffer_slave + 42)) {
                        missing_sync_data_slave = 0;
                        got_first_sync_data_slave = 1;
                        sync_data_buffer_slave_counter += 3;

                        // log_message("update sync_data_buffer_slave");
                        parse_sync_data(sync_data_buffer_slave);
                    }
                    // if the tail is missing, keep finding the next sync data header
                    else {
                        missing_sync_data_slave = 0;
                        got_first_sync_data_slave = 0;
                        sync_data_buffer_slave_counter = 0;
                    }
                }
            }
            else if (got_first_sync_data_slave) {
                parse_event_data(current_location);
            }
        }
    }
}

static int is_sync_header(unsigned char *Target) {
    static unsigned char ref = 0xCA;

    return (*Target == ref);
}

static int is_sync_tail(unsigned char *Target) {
    static unsigned char ref[3] = {0xF2, 0xF5, 0xFA};

    return (!memcmp(Target, ref, 3));
}

///// parse science sync data /////

static void parse_sync_data(unsigned char *Target) {
    unsigned char buffer[2];
    Time time_before;

    // time_buffer->fine_counter = 0;
    // separate master and slave cases
    if (event_buffer->gtm_module == 0) {
        time_buffer->fine_counter_master = 0;
        // pps count
        memcpy(buffer, Target + 1, 2);
        buffer[0] = buffer[0] & 0x7F; // mask gtm module
        big2little_endian(buffer, 2);
        memcpy(&(event_buffer->pps_counter_master), buffer, 2);
        event_buffer->pps_counter = event_buffer->pps_counter_master;
    }
    else {
        time_buffer->fine_counter_slave = 0;
        // pps count
        memcpy(buffer, Target + 1, 2);
        buffer[0] = buffer[0] & 0x7F; // mask gtm module
        big2little_endian(buffer, 2);
        memcpy(&(event_buffer->pps_counter_slave), buffer, 2);
        event_buffer->pps_counter = event_buffer->pps_counter_slave;
    }

    // need cheching!!!
    // CMD-SAD sequence number
    memcpy(&(event_buffer->cmd_seq_num), Target + 3, 1);
    // UTC
    memcpy(&time_before, time_buffer, sizeof(Time));
    parse_utc_time_sync(Target + 4);
    // log_message("day %u, hour %u, min %u, sec %f", time_buffer->day, time_buffer->hour, time_buffer->minute, time_buffer->sec);
    //  ECI position stuff
    parse_position(Target + 10);

    time_buffer->pps_counter++; // ???
    // if UTC update, reset out own pps
    if (!compare_UTC(&time_before, time_buffer))
    {
        // printf("%5u;%3u;%3u;%5u;%3u;%3u;%3u;%3u\n", time_before.year, time_before.month, time_before.mday, time_before.day, time_before.hour, time_before.minute, time_before.sec, time_before.sub_sec);
        // printf("%5u;%3u;%3u;%5u;%3u;%3u;%3u;%3u\n", time_buffer->year, time_buffer->month, time_buffer->mday, time_buffer->day, time_buffer->hour, time_buffer->minute, time_buffer->sec, time_buffer->sub_sec);
        // printf("\n");
        time_buffer->pps_counter_base = time_buffer->pps_counter; // ???
    }

    write_sync_data();
}

void big2little_endian(void *Target, size_t TargetSize) {
    unsigned char *buffer = NULL;
    size_t i;

    buffer = (unsigned char *)malloc(TargetSize);
    for (i = 0; i < TargetSize; ++i) {
        buffer[i] = ((unsigned char *)Target)[TargetSize - 1 - i];
    }

    memcpy(Target, buffer, TargetSize);
    free(buffer);
}

// should be wrote later when the format is clear, it's a place holder now
void parse_utc_time_sync(unsigned char *Target) {
    // year
    time_buffer->year = 2022;
    // day
    memcpy(&(time_buffer->day), Target, 2);
    big2little_endian(&(time_buffer->day), 2);
    // hour
    memcpy(&(time_buffer->hour), Target + 2, 1);
    // minute
    memcpy(&(time_buffer->minute), Target + 3, 1);
    // sec
    memcpy(&(time_buffer->sec), Target + 4, 1);
    // sub sec (ms)
    memcpy(&(time_buffer->sub_sec), Target + 5, 1);

    return;
}

void parse_position(unsigned char *Target) {
    memcpy(&(position_buffer->x), Target, 4);
    memcpy(&(position_buffer->y), Target + 4, 4);
    memcpy(&(position_buffer->z), Target + 8, 4);
    memcpy(&(position_buffer->x_velocity), Target + 12, 4);
    memcpy(&(position_buffer->y_velocity), Target + 16, 4);
    memcpy(&(position_buffer->z_velocity), Target + 20, 4);
    memcpy(&(position_buffer->quaternion1), Target + 24, 2);
    memcpy(&(position_buffer->quaternion2), Target + 26, 2);
    memcpy(&(position_buffer->quaternion3), Target + 28, 2);
    memcpy(&(position_buffer->quaternion4), Target + 30, 2);
}

int compare_UTC(Time *Time1, Time *Time2) {
    return (Time1->year == Time2->year && Time1->month == Time2->month && Time1->mday == Time2->mday && Time1->day == Time2->day && Time1->hour == Time2->hour && Time1->minute == Time2->minute && Time1->sec == Time2->sec && Time1->sub_sec == Time2->sub_sec);
}

static void write_sync_data(void) {
    if (export_mode == 1 || export_mode == 3) {
        fprintf(raw_output_file, "sync: %5u, %3u\n", event_buffer->pps_counter, event_buffer->cmd_seq_num);
    }
}

void get_month_and_mday(void) {
    struct tm time_old, *time_new = NULL;
    time_t loctime;

    time_old.tm_sec = 0;
    time_old.tm_min = 0;
    time_old.tm_hour = 0;
    time_old.tm_mday = (int)time_buffer->day;
    time_old.tm_mon = 1;
    time_old.tm_year = (int)time_buffer->year - 1900; // tm struct start from 1900
    time_old.tm_wday = 0;
    time_old.tm_yday = 0;
    time_old.tm_isdst = 0;

    loctime = mktime(&time_old);
    time_new = localtime(&loctime);
    if (!time_new)
    {
        log_error("NULL time_new in get_month_and_mday");
    }
    time_buffer->month = (uint8_t)time_new->tm_mon;
    time_buffer->mday = (uint8_t)time_new->tm_mday;
}

double find_time_delta(Time *TimeStart, Time *TimeEnd) {
    double del_sec = 0;
    del_sec += (TimeEnd->year - TimeStart->year) * 31536000;
    del_sec += (TimeEnd->day - TimeStart->day) * 86400;
    del_sec += (TimeEnd->hour - TimeStart->hour) * 3600;
    del_sec += (TimeEnd->minute - TimeStart->minute) * 60;
    del_sec += (calc_sec(TimeEnd) - calc_sec(TimeStart));

    return del_sec;
}

double calc_sec(Time *Time) {
    double total_sec;

    total_sec = (double)Time->sec + ((double)Time->sub_sec) * 0.001 + (double)(Time->pps_counter - Time->pps_counter_base) + ((double)Time->fine_counter) * 0.24 * 0.000001;

    // deal with pps counter reset
    if (Time->pps_counter_base > Time->pps_counter) {
        total_sec += pow(2, 15);
    }

    return total_sec;
}

///// parse science event data /////

static void parse_event_data(unsigned char *Target) {
    unsigned char buffer[4] = {0x00, 0x00, 0x00, 0x00};

    if ((*Target & 0xC0) == 0x80) {
        // event time debug info
        memcpy(&buffer[0], Target, 1);
        buffer[0] = buffer[0] >> 2; // keep header and buffer ID
        buffer[0] = buffer[0] & 0x0F; // keep buffer ID
        memcpy(&(event_buffer->event_time_buffer_id), &buffer[0], 1);

        buffer[0] = 0x00; // reset
        // event time data
        memcpy(&buffer[1], Target, 3);
        buffer[1] = buffer[1] & 0x03; // mask the header & buffer ID
        big2little_endian(buffer, 4);

        memcpy(&(event_buffer->fine_counter), buffer, 4);

        // separate master and slave cases
        if (event_buffer->gtm_module == 0) {
            event_buffer->fine_counter_master = event_buffer->fine_counter;
            if (event_buffer->fine_counter < time_buffer->fine_counter_master) {
                log_message("fine_counter_master reset, old = %8u, new = %8u", time_buffer->fine_counter_master, event_buffer->fine_counter);
                // got_first_sync_data = 0; // current is useless!!!
            }
            memcpy(&(time_buffer->fine_counter_master), buffer, 4);
        }
        else {
            event_buffer->fine_counter_slave = event_buffer->fine_counter;
            if (event_buffer->fine_counter < time_buffer->fine_counter_slave) {
                log_message("fine_counter_slave reset, old = %8u, new = %8u", time_buffer->fine_counter_slave, event_buffer->fine_counter);
                // got_first_sync_data = 0; // current is useless!!!
            }
            memcpy(&(time_buffer->fine_counter_slave), buffer, 4);
        }

        write_event_time();
        return;
    }

    if ((*Target & 0xC0) == 0x40) {
            parse_event_adc(Target);
        }
}

static void write_event_time(void) {
    if (export_mode == 1 || export_mode == 3) {
        fprintf(raw_output_file, "event time: %10u;%3u\n", event_buffer->fine_counter, event_buffer->event_time_buffer_id);
    }
}

static void parse_event_adc(unsigned char *Target) {
    unsigned char buffer[3] = {0x00, 0x00, 0x00};
    unsigned char adc_buffer[2];
    int16_t adc_temp;

    event_buffer->if_hit = ((*Target & 0x40) == 0x40);
    event_buffer->gtm_module = (*Target & 0x20) ? SLAVE : MASTER;
    event_buffer->citiroc_id = (*Target & 0x10) ? 1 : 0;
    event_buffer->energy_filter = (*(Target + 1) & 0x40) ? 1 : 0;

    // read channel id, it's spilt between bytes
    memcpy(buffer, Target, 3);
    left_shift_mem(buffer, 3, 4);
    buffer[0] = buffer[0] >> 3;
    memcpy(&(event_buffer->channel_id), buffer, 1);

    // read adc value
    memcpy(adc_buffer, Target + 1, 2);
    adc_temp = ( ((adc_buffer[0] & 0x3F) << 8) | (adc_buffer[1]) );
    if (adc_temp > 0x2AF8) { // 5500*2
        adc_temp = adc_temp | 0xC000; // 11...
    }
    memcpy(&(event_buffer->adc_value), &adc_temp, 2);

    // update_energy_from_adc();

    write_event_buffer();

    return;
}

// shift the array n bits left, you should make sure 0<=bits<=7
void left_shift_mem(unsigned char *Target, size_t TargetSize, uint8_t Bits) {
    unsigned char current, next;
    size_t i;

    for (i = 0; i < TargetSize - 1; ++i) {
        current = Target[i];
        next = Target[i + 1];
        Target[i] = (current << Bits) | (next >> (8 - Bits));
    }
    // shift the last element
    Target[TargetSize - 1] = Target[TargetSize - 1] << Bits;
}

static void write_event_buffer(void) {
    static char detector_name[2][2][2][3] = {{{"PN\0", "PB\0"}, {"PT\0", "PP\0"}}, {{"NP\0", "NB\0"}, {"NT\0", "NN\0"}}};

    if (export_mode == 1 || export_mode == 3) {
        fprintf(raw_output_file, "event adc: ");
        
        // // weird!!!
        // fprintf(raw_outfile, "%1u;%5u;%10u;%1u;%1u;%3u;%1u;%5i\n", event_buffer->if_hit, event_buffer->pps_counter, event_buffer->fine_counter, event_buffer->gtm_module, event_buffer->citiroc_id, event_buffer->channel_id, event_buffer->energy_filter, event_buffer->adc_value);
        
        // // temporary output for realtime plotting
        // fprintf(raw_adc_only_outfile, "%u;%u;%u;%u;%i\n", event_buffer->gtm_module, event_buffer->citiroc_id, event_buffer->channel_id, event_buffer->energy_filter, event_buffer->adc_value);

        // separate master and slave cases
        if (event_buffer->gtm_module == 0) {
            fprintf(raw_output_file, "%1u;%5u;%10u;%1u;%1u;%3u;%1u;%5i\n", event_buffer->if_hit, event_buffer->pps_counter_master, event_buffer->fine_counter_master, event_buffer->gtm_module, event_buffer->citiroc_id, event_buffer->channel_id, event_buffer->energy_filter, event_buffer->adc_value);
        }
        else {
            fprintf(raw_output_file, "%1u;%5u;%10u;%1u;%1u;%3u;%1u;%5i\n", event_buffer->if_hit, event_buffer->pps_counter_slave, event_buffer->fine_counter_slave, event_buffer->gtm_module, event_buffer->citiroc_id, event_buffer->channel_id, event_buffer->energy_filter, event_buffer->adc_value);
        }
    }
    if (export_mode == 2 || export_mode == 3) {
        // separate master and slave cases
        if (event_buffer->gtm_module == 0) {
            fprintf(science_pipeline_output_file, "%u;%i;%i;%u;%u;%u;%i\n", event_buffer->gtm_module, event_buffer->pps_counter_master, event_buffer->fine_counter_master, event_buffer->citiroc_id, event_buffer->channel_id, event_buffer->energy_filter, event_buffer->adc_value);
        }
        else {
            fprintf(science_pipeline_output_file, "%u;%i;%i;%u;%u;%u;%i\n", event_buffer->gtm_module, event_buffer->pps_counter_slave, event_buffer->fine_counter_slave, event_buffer->citiroc_id, event_buffer->channel_id, event_buffer->energy_filter, event_buffer->adc_value);
        }
    }
}

/// back to parse science data ///

void parse_sd_header(unsigned char *Target) {
    // static int got_first_sd_header = 0;
    unsigned char new_gtm_module = 0x00;
    uint8_t new_sequence_count;

    memcpy(&new_gtm_module, Target + 1, 1);
    if (new_gtm_module == 0x55) {
        event_buffer->gtm_module = 0;
    }
    else {
        event_buffer->gtm_module = 1;
    }

    // parse sequence count and check packet continuity
    memcpy(&new_sequence_count, Target + 3, 1);

    write_sd_header(new_sequence_count);

    if (!got_first_sd_header) {
        sequence_count = new_sequence_count;
        got_first_sd_header = 1;
        return;
    }
    // make sure the sequence count is continuous
    if (sequence_count == 255) {
        continuous_packet = (new_sequence_count == 0);
    }
    else {
        continuous_packet = (new_sequence_count == sequence_count + 1);
    }

    if (!continuous_packet) {
        log_message("sequence count not continuous, old sequence count = %i, new seqence count= %i", sequence_count, new_sequence_count);
    }

    sequence_count = new_sequence_count;
}

static void write_sd_header(uint8_t SequenceCount) {
    if (export_mode == 1 || export_mode == 3) {
        fprintf(raw_output_file, "sd header: %3u\n", SequenceCount);
    }
}

void free_got_first_sd_header() {
    got_first_sd_header = 0;
}

/// parse_science_data_end ///

//* function_end *//
