# Welcome to SDRDPy

SDRDPy is an application designed for graphically visualizing knowledge obtained through supervised descriptive rule algorithms.

## Requirements 
The required version of Windows is 10 or later, and it is only for 64-bit devices. It is a lightweight tool, so a powerful RAM and CPU are **not** necessary.

## Installation Manual
To learn how to install the application, click [here](Manuals/Installation_Manual.md).

## User Guide
To understand how to use the application, click [here](Manuals/User_Guide.md).

## Including New Algorithms
To discover how to include new algorithms in the application, click [here](Manuals/Including_new_algorithms.md).

## Project Architecture
- In the "assets" folder, you'll find the logo and the image used in the application.
- The Windows executable is located in `Executable Windows` for using the application on Windows.
- The `lectura_ficheros` directory includes the .py files that read the rule files of the corresponding algorithm with the same name.
- Different user manuals are stored in the `Manuals` directory.
- Implementation of various screens in the `screens` directory.
- General implementations for the entire application, such as rule evaluation, constants, style, and the rule class, can be found in the `utils` directory.
- The `main.py` file initiates the application.
- The `Manager.py` file handles window transitions within the application.
