@echo off

call .\env\Scripts\activate.bat

rm .\dist\*

python -m build

python -m twine upload dist/*
