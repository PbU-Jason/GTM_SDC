#ifndef GTM_DECODER_FUNCTION_H
#define GTM_DECODER_FUNCTION_H

#include <stdio.h>  // for size_t, File, printf, fopen, ..., etc
#include <stdint.h> // for uint8_t, uint16_t & uint32_t

// refer to GICD (may not be used)

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

// refer to ICD (may not be used)

#define TMTC_DATA_SIZE 128

#define SCIENCE_HEADER_SIZE 6
#define SCIENCE_DATA_SIZE 1104

#define SCIENCE_DATA_SYNC_SIZE 45
#define SCIENCE_DATA_EVENT_TIME_SIZE 3
#define SCIENCE_DATA_EVENT_ADC_SIZE 3



//* define_public_type_for_global_buffer *//

// tmtc and science shared
typedef struct UTC {
    uint16_t year;
    uint16_t day_of_year;
    uint8_t  hour;
    uint8_t  minute;
    uint8_t  second;
    uint8_t  subsecond;
} UTC;

typedef struct TMTC {

    // sequence count from TASA
    uint16_t source_sequence_count;

    unsigned char head[2];
    uint8_t       gtm_id; // 0x02 = master; 0x05 = slave
    uint16_t      packet_counter;
    uint8_t       data_length_msb;
    uint8_t       data_length_120_byte;

    // have defined UTC

    int           gtm_id_in_pps_counter; // 0 = master; 1 = slave
    uint16_t      pps_counter;
    unsigned char fine_time_counter[3];
    int8_t        board_temp_1;
    int8_t        board_temp_2;
    unsigned char citiroc_1_temp[2];
    unsigned char citiroc_2_temp[2];
    unsigned char citiroc_1_livetime_busy[3];
    unsigned char citiroc_2_livetime_busy[3];
    uint8_t       citiroc_1_hit[32];
    uint8_t       citiroc_2_hit[32];
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
    int8_t        i_monitor_u22_temp;
    uint8_t       hv_input_i;
    uint8_t       hv_input_v;
    uint8_t       hv_input_i_v;
    int8_t        i_monitor_u21_temp;

    uint8_t       cmd_recv_checksum;
    uint8_t       cmd_calc_checksum;
    uint8_t       cmd_recv_number;
    uint8_t       tmtc_empty[5];
    unsigned char citiroc_1_livetime_buffer_busy[3]; // should be lifetime?
    unsigned char citiroc_2_livetime_buffer_busy[3];
    uint8_t       checksum;
    unsigned char tail[2];
} TMTC;

typedef struct Science {

    // gtm id following head
    int gtm_id; // 0x55 = master = 0; 0xAA = slave = 1
    
    /// sync_data ///

    unsigned char sync_header[1];
    int           sync_gtm_id; // 0 = master; 1 = slave

    // to keep correct time tag when data switch
    uint16_t      sync_pps_counter_master;
    uint16_t      sync_pps_counter_slave;

    uint8_t       sync_cmd_sequence_number;

    // have defined UTC

    uint32_t      sync_x;
    uint32_t      sync_y;
    uint32_t      sync_z;
    uint32_t      sync_v_x;
    uint32_t      sync_v_y;
    uint32_t      sync_v_z;
    uint16_t      sync_quaternion_1;
    uint16_t      sync_quaternion_2;
    uint16_t      sync_quaternion_3;
    uint16_t      sync_quaternion_4;
    unsigned char sync_tail[3];

    /// sync_data_end ///

    /// event_time_data ///

    uint8_t       event_time_buffer_id;

    // to keep correct time tag when data switch
    uint32_t      event_time_fine_time_counter_master;
    uint32_t      event_time_fine_time_counter_slave;

    /// event_time_data_end ///
    
    /// event_adc_data ///

    int           event_adc_gtm_id; // 0 = master; 1 = slave
    uint8_t       event_adc_citiroc_id; // 0 = A = 1; 1 = B = 2
    uint8_t       event_adc_channel_id;
    uint8_t       event_adc_gain; // 0 = low; 1 = high
    int16_t       event_adc_adc_value;

    /// event_adc_data_end ///

} Science;

//* define_public_type_for_global_buffer_end *//



//* declare_global_variable *//

/// main ///

extern int decode_mode; // inverse concept is static
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
void initailize_variable();
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
void parse_tmtc_utc(unsigned char *target);
void write_tmtc_buffer_master_and_slave();

/// parse_tmtc_data_end ///

/// parse_science_data ///

int is_science_gicd_marker(unsigned char *target);
int is_science_icd_head(unsigned char *target);
void parse_science_packet(unsigned char *target);
int is_sync_header(unsigned char *target);
int is_sync_tail(unsigned char *target);
void parse_sync_data(unsigned char *target);
void parse_utc_time_sync(unsigned char *target);
void parse_position(unsigned char *target);
int compare_UTC(Time *Time1, Time *Time2);
static void write_sync_data(void);
void get_month_and_mday(void);
double find_time_delta(Time *TimeStart, Time *TimeEnd);
double calc_sec(Time *Time);
static void parse_event_data(unsigned char *target);
static void write_event_time(void);
static void parse_event_adc(unsigned char *target);
void left_shift_mem(unsigned char *target, size_t targetSize, uint8_t Bits);
static void write_science_buffer(void);
void parse_sd_header(unsigned char *target);
static void write_sd_header(uint8_t SequenceCount);
void free_got_first_sd_header();

/// parse_science_data_end ///

//* function_end *//

#endif
