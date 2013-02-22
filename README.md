# DROPPER #

Script to share file(s) via Dropbox public folder. Receives from stdin list of absolute paths to files/directories to share. Returns URL to Dropbox shared file. In case of folders or multiple files it compress everything to "archive.zip" and publish it.

You need to change at least `public_user_id` in `cfg` dict to make it work. To obtain `public_user_id` you need to put something to your Dropbox Public folder, right-click on it, and select Dropbox -&gt; Copy Public Link. You'll get url like `https://dl.dropbox.com/u/12345/myfile.txt`. The numbers you see instead of 12345 is your `public_user_id`.

## Using as an service under Mac OSX

 * Put dropper.py somewhere. Let say in `$HOME/bin`
 * Run an "Automator". Select "Service".
 * Select "Service receives selected": "Files and Folders", "in": "Finder"
 * Add action "Run shell script", select `/bin/bash`, "Pass input": "to stdin"
 * Put line `cat | python $HOME/bin/dropper.py`
 * Append action "Copy to clipboard"
 * Save is as "Share with Dropbox"
 
Now select one or multiple file(s) and folder(s), right-click and select "Share with Dropbox". After script finishes you'll have URL in your clipboard.

## Sidenotes

 * It had been tested only under Mac OSX 10.8.

