from cx_Freeze import setup, Executable

base = None    

executables = [Executable("main.py", base=base, targetName="Let it Ride.exe")]

include_files = [
    "README.md",
    "LICENSE.md",
    "assets"
]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
        'include_files': include_files
    },    
}

setup(
    name = "Let it ride",
    author = "Micheal Cardy, Bailey D'Amour, and Joseph Miller",
    options = options,
    version = "0.2.0",
    description = 'Final project for MATH 3808',
    license = 'MIT',
    executables = executables
)