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
    options = options,
    version = "0.1.0",
    description = '',
    executables = executables
)