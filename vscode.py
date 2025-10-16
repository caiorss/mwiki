#!/usr/bin/env python
"""
Python script for generating .vscode/settings.json and .vscode/launch.json 
files  for Vscode (Visual Studio Code) and Pipenv integration, 
enabling intelisense, code completion, debugging and unit
test discovery.

Usage:

STEP 1: 
  Go to project root directory in terminal and run:

       $ python vscode.py 
     
     Or
      
      $ ./vscode.py 
     
     Or
     
      $ make vscode

STEP 2: 
   Type Ctrl + P to open the command pallet and select the command 
   'Select the Intepreter', then select the Python interpreter of the 
   Virtualenv path.
     
 References:

   + https://code.visualstudio.com/docs/python/environments
   + https://pconwell.github.io/cheat/python-vscode-pipenv.html
   + https://dev.to/vorsprung/vscode-pipenv-python-34pf

"""

import sys
import os
import pathlib 

def mkdir(path: str):
  import os
  try:
    os.makedirs(path)
  except OSError:
    pass

def get_proc_output(args):
    import subprocess 
    proc = subprocess.run(args, capture_output = True, text = True)
    ret = proc.returncode 
    stdout = proc.stdout
    out = (ret, stdout.strip())
    return out


# Get user directory in platform-independet way
HOMEDIR = str(pathlib.Path.home())
#### (status, PIPENVPATH) = get_proc_output(["pipenv", "--venv"])
#### PIPENVPATH = PIPENVPATH.strip()

## VENVPATH    = ""
## PYTHONPATH  = ""

(status, PYTHONPATH) = get_proc_output(["poetry", "env", "info", "--executable"])
(status, VENVPATH)   = get_proc_output(["poetry", "env", "info", "--path"])

### if "linux" in sys.platform:
###     ## VENVPATH = f"{HOMEDIR}/.local/share/virtualenvs"
###     ###PYTHONPATH = f"{PIPENVPATH}/bin/python"
### # Not tested on Windows yet
### elif "windows" in sys.platform:
###     VENVPATH = f"{HOMEDIR}/.virtualenvs"
###     PYTHONPATH = f"{PIPENVPATH}/bin/Scripts/python.exe"
### else:
###     raise NotImplementedError(f"Not implemented for this operating system: '{sys.platform}'")


## Content of .vscode/settings.json 
## Project settings (aka configuration)
content_settings = """
{
    "files.exclude": {
          "**/.git": true
        , "**/.svn": true
        , "**/.hg": true
        , "**/CVS": true
        , "**/.DS_Store": true
        , "**/*.pyc": true
        , "**/__pycache__": true
        , "**/flask_session": true
    }
    , "python.pythonPath": "{{PYTHONPATH}}"
    , "python.venvPath": "{{VENVPATH}}"
    , "code-runner.executorMap": {
        "python": "$pythonPath $fullFileName",
    }
    , "code-runner.runInTerminal": true

    , "python.testing.pytestArgs": [
        "."
    ]
    , "python.testing.unittestEnabled": false
    , "python.testing.pytestEnabled": true    
    , "pyhton.linting.enabled": true 
    , "python.linting.PylintEnabled": true 
}
"""

content_settings = ( content_settings
                .strip()
                .replace("{{VENVPATH}}",    VENVPATH) 
                .replace("{{PYTHONPATH}}", PYTHONPATH) 
            )


## Content of .vscode/launch.json 
## Debugging settings 
launch_settinngs = """
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        
        {
              "name": "Python: Current file"
            , "type":    "python"
            , "request": "launch"
            , "program": "${file}"
            , "console": "integratedTerminal"
        }
    ]
}
"""

launch_settinngs = launch_settinngs.strip()

print(" [INFO] Content of file .vscode/settings.json:")
print(content_settings)
print(" [INFO] Content of file .vscode/launch.json:")
print(launch_settinngs)

# Create .vscode folder
mkdir(".vscode")

with open(".vscode/settings.json", "w") as fd:
   fd.write(content_settings)

with open(".vscode/launch.json", "w") as fd:
   fd.write(launch_settinngs)

print(" [INFO] Finished Ok.")



