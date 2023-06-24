#ifndef GTM_DECODER_FUNCTION_H
#define GTM_DECODER_FUNCTION_H

#include <stdio.h>
#include <stdint.h>

#define NSPO_DATA_SIZE 1127 // total size of a NSPO packet
#define NSPO_HEADER_SIZE 16 // spacewire RMAP HEAD + CRC
#define NSPO_TAIL_SIZE 1    // data CRC8 value, EOP control character is not included

#define SCIENCE_DATA_SIZE 1104
#define SD_HEADER_SIZE 6
#define SYNC_DATA_SIZE 45

#define TMTC_DATA_SIZE 128

typedef struct Time {
    // from UTC
    uint16_t year;
    uint8_t  month;
    uint8_t  mday; // this is the day in the month
    uint16_t day; // this is the day from 1/1 of the year
    uint8_t  hour;
    uint8_t  minute;
    uint8_t  sec;
    uint8_t  sub_sec; // msec

    // from sync and event time

    // ???
    uint32_t pps_counter; // it's our own pps counter
    uint32_t pps_counter_base;

    // for master and slave
    uint32_t fine_counter; // 0.24 usec
    uint32_t fine_counter_master;
    uint32_t fine_counter_slave;
} Time;

typedef enum Module {
    MASTER,
    SLAVE
} Module;

typedef struct Attitude {
    uint32_t x;
    uint32_t y;
    uint32_t z;
    uint32_t x_velocity;
    uint32_t y_velocity;
    uint32_t z_velocity;
    uint16_t quaternion1;
    uint16_t quaternion2;
    uint16_t quaternion3;
    uint16_t quaternion4;
} Attitude;

typedef struct TMTC {
    unsigned char head[2];
    unsigned char tail[2];
    uint8_t       gtm_id;
    uint16_t      packet_counter;
    uint8_t       data_length_msb;
    uint8_t       data_length;
    int           gtm_id_in_pps_counter;
    uint16_t      pps_counter;
    unsigned char fine_counter[3];
    int8_t        board_temp1;
    int8_t        board_temp2;
    unsigned char citiroc1_temp[2];
    unsigned char citiroc2_temp[2];
    unsigned char citiroc1_livetime_busy[3];
    unsigned char citiroc2_livetime_busy[3];
    uint8_t       citiroc1_hit[32];
    uint8_t       citiroc2_hit[32];
    uint16_t      citiroc1_trigger;
    uint16_t      citiroc2_trigger;
    uint8_t       counter_period;
    uint8_t       hv_dac1;
    uint8_t       hv_dac2;

    // for master
    uint8_t  spw_a_error_count;
    uint8_t  spw_a_last_receive;
    uint8_t  spw_b_error_count;
    uint8_t  spw_b_last_receive;
    uint16_t spw_a_status;
    uint16_t spw_b_status;

    // for slave
    uint8_t  input_i;
    uint8_t  input_v;
    uint8_t  input_i_v;
    int8_t   i_monitor_u22_temp;
    uint8_t  hv_input_i;
    uint8_t  hv_input_v;
    uint8_t  hv_input_i_v;
    int8_t   i_monitor_u21_temp;

    uint8_t       recv_checksum;
    uint8_t       calc_checksum;
    uint8_t       recv_num;
    uint8_t       tmtc_empty[5];
    unsigned char citiroc1_livetime_buffer_busy[3];
    unsigned char citiroc2_livetime_buffer_busy[3];
    uint8_t       checksum;
} TMTC;

typedef struct Science {
    uint8_t  if_hit;
    Module   gtm_module;

    // for master and slave
    uint16_t pps_counter;
    uint16_t pps_counter_master;
    uint16_t pps_counter_slave;

    // need checking
    uint8_t  cmd_seq_num; // CMD-SAD sequence number

    uint8_t  event_time_buffer_id;
    
    // for master and slave
    uint32_t fine_counter;
    uint32_t fine_counter_master;
    uint32_t fine_counter_slave;

    uint8_t  citiroc_id;
    uint8_t  channel_id;
    uint8_t  energy_filter;
    int16_t  adc_value;
    double   energy;
} Science;

