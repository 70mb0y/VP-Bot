# VP-Bot
Automate the VP based on alliance name for approval.

You can break out of the code - stop running it by using <Ctrl> + <c> buttons.

There are some personal preferences in here but do as you wish and what makes life simpler for you.
Visual Studio Code is easy way to run it or cmd or powershell, whatever your flavor.

There are currently 5 second delays between actions, which seem long, however when running behind protective walls delays in screen load can occur and the 5 seconds helps prevent the clicking from being disassocated to the correct position on the screen due to loading lag.

Steps:
Install python:  https://www.python.org/downloads/   during installation I recommend including PATH on the first screen of the install, it simplifies things.

Install Visual Studio Code (if desired): https://code.visualstudio.com/download

Install Tesseract-OCR: https://docs.coro.net/featured/agent/install-tesseract-windows/

Install Last War on the PC, you can chose to run behind an emulator if desired, this will not impact the bot since it runs 100% off of pixel locations.
 - If you are super nerdy and want to run it on a mobile device you can also use a terminal emulator on a mobile to perform the setup.

In commandlines or code:
You will need to run "pip install" for several of the import calls for the code one of the most important being pyautogui as it holds many of the dependencies.

MouseLocation.py will assist in inputting the proper locations in the code where a "click" is required for approval and rejections as well as cycling through the titles. 

ScrollUp.py will assist with the "list" when it is longer than the initial display.  You will need to use MouseLocation.py to identify where the mouse position needs to start. Then also, the top item on the list and then measure to the bottom of the list box, not the actual list.  Do the math to identify how much Y is from the top of this box to the bottom and this will be the input in the script to allow the drag motion to occur properly.

TestOCR.py will assist in ensuring the alliance name is being read properly and may require some movement on location to get the alliance name inside the "box".

VPBot.py is the main code that will need updated with:
 - Line 13: the file path to tesseract.exe
 - Line 15: the alliance names that are approved to get buffs
 - Line 34: The name/list region, where it picks up the alliance name within the "list"
 - Line 19-23: locations for the titles to be selected
 - Line 27-31: the "list" access button, where the approve, reject, and confirm buttons are, and where to close/exit out of the windows.
 - Line 41-44: the "click drag" configuration.  This will help in preventing location issues during the approvals when the list grows longer than the initial screen load length.




