#include "GTM_Decoder_Function.h"

#include <stdarg.h> // for va_list, va_start(), va_arg() & va_end()

// #include <time.h>   // for mktime & localtime (also has size_t)
// #include <math.h>   // for pow



//* define_global_variable *//

/// main ///

int decode_mode;
int export_mode;

/// main_end ///

/// create_basic_buffer ///

// for input binary
size_t max_input_binary_buffer_size = 1174405120; // 1 GB
unsigned char *input_binary_buffer; // tmtc and science shared

/// create_basic_buffer_end ///

/// open_all_file ///

FILE *input_binary_file;

/// open_all_file_end ///

//* define_global_variable_end *//



//* local_variable *//

/// create_basic_buffer ///

// for typedef struct
TMTC *tmtc_buffer;
Science *science_buffer;

/// create_basic_buffer_end ///

/// open_all_file ///

FILE *raw_output_file; // tmtc and science shared
FILE *tmtc_master_output_file;
FILE *tmtc_slave_output_file;
FILE *science_pipeline_output_file;

char tmtc_csv_column_name_all[] = "Pre-Byte 0;Pre-Byte 1;Pre-Byte 2;Pre-Byte 3;Pre-Byte 4;Pre-Byte 5;Pre-Byte 6;Pre-Byte 7;Pre-Byte 8;Pre-Byte 9;Pre-Byte 10;Pre-Byte 11;Pre-Byte 12;Pre-Byte 13;Pre-Byte 14;Pre-Byte 15;Byte 0;Byte 1;Byte 2;Byte 3;Byte 4;Byte 5;Byte 6;Byte 7;Byte 8;Byte 9;Byte 10;Byte 11;Byte 12;Byte 13;Byte 14;Byte 15;Byte 16;Byte 17;Byte 18;Byte 19;Byte 20;Byte 21;Byte 22;Byte 23;Byte 24;Byte 25;Byte 26;Byte 27;Byte 28;Byte 29;Byte 30;Byte 31;Byte 32;Byte 33;Byte 34;Byte 35;Byte 36;Byte 37;Byte 38;Byte 39;Byte 40;Byte 41;Byte 42;Byte 43;Byte 44;Byte 45;Byte 46;Byte 47;Byte 48;Byte 49;Byte 50;Byte 51;Byte 52;Byte 53;Byte 54;Byte 55;Byte 56;Byte 57;Byte 58;Byte 59;Byte 60;Byte 61;Byte 62;Byte 63;Byte 64;Byte 65;Byte 66;Byte 67;Byte 68;Byte 69;Byte 70;Byte 71;Byte 72;Byte 73;Byte 74;Byte 75;Byte 76;Byte 77;Byte 78;Byte 79;Byte 80;Byte 81;Byte 82;Byte 83;Byte 84;Byte 85;Byte 86;Byte 87;Byte 88;Byte 89;Byte 90;Byte 91;Byte 92;Byte 93;Byte 94;Byte 95;Byte 96;Byte 97;Byte 98;Byte 99;Byte 100;Byte 101;Byte 102;Byte 103;Byte 104;Byte 105;Byte 106;Byte 107;Byte 108;Byte 109;Byte 110;Byte 111;Byte 112;Byte 113;Byte 114;Byte 115;Byte 116;Byte 117;Byte 118;Byte 119;Byte 120;Byte 121;Byte 122;Byte 123;Byte 124;Byte 125;Byte 126;Byte 127\n";
char tmtc_csv_column_name_master[] = "Source Sequence Count;GICD Year;GICD Day;GICD Hour;GICD Minute;GICD Second;GICD Subsecond;Header;GTM ID;Packet Counter;Data Length (MSB);Data Length;ICD Year;ICD Day;ICD Hour;ICD Minute;ICD Second;ICD Subsecond;GTM ID in Lastest PPS Counter;Lastest PPS Counter;Lastest Fine Time Counter Value Between 2 PPSs;Board Temperature#1;Board Temperature#2;CITIROC1 Temperature;CITIROC2 Temperature;CITIROC1 Live Time (Busy);CITIROC2 Live Time (Busy);CITIROC1 Hit Counter#0;CITIROC1 Hit Counter#1;CITIROC1 Hit Counter#2;CITIROC1 Hit Counter#3;CITIROC1 Hit Counter#4;CITIROC1 Hit Counter#5;CITIROC1 Hit Counter#6;CITIROC1 Hit Counter#7;CITIROC1 Hit Counter#8;CITIROC1 Hit Counter#9;CITIROC1 Hit Counter#10;CITIROC1 Hit Counter#11;CITIROC1 Hit Counter#12;CITIROC1 Hit Counter#13;CITIROC1 Hit Counter#14;CITIROC1 Hit Counter#15;CITIROC1 Hit Counter#16;CITIROC1 Hit Counter#17;CITIROC1 Hit Counter#18;CITIROC1 Hit Counter#19;CITIROC1 Hit Counter#20;CITIROC1 Hit Counter#21;CITIROC1 Hit Counter#22;CITIROC1 Hit Counter#23;CITIROC1 Hit Counter#24;CITIROC1 Hit Counter#25;CITIROC1 Hit Counter#26;CITIROC1 Hit Counter#27;CITIROC1 Hit Counter#28;CITIROC1 Hit Counter#29;CITIROC1 Hit Counter#30;CITIROC1 Hit Counter#31;CITIROC2 Hit Counter#0;CITIROC2 Hit Counter#1;CITIROC2 Hit Counter#2;CITIROC2 Hit Counter#3;CITIROC2 Hit Counter#4;CITIROC2 Hit Counter#5;CITIROC2 Hit Counter#6;CITIROC2 Hit Counter#7;CITIROC2 Hit Counter#8;CITIROC2 Hit Counter#9;CITIROC2 Hit Counter#10;CITIROC2 Hit Counter#11;CITIROC2 Hit Counter#12;CITIROC2 Hit Counter#13;CITIROC2 Hit Counter#14;CITIROC2 Hit Counter#15;CITIROC2 Hit Counter#16;CITIROC2 Hit Counter#17;CITIROC2 Hit Counter#18;CITIROC2 Hit Counter#19;CITIROC2 Hit Counter#20;CITIROC2 Hit Counter#21;CITIROC2 Hit Counter#22;CITIROC2 Hit Counter#23;CITIROC2 Hit Counter#24;CITIROC2 Hit Counter#25;CITIROC2 Hit Counter#26;CITIROC2 Hit Counter#27;CITIROC2 Hit Counter#28;CITIROC2 Hit Counter#29;CITIROC2 Hit Counter#30;CITIROC2 Hit Counter#31;CITIROC1 Trigger Counter;CITIROC2 Trigger Counter;Counter Period Setting;HV DAC1;HV DAC2;SPW#A Error Count;SPW#A Last Recv Byte;SPW#B Error Count;SPW#B Last Recv Byte;SPW#A Status;SPW#B Status;Recv Checksum of Last CMD;Calc Checksum of Last CMD;Number of Recv CMDs;Bytes 114;Bytes 115;Bytes 116;Bytes 117;Bytes 118;CITIROC1 Live Time (Buffer+Busy);CITIROC2 Live Time (Buffer+Busy);Checksum;Tail\n";
char tmtc_csv_column_name_slave[] = "Source Sequence Count;GICD Year;GICD Day;GICD Hour;GICD Minute;GICD Second;GICD Subsecond;Header;GTM ID;Packet Counter;Data Length (MSB);Data Length;ICD Year;ICD Day;ICD Hour;ICD Minute;ICD Second;ICD Subsecond;GTM ID in Lastest PPS Counter;Lastest PPS Counter;Lastest Fine Time Counter Value Between 2 PPSs;Board Temperature#1;Board Temperature#2;CITIROC1 Temperature;CITIROC2 Temperature;CITIROC1 Live Time (Busy);CITIROC2 Live Time (Busy);CITIROC1 Hit Counter#0;CITIROC1 Hit Counter#1;CITIROC1 Hit Counter#2;CITIROC1 Hit Counter#3;CITIROC1 Hit Counter#4;CITIROC1 Hit Counter#5;CITIROC1 Hit Counter#6;CITIROC1 Hit Counter#7;CITIROC1 Hit Counter#8;CITIROC1 Hit Counter#9;CITIROC1 Hit Counter#10;CITIROC1 Hit Counter#11;CITIROC1 Hit Counter#12;CITIROC1 Hit Counter#13;CITIROC1 Hit Counter#14;CITIROC1 Hit Counter#15;CITIROC1 Hit Counter#16;CITIROC1 Hit Counter#17;CITIROC1 Hit Counter#18;CITIROC1 Hit Counter#19;CITIROC1 Hit Counter#20;CITIROC1 Hit Counter#21;CITIROC1 Hit Counter#22;CITIROC1 Hit Counter#23;CITIROC1 Hit Counter#24;CITIROC1 Hit Counter#25;CITIROC1 Hit Counter#26;CITIROC1 Hit Counter#27;CITIROC1 Hit Counter#28;CITIROC1 Hit Counter#29;CITIROC1 Hit Counter#30;CITIROC1 Hit Counter#31;CITIROC2 Hit Counter#0;CITIROC2 Hit Counter#1;CITIROC2 Hit Counter#2;CITIROC2 Hit Counter#3;CITIROC2 Hit Counter#4;CITIROC2 Hit Counter#5;CITIROC2 Hit Counter#6;CITIROC2 Hit Counter#7;CITIROC2 Hit Counter#8;CITIROC2 Hit Counter#9;CITIROC2 Hit Counter#10;CITIROC2 Hit Counter#11;CITIROC2 Hit Counter#12;CITIROC2 Hit Counter#13;CITIROC2 Hit Counter#14;CITIROC2 Hit Counter#15;CITIROC2 Hit Counter#16;CITIROC2 Hit Counter#17;CITIROC2 Hit Counter#18;CITIROC2 Hit Counter#19;CITIROC2 Hit Counter#20;CITIROC2 Hit Counter#21;CITIROC2 Hit Counter#22;CITIROC2 Hit Counter#23;CITIROC2 Hit Counter#24;CITIROC2 Hit Counter#25;CITIROC2 Hit Counter#26;CITIROC2 Hit Counter#27;CITIROC2 Hit Counter#28;CITIROC2 Hit Counter#29;CITIROC2 Hit Counter#30;CITIROC2 Hit Counter#31;CITIROC1 Trigger Counter;CITIROC2 Trigger Counter;Counter Period Setting;HV DAC1;HV DAC2;Input Current Value;Input Voltage Value;Current Monitor Chip (U22) Temperature;HV Input Current Value;HV Input Voltage Value;Current Monitor Chip (U21) Temperature;Recv Checksum of Last CMD;Calc Checksum of Last CMD;Number of Recv CMDs;Bytes 114;Bytes 115;Bytes 116;Bytes 117;Bytes 118;CITIROC1 Live Time (Buffer+Busy);CITIROC2 Live Time (Buffer+Busy);Checksum;Tail\n";
char science_csv_pipeline_column_name[] = "GTM ID;Day of Year;Hour;Minute;Second;Subsecond;X;Y;Z;Vx;Vy;Vz;Q1;Q2;Q3;Q4;PPS;Fine Time;CITIROC;Channel;Gain;ADC\n";

