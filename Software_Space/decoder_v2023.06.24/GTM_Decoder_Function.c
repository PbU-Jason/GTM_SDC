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

/// main_end ///

/// create_basic_buffer ///

// for input binary
size_t max_input_binary_buffer_size = 1174405120; // 1 GB
unsigned char *input_binary_buffer  = NULL; // tmtc and science shared

/// create_basic_buffer_end ///

/// open_all_file ///

FILE *input_binary_file = NULL;

/// open_all_file_end ///

//* define_global_variable_end *//



//* local_variable *//

/// create_basic_buffer ///

// for typedef struct
UTC *utc_buffer         = NULL; // tmtc and science shared
TMTC *tmtc_buffer       = NULL;
Science *science_buffer = NULL;

/// create_basic_buffer_end ///

/// open_all_file ///

FILE *raw_output_file              = NULL; // tmtc and science shared
FILE *tmtc_master_output_file      = NULL;
FILE *tmtc_slave_output_file       = NULL;
FILE *science_pipeline_output_file = NULL;

char tmtc_csv_header_all[] = "Bytes 0;Bytes 1;Bytes 2;Bytes 3;Bytes 4;Bytes 5;Bytes 6;Bytes 7;Bytes 8;Bytes 9;Bytes 10;Bytes 11;Bytes 12;Bytes 13;Bytes 14;Bytes 15;Bytes 16;Bytes 17;Bytes 18;Bytes 19;Bytes 20;Bytes 21;Bytes 22;Bytes 23;Bytes 24;Bytes 25;Bytes 26;Bytes 27;Bytes 28;Bytes 29;Bytes 30;Bytes 31;Bytes 32;Bytes 33;Bytes 34;Bytes 35;Bytes 36;Bytes 37;Bytes 38;Bytes 39;Bytes 40;Bytes 41;Bytes 42;Bytes 43;Bytes 44;Bytes 45;Bytes 46;Bytes 47;Bytes 48;Bytes 49;Bytes 50;Bytes 51;Bytes 52;Bytes 53;Bytes 54;Bytes 55;Bytes 56;Bytes 57;Bytes 58;Bytes 59;Bytes 60;Bytes 61;Bytes 62;Bytes 63;Bytes 64;Bytes 65;Bytes 66;Bytes 67;Bytes 68;Bytes 69;Bytes 70;Bytes 71;Bytes 72;Bytes 73;Bytes 74;Bytes 75;Bytes 76;Bytes 77;Bytes 78;Bytes 79;Bytes 80;Bytes 81;Bytes 82;Bytes 83;Bytes 84;Bytes 85;Bytes 86;Bytes 87;Bytes 88;Bytes 89;Bytes 90;Bytes 91;Bytes 92;Bytes 93;Bytes 94;Bytes 95;Bytes 96;Bytes 97;Bytes 98;Bytes 99;Bytes 100;Bytes 101;Bytes 102;Bytes 103;Bytes 104;Bytes 105;Bytes 106;Bytes 107;Bytes 108;Bytes 109;Bytes 110;Bytes 111;Bytes 112;Bytes 113;Bytes 114;Bytes 115;Bytes 116;Bytes 117;Bytes 118;Bytes 119;Bytes 120;Bytes 121;Bytes 122;Bytes 123;Bytes 124;Bytes 125;Bytes 126;Bytes 127\n";
char tmtc_csv_header_master[] = "Header;GTM ID;Packet Counter;Data Length (MSB);Data Length;UTC Year;UTC Day;UTC Hour;UTC Minute;UTC Second;UTC Subsecond;GTM ID in Lastest PPS Counter;Lastest PPS Counter;Lastest Fine Time Counter Value Between 2 PPSs;Board Temperature#1;Board Temperature#2;CITIROC1 Temperature;CITIROC2 Temperature;CITIROC1 Live Time (Busy);CITIROC2 Live Time (Busy);CITIROC1 Hit Counter#0;CITIROC1 Hit Counter#1;CITIROC1 Hit Counter#2;CITIROC1 Hit Counter#3;CITIROC1 Hit Counter#4;CITIROC1 Hit Counter#5;CITIROC1 Hit Counter#6;CITIROC1 Hit Counter#7;CITIROC1 Hit Counter#8;CITIROC1 Hit Counter#9;CITIROC1 Hit Counter#10;CITIROC1 Hit Counter#11;CITIROC1 Hit Counter#12;CITIROC1 Hit Counter#13;CITIROC1 Hit Counter#14;CITIROC1 Hit Counter#15;CITIROC1 Hit Counter#16;CITIROC1 Hit Counter#17;CITIROC1 Hit Counter#18;CITIROC1 Hit Counter#19;CITIROC1 Hit Counter#20;CITIROC1 Hit Counter#21;CITIROC1 Hit Counter#22;CITIROC1 Hit Counter#23;CITIROC1 Hit Counter#24;CITIROC1 Hit Counter#25;CITIROC1 Hit Counter#26;CITIROC1 Hit Counter#27;CITIROC1 Hit Counter#28;CITIROC1 Hit Counter#29;CITIROC1 Hit Counter#30;CITIROC1 Hit Counter#31;CITIROC2 Hit Counter#0;CITIROC2 Hit Counter#1;CITIROC2 Hit Counter#2;CITIROC2 Hit Counter#3;CITIROC2 Hit Counter#4;CITIROC2 Hit Counter#5;CITIROC2 Hit Counter#6;CITIROC2 Hit Counter#7;CITIROC2 Hit Counter#8;CITIROC2 Hit Counter#9;CITIROC2 Hit Counter#10;CITIROC2 Hit Counter#11;CITIROC2 Hit Counter#12;CITIROC2 Hit Counter#13;CITIROC2 Hit Counter#14;CITIROC2 Hit Counter#15;CITIROC2 Hit Counter#16;CITIROC2 Hit Counter#17;CITIROC2 Hit Counter#18;CITIROC2 Hit Counter#19;CITIROC2 Hit Counter#20;CITIROC2 Hit Counter#21;CITIROC2 Hit Counter#22;CITIROC2 Hit Counter#23;CITIROC2 Hit Counter#24;CITIROC2 Hit Counter#25;CITIROC2 Hit Counter#26;CITIROC2 Hit Counter#27;CITIROC2 Hit Counter#28;CITIROC2 Hit Counter#29;CITIROC2 Hit Counter#30;CITIROC2 Hit Counter#31;CITIROC1 Trigger Counter;CITIROC2 Trigger Counter;Counter Period Setting;HV DAC1;HV DAC2;SPW#A Error Count;SPW#A Last Recv Byte;SPW#B Error Count;SPW#B Last Recv Byte;SPW#A Status;SPW#B Status;Recv Checksum of Last CMD;Calc Checksum of Last CMD;Number of Recv CMDs;Bytes 114;Bytes 115;Bytes 116;Bytes 117;Bytes 118;CITIROC1 Live Time (Buffer+Busy);CITIROC2 Live Time (Buffer+Busy);Checksum;Tail\n";
char tmtc_csv_header_slave[] = "Header;GTM ID;Packet Counter;Data Length (MSB);Data Length;UTC Year;UTC Day;UTC Hour;UTC Minute;UTC Second;UTC Subsecond;GTM ID in Lastest PPS Counter;Lastest PPS Counter;Lastest Fine Time Counter Value Between 2 PPSs;Board Temperature#1;Board Temperature#2;CITIROC1 Temperature;CITIROC2 Temperature;CITIROC1 Live Time (Busy);CITIROC2 Live Time (Busy);CITIROC1 Hit Counter#0;CITIROC1 Hit Counter#1;CITIROC1 Hit Counter#2;CITIROC1 Hit Counter#3;CITIROC1 Hit Counter#4;CITIROC1 Hit Counter#5;CITIROC1 Hit Counter#6;CITIROC1 Hit Counter#7;CITIROC1 Hit Counter#8;CITIROC1 Hit Counter#9;CITIROC1 Hit Counter#10;CITIROC1 Hit Counter#11;CITIROC1 Hit Counter#12;CITIROC1 Hit Counter#13;CITIROC1 Hit Counter#14;CITIROC1 Hit Counter#15;CITIROC1 Hit Counter#16;CITIROC1 Hit Counter#17;CITIROC1 Hit Counter#18;CITIROC1 Hit Counter#19;CITIROC1 Hit Counter#20;CITIROC1 Hit Counter#21;CITIROC1 Hit Counter#22;CITIROC1 Hit Counter#23;CITIROC1 Hit Counter#24;CITIROC1 Hit Counter#25;CITIROC1 Hit Counter#26;CITIROC1 Hit Counter#27;CITIROC1 Hit Counter#28;CITIROC1 Hit Counter#29;CITIROC1 Hit Counter#30;CITIROC1 Hit Counter#31;CITIROC2 Hit Counter#0;CITIROC2 Hit Counter#1;CITIROC2 Hit Counter#2;CITIROC2 Hit Counter#3;CITIROC2 Hit Counter#4;CITIROC2 Hit Counter#5;CITIROC2 Hit Counter#6;CITIROC2 Hit Counter#7;CITIROC2 Hit Counter#8;CITIROC2 Hit Counter#9;CITIROC2 Hit Counter#10;CITIROC2 Hit Counter#11;CITIROC2 Hit Counter#12;CITIROC2 Hit Counter#13;CITIROC2 Hit Counter#14;CITIROC2 Hit Counter#15;CITIROC2 Hit Counter#16;CITIROC2 Hit Counter#17;CITIROC2 Hit Counter#18;CITIROC2 Hit Counter#19;CITIROC2 Hit Counter#20;CITIROC2 Hit Counter#21;CITIROC2 Hit Counter#22;CITIROC2 Hit Counter#23;CITIROC2 Hit Counter#24;CITIROC2 Hit Counter#25;CITIROC2 Hit Counter#26;CITIROC2 Hit Counter#27;CITIROC2 Hit Counter#28;CITIROC2 Hit Counter#29;CITIROC2 Hit Counter#30;CITIROC2 Hit Counter#31;CITIROC1 Trigger Counter;CITIROC2 Trigger Counter;Counter Period Setting;HV DAC1;HV DAC2;Input Current Value;Input Voltage Value;Current Monitor Chip (U22) Temperature;HV Input Current Value;HV Input Voltage Value;Current Monitor Chip (U21) Temperature;Recv Checksum of Last CMD;Calc Checksum of Last CMD;Number of Recv CMDs;Bytes 114;Bytes 115;Bytes 116;Bytes 117;Bytes 118;CITIROC1 Live Time (Buffer+Busy);CITIROC2 Live Time (Buffer+Busy);Checksum;Tail\n";
char science_csv_pipeline_header[] = "Module;PPS;FineTime;CITIROC;Channel;Gain;ADC\n";

