#!/usr/bin/python
#
# Google Apps Shell
#
# Google Apps Shell is a script allowing Google Apps administrators to issue simple commands to their Apps domain.
# For more information, see http://code.google.com/p/google-apps-shell/
# It was inspired by the Google Apps Manager (see http://code.google.com/p/google-apps/manager/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Apps Shell is a script allowing Google Apps administrators to issue simple commands to their Apps domain."""

__author__ = 'jeffpickhardt@google.com (Jeff Pickhardt)'
__version__ = '1.1.3'
__license__ = 'Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0)'

import sys, os, time, datetime, random, cgi, socket, urllib, csv
from sys import exit
import gdata.apps.service
import gdata.apps.emailsettings.service
import gdata.apps.adminsettings.service
import gdata.apps.groups.service
import gdata.apps.audit.service
import gdata.apps.multidomain.service
import gdata.apps.orgs.service
import gdata.apps.res_cal.service
from hashlib import sha1
import getpass

## VARIOUS HELPER FUNCTIONS ##
def str_to_bool(string, case_sensitive=False, true_words=['true', 'on'], false_words=['false', 'off']):
    if not case_sensitive:
        string = string.lower()
    if string in true_words:
        return True
    elif string in false_words:
        return False
    else:
        raise Exception('Could not convert %s to a boolean.' % string)    

## CREDENTIALS / AUTHENTICATION RELATED STUFF ##
class Credentials:
    def __init__(self, email='', password=''):
        """Comments"""
        
        if len(email):
            split = email.split('@')
            self.username = split[0]
            self.domain = split[1]
            self.password = password
        else:
            self.username = ''
            self.domain = ''
            self.password = ''
            # self.log_in will attempt to use last authentication token used
          
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
        if os.path.abspath('/') != -1:
            divider = '/'
        else:
            divider = '\\'
        self.token_path = path+divider+'gas_credential_log.txt'
        self.log_in()
    
    def get_email(self):
        """Returns the email address made up from the username and domain name."""
        return self.username+'@'+self.domain
    
    def get_username(self):
        """Returns the currently logged in username."""
        return self.username
    
    def get_domain(self):
        """Returns the currently logged in domain name."""
        return self.domain
    
    def credential_line_to_list(self, line):
        split_line = line.split(',')
        split_line = [new_line.strip() for new_line in split_line]
        
        if len(split_line)==5:
            return split_line # in format date, activity, username, domain, token
        else:
            return ['','','','','']
        
    def last_credentials(self):
        # First checks to see whether the username/password combination has a token from Google.
        try:
            if os.path.isfile(self.token_path):
                token_file = open(self.token_path, 'r')
                token_fileLines = token_file.readlines()
                token_file.close()
            
                last_line = token_fileLines[-1] # the last line in the file should be the most up-to-date authorization token
                return self.credential_line_to_list(last_line)
            else:
                return ['','','','','']
        except:
            return ['','','','','']

    def get_email_settings_object(self):
        try:
            return self.EmailSettings
        except:
            self.EmailSettings = gdata.apps.emailsettings.service.EmailSettingsService(domain=self.domain)
            self.EmailSettings.SetClientLoginToken(self.service.current_token.get_token_string())
            return self.EmailSettings

    def log_in(self):
        """Authorizes the username, domain, and password with Google.  Stores a token in the text file tokens.txt"""
        is_authorized = False
        
        # First checks to see whether the username/password combination has a token from Google.
        (line_date, line_activity, line_username, line_domain, line_token) = self.last_credentials()
        if (line_username==self.username and line_domain==self.domain) or self.username=='':
            # Either the token matches, or no username was given, in which case we'll try the last token.
            try:
                service = gdata.apps.service.AppsService(domain=line_domain)
                service.SetClientLoginToken(line_token)
                service.RetrieveUser(line_username) # test that we're successfully authorized
                
                is_authorized = True
                self.domain = line_domain
                self.username = line_username
                self.token=line_token
            except gdata.apps.service.AppsForYourDomainException, e:
                pass
            except socket.error, e:
                raise Exception("Failed to connect to Google's servers.")
        
        if not is_authorized:
            service = gdata.apps.service.AppsService(email=self.get_email(), domain=self.domain, password=self.password)
            try:
                service.ProgrammaticLogin()
                service.RetrieveUser(self.username) # test that we're successfully authorized
                is_authorized = True
            except gdata.service.BadAuthentication, e:
                raise Exception("Invalid username and password combination. Please try again.")
            except gdata.apps.service.AppsForYourDomainException, e:
                raise Exception ("Either the user you entered is not a Google Apps Administrator or the Provisioning API is not enabled for your domain. Please see: http://www.google.com/support/a/bin/answer.py?hl=en&answer=60757")
            except socket.error, e:
                raise Exception("Failed to connect to Google's servers.")
            
            self.token = service.current_token.get_token_string()
            
            token_file = open(self.token_path, 'a')
            token_file.write("\n"+time.asctime() + ',log_in,' + self.username + ',' + self.domain + ',' + self.token)
            token_file.close()
            
        self.service = service
        return service
    
    def log_out(self):
        """Removes the authentication token from the token file, and adds a log out activity."""
        
        token_file = open(self.token_path, 'r')
        token_lines = token_file.readlines()
        token_file.close()
        
        token_file = open(self.token_path, 'w')
        for line in token_lines:
            (line_date, line_activity, line_username, line_domain, line_token) = self.credential_line_to_list(line)
            if line_activity=='log_in' and line_token==self.token:
                token_file.write(line_date + ',log_in,' + line_username + ',' + line_domain + ',' + 'removed')
            else:
                token_file.write(line)
        token_file.write("\n"+time.asctime() + ',log_out,' + self.username + ',' + self.domain + ',no_token')
        token_file.close()
        
        self.username = ''
        self.domain = ''
        self.token = ''
        self.service = False