/// open_all_file_end ///

/// parse_science_packet ///

unsigned char *science_sync_master_buffer;
int science_sync_master_buffer_counter;
unsigned char *science_sync_slave_buffer;
int science_sync_slave_buffer_counter;

int stop_find_sync_data_header_master_flag; // 0 = don't stop; 1 = stop
int stop_find_sync_data_header_slave_flag;

int have_complete_sync_data_master_flag; // 0 = have not; 1 = have
int have_complete_sync_data_slave_flag;

/// parse_science_packet_end ///

//* local_variable_end *//



//* function *//

/// main ///

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

void initailize_sync_data_flag() { // for continuously decode
    int science_sync_master_buffer_counter     = 0;
    int science_sync_slave_buffer_counter      = 0;
    int stop_find_sync_data_header_master_flag = 0;
    int stop_find_sync_data_header_slave_flag  = 0;
    int have_complete_sync_data_master_flag    = 0;
    int have_complete_sync_data_slave_flag     = 0;
}

void create_basic_buffer() {

    // dynamically allocate a single large block of memory with the specified size

    input_binary_buffer = (unsigned char *)malloc(max_input_binary_buffer_size);
    
    tmtc_buffer = (TMTC *)malloc(sizeof(TMTC));
    science_buffer = (Science *)malloc(sizeof(Science));

    if (decode_mode == 2) {
        science_sync_master_buffer = (unsigned char *)malloc(45);
        science_sync_slave_buffer = (unsigned char *)malloc(45);
    }
}

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
                fputs(tmtc_csv_column_name_all, raw_output_file);
            }
            free(raw_output_path);

            // only master
            tmtc_master_output_path = str_append(input_file_path, "_tmtc_master.csv");
            tmtc_master_output_file = fopen(tmtc_master_output_path, "a");
            if (ftell(tmtc_master_output_file) == 0) {
                fputs(tmtc_csv_column_name_master, tmtc_master_output_file);
            }
            free(tmtc_master_output_path);

            // only slave
            tmtc_slave_output_path = str_append(input_file_path, "_tmtc_slave.csv");
            tmtc_slave_output_file = fopen(tmtc_slave_output_path, "a");
            if (ftell(tmtc_slave_output_file) == 0) {
                fputs(tmtc_csv_column_name_slave, tmtc_slave_output_file);
            }
            free(tmtc_slave_output_path);
            break;

        // decode science data
        case 2:
            if (export_mode == 1) {
                raw_output_path = str_append(input_file_path, "_science_raw.txt");
                raw_output_file = fopen(raw_output_path, "a");
                if (ftell(raw_output_file) == 0) {
                    fprintf(raw_output_file, "================================================================================\n");
                    fprintf(raw_output_file, "packet: gtm_id; previous_crc8; sequence_count\n");
                    fprintf(raw_output_file, "sync         : gtm_id; pps_counts; cmd_sequence_number\n");
                    fprintf(raw_output_file, "sync      utc: day_of_year; hour; minute; second; subsecond\n");
                    fprintf(raw_output_file, "sync attitude: x; y; z; v_x; v_y; v_z; q_1; q_2; q_3; q_4\n");
                    fprintf(raw_output_file, "event time: buffer_id; fine_time_counter\n");
                    fprintf(raw_output_file, "event  adc: hit_flag; gtm_id; citiroc_id; channel_id; gain; adc_value\n");
                    fprintf(raw_output_file, "unknow 3 bytes: gtm_id\n");
                    fprintf(raw_output_file, "================================================================================\n");
                }
                free(raw_output_path);
            }
            else if (export_mode == 2) {
                science_pipeline_output_path = str_append(input_file_path, "_science_pipeline.csv");
                science_pipeline_output_file = fopen(science_pipeline_output_path, "a");
                if (ftell(science_pipeline_output_file) == 0) {
                    fputs(science_csv_pipeline_column_name, science_pipeline_output_file);
                }
                free(science_pipeline_output_path);
            }
            else if (export_mode == 3) {
                raw_output_path = str_append(input_file_path, "_science_raw.txt");
                raw_output_file = fopen(raw_output_path, "a");
                if (ftell(raw_output_file) == 0) {
                    fprintf(raw_output_file, "================================================================================\n");
                    fprintf(raw_output_file, "packet: gtm_id; previous_crc8; sequence_count\n");
                    fprintf(raw_output_file, "sync         : gtm_id; pps_counts; cmd_sequence_number\n");
                    fprintf(raw_output_file, "sync      utc: day_of_year; hour; minute; second; subsecond\n");
                    fprintf(raw_output_file, "sync attitude: x; y; z; v_x; v_y; v_z; q_1; q_2; q_3; q_4\n");
                    fprintf(raw_output_file, "event time: buffer_id; fine_time_counter\n");
                    fprintf(raw_output_file, "event  adc: hit_flag; gtm_id; citiroc_id; channel_id; gain; adc_value\n");
                    fprintf(raw_output_file, "unknow 3 bytes: gtm_id\n");
                    fprintf(raw_output_file, "================================================================================\n");
                }
                free(raw_output_path);

                science_pipeline_output_path = str_append(input_file_path, "_science_pipeline.csv");
                science_pipeline_output_file = fopen(science_pipeline_output_path, "a");
                if (ftell(science_pipeline_output_file) == 0) {
                    fputs(science_csv_pipeline_column_name, science_pipeline_output_file);
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

// similar with log_error, but no exit
void log_message(const char *sentence, ...) {
    va_list args;

    va_start(args, sentence);
    printf("Message: "); vprintf(sentence, args); printf("\n");
    va_end(args);
}

char *str_append(char *pre_fix, char *post_fix) {
    char *new;
    size_t size_prefix, size_postfix;

    size_prefix = strlen(pre_fix); // not count \0
    size_postfix = strlen(post_fix);
    new = (char *)malloc(size_prefix+size_postfix+1); // +1 to keep \0 place

    memcpy(new, pre_fix, size_prefix+1); // again, +1 to keep \0 place
    strcat(new, post_fix); // automatically repalce \0 of pre_fix and add \0 after post_fix
    
    return new;
}

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

void destroy_basic_buffer() {
    // destroy input_binary_buffer independently

    free(tmtc_buffer);
    free(science_buffer);

    if (decode_mode == 2) {
        free(science_sync_master_buffer);
        free(science_sync_slave_buffer);
    }
}

/// main_end ///

/// parse_tmtc_data ///

int is_tmtc_gicd_header(unsigned char *target) {
    unsigned char ref[2] = {0x08, 0x91};

    if (!memcmp(ref, target, 2)) {
        // if ref & target store the same info, memcmp will report 0
        // otherwise, it will report a number != 0

        return 1; // == true in c
    }

    return 0; // == flase in c
}

int is_tmtc_icd_head(unsigned char *target) {
    unsigned char ref[2] = {0x55, 0xAA};

    if (!memcmp(ref, target, 2)) {
        return 1;
    }

    return 0;
}

int is_tmtc_icd_tail(unsigned char *target) {
    unsigned char ref[2] = {0xFB, 0xF2};

    if (!memcmp(ref, target, 2)) {
        return 1;
    }

    return 0;
}

void write_tmtc_raw_all(unsigned char *target) { 
    unsigned char byte_buffer[1];

    for (size_t i = 0; i < 144; i++) {
        memcpy(byte_buffer, target+i, 1);
        fprintf(raw_output_file, "%u;", byte_buffer[0]);
        if (i == 143) {
            fprintf(raw_output_file, "\n");
        }
    }
}

void parse_tmtc_packet(unsigned char *target) {
    int tmtc_16_byte_shift = TMTC_PACKET_HEADER_SIZE+TMTC_DATA_FIELD_HEADER_SIZE;

    // sequence count from TASA
    *(target+TMTC_PACKET_ID_SIZE) = *(target+TMTC_PACKET_ID_SIZE) & 0x3F; // mask segmentation flag
    memcpy(&(tmtc_buffer->source_sequence_count), target+TMTC_PACKET_ID_SIZE, TMTC_PACKET_SEQUENCE_CONTROL_SIZE);
    simple_big2little_endian(&(tmtc_buffer->source_sequence_count), 2);

    // utc from TASA
    parse_tmtc_gicd_utc(target+TMTC_PACKET_HEADER_SIZE);

    // header
    memcpy(tmtc_buffer->header, target+tmtc_16_byte_shift, 2);

    // gtm id
    tmtc_buffer->gtm_id = (*(target+tmtc_16_byte_shift+2) == 0x02) ? 0 : 1; // 0x02 = master = 0; 0x05 = slave = 1

    // packet counter
    memcpy(&(tmtc_buffer->packet_counter), target+tmtc_16_byte_shift+3, 2);
    simple_big2little_endian(&(tmtc_buffer->packet_counter), 2);

    // data length
    memcpy(&(tmtc_buffer->data_length_msb), target+tmtc_16_byte_shift+5, 1);
    memcpy(&(tmtc_buffer->data_length_120_byte), target+tmtc_16_byte_shift+6, 1);

    // utc in 128 bytes
    parse_tmtc_icd_utc(target+tmtc_16_byte_shift+7);

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
    if ((*(target+tmtc_16_byte_shift+25) & 0x80) == 0x80) { // negtive case
        tmtc_buffer->citiroc_2_temp[1] = 0xC0 | ((*(target+tmtc_16_byte_shift+25) & 0x7E) >> 1);
    }
    else { // positive case
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

    if (tmtc_buffer->gtm_id == 0) {
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
    else if (tmtc_buffer->gtm_id == 1) {
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

    write_tmtc_buffer_master_or_slave();
}

void simple_big2little_endian(void *target, size_t reverse_size) {
    unsigned char *reverse_buffer;

    reverse_buffer = (unsigned char *)malloc(reverse_size);

    // reversely copy data from target to reverse_buffer
    for (size_t i = 0; i < reverse_size; i++) {
        reverse_buffer[i] = ((unsigned char *)target)[(reverse_size-1)-i];
    }

    // update target by reverse_buffer
    memcpy(target, reverse_buffer, reverse_size);

    free(reverse_buffer);
}

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

    // recover 3 bytes
    fine_time_counter = (tmtc_buffer->fine_time_counter[0] << 16) | (tmtc_buffer->fine_time_counter[1] << 8) | tmtc_buffer->fine_time_counter[2];
    citiroc_1_livetime_busy = (tmtc_buffer->citiroc_1_livetime_busy[0] << 16) | (tmtc_buffer->citiroc_1_livetime_busy[1] << 8) | tmtc_buffer->citiroc_1_livetime_busy[2];
    citiroc_2_livetime_busy = (tmtc_buffer->citiroc_2_livetime_busy[0] << 16) | (tmtc_buffer->citiroc_2_livetime_busy[1] << 8) | tmtc_buffer->citiroc_2_livetime_busy[2];
    citiroc_1_livetime_buffer_busy = (tmtc_buffer->citiroc_1_livetime_buffer_busy[0] << 16) | (tmtc_buffer->citiroc_1_livetime_buffer_busy[1] << 8) | tmtc_buffer->citiroc_1_livetime_buffer_busy[2];
    citiroc_2_livetime_buffer_busy = (tmtc_buffer->citiroc_2_livetime_buffer_busy[0] << 16) | (tmtc_buffer->citiroc_2_livetime_buffer_busy[1] << 8) | tmtc_buffer->citiroc_2_livetime_buffer_busy[2];

    // recover citiroc_1_temp (int16_t, don't need to reverse index due to little endian)
    citiroc_1_temp = (tmtc_buffer->citiroc_1_temp[1] << 8) |  tmtc_buffer->citiroc_1_temp[0];
    citiroc_2_temp = (tmtc_buffer->citiroc_2_temp[1] << 8) |  tmtc_buffer->citiroc_2_temp[0];


    if (tmtc_buffer->gtm_id == 0) {
        output_file = tmtc_master_output_file;
    }
    else {
        output_file = tmtc_slave_output_file;

        // recover i & v monitor
        input_i = ( ((tmtc_buffer->input_i >> 4) << 8) | ((tmtc_buffer->input_i << 4) | (tmtc_buffer->input_i_v >> 4)) );
        input_v = ( ((tmtc_buffer->input_v >> 4) << 8) | ((tmtc_buffer->input_v << 4) | (tmtc_buffer->input_i_v & 0x0F)) );
        hv_input_i = ( ((tmtc_buffer->hv_input_i >> 4) << 8) | ((tmtc_buffer->hv_input_i << 4) | (tmtc_buffer->hv_input_i_v >> 4)) );
        hv_input_v = ( ((tmtc_buffer->hv_input_v >> 4) << 8) | ((tmtc_buffer->hv_input_v << 4) | (tmtc_buffer->hv_input_i_v & 0x0F)) );
        // ((tmtc_buffer->input_i >> 4) << 8) is ok, it's like ((tmtc_buffer->input_i & 0xF0) << 4)
        // ((tmtc_buffer->input_v >> 4) << 8) is ok, it's like ((tmtc_buffer->input_v & 0xF0) << 4)
        // ((tmtc_buffer->hv_input_i >> 4) << 8) is ok, it's like ((tmtc_buffer->hv_input_i & 0xF0) << 4)
        // ((tmtc_buffer->hv_input_v >> 4) << 8) is ok, it's like ((tmtc_buffer->hv_input_v & 0xF0) << 4)
    }

    // from TASA
    fprintf(output_file, \
    "%u;%u;%u;%u;%u;%u;%u", \
    tmtc_buffer->source_sequence_count, tmtc_buffer->gicd_year, tmtc_buffer->gicd_day_of_year, tmtc_buffer->gicd_hour, tmtc_buffer->gicd_minute, tmtc_buffer->gicd_second, tmtc_buffer->gicd_subsecond);


    // 128 bytes data
    fprintf(output_file, ";%X%X", tmtc_buffer->header[0], tmtc_buffer->header[1]);
    fprintf(output_file, \
    ";%u;%u;%u;%u \
    ;%u;%u;%u;%u;%u;%u \
    ;%u;%u;%d \
    ;%d;%d;%d;%d;%d;%d", \
    tmtc_buffer->gtm_id, tmtc_buffer->packet_counter, tmtc_buffer->data_length_msb, tmtc_buffer->data_length_120_byte, \
    tmtc_buffer->icd_year, tmtc_buffer->icd_day_of_year, tmtc_buffer->icd_hour, tmtc_buffer->icd_minute, tmtc_buffer->icd_second, tmtc_buffer->icd_second, \
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

    if (tmtc_buffer->gtm_id == 0) { // master
        fprintf(output_file, ";%X;%X;%X;%X;%X;%X", \
        tmtc_buffer->spw_a_error_count, tmtc_buffer->spw_a_last_recv_byte, tmtc_buffer->spw_b_error_count, tmtc_buffer->spw_b_last_recv_byte, tmtc_buffer->spw_a_status, tmtc_buffer->spw_b_status);
    }
    else { // slave
        fprintf(output_file, ";%u;%u;%d;%u;%u;%d", \
        input_v, input_i, tmtc_buffer->i_monitor_u22_temp, hv_input_v, hv_input_i, tmtc_buffer->i_monitor_u21_temp);
    }
    
    fprintf(output_file, ";%u;%u;%u", \
    tmtc_buffer->cmd_recv_checksum, tmtc_buffer->cmd_calc_checksum, tmtc_buffer->cmd_recv_number);
    
    for (int i = 0; i < 5; ++i) {
        fprintf(output_file, ";%u", tmtc_buffer->tmtc_empty[i]);
    }

    fprintf(output_file, ";%d;%d;%u", citiroc_1_livetime_buffer_busy, citiroc_2_livetime_buffer_busy, tmtc_buffer->checksum);
    fprintf(output_file, ";%X%X\n", tmtc_buffer->tail[0], tmtc_buffer->tail[1]);
}

/// parse_tmtc_data_end ///

/// parse_science_data ///

int is_science_gicd_marker(unsigned char *target) {
    unsigned char ref[SCIENCE_ATTACHED_SYNCHRO_MARKER_SIZE] = {0x1A, 0xCF, 0xFC, 0x1D};

    if (!memcmp(ref, target, SCIENCE_ATTACHED_SYNCHRO_MARKER_SIZE)) {
        return 1;
    }

    return 0;
}

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

void parse_science_packet(unsigned char *target) {
    // 45 bytes sync data in 1104 bytes science data may be truncated since master/slave switch
    // need science_sync_master_buffer and science_sync_slave_buffer to temporarily keep sync info

    unsigned char *science_data_pointer;

    // record previous crc8 and sequence count at beginning
    memcpy(&(science_buffer->previous_crc8), target+2, 1);
    memcpy(&(science_buffer->sequence_count), target+3, 1);

    write_science_packet_beginning();

    // moave 6 bytes to skip SCIENCE_HEADER_SIZE
    science_data_pointer = target+SCIENCE_HEADER_SIZE;

    // move buffer pointer 3 bytes each time
    for (size_t i = 0; i < SCIENCE_DATA_SIZE/3; i++) {

        // separate master and slave cases
        if (science_buffer->gtm_id == 0) { // master case

            // always look for sync data header
            if (!stop_find_sync_data_header_master_flag) { // look for sync data header

                // if find sync data header
                if (is_science_sync_header(science_data_pointer+(i*3))) {

                    // store 3 bytes to science_sync_master_buffer
                    memcpy(science_sync_master_buffer+science_sync_master_buffer_counter, science_data_pointer+(i*3), 3);
                    science_sync_master_buffer_counter+=3;

                    // stop looking for sync data header and have uncomplete sync data 
                    stop_find_sync_data_header_master_flag = 1;
                    have_complete_sync_data_master_flag = 0;
                }

                // if no find sync data header and have complete sync data
                if (have_complete_sync_data_master_flag) {
                    parse_science_event_data(science_data_pointer+(i*3));
                }
            }
            else { // stop looking for sync data header

                // store 3 bytes to science_sync_master_buffer
                memcpy(science_sync_master_buffer+science_sync_master_buffer_counter, science_data_pointer+(i*3), 3);
                science_sync_master_buffer_counter+=3;

                // all 45 bytes have been stored in science_sync_master_buffer
                if (science_sync_master_buffer_counter == 45) {

                    // check sync data tail
                    if (!is_science_sync_tail(science_sync_master_buffer+42)) { // is not sync tail
                        // log_error("Please check sync header defined in ICD!");

                        // recover 45 bytes in science_sync_master_buffer
                        for (size_t j = 0; j < 45/3; j++) {
                            parse_science_event_data(science_sync_master_buffer+(j*3));
                        }

                        // look for sync data header and have complete sync data
                        stop_find_sync_data_header_master_flag = 0;
                        have_complete_sync_data_master_flag = 1;

                        // reset science_sync_master_buffer_counter
                        science_sync_master_buffer_counter = 0;
                    }
                    else { // is sync tail

                        // look for sync data header and have complete sync data
                        stop_find_sync_data_header_master_flag = 0;
                        have_complete_sync_data_master_flag = 1;

                        // reset science_sync_master_buffer_counter
                        science_sync_master_buffer_counter = 0;

                        parse_science_sync_data(science_sync_master_buffer);
                    }
                }
            }
        }
        else { // slave case

            // always look for sync data header
            if (!stop_find_sync_data_header_slave_flag) { // look for sync data header

                // if find sync data header
                if (is_science_sync_header(science_data_pointer+(i*3))) {

                    // store 3 bytes to science_sync_slave_buffer
                    memcpy(science_sync_slave_buffer+science_sync_slave_buffer_counter, science_data_pointer+(i*3), 3);
                    science_sync_slave_buffer_counter+=3;

                    // stop looking for sync data header and have uncomplete sync data 
                    stop_find_sync_data_header_slave_flag = 1;
                    have_complete_sync_data_slave_flag = 0;
                }

                // if no find sync data header and have complete sync data
                if (have_complete_sync_data_slave_flag) {
                    parse_science_event_data(science_data_pointer+(i*3));
                }
            }
            else { // stop looking for sync data header

                // store 3 bytes to science_sync_slave_buffer
                memcpy(science_sync_slave_buffer+science_sync_slave_buffer_counter, science_data_pointer+(i*3), 3);
                science_sync_slave_buffer_counter+=3;

                // all 45 bytes have been stored in science_sync_slave_buffer
                if (science_sync_slave_buffer_counter == 45) {

                    // check sync data tail
                    if (!is_science_sync_tail(science_sync_slave_buffer+42)) { // is not sync tail
                        // log_error("Please check sync header defined in ICD!");

                        // recover 45 bytes in science_sync_slave_buffer
                        for (size_t j = 0; j < 45/3; j++) {
                            parse_science_event_data(science_sync_slave_buffer+(j*3));
                        }

                        // look for sync data header and have complete sync data
                        stop_find_sync_data_header_slave_flag = 0;
                        have_complete_sync_data_slave_flag = 1;

                        // reset science_sync_slave_buffer_counter
                        science_sync_slave_buffer_counter = 0;
                    }
                    else { // is sync tail

                        // look for sync data header and have complete sync data
                        stop_find_sync_data_header_slave_flag = 0;
                        have_complete_sync_data_slave_flag = 1;

                        // reset science_sync_slave_buffer_counter
                        science_sync_slave_buffer_counter = 0;

                        parse_science_sync_data(science_sync_slave_buffer);
                    }
                }
            }
        }
    }
}

void write_science_packet_beginning() {
    if (export_mode == 1 || export_mode == 3) {
        fprintf(raw_output_file, "packet: %1u; %3u; %3u\n", science_buffer->gtm_id, science_buffer->previous_crc8, science_buffer->sequence_count);
    }
}

int is_science_sync_header(unsigned char *target) {
    unsigned char ref[1] = {0xCA};

    if (!memcmp(ref, target, 1)) {
        return 1;
    }

    return 0;
}

void parse_science_event_data(unsigned char *target) {

    // check event time or event adc
    if ((*target & 0xC0) == 0x80) { // event time case
        parse_science_event_time(target);
    }
    else if ((*target & 0xC0) == 0x40) { // event adc case
        parse_science_event_adc(target);
    } 
    else { // weird 3 bytes
        fprintf(raw_output_file, "unknow 3 bytes: %1u\n", science_buffer->gtm_id);
    }
}

void parse_science_event_time(unsigned char *target) {
    unsigned char buffer_id_buffer[1];
    unsigned char fine_time_counter_buffer[3];

    // separate master and slave cases
    if (science_buffer->gtm_id == 0) { // for master

        // for buffer id
        memcpy(buffer_id_buffer, target, 1);
        buffer_id_buffer[0] = (buffer_id_buffer[0] << 2); // remove bits 23 & 22
        buffer_id_buffer[0] = (buffer_id_buffer[0] >> 4); // remove bits 17 & 16
        // (buffer_id_buffer[0] << 2) >> 4 == (buffer_id_buffer[0] >> 2) which is wrong!
        memcpy(&(science_buffer->master_event_time_buffer_id), buffer_id_buffer, 1);

        // for fine time counter
        memcpy(fine_time_counter_buffer, target, 3);
        fine_time_counter_buffer[0] = (fine_time_counter_buffer[0] & 0x03); // remove bits 23 to 18
        science_buffer->master_event_time_fine_time_counter = fine_time_counter_buffer[0] << 16 | fine_time_counter_buffer[1] << 8 | fine_time_counter_buffer[2];
    }
    else { // for slave

        // for buffer id
        memcpy(buffer_id_buffer, target, 1);
        buffer_id_buffer[0] = (buffer_id_buffer[0] << 2); // remove bits 23 & 22
        buffer_id_buffer[0] = (buffer_id_buffer[0] >> 4); // remove bits 17 & 16
        // (buffer_id_buffer[0] << 2) >> 4 == (buffer_id_buffer[0] >> 2) which is wrong!
        memcpy(&(science_buffer->slave_event_time_buffer_id), buffer_id_buffer, 1);

        // for fine time counter
        memcpy(fine_time_counter_buffer, target, 3);
        fine_time_counter_buffer[0] = (fine_time_counter_buffer[0] & 0x03); // remove bits 23 to 18
        science_buffer->slave_event_time_fine_time_counter = fine_time_counter_buffer[0] << 16 | fine_time_counter_buffer[1] << 8 | fine_time_counter_buffer[2];

    }

    write_science_event_time();
}

void write_science_event_time() {

    // separate master and slave cases
    if (science_buffer->gtm_id == 0) { // for master
        if (export_mode == 1 || export_mode == 3) {
            fprintf(raw_output_file, "event time: %2u; %6d\n", science_buffer->master_event_time_buffer_id, science_buffer->master_event_time_fine_time_counter);
        }
    }
    else { // for slave
        if (export_mode == 1 || export_mode == 3) {
            fprintf(raw_output_file, "event time: %2u; %6d\n", science_buffer->slave_event_time_buffer_id, science_buffer->slave_event_time_fine_time_counter);
        }
    }
}

void parse_science_event_adc(unsigned char *target) {
    unsigned char adc_buffer[3];
    int16_t adc_value_temp;

    memcpy(adc_buffer, target, 3);

    // hit case
    science_buffer->event_adc_hit_flag = (adc_buffer[0] & 0x40) ? 1 : 0; // 0 = no hit; 1 = hit (should always hit!)

    // gtm id in event adc
    science_buffer->event_adc_gtm_id = (adc_buffer[0] & 0x20) ? 1 : 0; // 0 = master; 1 = slave

    // citiroc id
    science_buffer->event_adc_citiroc_id = (adc_buffer[0] & 0x10) ? 1 : 0; // 0 = A = 1; 1 = B = 2

    // channel id
    science_buffer->event_adc_channel_id = ((adc_buffer[0] & 0x0F) << 1) | (adc_buffer[1] >> 7);

    // gain
    science_buffer->event_adc_gain = (adc_buffer[1] & 0x40) ? 1 : 0; // 0 = low; 1 = high

    // adc value
    adc_value_temp = ( ((adc_buffer[1] & 0x3F) << 8) | (adc_buffer[2]) );
    if (adc_value_temp > 0x2AF8) { // 5500*2
        adc_value_temp = adc_value_temp | 0xC000; // 11...
    }
    science_buffer->event_adc_adc_value = adc_value_temp;

    write_science_event_adc();

    return;
}

void write_science_event_adc() {
    if (export_mode == 1 || export_mode == 3) {
        fprintf(raw_output_file, "event  adc: ");
        fprintf(raw_output_file, "%1u; %1u; %1u;", \
        science_buffer->event_adc_hit_flag, science_buffer->event_adc_gtm_id, science_buffer->event_adc_citiroc_id);
        fprintf(raw_output_file, "%2u; %1u; %6d\n", \
        science_buffer->event_adc_channel_id, science_buffer->event_adc_gain, science_buffer->event_adc_adc_value);
    }

    // export pipeline data if needed
    export_science_pipeline_output();
}

void export_science_pipeline_output() {
    if (export_mode == 2 || export_mode == 3) {

        // separate master and slave cases
        if (science_buffer->gtm_id == 0) { // master
            fprintf(science_pipeline_output_file, "%u", science_buffer->gtm_id);

            //  weird! can't use \ to jump line?
            fprintf(science_pipeline_output_file, \
            ";%u;%u;%u;%u;%u;%u;%u;%u;%u;%u;%u;%u;%u;%u;%u", \
            science_buffer->master_sync_day_of_year, science_buffer->master_sync_hour, science_buffer->master_sync_minute, science_buffer->master_sync_second, science_buffer->master_sync_subsecond, \
            science_buffer->master_sync_x, science_buffer->master_sync_y, science_buffer->master_sync_z, \
            science_buffer->master_sync_v_x, science_buffer->master_sync_v_y, science_buffer->master_sync_v_z, \
            science_buffer->master_sync_quaternion_1, science_buffer->master_sync_quaternion_2, science_buffer->master_sync_quaternion_3, science_buffer->master_sync_quaternion_4);

            //  weird! can't use \ to jump line?
            fprintf(science_pipeline_output_file, \
            ";%u;%u;%u;%u;%u;%d\n", \
            science_buffer->master_sync_pps_counts, science_buffer->master_event_time_fine_time_counter, \
            science_buffer->event_adc_citiroc_id, science_buffer->event_adc_channel_id, science_buffer->event_adc_gain, science_buffer->event_adc_adc_value);
        }
        else { // slave
            fprintf(science_pipeline_output_file, "%u", science_buffer->gtm_id);

            //  weird! can't use \ to jump line?
            fprintf(science_pipeline_output_file, \
            ";%u;%u;%u;%u;%u;%u;%u;%u;%u;%u;%u;%u;%u;%u;%u", \
            science_buffer->slave_sync_day_of_year, science_buffer->slave_sync_hour, science_buffer->slave_sync_minute, science_buffer->slave_sync_second, science_buffer->slave_sync_subsecond, \
            science_buffer->slave_sync_x, science_buffer->slave_sync_y, science_buffer->slave_sync_z, \
            science_buffer->slave_sync_v_x, science_buffer->slave_sync_v_y, science_buffer->slave_sync_v_z, \
            science_buffer->slave_sync_quaternion_1, science_buffer->slave_sync_quaternion_2, science_buffer->slave_sync_quaternion_3, science_buffer->slave_sync_quaternion_4);

            //  weird! can't use \ to jump line?
            fprintf(science_pipeline_output_file, \
            ";%u;%u;%u;%u;%u;%d\n", \
            science_buffer->slave_sync_pps_counts, science_buffer->slave_event_time_fine_time_counter, \
            science_buffer->event_adc_citiroc_id, science_buffer->event_adc_channel_id, science_buffer->event_adc_gain, science_buffer->event_adc_adc_value);
        }
    }
}

int is_science_sync_tail(unsigned char *target) {
    unsigned char ref[3] = {0xF2, 0xF5, 0xFA};

    if (!memcmp(ref, target, 3)) {
        return 1;
    }

    return 0;
}

void parse_science_sync_data(unsigned char *target) {
    // due to automatic padding in structure alignment
    // it's not good to use relative position to find address
    
    // separate master and slave cases
    if (science_buffer->gtm_id == 0) { // master

        // header
        memcpy(science_buffer->master_sync_header, target, 1);

        // gtm id
        science_buffer->master_sync_gtm_id = ((*(target+1) & 0x80) == 0x80) ? 1 : 0; // 0 = master; 1 = slave

        // pps counts
        *(target+1) = *(target+1) & 0x7F; // mask gtm id
        memcpy(&(science_buffer->master_sync_pps_counts), target+1, 2);
        simple_big2little_endian(&(science_buffer->master_sync_pps_counts), 2);

        // cmd sequence number
        memcpy(&(science_buffer->master_sync_cmd_sequence_number), target+3, 1);

        parse_science_sync_utc(target+4);
        parse_science_sync_attitude(target+10);

        // tail
        memcpy(&(science_buffer->master_sync_tail), target+42, 3);

        write_science_sync_data();
    }
    else { // slave

        // header
        memcpy(science_buffer->slave_sync_header, target, 1);

        // gtm id
        science_buffer->slave_sync_gtm_id = ((*(target+1) & 0x80) == 0x80) ? 1 : 0; // 0 = master; 1 = slave

        // pps counts
        *(target+1) = *(target+1) & 0x7F; // mask gtm id
        memcpy(&(science_buffer->slave_sync_pps_counts), target+1, 2);
        simple_big2little_endian(&(science_buffer->slave_sync_pps_counts), 2);

        // cmd sequence number
        memcpy(&(science_buffer->slave_sync_cmd_sequence_number), target+3, 1);

        parse_science_sync_utc(target+4);
        parse_science_sync_attitude(target+10);

        // tail
        memcpy(&(science_buffer->slave_sync_tail), target+42, 3);

        write_science_sync_data();
    }
}

void parse_science_sync_utc(unsigned char *target) {

    // separate master and slave cases
    if (science_buffer->gtm_id == 0) { // master

        // day of year
        memcpy(&(science_buffer->master_sync_day_of_year), target, 2);
        simple_big2little_endian(&(science_buffer->master_sync_day_of_year), 2);

        // hour
        memcpy(&(science_buffer->master_sync_hour), target+2, 1);

        // minute
        memcpy(&(science_buffer->master_sync_minute), target+3, 1);

        // second
        memcpy(&(science_buffer->master_sync_second), target+4, 1);

        // subsecond
        memcpy(&(science_buffer->master_sync_subsecond), target+5, 1);
    }
    else { // slave

        // day of year
        memcpy(&(science_buffer->slave_sync_day_of_year), target, 2);
        simple_big2little_endian(&(science_buffer->slave_sync_day_of_year), 2);

        // hour
        memcpy(&(science_buffer->slave_sync_hour), target+2, 1);

        // minute
        memcpy(&(science_buffer->slave_sync_minute), target+3, 1);

        // second
        memcpy(&(science_buffer->slave_sync_second), target+4, 1);

        // subsecond
        memcpy(&(science_buffer->slave_sync_subsecond), target+5, 1);
    }
}

void parse_science_sync_attitude(unsigned char *target) {

    // separate master and slave cases
    if (science_buffer->gtm_id == 0) { // master

        // x, y & z position
        memcpy(&(science_buffer->master_sync_x), target, 4);
        simple_big2little_endian(&(science_buffer->master_sync_x), 4);
        memcpy(&(science_buffer->master_sync_y), target+4, 4);
        simple_big2little_endian(&(science_buffer->master_sync_y), 4);
        memcpy(&(science_buffer->master_sync_z), target+8, 4);
        simple_big2little_endian(&(science_buffer->master_sync_z), 4);

        // x, y & z velocity
        memcpy(&(science_buffer->master_sync_v_x), target+12, 4);
        simple_big2little_endian(&(science_buffer->master_sync_v_x), 4);
        memcpy(&(science_buffer->master_sync_v_y), target+16, 4);
        simple_big2little_endian(&(science_buffer->master_sync_v_y), 4);
        memcpy(&(science_buffer->master_sync_v_z), target+20, 4);
        simple_big2little_endian(&(science_buffer->master_sync_v_z), 4);

        // quaternion
        memcpy(&(science_buffer->master_sync_quaternion_1), target+24, 2);
        simple_big2little_endian(&(science_buffer->master_sync_quaternion_1), 2);
        memcpy(&(science_buffer->master_sync_quaternion_2), target+26, 2);
        simple_big2little_endian(&(science_buffer->master_sync_quaternion_2), 2);
        memcpy(&(science_buffer->master_sync_quaternion_3), target+28, 2);
        simple_big2little_endian(&(science_buffer->master_sync_quaternion_3), 2);
        memcpy(&(science_buffer->master_sync_quaternion_4), target+30, 2);
        simple_big2little_endian(&(science_buffer->master_sync_quaternion_4), 2);
    }
    else { // slave

        // x, y & z position
        memcpy(&(science_buffer->slave_sync_x), target, 4);
        simple_big2little_endian(&(science_buffer->slave_sync_x), 4);
        memcpy(&(science_buffer->slave_sync_y), target+4, 4);
        simple_big2little_endian(&(science_buffer->slave_sync_y), 4);
        memcpy(&(science_buffer->slave_sync_z), target+8, 4);
        simple_big2little_endian(&(science_buffer->slave_sync_z), 4);

        // x, y & z velocity
        memcpy(&(science_buffer->slave_sync_v_x), target+12, 4);
        simple_big2little_endian(&(science_buffer->slave_sync_v_x), 4);
        memcpy(&(science_buffer->slave_sync_v_y), target+16, 4);
        simple_big2little_endian(&(science_buffer->slave_sync_v_y), 4);
        memcpy(&(science_buffer->slave_sync_v_z), target+20, 4);
        simple_big2little_endian(&(science_buffer->slave_sync_v_z), 4);

        // quaternion
        memcpy(&(science_buffer->slave_sync_quaternion_1), target+24, 2);
        simple_big2little_endian(&(science_buffer->slave_sync_quaternion_1), 2);
        memcpy(&(science_buffer->slave_sync_quaternion_2), target+26, 2);
        simple_big2little_endian(&(science_buffer->slave_sync_quaternion_2), 2);
        memcpy(&(science_buffer->slave_sync_quaternion_3), target+28, 2);
        simple_big2little_endian(&(science_buffer->slave_sync_quaternion_3), 2);
        memcpy(&(science_buffer->slave_sync_quaternion_4), target+30, 2);
        simple_big2little_endian(&(science_buffer->slave_sync_quaternion_4), 2);
    }
}

void write_science_sync_data() {

    // separate master and slave cases
    if (science_buffer->gtm_id == 0) { // for master
        if (export_mode == 1 || export_mode == 3) {
            fprintf(raw_output_file, "sync         : %1u; %5u; %3u\n", \
            science_buffer->master_sync_gtm_id, science_buffer->master_sync_pps_counts, science_buffer->master_sync_cmd_sequence_number);

            fprintf(raw_output_file, "sync      utc: %3u; %2u; %2u; %2u; %3u\n", \
            science_buffer->master_sync_day_of_year, science_buffer->master_sync_hour, science_buffer->master_sync_minute, science_buffer->master_sync_second, science_buffer->master_sync_subsecond);
            
            fprintf(raw_output_file, "sync attitude: ");
            fprintf(raw_output_file, "%10u; %10u; %10u;", \
            science_buffer->master_sync_x, science_buffer->master_sync_y, science_buffer->master_sync_z);
            fprintf(raw_output_file, "%10u; %10u; %10u;", \
            science_buffer->master_sync_v_x, science_buffer->master_sync_v_y, science_buffer->master_sync_v_z);
            fprintf(raw_output_file, "%5u; %5u; %5u; %5u\n", \
            science_buffer->master_sync_quaternion_1, science_buffer->master_sync_quaternion_2, science_buffer->master_sync_quaternion_3, science_buffer->master_sync_quaternion_4);
        }
    }
    else { // for slave
        if (export_mode == 1 || export_mode == 3) {
            fprintf(raw_output_file, "sync         : %1u; %5u; %3u\n", \
            science_buffer->slave_sync_gtm_id, science_buffer->slave_sync_pps_counts, science_buffer->slave_sync_cmd_sequence_number);

            fprintf(raw_output_file, "sync      utc: %3u; %2u; %2u; %2u; %3u\n", \
            science_buffer->slave_sync_day_of_year, science_buffer->slave_sync_hour, science_buffer->slave_sync_minute, science_buffer->slave_sync_second, science_buffer->slave_sync_subsecond);
            
            fprintf(raw_output_file, "sync attitude: ");
            fprintf(raw_output_file, "%10u; %10u; %10u;", \
            science_buffer->slave_sync_x, science_buffer->slave_sync_y, science_buffer->slave_sync_z);
            fprintf(raw_output_file, "%10u; %10u; %10u;", \
            science_buffer->slave_sync_v_x, science_buffer->slave_sync_v_y, science_buffer->slave_sync_v_z);
            fprintf(raw_output_file, "%5u; %5u; %5u; %5u\n", \
            science_buffer->slave_sync_quaternion_1, science_buffer->slave_sync_quaternion_2, science_buffer->slave_sync_quaternion_3, science_buffer->slave_sync_quaternion_4);
        }
    }
}

/// parse_science_data_end ///

//* function_end *//