// global variables
extern int decode_mode;
extern int extract_mode;
extern int export_mode;
// extern int hit_mode;
// extern int gain_mode;
extern FILE *bin_infile;
extern FILE *raw_extract_outfile;
extern FILE *raw_outfile;
extern FILE *raw_sync_outfile;
extern FILE *raw_adc_only_outfile;
extern FILE *pipeline_outfile;
extern FILE *pipeline_sync_outfile;
extern FILE *tmtc_master_outfile;
extern FILE *tmtc_slave_outfile;

extern size_t max_binary_buffer_size; // 1GB
extern unsigned char *binary_buffer;

extern unsigned char *sync_data_buffer;
extern unsigned char *sync_data_buffer_master;
extern unsigned char *sync_data_buffer_slave;

extern Time *time_buffer;
extern Time *time_start;
extern Attitude *position_buffer;
extern Attitude *pre_position;
extern Science *event_buffer;
extern TMTC *tmtc_buffer;

extern int sync_data_buffer_counter;
extern int sync_data_buffer_master_counter;
extern int sync_data_buffer_slave_counter;
extern int missing_sync_data;   // =1 after sync data with no tail
extern int missing_sync_data_master;
extern int missing_sync_data_slave;
extern int got_first_sync_data; // =1 after parsing first sync data
extern int got_first_sync_data_master;
extern int got_first_sync_data_slave;

extern int continuous_packet;
// end

/// main ///
void check_endianness(void);
void log_error(const char *Format, ...);
void log_message(const char *Format, ...);
char *str_remove(char *Str, const char *Sub);
char *str_append(char *Prefix, char *Postfix);
void create_all_buffer(void);
void destroy_all_buffer(void);
void open_all_file(char *InputFilePath, char *OutFilePath);
void close_all_file(void);

/// extract science data ///
size_t read_from_file(unsigned char *TargetBuffer, FILE *FileStream, size_t MaxSize);
int is_nspo_header(unsigned char *Target);
void pop_bytes(unsigned char *Target, size_t PopSize, size_t TotalSize);

/// parse science data ///
int find_next_sd_header(unsigned char *Buffer, size_t CurrentSdHeaderLocation, size_t ActualBufferSize);
int is_sd_header(unsigned char *Target);
void parse_science_packet(unsigned char *Buffer, size_t MaxLocation);
static int is_sync_header(unsigned char *Target);
static int is_sync_tail(unsigned char *Target);
static void parse_sync_data(unsigned char *Target);
void big2little_endian(void *Target, size_t TargetSize);
void parse_utc_time_sync(unsigned char *Target);
void parse_position(unsigned char *Target);
int compare_UTC(Time *Time1, Time *Time2);
static void write_sync_data(void);
void get_month_and_mday(void);
double find_time_delta(Time *TimeStart, Time *TimeEnd);
double calc_sec(Time *Time);
static void parse_event_data(unsigned char *Target);
static void write_event_time(void);
static void parse_event_adc(unsigned char *Target);
void left_shift_mem(unsigned char *Target, size_t TargetSize, uint8_t Bits);
static void write_event_buffer(void);
void parse_sd_header(unsigned char *Target);
static void write_sd_header(uint8_t SequenceCount);
void free_got_first_sd_header();

/// parse tmtc data ///
int is_tmtc_header(unsigned char *Target);
int is_tmtc_tail(unsigned char *Targrt);
void parse_tmtc_packet(unsigned char *Target);
void parse_utc_time_tmtc(unsigned char *Target);
void write_tmtc_buffer_all(unsigned char *Target);
void write_tmtc_buffer_master(void);
void write_tmtc_buffer_slave(void);

#endif