def log_in(email='', password=''):
    """Logs in with the credentials provided by the email and password arguments."""
    credential = Credentials(email=args[1], password=args[2])
    return credential

def log_out(credential):
    """Logs out of the current credentials."""
    credential.log_out()
    
def print_authentication(credential=None):
    """Prints output explaining the current authentication status."""
    try:
        if not credential:
            credential = Credentials()
        log('Currently authenticated as %s to %s' % (credential.get_email(), credential.get_domain()))
    except:
        log('GAS is not currently signed in to Google.')

## USER FUNCTIONS ##
def create_user(credential, user_name, first_name, last_name, password, password_hash_function=None, suspended='false', quota_limit=None, change_password=None):
    """Creates a user."""
        
    if not password_hash_function:
        new_hash = sha1()
        new_hash.update(password)
        password = new_hash.hexdigest()
        password_hash_function = 'SHA-1'
    
    old_domain=''
    if user_name.find('@') > 0:
        old_domain = credential.service.domain
        credential.service.domain = user_name[user_name.find('@')+1:]
        user_name = user_name[:user_name.find('@')]
        
    log("Creating account for %s" % user_name)
    try:
        credential.service.CreateUser(user_name=user_name, family_name=last_name, given_name=first_name, password=password, suspended=suspended, quota_limit=quota_limit, password_hash_function=password_hash_function, change_password=change_password)
    except gdata.apps.service.AppsForYourDomainException, e:
        if e.reason == 'EntityExists':
            raise Exception('EntityExists error. '+user_name+" is an existing user, group or nickname. Please delete the existing entity with this name before creating "+user_name)
        elif e.reason == 'UserDeletedRecently':
            raise Exception('UserDeletedRecently error. '+user_name+" was recently deleted within five days. You'll need to wait five days before a user can be created or renamed to this name.")
        else:
            raise StandardError('An error occurred: '+e.reason)        
    
    
    if old_domain:
        # reset domain to the old domain
        credential.service.domain = old_domain

