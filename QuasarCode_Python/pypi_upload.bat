@echo off

call .\env\Scripts\activate.bat

python -m build

python -m twine upload dist/*
