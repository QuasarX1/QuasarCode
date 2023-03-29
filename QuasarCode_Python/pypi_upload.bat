@echo off

call .\env\Scripts\activate.bat

del /F /Q .\dist\*

python -m build

python -m twine upload dist/*
