# Introduction #

Google Apps Shell Interface (GASI) is a graphical user interface designed to simplify use of Google Apps API commands.  The commands available are those from the Google Apps Shell (GAS).

Google Apps Shell (GAS) is a script enabling Google Apps administrators to leverage the Google Apps APIs without making their own program.



This project hosts both GASI and GAS.

# Details #

The Google Apps Shell Interface makes it simple to programmatically issue commands to your Google Apps account.  It allows users to programmatically execute commands from both GAS without having to write a bash script.  Some use cases include:
  * Changing every user's signature to a custom signature including their email address.
  * Moving every user from one domain to another, then removing the old user alias.
  * ...and many other interesting combination of Google Apps API commands.

GAS was influenced by the open source project Google Apps Manager (GAM), but is distinct from GAM.

# Download #

To download the most recent version of Google Apps Shell, use the following link:

[Download gasi.zip (right click and select save as)](http://google-apps-shell.googlecode.com/svn/trunk/gasi.zip)


# Install #

Installation is straightforward so long as you have Python installed.
  1. Download gasi.zip
  1. Unzip gasi.zip
  1. On Mac OS X, double click on gasi.app located in the mac\_app folder.
  1. On Windows, double click on gasi.exe located in the windows\_app directory.
  1. If the executable fails to run on your computer, it is probably because the executable was built on a computer with different specs from yours. You can still use GASI by executing gasi.py through a command line. (In the future, an installer may be provided to build GASI on the target machine)
  1. To execute gasi.py from the command line interface, navigate to the gasi directory. Then execute a command to open gasi.py with Python. This command is typically "python gasi.py"

If you are not sure if you have Python installed, try running the command "python gasi.py" anyway.  If you don't have Python installed, you can get it at [python.org](http://www.python.org/).


# Getting Started #

Once you have successfully installed and opened GASI, you are ready to read the [Getting Started with GASI](http://code.google.com/p/google-apps-shell/wiki/GettingStarted) documentation.