/// open_all_file_end ///

/// parse_science_packet ///

unsigned char *science_sync_master_buffer = NULL;
int science_sync_master_buffer_counter    = 0;
unsigned char *science_sync_slave_buffer  = NULL;
int science_sync_slave_buffer_counter     = 0;

int stop_find_sync_data_header_master_flag = 0; // 0 = don't stop; 1 = stop
int stop_find_sync_data_header_slave_flag  = 0;
int have_complete_sync_data_master_flag = 0; // 0 = have not; 1 = have
int have_complete_sync_data_slave_flag  = 0;

/// parse_science_packet_end ///

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
void initailize_sync_data_flag() { // for continuously decode
    int sync_data_buffer_master_counter = 0;
    int sync_data_buffer_slave_counter  = 0;

    int have_complete_sync_data_master_flag = 0; // 0 = have not; 1 = have
    int have_complete_sync_data_slave_flag  = 0;
    int sync_data_truncation_master_flag    = 0; // 0 = without truncation; 1 = without truncation
    int sync_data_truncation_slave_flag     = 0;
}

// checked~
void create_basic_buffer() {

    // dynamically allocate a single large block of memory with the specified size

    input_binary_buffer = (unsigned char *)malloc(max_input_binary_buffer_size);
    
    tmtc_buffer = (TMTC *)malloc(sizeof(TMTC));
    science_buffer = (Science *)malloc(sizeof(Science));
}

