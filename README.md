# Squawk!

Squawk! is a small utility originally created to generate valid transponder
codes for flight simulation flights that aren't ATC-controlled.

Additionally it includes a top of descent calculator and it can pull METAR/TAF
information from the real world (your simulator's weather may differ).

## Building

To build Squawk!, after cloning the repository to a local folder, set up a
virtual environment in that folder:

```
python -m venv .
```

After activating the environment, install the dependencies from PIP:

```
pip install -r requirements.txt
```

Then, build Squawk! by running:

```
pyinstaller --clean --noconfirm squawk.spec
```

There will be an executable file created in the `dist` folder.
