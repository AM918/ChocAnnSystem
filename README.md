This is a project for COMP370.
Project by: Ahmed Almogeet (Coding/Design), Benjamin Friesen (Coding/Design), Michael Bennett (Coding/Design)

This project was programmed in Python using the package PyQt5.

As PyQt5 requires SIPS, this project can only be successfully run with Python 3.5 (unless a compatible version of PyQt5 & SIPS are built from source)

The package PyQt5 which can be installed via:
`pip install PyQt5` (or, potentially, `pip3 install PyQt5`)

I have bundled this project with a portable Python virtual environment, custom set up to work. 

To run the project without any hassle, run in command line from the project's root:
pyqt_env\Scripts\activate
pyqt_env\Scripts\python.exe main.py

Due to issues with relative paths, this will only work if run from the R: directory, the only directory that is constant in pathname for all users. (As far as I'm aware.) You should be able to run the project from the R: directory by pasting it into the top-level R:/ folder and then opening it in the commandline window and executing the scripts above. The folder must be renamed to `comp370-project` - again, this is due to pathing issues, according to where exactly the python executable I've bundled with the project was at the time of creating the virtual environment.
