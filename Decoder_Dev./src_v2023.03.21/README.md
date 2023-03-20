# GTM/SDC - Decoder
In this document, we will learn how to install and use the decoder developed by NTHU GTM team. This decoder is a cross-platform software, supporting MacOS, Linux and Windows. We can find more details in [Installation](#Installation) section. The purpose of this software is to decode those binary data recorded by GTM on Formosat-8B to human-readable data based on internal GTM definition. Please go [Utility](#Utility) section to understand more.

## Installation

To speed up the decoding process, we use C language to handle heavy memory calculations. In addition, we imported Qt5 libary in Python language to build a friendly user interface (UI) to prevent the user from typing a lot of trivial commands in Terminal to trigger the decoder, such as TeleMetry and TeleCommand (TM/TC) or Science Data (SD), raw or pipeline SD, ..., etc. Therefore, please pre-install [GCC](#GCC) and [Python](#Python) in the device, then we can [Install and Execute Decoder](#Install and Execute Decoder) smoothly.

### GCC

The GNU Compiler Collection (GCC), as it literally means, is a collection of compilers produced by the GNU project, which allowing developers around the world can use this free and powerful tool to compile various programming languages, including C. Furthermore, since our C programs need to be called from Python, instead of linking all compiled object files (.o) into an executable (.out) with GCC, we actually use GCC to link all compiled object file (.o) together to create a dynamic library (different suffix in each Operation System (OS), please refer to [Install and Execute Decoder](#Install and Execute Decoder) section to call.

For installation, the process is simpler for <a href="#GCC_MacOS">MacOS</a> and <a href="#GCC_Linux">Linux</a> than <a href="#GCC_Windows">Windows</a> because GNU is Unix-like OS. If the device has not yet been installed with GCC, please move to the corresponding section to learn it.

- ##### <a id="GCC_MacOS"></a> MacOS

  - 

- ##### <a id="GCC_Linux"></a> Linux

  ```
  sudo apt update
  sudo apt install build-essential
  ```

  `gcc --version` to verify a successful installation

- ##### <a id="GCC_Windows"></a> Windows

  

### Python 

using coda to manage a new clear Python environment

### Install and Execute Decoder

666

## Utility

fffffff
