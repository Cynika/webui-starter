@echo off

if exist "%CD%\venv\pyvenv.cfg" (
echo home =%~dp0Python310> %CD%\venv\pyvenv.cfg
echo include-system-site-packages = false >> %CD%\venv\pyvenv.cfg
echo version = 3.10.6 >> %CD%\venv\pyvenv.cfg
)

set USERPROFILE=%CD%
set PATH=%CD%\Python310;%CD%\Python310\Scripts
set PATH=%CD%\PortableGit;%CD%\PortableGit\bin

set TRANSFORMERS_CACHE=%CD%\.cache\huggingface\transformers
set XDG_CACHE_HOME=%CD%\.cache
set MATPLOTLIBRC=%CD%\.cache

set PYTHONHOME=%CD%\Python310
set PYTHONPATH=%CD%\venv\Lib\site-packages
set GIT=%CD%\PortableGit\bin\git.exe

set PYTHON=%CD%\Python310\Python.exe
set VENV_DIR=venv
set COMMANDLINE_ARGS=--deepdanbooru --xformers --api
 
start http://localhost:7860/

call webui.bat 