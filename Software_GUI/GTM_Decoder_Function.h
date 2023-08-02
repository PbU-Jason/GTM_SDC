#ifndef GTM_DECODER_FUNCTION_H
#define GTM_DECODER_FUNCTION_H

#include <stdio.h>  // for size_t, File, printf, fopen, ..., etc
#include <stdlib.h> // for exit & malloc (also has size_t)
#include <string.h> // for strlen, memcpy, strcat & memcmp (also has size_t)

#include <stdint.h> // for uint8_t, uint16_t & uint32_t

// refer to GICD

#define TMTC_PACKET_HEADER_SIZE 6
#define TMTC_PACKET_ID_SIZE 2
#define TMTC_PACKET_SEQUENCE_CONTROL_SIZE 2
#define TMTC_PACKET_LENGTH_SIZE 2

#define TMTC_PACKET_DATA_FIELD_SIZE 138
#define TMTC_DATA_FIELD_HEADER_SIZE 10
#define TMTC_SOURCE_DATA_SIZE 128

#define SCIENCE_ATTACHED_SYNCHRO_MARKER_SIZE 4

#define SCIENCE_TRANSFER_FRAME_SIZE 1115
#define SCIENCE_PRIMARY_HEADER_SIZE 6
#define SCIENCE_TRANSFER_FRAME_DATA_FIELD_SIZE 1105
#define SCIENCE_TRANSFER_FRAME_TRAILER_SIZE 4

#define SCIENCE_REED_SOLOMON_CHECK_SYMBOLS_SIZE 160

// refer to ICD

#define TMTC_DATA_SIZE 128

#define SPACEWIRE_RMAP_HEAD_SIZE 16
#define SCIENCE_HEADER_SIZE 6
#define SCIENCE_DATA_SIZE 1104
#define SCIENCE_CRC8_SIZE 1

#define SCIENCE_DATA_SYNC_SIZE 45
#define SCIENCE_DATA_EVENT_TIME_SIZE 3
#define SCIENCE_DATA_EVENT_ADC_SIZE 3



//* define_public_type_for_global_buffer *//

typedef struct TMTC {

    /// sequence_count_and_utc_from_TASA ///

    uint16_t source_sequence_count;
    uint16_t gicd_year;
    uint16_t gicd_day_of_year;
    uint8_t  gicd_hour;
    uint8_t  gicd_minute;
    uint8_t  gicd_second;
    uint8_t  gicd_subsecond;

    /// sequence_count_and_utc_from_TASA_end ///

    /// 128_byte_tmtc ///

    unsigned char header[2];
    uint8_t       gtm_id; // 0x02 = master; 0x05 = slave
    uint16_t      packet_counter;
    uint8_t       data_length_msb;
    uint8_t       data_length_120_byte;
    uint16_t      icd_year;
    uint16_t      icd_day_of_year;
    uint8_t       icd_hour;
    uint8_t       icd_minute;
    uint8_t       icd_second;
    uint8_t       icd_subsecond;
    uint8_t       gtm_id_in_pps_counter; // 0 = master; 1 = slave
    uint16_t      pps_counter;
    unsigned char fine_time_counter[3];
    int8_t        board_temp_1; // sign
    int8_t        board_temp_2; // sign
    unsigned char citiroc_1_temp[2]; // sign
    unsigned char citiroc_2_temp[2]; // sign
    unsigned char citiroc_1_livetime_busy[3];
    unsigned char citiroc_2_livetime_busy[3];
    uint8_t       citiroc_1_hit_counter[32];
    uint8_t       citiroc_2_hit_counter[32];
    uint16_t      citiroc_1_trigger_counter;
    uint16_t      citiroc_2_trigger_counter;
    uint8_t       counter_period;
    uint8_t       hv_dac_1;
    uint8_t       hv_dac_2;

    // for master
    uint8_t       spw_a_error_count;
    uint8_t       spw_a_last_recv_byte;
    uint8_t       spw_b_error_count;
    uint8_t       spw_b_last_recv_byte;
    uint16_t      spw_a_status;
    uint16_t      spw_b_status;

    // for slave
    uint8_t       input_i;
    uint8_t       input_v;
    uint8_t       input_i_v;
    int8_t        i_monitor_u22_temp; // sign
    uint8_t       hv_input_i;
    uint8_t       hv_input_v;
    uint8_t       hv_input_i_v;
    int8_t        i_monitor_u21_temp; // sign

    uint8_t       cmd_recv_checksum;
    uint8_t       cmd_calc_checksum;
    uint8_t       cmd_recv_number;
    uint8_t       tmtc_empty[5];
    unsigned char citiroc_1_livetime_buffer_busy[3]; // should be lifetime?
    unsigned char citiroc_2_livetime_buffer_busy[3];
    uint8_t       checksum;
    unsigned char tail[2];

    /// 128_byte_tmtc_end ///

} TMTC;