def update_user(credential, user_name, new_user_name=None, first_name=None, last_name=None, password=None, password_hash_function=None, admin=None, suspended=None, ip_whitelisted=None, change_password=None):
    """Updates the user."""
    old_domain=''
    if user_name.find('@') > 0:
        old_domain = credential.service.domain
        credential.service.domain = user_name[user_name.find('@')+1:]
        user_name = user_name[:user_name.find('@')]
    
    user = credential.service.RetrieveUser(user_name)
    
    if new_user_name!=None:
        user.login.user_name = new_user_name

    if first_name!=None:
        user.name.given_name = first_name
    
    if last_name!=None:
        user.name.family_name = last_name
    
    if password!=None:
        if not password_hash_function:
            new_hash = sha1()
            new_hash.update(password)
            password = new_hash.hexdigest()
            password_hash_function = 'SHA-1'
        user.login.password = password
        user.login.hash_function_name = password_hash_function
    
    if admin!=None:
        if not admin:
            user.login.admin = 'false'
        else:
            user.login.admin = 'true'
    
    if suspended!=None:
        if not suspended:
            user.login.suspended = 'false'
        else:
            user.login.suspended = 'true'
    
    if ip_whitelisted!=None:
        if not ip_whitelisted:
            user.login.ip_whitelisted = 'false'
        else:
            user.login.ip_whitelisted = 'true'
    
    if change_password!=None:
        if not ip_whitelisted:
            user.login.change_password = 'false'
        else:
            user.login.change_password = 'true'
    
    log('Updating %s' % user_name)
    try:
        credential.service.UpdateUser(user_name, user)
    except gdata.apps.service.AppsForYourDomainException, e:
        if e.reason == 'EntityExists':
            raise Exception('EntityExists error. '+user.login.user_name+" is an existing user, group or nickname. Please delete the existing entity with this name before renaming "+user_name)
        elif e.reason == 'UserDeletedRecently':
            raise Exception('UserDeletedRecently error. '+user.login.user_name+" was recently deleted within five days. You'll need to wait five days before a user can be created or renamed to this name.")
        else:
            raise StandardError('An error occurred: '+e.reason)        
    
    if old_domain:
        # reset domain to the old domain
        credential.service.domain = old_domain

def read_user(credential, user_name, first_name=True, last_name=True, admin=True, suspended=True, ip_whitelisted=True, change_password=True, agreed_to_terms=True):
    """Reads the user with username user_name."""
    old_domain=''
    if user_name.find('@') > 0:
        old_domain = credential.service.domain
        credential.service.domain = user_name[user_name.find('@')+1:]
        user_name = user_name[:user_name.find('@')]
    
    try:
        user = credential.service.RetrieveUser(user_name)
    except gdata.apps.service.AppsForYourDomainException, e:
        if e.reason == 'EntityDoesNotExist':
            raise Exception('EntityDoesNotExist error. '+user_name+" does not exist.")
        else:
            raise StandardError('An error occurred: '+e.reason)        
    
    print 'User: %s' % user.login.user_name
    
    if first_name:
        print 'First Name: %s' % user.name.given_name
    
    if last_name:
        print 'Last Name: %s' % user.name.family_name
    
    if admin:
        print 'Is Admin: %s' % user.login.admin
    
    if suspended:
        print 'Is Suspended: %s' % user.login.suspended
    
    if ip_whitelisted:
        print 'IP Whitelisted: %s' % user.login.ip_whitelisted
    
    if change_password:
        print 'Must Change Password: %s' % user.login.change_password
    
    if agreed_to_terms:
        print 'Has Agreed to Terms: %s' % user.login.agreed_to_terms    
    
    if old_domain:
        # reset domain to the old domain
        credential.service.domain = old_domain

def suspend_user(credential, user_name):
    """Suspends the user with username user_name."""
    old_domain=''
    if user_name.find('@') > 0:
        old_domain = credential.service.domain
        credential.service.domain = user_name[user_name.find('@')+1:]
        user_name = user_name[:user_name.find('@')]
    
    log('Suspending %s' % user_name)
    credential.service.SuspendUser(user_name)
    
    if old_domain:
        # reset domain to the old domain
        credential.service.domain = old_domain

def restore_user(credential, user_name):
    """Suspends the user with username user_name."""
    old_domain=''
    if user_name.find('@') > 0:
        old_domain = credential.service.domain
        credential.service.domain = user_name[user_name.find('@')+1:]
        user_name = user_name[:user_name.find('@')]
    
    log('Restoring %s' % user_name)
    credential.service.RestoreUser(user_name)

    if old_domain:
        # reset domain to the old domain
        credential.service.domain = old_domain

