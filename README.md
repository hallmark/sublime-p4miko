Sublime Text 2 Perforce-over-SSH Plugin
=======================================

## Installation

  Currently, the best way to install the `sublime-p4miko` plugin is to download the ZIP file and unzip it into the following location:
  
      /Users/<username>/Library/Application Support/Sublime Text 2/Packages/
  
  Hint: To view the `Library` folder in the Finder, click on the Go menu, hold down the Option key, and you should see the Library folder as a menu item.

  You will also need to add a User settings file, ensure that the `paramiko` python package is installed, and optionally add a Sublime project-specific setting.
  
  Create a new file in Sublime and save it to this location:
  
      /Users/<username>/Library/Application Support/Sublime Text 2/Packages/User/p4miko.sublime-settings
  
  Hint: Having trouble saving to the hidden `Library` folder? In the Save dialog, hit Command-Shift-`.` to toggle display of hidden files and folders.
  
  The plugin user settings file `p4miko.sublime-settings` should look something like this:

```js
{
  "perforce_ssh_host": "myserverbox.example.com",
  "perforce_local_client_prefix": "/Volumes/jdoe/src",
  "perforce_ssh_remote_client_prefix": "/home/jdoe/src"
}
```

  To configure a particular Sublime project so that the `p4 opened` command is enabled, edit the project settings (menu Project -> Edit Project) and add the `perforce_remote_project_prefix` setting as in this example:

```js
{
  "folders": [],
  "settings":
  {
    "perforce_remote_project_prefix": "/home/<username>/src/myproject/main"
  }
}
```

If the plugin still does not appear to work (you may see a brief warning message in the bottom status bar that says, "Install paramiko locally to enable p4miko plugin"), install the `paramiko` Python package for your Mac.  Sublime Text is configured to use Python 2.6, so you will need to install `paramiko` for Python 2.6:

      $ sudo easy_install-2.6 paramiko

Finally, if the plugin does not appear to be picking up your most recent configuration or Python package installation changes, restart Sublime Text 2 and try again.

## Quick Start

To view the opened files in a project, press Control-Shift-O.  
To checkout/open a file for edit, press Control-Shift-E.  
To revert changes for a file, press Control-Shift-R.  
To add a file, press Control-Shift-I.  

## Features

  * p4 edit
  * p4 revert
  * p4 opened
  * p4 add

## License 

(The MIT License)

Copyright (c) 2013 Mark Ture &lt;mark.ture@gmail.com&gt;

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