typedef struct Science {

    // info. following head
    uint8_t gtm_id; // 0x55 = master = 0; 0xAA = slave = 1
    uint8_t previous_crc8;
    uint8_t sequence_count;
    
    /// sync_data ///

    // for master
    unsigned char master_sync_header[1]; // unsigned char [1] = 1 byte
    uint8_t       master_sync_gtm_id; // 0 = master; 1 = slave
    uint16_t      master_sync_pps_counts;
    uint8_t       master_sync_cmd_sequence_number;
    uint16_t      master_sync_day_of_year;
    uint8_t       master_sync_hour;
    uint8_t       master_sync_minute;
    uint8_t       master_sync_second;
    uint8_t       master_sync_subsecond;
    uint32_t      master_sync_x;
    uint32_t      master_sync_y;
    uint32_t      master_sync_z;
    uint32_t      master_sync_v_x;
    uint32_t      master_sync_v_y;
    uint32_t      master_sync_v_z;
    uint16_t      master_sync_quaternion_1;
    uint16_t      master_sync_quaternion_2;
    uint16_t      master_sync_quaternion_3;
    uint16_t      master_sync_quaternion_4;
    unsigned char master_sync_tail[3];

    // for slave
    unsigned char slave_sync_header[1];
    uint8_t       slave_sync_gtm_id;
    uint16_t      slave_sync_pps_counts;
    uint8_t       slave_sync_cmd_sequence_number;
    uint16_t      slave_sync_day_of_year;
    uint8_t       slave_sync_hour;
    uint8_t       slave_sync_minute;
    uint8_t       slave_sync_second;
    uint8_t       slave_sync_subsecond;
    uint32_t      slave_sync_x;
    uint32_t      slave_sync_y;
    uint32_t      slave_sync_z;
    uint32_t      slave_sync_v_x;
    uint32_t      slave_sync_v_y;
    uint32_t      slave_sync_v_z;
    uint16_t      slave_sync_quaternion_1;
    uint16_t      slave_sync_quaternion_2;
    uint16_t      slave_sync_quaternion_3;
    uint16_t      slave_sync_quaternion_4;
    unsigned char slave_sync_tail[3];

    /// sync_data_end ///

    /// event_time_data ///
    
    // for master
    uint8_t       master_event_time_buffer_id;
    int           master_event_time_fine_time_counter;

    // for slave
    uint8_t       slave_event_time_buffer_id;
    int           slave_event_time_fine_time_counter;

    /// event_time_data_end ///
    
    /// event_adc_data ///

    uint8_t       event_adc_hit_flag; // 0 = no hit; 1 = hit (should always hit!)
    uint8_t       event_adc_gtm_id; // 0 = master; 1 = slave
    uint8_t       event_adc_citiroc_id; // 0 = A = 1; 1 = B = 2
    uint8_t       event_adc_channel_id;
    uint8_t       event_adc_gain; // 0 = low; 1 = high
    int16_t       event_adc_adc_value; // sign

    /// event_adc_data_end ///

} Science;

//* define_public_type_for_global_buffer_end *//



//* declare_global_variable *//

/// main ///

extern int in_space_flag;
extern int decode_mode;
extern int export_mode;

/// main_end ///

/// create_basic_buffer ///

// for input binary
extern size_t max_input_binary_buffer_size;
extern unsigned char *input_binary_buffer;

/// create_basic_buffer_end ///

/// open_all_file ///

extern FILE *input_binary_file;

/// open_all_file_end ///

//* declare_global_variable_end *//



//* functions *//

/// main ///

void check_endianness();
void log_error(const char *sentence, ...);
void initailize_sync_data_flag();
void create_basic_buffer();
void open_all_file(char *input_file_path);
void log_message(const char *sentence, ...);
char *str_append(char *pre_fix, char *post_fix);
void close_all_file();
void destroy_basic_buffer();

/// main_end ///

/// parse_tmtc_data ///

int is_tmtc_gicd_header(unsigned char *target);
int is_tmtc_icd_head(unsigned char *target);
int is_tmtc_icd_tail(unsigned char *target);
void write_tmtc_raw_all(unsigned char *target);
void parse_tmtc_packet(unsigned char *target);
void simple_big2little_endian(void *target, size_t reverse_size);
void parse_tmtc_gicd_utc(unsigned char *target);
void parse_tmtc_icd_utc(unsigned char *target);
void write_tmtc_buffer_master_or_slave();

/// parse_tmtc_data_end ///

/// parse_science_data ///

int is_science_gicd_marker(unsigned char *target);
int is_science_icd_spacewire_rmap_head(unsigned char *target);
int is_science_icd_head(unsigned char *target);
int parse_science_packet(unsigned char *target);
void write_science_packet_beginning();
int is_science_sync_header(unsigned char *target);
int parse_science_event_data(unsigned char *target);
void parse_science_event_time(unsigned char *target);
void write_science_event_time();
void parse_science_event_adc(unsigned char *target);
void write_science_event_adc();
void export_science_pipeline_output();
int is_science_sync_tail(unsigned char *target);
void parse_science_sync_data(unsigned char *target);
void parse_science_sync_utc(unsigned char *target);
void parse_science_sync_attitude(unsigned char *target);
void write_science_sync_data();

/// parse_science_data_end ///

//* function_end *//

#endif
