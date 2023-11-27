# Software Engineering (3)

**Made by:**
- Oliver Lind Kristiansen
- Nontagan Phomin
- Erik Evjen
- Sakariya Adan Mahamud
- Stephen Stenberg

**The project documentation and the individual attachments are inside the documentation folder.**

Link til github repository: https://github.com/olindkri/SE-G3

Make sure you have Python 3.8 or newer installed.
Python version downloads:
https://www.python.org/downloads/

## Prototype

**Write the following commands in the terminal or powershell:**
> Make sure you are inside the /SE-G3 directory.

&nbsp;&nbsp;&nbsp;&nbsp;`pip install virtualenv`

&nbsp;&nbsp;&nbsp;&nbsp;`python -m venv env`

&nbsp;&nbsp;&nbsp;&nbsp;`env/Scripts/activate`

&nbsp;&nbsp;&nbsp;&nbsp;`source env/bin/activate`

&nbsp;&nbsp;&nbsp;&nbsp;`pip install -r ./requirements.txt`

<br>

**Now you can run the prototype by typing this command in the terminal:**

&nbsp;&nbsp;&nbsp;&nbsp;`flask run`

## Testing

**Write the following commands in the terminal or powershell:**
> Make sure you are inside the /SE-G3 directory.

If already in virtual environment:

&nbsp;&nbsp;&nbsp;&nbsp;`coverage run -m pytest -s -v test/test_app.py`

&nbsp;&nbsp;&nbsp;&nbsp;`coverage report`

If not in a virtual environment, run the first three lines in the prototype section. Run the testing lines after.

