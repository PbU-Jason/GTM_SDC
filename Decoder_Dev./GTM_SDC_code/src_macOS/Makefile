.c.o:
	gcc -fPIC -c $<

all: GTM_Decoder_Function.o GTM_Decoder_CRC_Check.o GTM_Decoder_Extract_Science_Data.o GTM_Decoder_Parse_Science_Data.o GTM_Decoder_Parse_TMTC_Data.o GTM_Decoder_Parse_Both_TMTC_Science_Data.o GTM_Decoder_Main.o
	gcc -dynamiclib GTM_Decoder_Function.o GTM_Decoder_CRC_Check.o GTM_Decoder_Extract_Science_Data.o GTM_Decoder_Parse_Science_Data.o GTM_Decoder_Parse_TMTC_Data.o GTM_Decoder_Parse_Both_TMTC_Science_Data.o -o libheader.dylib
	gcc -dynamiclib GTM_Decoder_Main.o -Wl,-rpath . -L . -lheader -o GTM_Decoder_Main.dylib
