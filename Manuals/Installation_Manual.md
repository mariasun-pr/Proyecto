# Installation Manual 
The application can be started in two different ways. 
1.  **Console:** 
To start the application from the console, it is necessary to follow the following steps:
 1.1. Verify that Python version 3.x.x is installed on the computer. If Python is not installed, Python can be downloaded from the official Python website, and the recommended version 3.11.0 can be selected, as this is the version used in the implementation of the application. 
1.2. Verify that the Matplotlib library is installed. If Matplotlib is not installed, the Matplotlib library can be installed using the following command in the console: `pip install matplotlib` 
1.3. Verify that the Numpy library is installed. If Numpy is not installed, the Numpy library can be installed using the following command in the console: `pip install numpy` 
1.4. Once it has been verified that Python, Matplotlib, and Numpy are installed, the application can be started from the console using the following command: `python [project path]\main.py` Where `project path` is the path to the project folder.


2. **Executable:** 
An executable has been created using pyinstaller that allows running the desktop application on the OS without the need to download Python or any other additional library. 
To run the application, one must select the directory corresponding to their OS and open it. Next, find the `dist` folder and open the `main` directory. Inside this directory, there is a file called `main.exe` with the application icon. Double-clicking on this file will start the application.