def rename_user(credential, user_name, new_user_name):
    """Renames the user with username user_name with new_user_name. This function is explicitly included since renaming user is such a popular feature."""
    update_user(credential, user_name, new_user_name)

def delete_user(credential, user_name, no_rename=False):
    """Deletes the user with username user_name. The username is first renamed to include the current timestamp; this is so that a new user with the same username can be recreated immediately. If no_rename is set, this part is skipped."""
    old_domain=''
    if user_name.find('@') > 0:
        old_domain = credential.service.domain
        credential.service.domain = user_name[user_name.find('@')+1:]
        user_name = user_name[:user_name.find('@')]
    
    if no_rename.lower()=='true':
        log('Deleting %s' % user_name)
        credential.service.DeleteUser(user_name)
    else:
        time_stamp = time.strftime("%Y%m%d%H%M%S")
        renamed_user_name = user_name+'-'+time_stamp
        user = credential.service.RetrieveUser(user_name)
        user.login.user_name = renamed_user_name
        log('Renaming %s to %s' % (user_name, renamed_user_name))
        credential.service.UpdateUser(user_name, user)
        log('Deleting %s' % renamed_user_name)
        credential.service.DeleteUser(renamed_user_name)
    
    if old_domain:
        # reset domain to the old domain
        credential.service.domain = old_domain


## USER EMAIL SETTING FUNCTIONS ##

def create_label(credential, user_name, label):
    """Creates a label for user_name."""
    old_domain=''
    if user_name.find('@') > 0:
        old_domain = credential.service.domain
        credential.service.domain = user_name[user_name.find('@')+1:]
        user_name = user_name[:user_name.find('@')]
        
    email_settings = credential.get_email_settings_object()
    log('Creating label %s for %s' % (label, user_name))
    email_settings.CreateLabel(user_name, label)
    
    if old_domain:
        # reset domain to the old domain
        credential.service.domain = old_domain

def create_filter(credential, user_name, mail_from=None, mail_to=None, subject=None,
                   has_the_word=None, does_not_have_the_word=None,
                   has_attachment='false', label=None, should_mark_as_read='false',
                   should_archive='false'):
    """Just a pass-through for the GData CreateFilter method."""
    old_domain=''
    if user_name.find('@') > 0:
        old_domain = credential.service.domain
        credential.service.domain = user_name[user_name.find('@')+1:]
        user_name = user_name[:user_name.find('@')]
    
    has_attachment = str_to_bool(has_attachment)
    should_mark_as_read = str_to_bool(should_mark_as_read)
    should_archive = str_to_bool(should_archive)
    
    email_settings = credential.get_email_settings_object()
    log('Creating filter for %s' % user_name)
    email_settings.CreateFilter(username=user_name, from_=mail_from, to=mail_to, subject=subject,
                       has_the_word=has_the_word, does_not_have_the_word=does_not_have_the_word,
                       has_attachment=has_attachment, label=label, should_mark_as_read=should_mark_as_read,
                       should_archive=should_archive)
    
    if old_domain:
        # reset domain to the old domain
        credential.service.domain = old_domain

def update_web_clips(credential, user_name, enable):
    """Enables or disables web clips for user_name."""
    old_domain=''
    if user_name.find('@') > 0:
        old_domain = credential.service.domain
        credential.service.domain = user_name[user_name.find('@')+1:]
        user_name = user_name[:user_name.find('@')]
    
    enable = str_to_bool(enable)
    email_settings = credential.get_email_settings_object()
    if enable:
        log('Enabling web clips for %s' % user_name)
    else:
        log('Disabling web clips for %s' % user_name)
    email_settings.UpdateWebClipSettings(user_name, enable)
    
    if old_domain:
        # reset domain to the old domain
        credential.service.domain = old_domain

def create_send_as(credential, user_name, name, address, reply_to=None, make_default='false'):
    """Creates a send_as alias for user_name."""
    old_domain=''
    if user_name.find('@') > 0:
        old_domain = credential.service.domain
        credential.service.domain = user_name[user_name.find('@')+1:]
        user_name = user_name[:user_name.find('@')]
    
    make_default = str_to_bool(make_default)
    
    email_settings = credential.get_email_settings_object()
    log('Creating send as alias for %s to send as %s' % (user_name, address))
    email_settings.CreateSendAsAlias(user_name, name, address, reply_to, make_default)
    
    if old_domain:
        # reset domain to the old domain
        credential.service.domain = old_domain
    
