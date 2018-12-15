from cx_Freeze import setup, Executable

base = None    

executables = [Executable("main.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "Let it ride",
    options = options,
    version = "0.1.0",
    description = '',
    executables = executables,
    include_package_data = True
)