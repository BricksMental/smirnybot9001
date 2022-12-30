# smirnybot9001
A twitch chatbot for displaying LEGO sets, minifigs and parts on an HTML overlay

## Installation - Windows

1. Download and Install Python https://www.python.org/downloads/
2. Select a directory to install a Python virtualenv and open a command line with the
following instructions
3. Using Command line, create the venv: `python -m venv VENVDIR`. e.g. `C:\Users\***User***\>python -m venv Smirny_Venv`
4. Activate the venv: `VENVDIR/Scripts/activate.bat` e.g. `C:\Users\***User***\Smirny_Venv\Scripts>activate.bat` 
5. Install the SmirnyBot into the venv `python -m pip install smirnybot9001` e.g. `C:\Users\***User***\Smirny_Venv\Scripts>python -m pip install smirnybot9001`
6. Check that the Bot executables are installed in `VENVDIR/Scripts  smirnyboot9001.exe overlay.exe chatbot.exe`
7. Run `smirnyboot.exe --help` and note the default location of the config file (Usually ` HOMEDIR\smirnybot9001.conf`) e.g. `C:\Users\***User***\Smirny_Venv\Scripts>smirnyboot.exe -h` 
8. Copy the sample config file from `VENVDIR\Lib\site-packages\smirnybot9001\data\sample.conf` to the location noted above (from running `smirnyboot.exe --help`)
9. Create a token for your chatbot twitch user (we recommend using a different user than your personal one) by visiting: https://twitchtokengenerator.com/
10. Configure your newly created token and your channel name (Usually your personal username) in the config file leaving double quotation marks in place
11. Start the bot and overlay using the `smirnyboot9001.exe` executable
12. Browse to http://127.0.0.1:4711 using any browser to ensure that the overlay is running
13. Create a Browser Source in OBS and set the URL to: http://127.0.0.1:4711. Make sure the "Control audio via OBS option is set"
14. Test the bot! Enter `!set 10228` in your chat and see if the overlay displays the wanted set.



## Installation - Linux

The Bot has not been tested under Linux but should work just fine



## ‍☠

