# GTM/SDC - Decoder
In this document, we will learn how to install and use the decoder developed by NTHU GTM team. This decoder is a cross-platform software, supporting MacOS, Linux and Windows. We can find more details in [Installation](#Installation) section. The purpose of this software is to decode those binary data recorded by GTM on Formosat-8B to human-readable data based on internal GTM definition. Please go [Utility](#Utility) section to understand more.

## Installation

To speed up the decoding process, we use C language to handle heavy memory calculations. In addition, we imported Qt5 libary in Python language to build a friendly user interface (UI) to prevent the user from typing a lot of trivial commands in Terminal to trigger the decoder, such as TeleMetry and TeleCommand (TM/TC) or Science Data (SD), raw or pipeline SD, ..., etc. Therefore, please pre-install [GCC](#GCC) and [Python](#Python) in the device, then we can [Install and Execute Decoder](#Install-and-Execute-Decoder) smoothly.

### GCC

The GNU Compiler Collection (GCC), as it literally means, is a collection of compilers produced by the GNU project, which allowing developers around the world can use this free and powerful tool to compile various programming languages, including C. Furthermore, since our C programs need to be called from Python, instead of linking all compiled object files (.o) into an executable file (.out) with GCC, we actually use GCC to link all compiled object file (.o) together to create a dynamic library (different suffix in each Operation System (OS), please refer to [Install and Execute Decoder](#Install-and-Execute-Decoder) section) to call.

For installation, the process is simpler for <a href="#GCC-MacOS">MacOS</a> and <a href="#GCC-Linux">Linux</a> than <a href="#GCC-Windows">Windows</a> because GNU is Unix-like OS. If the device has not yet been installed with GCC, please move to the corresponding section to learn it.

<a name="GCC-MacOS"></a> 

- #### MacOS

  There are actually two approaches, Xcode and Homebrew, that can help us install GCC in MacOS. However, despite the fact that the former is not essentially GCC (it is Apple's Clang compiler, intentionally designed to be compatible with GCC), the latter takes longer to install and also requires changing the alias from `gcc-#` (# is the version number of GCC) to `gcc`, which is rather inconvenient. Therefore, we recommend using Xcode to install GCC.

  - Open App Store

  - Download Xcode

  - Install GCC (two methods)

    - Method 1: Run the following command in Terminal

      ```
      xcode-select --install
      ```

    - Method 2: Xcode app > Preferences > Downloads > Install Command Line Tools

  - Run `gcc --version` in Terminal to verify a successful installation

<a name="GCC-Linux"></a>

- #### Linux

  - Run the following commands in Terminal

    ```
    sudo apt update
    sudo apt install build-essential
    ```

  - Run `gcc --version` in Terminal to verify a successful installation

<a name="GCC-Windows"></a>

- #### Windows

  The Minimalist GNU for Windows (MinGW) and Cygwin (formerly known as gnuwin32, renamed Cygwin32 to avoid confusion with another GnuWin32 project to emphasize Cygnus' role in developing it , whose number was dropped when Microsoft registered the Win32 trademark) are two well-known projects that provide GCC functionality on Windows.

  Currently, most modern OS prefer 64-bit (because of its faster data speed and ability to address more memory) and use 64-bit edition of Python by default. As a result, MinGW (which only supports 32-bit Windows) is no longer practical. Fortunately, we still can use advanced MinGW-w64 (which supports 32 and 64-bit Windows) to substitute MinGW. 

  Considering that Cygwin effectively provides a Unix-like environment on 32 and 64-bit Windows, it is unfriendly for native Windows users to learn Unix commands. For this reason, we recommend using MinGW-w64 to compile code in Command Prompt on Windows.

  There are several ways can install MinGW-w64. We recommend installing MinGW-w64 by Cygwin (which contains **mingw64-x86_64-gcc-core** and **make** as packages) to take advantage of the graphical user interface (GUI) that Windows is known for to help us simplify the tedious installation process. This approach also eliminates the need to manually set environment variables.

  - Go [Cygwin](https://cygwin.com/install.html) to download **setup-x86_64.exe**
  - Open **setup-x86_64.exe**
  - Click "Next" until see "Select Package"
  - Select "Full" in "View"
  - Type "gcc" in "Search" > Find **mingw64-x86_64-gcc-core** in "Package" > Change "Skip" to lastet version in "New"
  - Type "make" in "Search" > Find **make** in "Package" > Change "Skip" to lastet version in "New"
  - Click "Next" until see "Finish" > Click "Finish"

### Python 

Using miniconda to manage a new clear Python environment

### Install and Execute Decoder

```
cd <your_gui_folder>
make -f Makefile_<your_OS>

conda create -n env_gtm python=3.9 –y
conda activate env_gtm
conda install anaconda::numpy -y
conda install anaconda::pandas -y
conda install conda-forge::matplotlib -y
conda install anaconda::pyqt –y
conda install conda-forge::pyqtgraph -y
conda install anaconda::scipy -y
conda install anaconda::scikit-learn -y
conda install anaconda::astropy -y
conda install conda-forge::skyfield –y(Linux should use "pip install skyfield”!)
conda install esri::pyquaternion -y
conda install conda-forge::shapely –y

python GTM_SDC_Start.py
```



## Utility

...