// checked~
void open_all_file(char *input_file_path) {
    char *raw_output_path; // tmtc and science shared
    char *tmtc_master_output_path;
    char *tmtc_slave_output_path;
    char *science_pipeline_output_path;
    
    // open input file
    input_binary_file = fopen(input_file_path, "rb");
    log_message("Successfully load input file");

    // open output file
    switch (decode_mode) {

        // decode tmtc data
        case 1:
            // master + slave
            raw_output_path = str_append(input_file_path, "_tmtc_all.csv");
            raw_output_file = fopen(raw_output_path, "a");
            if (ftell(raw_output_file) == 0) {
                fputs(tmtc_csv_header_all, raw_output_file);
            }
            free(raw_output_path);

            // only master
            tmtc_master_output_path = str_append(input_file_path, "_tmtc_master.csv");
            tmtc_master_output_file = fopen(tmtc_master_output_path, "a");
            if (ftell(tmtc_master_output_file) == 0) {
                fputs(tmtc_csv_header_master, tmtc_master_output_file);
            }
            free(tmtc_master_output_path);

            // only slave
            tmtc_slave_output_path = str_append(input_file_path, "_tmtc_slave.csv");
            tmtc_slave_output_file = fopen(tmtc_slave_output_path, "a");
            if (ftell(tmtc_slave_output_file) == 0) {
                fputs(tmtc_csv_header_slave, tmtc_slave_output_file);
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
                    fputs(science_csv_pipeline_header, science_pipeline_output_file);
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
                    fputs(science_csv_pipeline_header, science_pipeline_output_file);
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
    }
    log_message("Close all file");
}

// checked~
void destroy_basic_buffer() {
    // destroy input_binary_buffer independently

    free(tmtc_buffer);
    free(science_buffer);
}

/// main_end ///

/// parse_tmtc_data ///

// checked~
int is_tmtc_gicd_header(unsigned char *target) {
    unsigned char ref[2] = {0x08, 0x91};

    if (!memcmp(ref, target, 2)) {
        // if ref & target store the same info, memcmp will report 0
        // otherwise, it will report a number != 0

        return 1; // == true in c
    }

    return 0; // == flase in c
}

// checked~
int is_tmtc_icd_head(unsigned char *target) {
    unsigned char ref[2] = {0x55, 0xAA};

    if (!memcmp(ref, target, 2)) {
        return 1;
    }

    return 0;
}

// checked~
int is_tmtc_icd_tail(unsigned char *target) {
    unsigned char ref[2] = {0xFB, 0xF2};

    if (!memcmp(ref, target, 2)) {
        return 1;
    }

    return 0;
}

// checked~
void write_tmtc_raw_all(unsigned char *target) { 
    unsigned char byte_buffer[1];

    for (int i = 0; i < 128; i++) {
        memcpy(&(byte_buffer[0]), target+i, 1);
        fprintf(raw_output_file, "%d;", byte_buffer[0]);
        if (i == 127) {
            fprintf(raw_output_file, "\n");
        }
    }
}

// checked~
void parse_tmtc_packet(unsigned char *target) {
    int gtm_id_case;
    int tmtc_16_byte_shift = TMTC_PACKET_HEADER_SIZE+TMTC_DATA_FIELD_HEADER_SIZE;

    // sequence count from TASA
    *(target+TMTC_PACKET_ID_SIZE) = *(target+TMTC_PACKET_ID_SIZE) & 0x3F; // mask segmentation flag
    memcpy(tmtc_buffer->source_sequence_count, target+TMTC_PACKET_ID_SIZE, TMTC_PACKET_SEQUENCE_CONTROL_SIZE);
    simple_big2little_endian(&(tmtc_buffer->source_sequence_count), 2);

    // utc from TASA
    parse_tmtc_gicd_utc(target+TMTC_PACKET_HEADER_SIZE);

    // header
    memcpy(tmtc_buffer->header, target+tmtc_16_byte_shift, 2);

    // gtm id
    gtm_id_case = (*(target+tmtc_16_byte_shift+2) == 0x02) ? 0 : 1; // 0x02 = master = 0; 0x05 = slave = 1
    memcpy(&(tmtc_buffer->gtm_id), target+tmtc_16_byte_shift+2, 1);

    // packet counter
    memcpy(&(tmtc_buffer->packet_counter), target+tmtc_16_byte_shift+3, 2);
    simple_big2little_endian(&(tmtc_buffer->packet_counter), 2);

    // data length
    memcpy(&(tmtc_buffer->data_length_msb), target+tmtc_16_byte_shift+5, 1);
    memcpy(&(tmtc_buffer->data_length_120_byte), target+tmtc_16_byte_shift+6, 1);

    // utc
    parse_tmtc_gicd_utc(target+tmtc_16_byte_shift+7);

    // pps counter
    tmtc_buffer->gtm_id_in_pps_counter = ((*(target+tmtc_16_byte_shift+15) & 0x80) == 0x80) ? 1 : 0; // extract gtm id
    *(target+tmtc_16_byte_shift+15) = *(target+tmtc_16_byte_shift+15) & 0x7F; // mask gtm id
    memcpy(&(tmtc_buffer->pps_counter), target+tmtc_16_byte_shift+15, 2);
    simple_big2little_endian(&(tmtc_buffer->pps_counter), 2);

    // fine time counter (3 bytes, deal with when writting)
    memcpy(&(tmtc_buffer->fine_time_counter), target+tmtc_16_byte_shift+17, 3);

    // board temp (int8_t)
    memcpy(&(tmtc_buffer->board_temp_1), target+tmtc_16_byte_shift+20, 1);
    memcpy(&(tmtc_buffer->board_temp_2), target+tmtc_16_byte_shift+21, 1);

    // citiroc temp (definition is little-endian, and please notice unusual sign bit!)
    // (unusual 2 bytes, deal with when writting)

    memcpy(&(tmtc_buffer->citiroc_1_temp[0]), target+tmtc_16_byte_shift+22, 1);
    if ((*(target+tmtc_16_byte_shift+24) & 0x80) == 0x80) { // negtive case
        tmtc_buffer->citiroc_1_temp[1] = 0xC0 | ((*(target+tmtc_16_byte_shift+24) & 0x7E) >> 1);
        // 0x7E to mask bit 0 & 7
        // >> 1 to kill bit 0 and add new 0 at bit 7
        // 0xC0 | to trigger 2's complement 
    }
    else { // positive case
        tmtc_buffer->citiroc_1_temp[1] = 0x00 | ((*(target+tmtc_16_byte_shift+24) & 0x7E) >> 1);
    }

    memcpy(&(tmtc_buffer->citiroc_2_temp[0]), target+tmtc_16_byte_shift+23, 1);
    if ((*(target+tmtc_16_byte_shift+25) & 0x80) == 0x80) {
        tmtc_buffer->citiroc_2_temp[1] = 0xC0 | ((*(target+tmtc_16_byte_shift+25) & 0x7E) >> 1);
    }
    else {
        tmtc_buffer->citiroc_2_temp[1] = 0x00 | ((*(target+tmtc_16_byte_shift+25) & 0x7E) >> 1);
    }

    // citiroc livetime (3 bytes, deal with when writting)
    memcpy(&(tmtc_buffer->citiroc_1_livetime_busy), target+tmtc_16_byte_shift+26, 3); 
    memcpy(&(tmtc_buffer->citiroc_2_livetime_busy), target+tmtc_16_byte_shift+29, 3);
    
    // citiroc hit
    for (int i = 0; i < 32; ++i) {
        memcpy(&(tmtc_buffer->citiroc_1_hit_counter[i]), target+tmtc_16_byte_shift+32+i, 1);
        memcpy(&(tmtc_buffer->citiroc_2_hit_counter[i]), target+tmtc_16_byte_shift+64+i, 1);
    }
    // citiroc trigger counter
    memcpy(&(tmtc_buffer->citiroc_1_trigger_counter), target+tmtc_16_byte_shift+96, 2);
    simple_big2little_endian(&(tmtc_buffer->citiroc_1_trigger_counter), 2);
    memcpy(&(tmtc_buffer->citiroc_2_trigger_counter), target+tmtc_16_byte_shift+98, 2);
    simple_big2little_endian(&(tmtc_buffer->citiroc_2_trigger_counter), 2);

    // counter period
    memcpy(&(tmtc_buffer->counter_period), target+tmtc_16_byte_shift+100, 1);

    // hv dac
    memcpy(&(tmtc_buffer->hv_dac_1), target+tmtc_16_byte_shift+101, 1);
    memcpy(&(tmtc_buffer->hv_dac_2), target+tmtc_16_byte_shift+102, 1);

    if (gtm_id_case == 0) {
        // for master, spw
        memcpy(&(tmtc_buffer->spw_a_error_count), target+tmtc_16_byte_shift+103, 1);
        memcpy(&(tmtc_buffer->spw_a_last_recv_byte), target+tmtc_16_byte_shift+104, 1);
        memcpy(&(tmtc_buffer->spw_b_error_count), target+tmtc_16_byte_shift+105, 1);
        memcpy(&(tmtc_buffer->spw_b_last_recv_byte), target+tmtc_16_byte_shift+106, 1);
        memcpy(&(tmtc_buffer->spw_a_status), target+tmtc_16_byte_shift+107, 2);
        simple_big2little_endian(&(tmtc_buffer->spw_a_status), 2);
        memcpy(&(tmtc_buffer->spw_b_status), target+tmtc_16_byte_shift+109, 2);
        simple_big2little_endian(&(tmtc_buffer->spw_b_status), 2);
    }
    else if (gtm_id_case == 1) {
        // for slave, i & v monitor
        memcpy(&(tmtc_buffer->input_i), target+tmtc_16_byte_shift+103, 1);
        memcpy(&(tmtc_buffer->input_v), target+tmtc_16_byte_shift+104, 1);
        memcpy(&(tmtc_buffer->input_i_v), target+tmtc_16_byte_shift+105, 1);
        memcpy(&(tmtc_buffer->i_monitor_u22_temp), target+tmtc_16_byte_shift+106, 1); // (int8_t)
        memcpy(&(tmtc_buffer->hv_input_i), target+tmtc_16_byte_shift+107, 1);
        memcpy(&(tmtc_buffer->hv_input_v), target+tmtc_16_byte_shift+108, 1);
        memcpy(&(tmtc_buffer->hv_input_i_v), target+tmtc_16_byte_shift+109, 1);
        memcpy(&(tmtc_buffer->i_monitor_u21_temp), target+tmtc_16_byte_shift+110, 1); // (int8_t)
    }
    else {
        log_error("Please check tmtc GTM id!");
    }

    // cmd recv checksum
    memcpy(&(tmtc_buffer->cmd_recv_checksum), target+tmtc_16_byte_shift+111, 1);
    memcpy(&(tmtc_buffer->cmd_calc_checksum), target+tmtc_16_byte_shift+112, 1);

    // cmd recv number
    memcpy(&(tmtc_buffer->cmd_recv_number), target+tmtc_16_byte_shift+113, 1);

    // tmtc empty
    memcpy(&(tmtc_buffer->tmtc_empty), target+tmtc_16_byte_shift+114, 5);

    // citiroc livetime (3 bytes, deal with when writting)
    memcpy(&(tmtc_buffer->citiroc_1_livetime_buffer_busy), target+tmtc_16_byte_shift+119, 3); 
    memcpy(&(tmtc_buffer->citiroc_2_livetime_buffer_busy), target+tmtc_16_byte_shift+122, 3);

    // checksum
    memcpy(&(tmtc_buffer->checksum), target+tmtc_16_byte_shift+125, 1);

    // tail
    memcpy(tmtc_buffer->tail, target+tmtc_16_byte_shift+126, 2);

    // save tmtc_buffer
    write_tmtc_buffer_master_or_slave();
}

// checked~
void simple_big2little_endian(void *target, size_t reverse_size) {
    unsigned char *reverse_buffer;

    reverse_buffer = (unsigned char *)malloc(reverse_size);

    // reversely copy data from target to reverse_buffer
    for (size_t i = 0; i < reverse_size; i++) {
        reverse_buffer[i] = ((unsigned char *)target)[(reverse_size-1) - i];
    }

    // update target by reverse_buffer
    memcpy(target, reverse_buffer, reverse_size);

    free(reverse_buffer);
}

// checked~
void parse_tmtc_gicd_utc(unsigned char *target) {

    // year
    memcpy(&(tmtc_buffer->gicd_year), target, 2);
    simple_big2little_endian(&(tmtc_buffer->gicd_year), 2);

    // day of year
    memcpy(&(tmtc_buffer->gicd_day_of_year), target+2, 2);
    simple_big2little_endian(&(tmtc_buffer->gicd_day_of_year), 2);

    // hour
    memcpy(&(tmtc_buffer->gicd_hour), target+4, 1);

    // minute
    memcpy(&(tmtc_buffer->gicd_minute), target+5, 1);

    // second
    memcpy(&(tmtc_buffer->gicd_second), target+6, 1);

    // subsecond
    memcpy(&(tmtc_buffer->gicd_subsecond), target+7, 1);
}

// checked~
void parse_tmtc_icd_utc(unsigned char *target) {

    // year
    memcpy(&(tmtc_buffer->icd_year), target, 2);
    simple_big2little_endian(&(tmtc_buffer->icd_year), 2);

    // day of year
    memcpy(&(tmtc_buffer->icd_day_of_year), target+2, 2);
    simple_big2little_endian(&(tmtc_buffer->icd_day_of_year), 2);

    // hour
    memcpy(&(tmtc_buffer->icd_hour), target+4, 1);

    // minute
    memcpy(&(tmtc_buffer->icd_minute), target+5, 1);

    // second
    memcpy(&(tmtc_buffer->icd_second), target+6, 1);

    // subsecond
    memcpy(&(tmtc_buffer->icd_subsecond), target+7, 1);
}

// checked~
void write_tmtc_buffer_master_or_slave() {
    int gtm_id_case;

    int fine_time_counter;
    int citiroc_1_livetime_busy;
    int citiroc_2_livetime_busy;
    int citiroc_1_livetime_buffer_busy;
    int citiroc_2_livetime_buffer_busy;

    int16_t citiroc_1_temp;
    int16_t citiroc_2_temp;

    FILE *output_file;

    uint16_t input_i;
    uint16_t input_v;
    uint16_t hv_input_i;
    uint16_t hv_input_v;

    // gtm id
    gtm_id_case = (tmtc_buffer->gtm_id == 0x02) ? 0 : 1; // 0x02 = master = 0; 0x05 = slave = 1

    // recover 3 bytes
    fine_time_counter = (tmtc_buffer->fine_time_counter[0] << 16) | (tmtc_buffer->fine_time_counter[1] << 8) | tmtc_buffer->fine_time_counter[2];
    citiroc_1_livetime_busy = (tmtc_buffer->citiroc_1_livetime_busy[0] << 16) | (tmtc_buffer->citiroc_1_livetime_busy[1] << 8) | tmtc_buffer->citiroc_1_livetime_busy[2];
    citiroc_2_livetime_busy = (tmtc_buffer->citiroc_2_livetime_busy[0] << 16) | (tmtc_buffer->citiroc_2_livetime_busy[1] << 8) | tmtc_buffer->citiroc_2_livetime_busy[2];
    citiroc_1_livetime_buffer_busy = (tmtc_buffer->citiroc_1_livetime_buffer_busy[0] << 16) | (tmtc_buffer->citiroc_1_livetime_buffer_busy[1] << 8) | tmtc_buffer->citiroc_1_livetime_buffer_busy[2];
    citiroc_2_livetime_buffer_busy = (tmtc_buffer->citiroc_2_livetime_buffer_busy[0] << 16) | (tmtc_buffer->citiroc_2_livetime_buffer_busy[1] << 8) | tmtc_buffer->citiroc_2_livetime_buffer_busy[2];

    // recover citiroc_1_temp (int16_t, don't need to reverse index due to little endian)
    citiroc_1_temp = (tmtc_buffer->citiroc_1_temp[1] << 8) |  tmtc_buffer->citiroc_1_temp[0];
    citiroc_2_temp = (tmtc_buffer->citiroc_2_temp[1] << 8) |  tmtc_buffer->citiroc_2_temp[0];


    if (gtm_id_case == 0) {
        output_file = tmtc_master_output_file;
    }
    else {
        output_file = tmtc_slave_output_file;

        // recover i & v monitor
        input_i = ( ((tmtc_buffer->input_i >> 4) << 8) | ((tmtc_buffer->input_i << 4) | (tmtc_buffer->input_i_v >> 4)) );
        input_v = ( ((tmtc_buffer->input_v >> 4) << 8) | ((tmtc_buffer->input_v << 4) | (tmtc_buffer->input_i_v & 0x0F)) );
        hv_input_i = ( ((tmtc_buffer->hv_input_i >> 4) << 8) | ((tmtc_buffer->hv_input_i << 4) | (tmtc_buffer->hv_input_i_v >> 4)) );
        hv_input_v = ( ((tmtc_buffer->hv_input_v >> 4) << 8) | ((tmtc_buffer->hv_input_v << 4) | (tmtc_buffer->hv_input_i_v & 0x0F)) );
    }

    fprintf(output_file, "%X%X", tmtc_buffer->header[0], tmtc_buffer->header[1]); // head
    fprintf(output_file, \
    ";%u;%u;%u;%u \
    ;%u;%u;%u;%u;%u;%u \
    ;%i;%u;%i \
    ;%i;%i;%i;%i;%i;%i", \
    tmtc_buffer->gtm_id, tmtc_buffer->packet_counter, tmtc_buffer->data_length_msb, tmtc_buffer->data_length_120_byte, \
    utc_buffer->year, utc_buffer->day_of_year, utc_buffer->hour, utc_buffer->minute, utc_buffer->second, utc_buffer->subsecond, \
    tmtc_buffer->gtm_id_in_pps_counter, tmtc_buffer->pps_counter, fine_time_counter, \
    tmtc_buffer->board_temp_1, tmtc_buffer->board_temp_2, citiroc_1_temp, citiroc_2_temp, citiroc_1_livetime_busy, citiroc_2_livetime_busy);    
    
    for (int i = 0; i < 32; ++i) {
        fprintf(output_file, ";%u", tmtc_buffer->citiroc_1_hit_counter[i]);
    }
    for (int i = 0; i < 32; ++i) {
        fprintf(output_file, ";%u", tmtc_buffer->citiroc_2_hit_counter[i]);
    }

    fprintf(output_file, ";%u;%u;%u;%u;%u", \
    tmtc_buffer->citiroc_1_trigger_counter, tmtc_buffer->citiroc_2_trigger_counter, tmtc_buffer->counter_period, tmtc_buffer->hv_dac_1, tmtc_buffer->hv_dac_2);

    if (gtm_id_case == 0) {
        fprintf(output_file, ";%X;%X;%X;%X;%X;%X", \
        tmtc_buffer->spw_a_error_count, tmtc_buffer->spw_a_last_recv_byte, tmtc_buffer->spw_b_error_count, tmtc_buffer->spw_b_last_recv_byte, tmtc_buffer->spw_a_status, tmtc_buffer->spw_b_status);
    }
    else {
        fprintf(output_file, ";%u;%u;%i;%u;%u;%i", \
        input_v, input_i, tmtc_buffer->i_monitor_u22_temp, hv_input_v, hv_input_i, tmtc_buffer->i_monitor_u21_temp);
    }
    
    fprintf(output_file, ";%u;%u;%u", \
    tmtc_buffer->cmd_recv_checksum, tmtc_buffer->cmd_calc_checksum, tmtc_buffer->cmd_recv_number);
    
    for (int i = 0; i < 5; ++i) {
        fprintf(output_file, ";%u", tmtc_buffer->tmtc_empty[i]);
    }

    fprintf(output_file, ";%i;%i;%u", citiroc_1_livetime_buffer_busy, citiroc_2_livetime_buffer_busy, tmtc_buffer->checksum);
    fprintf(output_file, ";%X%X\n", tmtc_buffer->tail[0], tmtc_buffer->tail[1]); // tail
}

/// parse_tmtc_data_end ///

/// parse_science_data ///

// checked~
int is_science_gicd_marker(unsigned char *target) {
    unsigned char ref[SCIENCE_ATTACHED_SYNCHRO_MARKER_SIZE] = {0x1A, 0xCF, 0xFC, 0x1D};

    if (!memcmp(ref, target, SCIENCE_ATTACHED_SYNCHRO_MARKER_SIZE)) {
        return 1;
    }

    return 0;
}

// checked~
int is_science_icd_head(unsigned char *target) {
    unsigned char ref_master[2] = {0x88, 0x55};
    unsigned char ref_slave[2] = {0x88, 0xAA};

    if (!memcmp(target, ref_master, 2)) {
        science_buffer->gtm_id = 0;
        return 1;
    }
    else if (!memcmp(target, ref_slave, 2)) {
        science_buffer->gtm_id = 1;
        return 1;
    }
    else {
        return 0;
    }
}

// checked~
void parse_science_packet(unsigned char *target) {
    // 45 bytes sync data in 1104 bytes science data may be truncated since master/slave switch
    // need science_sync_master_buffer and science_sync_slave_buffer to temporarily keep sync info

    // move buffer pointer 3 bytes each time
    for (int i = 0; i < (SCIENCE_HEADER_SIZE+SCIENCE_DATA_SIZE)/3; i++) {
        
        // ignore SCIENCE_HEADER_SIZE
        if (i >= (SCIENCE_HEADER_SIZE)/3) {

            // separate master and slave cases
            if (science_buffer->gtm_id == 0) { // master case

                // always look for sync data header
                if (!stop_find_sync_data_header_master_flag) { // look for sync data header

                    // if find sync data header
                    if (is_sync_header(target+i)) {

                        // store 3 bytes to science_sync_master_buffer
                        memcpy(science_sync_master_buffer+science_sync_master_buffer_counter, target+i, 3);
                        science_sync_master_buffer_counter+=3;

                        // stop looking for sync data header and have uncomplete sync data 
                        stop_find_sync_data_header_master_flag = 1;
                        have_complete_sync_data_master_flag = 0;
                    }

                    // if no find sync data header and have complete sync data
                    if (have_complete_sync_data_master_flag) {

                        // parse 3 bytes event data
                        parse_event_data(target+i);
                    }
                }
                else { // stop looking for sync data header

                    // store 3 bytes to science_sync_master_buffer
                    memcpy(science_sync_master_buffer+science_sync_master_buffer_counter, target+i, 3);
                    science_sync_master_buffer_counter+=3;

                    // all 45 bytes have been stored in science_sync_master_buffer
                    if (science_sync_master_buffer_counter == 45) {

                        // check sync data tail
                        if (!is_sync_tail(science_sync_master_buffer+42)) {
                            log_error("Please check sync header defined in ICD!");
                        }

                        // look for sync data header and have complete sync data
                        stop_find_sync_data_header_master_flag = 0;
                        have_complete_sync_data_master_flag = 1;

                        // reset science_sync_master_buffer_counter
                        science_sync_master_buffer_counter = 0;

                        // parse 45 bytes sync data in science_sync_master_buffer
                        parse_science_sync_data(science_sync_master_buffer);
                    }
                }
            }
            else { // slave case

                // always look for sync data header
                if (!stop_find_sync_data_header_slave_flag) { // look for sync data header

                    // if find sync data header
                    if (is_sync_header(target+i)) {

                        // store 3 bytes to science_sync_slave_buffer
                        memcpy(science_sync_slave_buffer+science_sync_slave_buffer_counter, target+i, 3);
                        science_sync_slave_buffer_counter+=3;

                        // stop looking for sync data header and have uncomplete sync data 
                        stop_find_sync_data_header_slave_flag = 1;
                        have_complete_sync_data_slave_flag = 0;
                    }

                    // if no find sync data header and have complete sync data
                    if (have_complete_sync_data_slave_flag) {

                        // parse 3 bytes event data
                        parse_science_event_data(target+i);
                    }
                }
                else { // stop looking for sync data header

                    // store 3 bytes to science_sync_slave_buffer
                    memcpy(science_sync_slave_buffer+science_sync_slave_buffer_counter, target+i, 3);
                    science_sync_slave_buffer_counter+=3;

                    // all 45 bytes have been stored in science_sync_slave_buffer
                    if (science_sync_slave_buffer_counter == 45) {

                        // check sync data tail
                        if (!is_sync_tail(science_sync_slave_buffer+42)) {
                            log_error("Please check sync header defined in ICD!");
                        }

                        // look for sync data header and have complete sync data
                        stop_find_sync_data_header_slave_flag = 0;
                        have_complete_sync_data_slave_flag = 1;

                        // reset science_sync_slave_buffer_counter
                        science_sync_slave_buffer_counter = 0;

                        // parse 45 bytes sync data in science_sync_slave_buffer
                        parse_sync_data(science_sync_slave_buffer);
                    }
                }
            }
        }
    }
}

// checked~
int is_sync_header(unsigned char *target) {
    unsigned char ref = 0xCA;

    if (!memcmp(ref, target, 1)) {
        return 1;
    }

    return 0;
}

// checked~
int is_sync_tail(unsigned char *target) {
    unsigned char ref[3] = {0xF2, 0xF5, 0xFA};

    if (!memcmp(ref, target, 3)) {
        return 1;
    }

    return 0;
}

// checked~
void parse_science_sync_data(unsigned char *target) {
    unsigned char *first_byte_pointer;
    
    // redefine first byte pointer base on master ot slave
    if (science_buffer->gtm_id == 0) {
        first_byte_pointer = &(science_buffer->master_sync_header);
    }
    else {
        first_byte_pointer = &(science_buffer->slave_sync_header);
    }

    // header
    memcpy(first_byte_pointer, target, 1);

    // gtm id
    *(first_byte_pointer+4) = ((*(target+1) & 0x80) == 0x80) ? 1 : 0; // 0 = master; 1 = slave

    // pps counts
    *(target+1) = *(target+1) & 0x7F; // mask gtm id
    memcpy(first_byte_pointer+8, target+1, 2);
    simple_big2little_endian(first_byte_pointer+8, 2);

    // cmd sequence number
    memcpy(first_byte_pointer+10, target+3, 1);

    parse_science_sync_utc(target+4, first_byte_pointer);
    parse_science_sync_attitude(target+10, first_byte_pointer);

    // tail
    memcpy(first_byte_pointer+49, target+42, 3);

    write_science_sync_data();
}

// checked~
void parse_science_sync_utc(unsigned char *target, unsigned char *first_byte_pointer_in_sync_data) {
    unsigned char *first_byte_pointer_in_sync_utc;

    first_byte_pointer_in_sync_utc = first_byte_pointer_in_sync_data+11;
    // unsigned char [1] = 4 bytes
    // int = 4 bytes

    // day of year
    memcpy(first_byte_pointer_in_sync_utc, target, 2);
    simple_big2little_endian(first_byte_pointer_in_sync_utc, 2);

    // hour
    memcpy(first_byte_pointer_in_sync_utc+2, target+2, 1);

    // minute
    memcpy(first_byte_pointer_in_sync_utc+23, target+3, 1);

    // second
    memcpy(first_byte_pointer_in_sync_utc+4, target+4, 1);

    // subsecond
    memcpy(first_byte_pointer_in_sync_utc+5, target+5, 1);
}

// checked~
void parse_science_sync_attitude(unsigned char *target, unsigned char *first_byte_pointer_in_sync_data) {
    unsigned char *first_byte_pointer_in_sync_attitude;

    first_byte_pointer_in_sync_attitude = first_byte_pointer_in_sync_data+17;

    // x, y & z position
    memcpy(first_byte_pointer_in_sync_attitude, target, 4);
    simple_big2little_endian(first_byte_pointer_in_sync_attitude, 4);
    memcpy(first_byte_pointer_in_sync_attitude+4, target+4, 4);
    simple_big2little_endian(first_byte_pointer_in_sync_attitude+4, 4);
    memcpy(first_byte_pointer_in_sync_attitude+8, target+8, 4);
    simple_big2little_endian(first_byte_pointer_in_sync_attitude+8, 4);

    // x, y & z velocity
    memcpy(first_byte_pointer_in_sync_attitude+12, target+12, 4);
    simple_big2little_endian(first_byte_pointer_in_sync_attitude+12, 4);
    memcpy(first_byte_pointer_in_sync_attitude+16, target+16, 4);
    simple_big2little_endian(first_byte_pointer_in_sync_attitude+16, 4);
    memcpy(first_byte_pointer_in_sync_attitude+20, target+20, 4);
    simple_big2little_endian(first_byte_pointer_in_sync_attitude+20, 4);

    // quaternion
    memcpy(first_byte_pointer_in_sync_attitude+24, target+24, 2);
    simple_big2little_endian(first_byte_pointer_in_sync_attitude+24, 2);
    memcpy(first_byte_pointer_in_sync_attitude+26, target+26, 2);
    simple_big2little_endian(first_byte_pointer_in_sync_attitude+6, 2);
    memcpy(first_byte_pointer_in_sync_attitude+28, target+28, 2);
    simple_big2little_endian(first_byte_pointer_in_sync_attitude+28, 2);
    memcpy(first_byte_pointer_in_sync_attitude+30, target+30, 2);
    simple_big2little_endian(first_byte_pointer_in_sync_attitude+30, 2);
}

// waiting
void write_sync_data() {
    if (export_mode == 1 || export_mode == 3) {
        fprintf(raw_output_file, "sync: %5u, %3u\n", science_buffer->pps_counter, science_buffer->cmd_seq_num);
    }
}

// 
void parse_event_data(unsigned char *target) {
    unsigned char buffer[4] = {0x00, 0x00, 0x00, 0x00};

    if ((*target & 0xC0) == 0x80) {
        // event time debug info
        memcpy(&buffer[0], target, 1);
        buffer[0] = buffer[0] >> 2; // keep header and buffer ID
        buffer[0] = buffer[0] & 0x0F; // keep buffer ID
        memcpy(&(science_buffer->event_time_buffer_id), &buffer[0], 1);

        buffer[0] = 0x00; // reset
        // event time data
        memcpy(&buffer[1], target, 3);
        buffer[1] = buffer[1] & 0x03; // mask the header & buffer ID
        simple_big2little_endian(buffer, 4);

        memcpy(&(science_buffer->fine_counter), buffer, 4);

        // separate master and slave cases
        if (science_buffer->gtm_module == 0) {
            science_buffer->fine_counter_master = science_buffer->fine_counter;
            if (science_buffer->fine_counter < time_buffer->fine_counter_master) {
                log_message("fine_counter_master reset, old = %8u, new = %8u", time_buffer->fine_counter_master, science_buffer->fine_counter);
                // got_first_sync_data = 0; // current is useless!!!
            }
            memcpy(&(time_buffer->fine_counter_master), buffer, 4);
        }
        else {
            science_buffer->fine_counter_slave = science_buffer->fine_counter;
            if (science_buffer->fine_counter < time_buffer->fine_counter_slave) {
                log_message("fine_counter_slave reset, old = %8u, new = %8u", time_buffer->fine_counter_slave, science_buffer->fine_counter);
                // got_first_sync_data = 0; // current is useless!!!
            }
            memcpy(&(time_buffer->fine_counter_slave), buffer, 4);
        }

        write_event_time();
        return;
    }

    if ((*target & 0xC0) == 0x40) {
            parse_event_adc(target);
        }
}

// waiting
void write_event_time(void) {
    if (export_mode == 1 || export_mode == 3) {
        fprintf(raw_output_file, "event time: %10u;%3u\n", science_buffer->fine_counter, science_buffer->event_time_buffer_id);
    }
}

void parse_event_adc(unsigned char *target) {
    unsigned char buffer[3] = {0x00, 0x00, 0x00};
    unsigned char adc_buffer[2];
    int16_t adc_temp;

    science_buffer->if_hit = ((*target & 0x40) == 0x40);
    science_buffer->gtm_module = (*target & 0x20) ? SLAVE : MASTER;
    science_buffer->citiroc_id = (*target & 0x10) ? 1 : 0;
    science_buffer->energy_filter = (*(target + 1) & 0x40) ? 1 : 0;

    // read channel id, it's spilt between bytes
    memcpy(buffer, target, 3);
    left_shift_mem(buffer, 3, 4);
    buffer[0] = buffer[0] >> 3;
    memcpy(&(science_buffer->channel_id), buffer, 1);

    // read adc value
    memcpy(adc_buffer, target + 1, 2);
    adc_temp = ( ((adc_buffer[0] & 0x3F) << 8) | (adc_buffer[1]) );
    if (adc_temp > 0x2AF8) { // 5500*2
        adc_temp = adc_temp | 0xC000; // 11...
    }
    memcpy(&(science_buffer->adc_value), &adc_temp, 2);

    // update_energy_from_adc();

    write_science_buffer();

    return;
}

// shift the array n bits left, you should make sure 0<=bits<=7
void left_shift_mem(unsigned char *target, size_t targetSize, uint8_t Bits) {
    unsigned char current, next;
    size_t i;

    for (i = 0; i < targetSize - 1; ++i) {
        current = target[i];
        next = target[i + 1];
        target[i] = (current << Bits) | (next >> (8 - Bits));
    }
    // shift the last element
    target[targetSize - 1] = target[targetSize - 1] << Bits;
}

// waiting
void write_science_buffer() {
    static char detector_name[2][2][2][3] = {{{"PN\0", "PB\0"}, {"PT\0", "PP\0"}}, {{"NP\0", "NB\0"}, {"NT\0", "NN\0"}}};

    if (export_mode == 1 || export_mode == 3) {
        fprintf(raw_output_file, "event adc: ");
        
        // // weird!!!
        // fprintf(raw_outfile, "%1u;%5u;%10u;%1u;%1u;%3u;%1u;%5i\n", science_buffer->if_hit, science_buffer->pps_counter, science_buffer->fine_counter, science_buffer->gtm_module, science_buffer->citiroc_id, science_buffer->channel_id, science_buffer->energy_filter, science_buffer->adc_value);
        
        // // temporary output for realtime plotting
        // fprintf(raw_adc_only_outfile, "%u;%u;%u;%u;%i\n", science_buffer->gtm_module, science_buffer->citiroc_id, science_buffer->channel_id, science_buffer->energy_filter, science_buffer->adc_value);

        // separate master and slave cases
        if (science_buffer->gtm_module == 0) {
            fprintf(raw_output_file, "%1u;%5u;%10u;%1u;%1u;%3u;%1u;%5i\n", science_buffer->if_hit, science_buffer->pps_counter_master, science_buffer->fine_counter_master, science_buffer->gtm_module, science_buffer->citiroc_id, science_buffer->channel_id, science_buffer->energy_filter, science_buffer->adc_value);
        }
        else {
            fprintf(raw_output_file, "%1u;%5u;%10u;%1u;%1u;%3u;%1u;%5i\n", science_buffer->if_hit, science_buffer->pps_counter_slave, science_buffer->fine_counter_slave, science_buffer->gtm_module, science_buffer->citiroc_id, science_buffer->channel_id, science_buffer->energy_filter, science_buffer->adc_value);
        }
    }
    if (export_mode == 2 || export_mode == 3) {
        // separate master and slave cases
        if (science_buffer->gtm_module == 0) {
            fprintf(science_pipeline_output_file, "%u;%i;%i;%u;%u;%u;%i\n", science_buffer->gtm_module, science_buffer->pps_counter_master, science_buffer->fine_counter_master, science_buffer->citiroc_id, science_buffer->channel_id, science_buffer->energy_filter, science_buffer->adc_value);
        }
        else {
            fprintf(science_pipeline_output_file, "%u;%i;%i;%u;%u;%u;%i\n", science_buffer->gtm_module, science_buffer->pps_counter_slave, science_buffer->fine_counter_slave, science_buffer->citiroc_id, science_buffer->channel_id, science_buffer->energy_filter, science_buffer->adc_value);
        }
    }
}

void parse_sd_header(unsigned char *target) {
    // static int got_first_sd_header = 0;
    unsigned char new_gtm_module = 0x00;
    uint8_t new_sequence_count;

    memcpy(&new_gtm_module, target + 1, 1);
    if (new_gtm_module == 0x55) {
        science_buffer->gtm_module = 0;
    }
    else {
        science_buffer->gtm_module = 1;
    }

    // parse sequence count and check packet continuity
    memcpy(&new_sequence_count, target + 3, 1);

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

// waiting
static void write_sd_header(uint8_t SequenceCount) {
    if (export_mode == 1 || export_mode == 3) {
        fprintf(raw_output_file, "sd header: %3u\n", SequenceCount);
    }
}

/// parse_science_data_end ///

//* function_end *//