def update_forwarding(credential, user_name, enable, forward_to, action):
    """Enables or disables email forwarding for user_name. Action should be one of keep, archive, or delete."""
    old_domain=''
    if user_name.find('@') > 0:
        old_domain = credential.service.domain
        credential.service.domain = user_name[user_name.find('@')+1:]
        user_name = user_name[:user_name.find('@')]
    
    enable = str_to_bool(enable)
    action = action.upper()
    email_settings = credential.get_email_settings_object()
    if enable:
        log('Enabling forwarding for %s to forward to %s' % (user_name, forward_to))
    else:
        log('Disabling forwarding for %s' % user_name)
    email_settings.UpdateForwarding(user_name, enable, forward_to, action)
    
    if old_domain:
        # reset domain to the old domain
        credential.service.domain = old_domain


def update_pop(credential, user_name, enable, enable_for, action):
    """Enables or disables POP access for user_name."""
    old_domain=''
    if user_name.find('@') > 0:
        old_domain = credential.service.domain
        credential.service.domain = user_name[user_name.find('@')+1:]
        user_name = user_name[:user_name.find('@')]
    
    enable = str_to_bool(enable)
    enable_for = enable_for.upper()
    action = action.upper()
    
    email_settings = credential.get_email_settings_object()
    if enable:
        log('Enabling POP for %s' % user_name)
    else:
        log('Disabling POP for %s' % user_name)
    email_settings.UpdatePop(user_name, enable, enable_for, action)

    if old_domain:
        # reset domain to the old domain
        credential.service.domain = old_domain

def update_imap(credential, user_name, enable):
    """Enables or disables IMAP access for user_name."""
    old_domain=''
    if user_name.find('@') > 0:
        old_domain = credential.service.domain
        credential.service.domain = user_name[user_name.find('@')+1:]
        user_name = user_name[:user_name.find('@')]
    
    enable = str_to_bool(enable)
    
    email_settings = credential.get_email_settings_object()
    if enable:
        log('Enabling IMAP for %s' % user_name)
    else:
        log('Disabling IMAP for %s' % user_name)
    email_settings.UpdateImap(user_name, enable)

    if old_domain:
        # reset domain to the old domain
        credential.service.domain = old_domain

