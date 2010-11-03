#!/usr/bin/env python
# TOOD(pickhardt) refactor the SHEBANG
# UI for GAM

"""TODO(pickhardt) Refactor - Docstring necessary."""

import sys
import os
from Tkinter import * # TODO(pickhardt) refactor this to simply import Tkinter
import gam
import gam_commands
# Clean up gam_commands for proper use with this user interface library
for entry in gam_commands.commands:
  if gam_commands.commands[entry]['usage'][0:4] == 'gam ':
    gam_commands.commands[entry]['usage'] = gam_commands.commands[entry]['usage'][4:]
import shlex
import time
import tkFont
import webbrowser

def PathFromCurrent(relative_path):
  """Returns the operating system absolute path to a given relative path, from the current directory.
  
  Args:
    relative_path: the relative path to append to the current directory.
    
  Returns:
    This function returns the operating system absolute path to a given relative path, from the current directory.
  """
  path = os.path.dirname(os.path.abspath(sys.argv[0]))
  if os.path.abspath('/') != -1:
    divider = '/'
  else:
    divider = '\\'
  return path+divider+relative_path

class MyApp:
  """TODO(pickhardt)"""
  def __init__(self, parent):
    """TODO(pickhardt)"""
    self.parent = parent
    self.parent.title("Google Apps Shell")
    
    # build header frame
    self.header_frame = Frame(parent)
    self.header_frame.pack()
    self.MakeHeaderFrame(self.header_frame)
    
    # build help frame
    self.help_frame = Frame(parent)
    self.help_frame.pack()
    self.MakeHelpFrame(self.help_frame)
    
    # build credential frame
    self.credential_frame = Frame(parent, pady=40)
    self.credential_frame.pack()
    self.MakeCredentialFrame(self.credential_frame)
    
    # build command line frame
    self.command_frame = Frame(parent)
    self.command_frame.pack()
    self.MakeCommandFrame(self.command_frame)
    
    # build error frame
    self.error_frame = Frame(parent)
    self.error_frame.pack()
    self.MakeErrorFrame(self.error_frame)
    
    # build input/outputs
    self.extra_frame = Frame(parent)
    self.extra_frame.pack()
    self.MakeExtraFrame(self.extra_frame)
    
    # try to auto log in
    try:
      self.AutoLogIn()
    except:
      self.log_in_frame.pack()
  
  def MakeHelpFrame(self, parent_frame):
    self.current_help_command = ''
    
    self.help_button = Button(parent_frame, text="Open Documentation")
    self.help_button.pack(side=LEFT)
    self.help_button.bind("<Button-1>", self.PopHelp)
    self.help_button.bind("<Return>", self.PopHelp)
    
    self.website_button = Button(parent_frame, text="Open Website")
    self.website_button.pack(side=LEFT)
    self.website_button.bind("<Button-1>", self.OpenProjectWebsite)
    self.website_button.bind("<Return>", self.OpenProjectWebsite)
  
  def OpenProjectWebsite(self, event, url='http://code.google.com/p/google-apps-manager/'):
    """Opens the project website.
    
    Args:
      self: The object.
      event: The event calling this method.
      url: The url of the project website.
    
    Returns:
      Nothing.
    """
    webbrowser.open(url)
    
  def PopHelp(self, event, total_width=600):
    """Pops up a help dialog, allowing the user to get extra help.
    
    Args:
      self: The object.
      event: The event calling this method.
    
    Returns:
      Nothing.
    """
    helper_frame = Toplevel(width=total_width)
    helper_frame.title("Help")
        
    label = Label(helper_frame, text="Help")
    label.pack()
    
    help_menu_list = []
    for entry in gam_commands.commands:
      if entry!='_TEMPLATE':
        if 'category' in gam_commands.commands[entry]:
          command_entry = gam_commands.commands[entry]['category'] + ' > ' + gam_commands.commands[entry]['title']
        else:
          command_entry = gam_commands['title']
        help_menu_list.append((command_entry,entry))
    
    help_menu_list = sorted(help_menu_list, key=lambda entry: entry[0])
    help_menu = Menubutton(helper_frame,text='Select category...')
    help_menu.menu = Menu(help_menu)
    for entry in help_menu_list:
      help_menu.menu.add_command(label=entry[0], command=self.HelpFunction(entry[1]))
      
    help_menu.pack()
    help_menu['menu'] = help_menu.menu
    
    self.help_description = Label(helper_frame, wraplength=(total_width-50), justify=CENTER, padx=25)
    #self.help_description = Text(helper_frame, relief=FLAT)
    self.help_description.pack()
    
    button = Button(helper_frame, text="Copy to Execute Field", command=self.CopyHelpCommandToExecuteField)
    button.pack()

    button = Button(helper_frame, text="Close Help", command=helper_frame.destroy)
    button.pack()
  
  def CopyHelpCommandToExecuteField(self):
    currentCommand = str(self.command_field.get())
    textToAdd = self.current_help_command
    if currentCommand:
      textToAdd = '; '+textToAdd
    self.command_field.insert(END, textToAdd)
    self.command_field.focus_force()
  
  def HelpFunction(self, help_with):
    help_object = gam_commands.commands[help_with]
    def HelpForGivenEntry():
      example_strings = ["  %s\n%s\n\n" % (example[0], example[1]) for example in help_object['examples']]
      full_example_string = "\n".join(example_strings)
      helpful_description_text = """
Usage:
%s

Description:%s

Examples:
%s
""" % (help_object['usage'],help_object['description'],full_example_string)
      self.help_description.configure(text=helpful_description_text)
      self.current_help_command = help_object['usage']
    return HelpForGivenEntry
  
  def MakeExtraFrame(self, parent_frame):
    """TODO(pickhardt)"""
    self.left_container = Frame(parent_frame, bd=30)
    self.left_container.pack(side=LEFT)
        
    self.right_container = Frame(parent_frame, bd=30)
    self.right_container.pack(side=LEFT)
    
    ## Master template container ##
    label = Label(self.left_container, text='Master Template: (optional)')
    label.pack()
    
    temp_container = Frame(self.left_container)
    temp_container.pack()
    
    self.input_from = Entry(temp_container, width=30)
    self.input_from.configure(text="~/Desktop/master.txt")
    self.input_from.pack(side=LEFT)
    self.input_from.bind("<Return>", self.LoadInput)
    
    self.reload_button = Button(temp_container, text="Load")
    self.reload_button.pack(side=RIGHT)
    self.reload_button.bind("<Button-1>", self.LoadInput)
    self.reload_button.bind("<Return>", self.LoadInput)
    
    self.input_text = self.MakeTextFrame(self.left_container)
    
    ## Output container ##
    label = Label(self.right_container, text='Output File: (optional)')
    label.pack()
    
    temp_container2 = Frame(self.right_container)
    temp_container2.pack()
    
    self.output_to = Entry(temp_container2, width=30)
    self.output_to.configure(text="~/Desktop/output.txt")
    self.output_to.pack(side=LEFT)
    self.output_to.bind("<Return>", self.ClearOutput)
    
    self.clear_button = Button(temp_container2, text="Clear")
    self.clear_button.pack(side=RIGHT)
    self.clear_button.bind("<Button-1>", self.ClearOutput)
    self.clear_button.bind("<Return>", self.ClearOutput)
    
    self.output_text = self.MakeTextFrame(self.right_container)
      
  def MakeHeaderFrame(self, parent_frame):
    """TODO(pickhardt)"""
    big_font = tkFont.Font(family="Arial", size=24)
    
    label = Label(parent_frame, font=big_font, text='Google Apps Shell')
    label.pack()
    
    #photo = PhotoImage(file=PathFromCurrent("gam_logo.gif"))
    #photo_label = Label(parent_frame, image=photo)
    #photo_label.photo = photo
    #photo_label.pack()
  
  def MakeErrorFrame(self, parent_frame):
    """TODO(pickhardt)"""
    self.standard_error_label = Label(parent_frame, text='')
    self.standard_error_label.pack()
    
  def MakeTextFrame(self, frame, withScroll=True):
    """Define a new frame and put a text area in it."""
    text_frame=Frame(frame, relief=RIDGE, borderwidth=2)
    
    text=Text(text_frame,height=10,width=50,background='white')
    text.pack(side=LEFT)
    
    # put a scroll bar in the frame
    scroll=Scrollbar(text_frame)
    text.configure(yscrollcommand=scroll.set)
    scroll.pack(side=RIGHT,fill=Y)
    scroll.configure(command=text.yview)
    
    #pack everything
    text_frame.pack()
    return text
  
  def MakeCredentialFrame(self, parent_frame):
    """Builds the credential frame, which includes logged in/out info."""
    Label(parent_frame, text='Credentials').pack()
    
    self.log_in_frame = Frame(parent_frame)
    self.log_out_frame = Frame(parent_frame)
    
    username_label = Label(self.log_in_frame, text='Full username: (e.g. admin@domain.com)')
    username_label.pack()
    self.log_in_username = Entry(self.log_in_frame, width=30)
    self.log_in_username.pack()
    self.log_in_username.bind("<Return>", self.LogIn)
    
    password_label = Label(self.log_in_frame, text='Password:')
    password_label.pack()
    self.log_in_password = Entry(self.log_in_frame, width=30, show='*')
    self.log_in_password.pack()
    self.log_in_password.bind("<Return>", self.LogIn)
    
    self.log_in_button = Button(self.log_in_frame, text="Sign In")
    self.log_in_button.bind("<Button-1>", self.LogIn)
    self.log_in_button.bind("<Return>", self.LogIn)
    self.log_in_button.pack()
    
    self.log_out_label = Label(self.log_out_frame, text='Currently signed in to _____.')
    self.log_out_label.pack()
    
    self.log_out_button = Button(self.log_out_frame, text="Sign Out")
    self.log_out_button.bind("<Button-1>", self.LogOut)
    self.log_out_button.bind("<Return>", self.LogOut)
    self.log_out_button.pack()
  
  def MakeCommandFrame(self, parent_frame):
    """TODO(pickhardt)"""
    self.command_field = Entry(parent_frame, width=90, justify=CENTER)
    self.command_field.pack(side=LEFT)
    self.command_field.bind("<Return>", self.RunExecute)
    #self.command_field.focus_force()

    self.execute_button = Button(parent_frame, text="Execute")
    self.execute_button.pack(side=RIGHT)
    self.execute_button.bind("<Button-1>", self.RunExecute)
    self.execute_button.bind("<Return>", self.RunExecute)
  
  def RunExecute(self, event):
    """TODO(pickhardt)"""
    master_template_lines = self.input_text.get(1.0,END)
    master_template_lines = master_template_lines.split("\n")
    master_template = []
    for line in master_template_lines:
      if line:
        # only take the lines that contain text
        master_template.append(str(line))
    raw_command = self.command_field.get()
    commands = raw_command.split(';')
    self.RunCommands(commands, master_template)
  
  def RunCommands(self, commands, master_template=[]):
    """TODO(pickhardt)"""
    if not master_template:
      master_template = ['']
    for template in master_template:
      mapping = template.split(',')
      for temp_command in commands:
        command = temp_command.strip()
        if not command:
          continue
        for index in range(len(mapping)):
          #command = command.replace('\x00','') # no idea why this is happening...
          command = command.replace('{%d}' % (index+1), mapping[index].strip()) # Replace {i} with the value from the template.
        # Command now contains the right variables.
        # Execute it.
        command_list = [entry for entry in shlex.split(command)]
        sys.argv = [sys.argv[0]] # TODO(pickhardt) refactor the sys.argv into gam
        sys.argv.extend(command_list)
        try:
          sys.stderr.write('Executing: '+command)
          gam.execute() # requires arguments passed as sys.argv
          sys.stderr.write('Finished executing: '+command)
        except StandardError, e:
          sys.stderr.write(e)
        
  def LoadInput(self, event):
    """TODO(pickhardt)"""
    self.input_text.delete('1.0', END)
    try:
      with open(PathFromCurrent(self.input_from.get())) as input_file:
        self.input_text.insert('1.0', input_file.read())
    except:
      self.input_text.insert('1.0', 'Error reading file.')
  
  def ClearOutput(self, event):
    """Clears the output text."""
    # Commented out: deleting the output file. 
    #output_path = getOutputPath()
    #if os.path.exists(output_path):
    #  os.remove(output_path)
    self.output_text.delete('1.0', END)
  
  def LogOut(self, event):
    """TODO(pickhardt)"""
    # GAM specific code
    # delete token file
    token_file_path = gam.getTokenPath()
    if os.path.exists(token_file_path):
      os.remove(token_file_path)
    
    # delete auth file
    auth_file_path = gam.getAuthPath()
    if os.path.exists(auth_file_path):
      os.remove(auth_file_path)
    
    gam.domain = ''
    self.log_in_frame.pack()
    self.log_out_frame.pack_forget()
  
  def AutoLogIn(self):
    """TODO(pickhardt)"""
    apps = gam.getAppsObject()
    # if we get here, then we've successfully logged in
    self.log_out_label.configure(text='Currently signed in to '+apps.domain)
    self.log_in_frame.pack_forget()
    self.log_out_frame.pack()
  
  def LogIn(self, event):
    """TODO(pickhardt)"""
    fullUsername = self.log_in_username.get()
    password = self.log_in_password.get()
    try:
      username = fullUsername.split('@')[0]
      domain = fullUsername.split('@')[1]
    except:
      sys.stderr.write('Username must be of form: name@domain.com')
    
    apps = gam.getAppsObject(True, username, domain, password)
    # if we get here, then we've successfully logged in
    self.log_out_label.configure(text='Currently signed in to '+apps.domain)
    self.log_in_password.configure(text='')
    self.log_in_frame.pack_forget()
    self.log_out_frame.pack()
  
  def WriteOutput(self, text):
    """TODO(pickhardt) writes output."""
    try:
      with open(PathFromCurrent(self.output_to.get()), 'a') as output_file:
        output_file.write(text)
    except:
      pass
    self.output_text.insert(END, text)
    #self.output_text.update()
  
  def WriteError(self, text):
    """Writes error output.""" # TODO
    self.standard_error_label.configure(text=text)
    #self.standard_error_label.update()

  
root = Tk()
my_app = MyApp(root)

class StdOut:
  """A class holding the write function for writing the output of commands."""
  def __init__(self, app):
    self.app = app
  
  def write(self, text):
    """Writes output."""
    self.app.WriteOutput(text)
    self.app.extra_frame.update_idletasks()

std_out = StdOut(my_app)
sys.stdout = std_out
    
class StdErr:
  """A class holding the write function for writing errors (or really, writing anything, not necessarily errors, that shouldn't be pushed to the output file)."""
  def __init__(self, app):
    self.app = app
  
  def write(self, text):
    """Writes error output."""
    self.app.WriteError(text)
    self.app.error_frame.update_idletasks()

#std_err = StdErr(my_app)
#sys.stderr = std_err

if __name__ == '__main__':
  root.mainloop()
