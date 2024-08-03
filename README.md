# Squawk!

Squawk! is a small utility originally created to generate valid transponder
codes for flight simulation flights that aren't ATC-controlled.

Additionally it can pull METAR/TAF information from the real world (your
simulator's weather may differ).

## Building

To build Squawk!, it is recommended to setup a Python virtual environment:

```
python -m venv squawk
```

After activating the environment, install the dependencies from PIP:

```
pip install wxpython pyinstaller
```

Then, after pulling in the `squawk.py` and `squawk.ico` files, build Squawk!
by running:

```
pyinstaller --onefile --noconsole --icon=squawk.ico --add-data "squawk.ico:." squawk.py
```

There will be an executable file created in the `dist` folder.