def update_vacation(credential, user_name, enable, subject='', message='', contacts_only='false'):
    """Enables or disables a vacation responder for user_name."""
    old_domain=''
    if user_name.find('@') > 0:
        old_domain = credential.service.domain
        credential.service.domain = user_name[user_name.find('@')+1:]
        user_name = user_name[:user_name.find('@')]
    
    enable = str_to_bool(enable)
    contacts_only = str_to_bool(enable)
    
    # The following code is needed to properly deal with new lines. This was found in the Google Apps Manager, used here under the Apache 2.0 license.
    message = cgi.escape(message).replace('\\n', '&#xA;')
    vacation_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <atom:entry xmlns:atom="http://www.w3.org/2005/Atom" xmlns:apps="http://schemas.google.com/apps/2006">
        <apps:property name="enable" value="'''+str(enable)+'''" />
        <apps:property name="subject" value="'''+subject+'''" />
        <apps:property name="message" value="'''+message+'''" />
        <apps:property name="contactsOnly" value="'''+str(contacts_only)+'''" />
    </atom:entry>'''
    
    email_settings = credential.get_email_settings_object()
    uri = 'https://apps-apis.google.com/a/feeds/emailsettings/2.0/'+email_settings.domain+'/'+user_name+'/vacation'
    
    if enable:
        log('Enabling vacation responder for %s' % user_name)
    else:
        log('Disabling vacation responder for %s' % user_name)
    
    email_settings.Put(vacation_xml, uri) # JRP, 12/22/10 - we have to Put this since the GData library doesn't currently support new lines
    
    if old_domain:
        # reset domain to the old domain
        credential.service.domain = old_domain

def update_signature(credential, user_name, signature):
    """Replaces the user's signature with signature. Note that new lines are currently not supported."""
    old_domain=''
    if user_name.find('@') > 0:
        old_domain = credential.service.domain
        credential.service.domain = user_name[user_name.find('@')+1:]
        user_name = user_name[:user_name.find('@')]
    
    # The following code is needed to properly deal with new lines. This was found in the Google Apps Manager, used here under the Apache 2.0 license.
    signature = cgi.escape(signature).replace('\\n', '&#xA;')
    xml_signature = '''<?xml version="1.0" encoding="utf-8"?>
    <atom:entry xmlns:atom="http://www.w3.org/2005/Atom" xmlns:apps="http://schemas.google.com/apps/2006">
        <apps:property name="signature" value="'''+signature+'''" />
    </atom:entry>'''
    
    log('Updating signature for %s to %s' % (user_name, signature))
    
    email_settings = credential.get_email_settings_object()
    uri = 'https://apps-apis.google.com/a/feeds/emailsettings/2.0/'+email_settings.domain+'/'+user_name+'/signature'
    email_settings.Put(xml_signature, uri)
    
    if old_domain:
        # reset domain to the old domain
        credential.service.domain = old_domain

def update_language(credential, user_name, language):
    """Replaces the user's language."""
    old_domain=''
    if user_name.find('@') > 0:
        old_domain = credential.service.domain
        credential.service.domain = user_name[user_name.find('@')+1:]
        user_name = user_name[:user_name.find('@')]
    
    email_settings = credential.get_email_settings_object()
    log('Updating language for %s to %s' % (user_name, language))
    email_settings.UpdateLanguage(user_name, language)
    
    if old_domain:
        # reset domain to the old domain
        credential.service.domain = old_domain

def update_general():
    pass

## NICKNAME FUNCTIONS ##



## GROUP FUNCTIONS ##



## SHARED CONTACT FUNCTIONS ##



## MULTI DOMAIN FUNCTIONS ##



## RESOURCE CALENDAR FUNCTIONS ##



## AUDIT FUNCTIONS ##



## ORGANIZATIONAL UNIT FUNCTIONS ##



## DOCS FUNCTIONS ##



## PROCESSING FUNCTIONS ##

def log(message):
    """Logs the message."""
    print message

def build_arg_dict(args, case_sensitive=False):
    """Takes an array of arguments and builds a dictionary out of it."""
    dictionary = {}
    for arg in args:
        splits = arg.split('=')
        if len(splits)<2:
            splits.append(True)
        if not case_sensitive:
            # dictionary keys are not case sensitive
            splits[0]=splits[0].lower()
        dictionary[splits[0]]=splits[1]
    return dictionary

whitelist_functions = {
    'create_user': create_user,
    'read_user': read_user,
    'update_user': update_user,
    'delete_user': delete_user,
    'suspend_user': suspend_user,
    'restore_user': restore_user,
    'rename_user': rename_user,
    'create_label': create_label,
    'create_filter': create_filter,
    'create_send_as': create_send_as,
    'update_web_clips': update_web_clips,
    'update_forwarding': update_forwarding,
    'update_pop': update_pop,
    'update_imap': update_imap,
    'update_vacation': update_vacation,
    'update_signature': update_signature,
    'update_language': update_language
    }

def execute(args):
    call_function = args[0]
    dictionary = build_arg_dict(args[1:])
    
    # log_in and log_out are treated specially since they use the credential
    if call_function=='log_in':
        credential = Credentials(**dictionary)
    elif call_function=='log_out':
        try:
            credential = Credentials(**dictionary)
        except:
            raise Exception('Cannot log out because you are not logged in.')
        log_out(credential, **dictionary)
    elif call_function=='print_authentication':
        print_authentication()
    else:
        credential = Credentials('', '')
        if call_function in whitelist_functions:
            whitelist_functions[call_function](credential, **dictionary)
        else:
            raise Exception('Unknown function '+call_function)

## MAIN ##
def __main__():
    args = sys.argv
    if len(args)<=1:
        raise Exception('Must provide at least one argument.')
    execute(args[1:])

if __name__ == '__main__':
    __main__()