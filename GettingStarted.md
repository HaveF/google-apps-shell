# Prerequisites #

This page assumes you have already downloaded and installed GASI. If this is not the case, see the [Project Home](http://code.google.com/p/google-apps-shell/).


# Opening GASI #

  1. On Mac OS X, double click on gasi.app located in the mac\_app folder.
  1. On Windows, double click on gasi.exe located in the windows\_app directory.
  1. If the application fails to open, you may not have Python installed. It does not come pre-installed on Windows, for instance. See below for instructions on installing Python.
  1. If you use Linux or another operating system, you can still run GASI through a command line interface.  To do so, navigate to the gasi directory. Then execute a command to open gasi.py with Python. This command is typically "python gasi.py"

If you are not sure if you have Python installed, try running the command "python gasi.py" anyway.  If you don't have Python installed, you can get it at [python.org](http://www.python.org/).

At this point, you should see the following:

![![](http://google-apps-shell.googlecode.com/svn/trunk/wiki/images/blank.png)](http://google-apps-shell.googlecode.com/svn/trunk/wiki/images/blank.png)

# Authenticating to Google Apps #

In order for GASI to issue commands to your Google Apps, you have to be logged in through GASI.  To log in, enter an administrative username and password. If you have already logged in to GASI without logging out, you should already be logged in when GASI opens.

Once authenticated, you should see something like the following:

![![](http://google-apps-shell.googlecode.com/svn/trunk/wiki/images/authenticated.png)](http://google-apps-shell.googlecode.com/svn/trunk/wiki/images/authenticated.png)


# Issuing a Simple Command #

The graphical user interface GASI can call functions from GAS.  To see what commands you can use, either visit the [Documentation](https://code.google.com/p/google-apps-shell/wiki/Documentation) page or click Open Documentation in GASI.

To browse the possible commands, click Open Documentation.

To execute a command, type in the command and click Execute.  Here is an example of how to rename a user in Google Apps:

![![](http://google-apps-shell.googlecode.com/svn/trunk/wiki/images/rename.png)](http://google-apps-shell.googlecode.com/svn/trunk/wiki/images/simple_command.png)


# Issuing Commands from a Template #

GAS can execute custom commands generated from a CSV.

To use templates, first populate a CSV file with columns for each variable.  For example, the first column might be username, the second column might be firstname, and so on.  Then place the CSV file in the GASI directory, the same directory that the mac\_app and windows\_app directories are found.

Next, load the template to the Master Template in GASI by typing the file name under Master Template and clicking Load (template.csv, for instance). Then find the command you wish to use and enter it in the execution field. When executed, GASI will sequentially run the command for each row in the CSV, replacing any {N} string with the value of the Nth column.

For instance, if you load the template with a CSV containing:

```
John, Lennon, jlennon
Adrian, Peterson, apeterson
```

You could then set their signatures with the command:

`gas update_signature user_name={3}@altostrat.com signature="My name is {1} {2}. Email me at {3}@altostrat.com"`

Executing this command would update both signatures.

Here is a screen shot illustrating commands built from templates:

![![](http://google-apps-shell.googlecode.com/svn/trunk/wiki/images/command_from_template.png)](http://google-apps-shell.googlecode.com/svn/trunk/wiki/images/command_from_template.png)


# Issuing Compound Commands #

GASI can execute multiple commands sequentially. To execute multiple commands, put a semicolon in between each command. For instance, if you wish to create a nickname, as well as update a user's language setting, you could the execute field:

`gas create_nickname nickname=mickey user_name=michael; gas update_language user_name=michael language=en-GB"`

Executing this command would create a nickname "mickey" as well as set Michael's language to en-GB.

Here is a screen shot of a compound command:

![![](http://google-apps-shell.googlecode.com/svn/trunk/wiki/images/compound_command.png)](http://google-apps-shell.googlecode.com/svn/trunk/wiki/images/compound_command.png)


# Issuing Compound Commands from a Template #

Issuing commands from templates and issuing compound commands can be used together. For instance, you could create users as well as update their signature with the following compound command:

`gas create_user user_name={3} first_name={1} last_name={2} password={4}; gas update_signature user_name={3} signature="My name is {1} {2}."`

Here is a screen shot illustrating this concept:

![![](http://google-apps-shell.googlecode.com/svn/trunk/wiki/images/compound_commands_from_template.png)](http://google-apps-shell.googlecode.com/svn/trunk/wiki/images/compound_commands_from_template.png)


# Debugging Errors #

When an error occurs, GASI will output the error code underneath the execution bar.  The full error code can be viewed by clicking the View Last Error button.  Further, GASI logs all executing details in gas\_details\_log.txt.

To understand the error codes, look at the last error interpret the reason listed. For example, in the following screen shot, the error is an AppsForYourDomainException stating there is an invalid input walter2 with the reason EntityDoesNotExist.  In English, what this means is that the user walter2 does not exist in Google Apps, so it cannot be deleted.

![![](http://google-apps-shell.googlecode.com/svn/trunk/wiki/images/error.png)](http://google-apps-shell.googlecode.com/svn/trunk/wiki/images/error.png)