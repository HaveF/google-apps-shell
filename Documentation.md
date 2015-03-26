# Documentation #
This page contains a full listing of GAS commands.


---



# Authentication #

## Log In `(log_in)` ##

Logs GAS in to Google. This command should only be used from the command line, and not GASI.

**Usage:**

```
gas log_in email=<email> password=<password>
```

**Example:**

This example logs admin in to Google Apps, under the domain altostrat.com.

```
gas log_in email=admin@altostrat.com password=secret
```

## Log Out `(log_out)` ##

Logs GAS out of Google. This command should only be used from the command line, and not GASI.

**Usage:**

```
gas log_out
```

**Example:**

This example removes the authentication credentials from GAS.

```
gas log_out
```

## Print Authentication `(print_authentication)` ##

Prints out the current GAS authentication status, telling you whether you are logged in, and who you are logged in as.

**Usage:**

```
gas print_authentication
```

**Example:**

This example prints out the current authentication status.

```
gas print_authentication
```


---



# Email Settings #

## Create Filter `(create_filter)` ##

Creates a filter on behalf of user\_name.  Optional parameters include: mail\_from, mail\_to, subject, has\_the\_word, does\_not\_have\_the\_word, has\_attachment. Actions include label, should\_mark\_as\_read, and should\_archive.

**Usage:**

```
gas create_filter user_name=<name> [mail_from=<name>] [mail_to=<name>] [subject=<subject>] [has_the_word=<words>] [does_not_have_the_word=<words>] [has_attachment=<bool>] [label=<label>] [should_mark_as_read=<bool>] [should_archive=<bool>]
```

**Example:**

This example creates a filter for user jeff, labelling all mail from sandra with an attachment, and skipping the inbox by archiving the email.

```
gas create_filter user_name=jeff mail_from=sandra has_attachment=true label=Sandy should_archive=true
```

## Create Label `(create_label)` ##

Creates a new label for user\_name.

**Usage:**

```
gas create_label user_name=<name> label=<label>
```

**Example:**

This example creates a label for jeff@mydomain.com named Chrome.

```
gas create_label user_name=jeff label=Chrome
```

## Create Send As Alias `(create_send_as)` ##

Creates a send as alias on behalf of user\_name. This allows the user user\_name to send email as "name (address)" with an optional reply to.

**Usage:**

```
gas create_send_as user_name=<email> name=<name> address=<email> [reply_to=<email>] [make_default=true|false]
```

**Example:**

This example creates a send as alias for tim, allowing him to send as Timothy Johnson with timothy@domain.com.

```
gas create_send_as user_name=tim name="Timothy Johnson" address=timothy@domain.com reply_to=tim@domain.com
```

## Update Forwarding Mail `(update_forwarding)` ##

If enable is true, this creates a forwarding rule for user\_name, forwarding all incoming mail to enable\_for. Action describes what should happen to the email afterward. It'll either remain in the inbox, get archived, or get deleted. If enable is false, this disables any existing forwarding rule.

**Usage:**

```
gas update_forwarding user_name=<name> enable=<bool> [enable_for=<name>] [action=keep|archive|delete]
```

**Example:**

This example forwards all mail for sales@mydomain.com to kyle@mydomain.com.

```
gas update_forwarding user_name=sales enable=true forward_to=kyle@mydomain.com action=archive
```

## Update IMAP Access `(update_imap)` ##

Enables or disables IMAP access for user\_name.

**Usage:**

```
gas update_imap user_name=<name> enable=<bool>
```

**Example:**

This example enables IMAP access for user ken.

```
gas update_imap user_name=admin enable=true
```

## Update Language `(update_language)` ##

Sets the user's language preference to language. Some common language codes are en-US for American English, en-GB for British English, fr for French, and es for Spanish. For a full list of language codes, see http://code.google.com/googleapps/domain/email_settings/developers_guide_protocol.html#GA_email_language_tags

**Usage:**

```
gas update_language user_name=<name> language=<language>
```

**Example:**

This example sets the language preference to French.

```
gas update_language user_name=pierre language=fr
```

## Update POP Access `(update_pop)` ##

Enables or disables POP access for user\_name. Parameter enable\_for determines whether POP access is enabled from now on or for all mail. Action describes what should happen to the email afterward.

**Usage:**

```
gas update_pop user_name=<name> enable=<bool> enable_for=[all_mail|mail_from_now_on] action=[keep|archive|delete]
```

**Example:**

This example turns on POP access for user ken, for all mail, instructing Google to delete the mail after it has been accessed.

```
gas update_pop user_name=ken enable=true enable_for=all_mail action=delete
```

## Update Signature `(update_signature)` ##

Sets the user's signature to signature. Use \n for new lines.

**Usage:**

```
gas update_signature user_name=<name> signature=<signature>
```

**Example:**

This example sets a signature.

```
gas update_signature user_name=bill signature="Bill Johnson\nDirect line: 1-800-123-4567.
```

## Update Vacation Responder `(update_vacation)` ##

Creates or disables automatic vacation responder for user\_name. If the vacation responder is being created, contacts\_only describes whether the vacation alert should only be emailed to users in user\_name's personal contacts.

**Usage:**

```
gas update_vacation user_name=<name> enable=<bool> [subject=<subject>] [message=<message>] [contacts_only=<bool>]
```

**Example:**

This example creates an automatic vacation responder that will get sent to anyone who emails gonesurfing@domain.com.

```
gas update_vacation user_name=gonesurfing enable=true subject="OOO - Hawaii for Thanksgiving" message="I am out-of-office (Hawaii) and will be slow to respond to email. Aloha!" contacts_only=false
```

## Update Web Clips `(update_web_clips)` ##

Enables or disables web clips for a user.

**Usage:**

```
gas update_web_clips user_name=<name> enable=<bool>
```

**Example:**

This example turns off web clips for a user.

```
gas update_web_clips user_name=ben enable=false
```


---



# Groups #

## Add Member to Group `(add_member_to_group)` ##

Adds a member to a Google Group.

**Usage:**

```
gas add_member_to_group user=<name> id=<groupid>
```

**Example:**

This example beams up Scotty to the starship\_enterprise group.

```
gas add_member_to_group user=scotty id=starship_enterprise
```

## Add Owner to Group `(add_owner_to_group)` ##

Adds an owner to a Google Group.

**Usage:**

```
gas add_owner_to_group user=<name> id=<groupid>
```

**Example:**

This example adds picard to the starship\_enterprise group as an owner.

```
gas add_owner_to_group user=picard id=starship_enterprise
```

## Create Group `(create_group)` ##

Creates a group, groupid@yourdomain.com, with name and description. The permissions details the email permissions to the group.

**Usage:**

```
gas create_group id=<groupid> name=<name> description=<description> permission=[owner|member|domain|anyone]
```

**Example:**

This example creates a Google Group, sales, with email permissions such that anyone in the domain can email the group.

```
gas create_group id=sales name=Sales description="The sales group." permission=domain
```

## Delete Group `(delete_group)` ##

Deletes the Google Group.

**Usage:**

```
gas delete_group id=<groupid>
```

**Example:**

Deletes the sales group.

```
gas delete_group id=sales
```

## List Group Members `(list_group_members)` ##

Lists all Google Group members of the group. If suspended\_users is true, this will also list suspended users who are still members of the group.

**Usage:**

```
gas list_group_members id=<groupid> [suspended_users=true]
```

**Example:**

This example lists all members of the starship\_enterprise group.

```
gas list_group_members id=starship_enterprise suspended_users=true
```

## List Group Owners `(list_group_owners)` ##

Lists all Google Group owners of the group. If suspended\_users is true, this will also list suspended users who are still owners of the group.

**Usage:**

```
gas list_group_owners id=<groupid> [suspended_users=true]
```

**Example:**

This example lists all owners of the starship\_enterprise group, such as Jean-Luc Picard.

```
gas list_group_owners id=starship_enterprise suspended_users=true
```

## List All Groups `(list_groups)` ##

Lists all Google Groups in the domain.

**Usage:**

```
gas list_groups
```

**Example:**

This example lists all groups.

```
gas list_groups
```

## Read Group `(read_group)` ##

Outputs information about the Google Group.

**Usage:**

```
gas read_group id=<groupid>
```

**Example:**

This example outputs information about the sales group.

```
gas read_group id=sales
```

## Remove Member from Group `(remove_member_from_group)` ##

Removes a member from a Google Group.

**Usage:**

```
gas remove_member_from_group user=<name> id=<groupid>
```

**Example:**

This example removes a member from the starship\_enterprise group.

```
gas remove_member_from_group user=scotty id=starship_enterprise
```

## Remove Owner from Group `(remove_owner_from_group)` ##

Removes an owner from a Google Group

**Usage:**

```
gas remove_owner_from_group user=<name> id=<groupid>
```

**Example:**

This example removes owner picard from the starship\_enterprise group

```
gas remove_owner_from_group user=picard id=starship_enterprise
```

## Update Group `(update_group)` ##

Updates the group, groupid@yourdomain.com, with name and description. The permissions details the email permissions to the group.

**Usage:**

```
gas update_group id=<groupid> name=<name> description=<description> permission=[owner|member|domain|anyone]
```

**Example:**

This example the secret group to have the new settings.

```
gas update_group id=secret name=Secret description="New description" permission=member
```


---



# Nickname Settings #

## Create Nickname `(create_nickname)` ##

Creates a nickname on behalf of user\_name.

**Usage:**

```
gas create_nickname nickname=<nickname> user_name=<name>
```

**Example:**

This example creates a nickname for the user joseph, with the nickname joey.

```
gas create_nickname nickname=joey user_name=joseph
```

## Delete Nickname `(delete_nickname)` ##

Deletes a nickname, if it exists.

**Usage:**

```
gas delete_nickname nickname=<nickname>
```

**Example:**

This example deletes the nickname for joey.

```
gas delete_nickname nickname=joey
```

## Read Nickname `(read_nickname)` ##

Prints out a summary of the nickname, if it exists.

**Usage:**

```
gas read_nickname nickname=<nickname>
```

**Example:**

This example reads the nickname for joey.

```
gas read_nickname nickname=joey
```


---



# Organization #

## Add Users to Organization `(add_users_to_org)` ##

Adds a list of users to the specified organization.  Optional variable users\_to\_move contains a space-separated list of users to move to the organization.

**Usage:**

```
gas add_users_to_org name=<org> users_to_move=<user_list>
```

**Example:**

This example adds the users in users\_to\_move to the organization.

```
gas add_users_to_org name=<name> users_to_move="jeff courtney jedd sarah mike tessa stephanie"
```

## Create Organization `(create_org)` ##

Creates an organization unit org with a description.  If parent is specified, the organization is created under the parent.  If block\_inheritance is true, the organization does not inherit settings from the parent.

**Usage:**

```
gas create_org name=<org> description=<description> [parent=<parent_org>] [block_inheritance=true]
```

**Example:**

This example creates an organizational unnit for Canadian users in the company.

```
gas create_org name=canada description="Canadian users"
```

## Delete Organization `(delete_org)` ##

Deletes an organization. The organization must NOT contain any users, otherwise it cannot be deleted.

**Usage:**

```
gas delete_org name=<name>
```

**Example:**

This example deletes the sales organization.

```
gas delete_org name=Sales
```

## Read Organization `(read_org)` ##

Prints information about the organization.

**Usage:**

```
gas read_org name=<name>
```

**Example:**

This example prints information about the Sales organization.

```
gas read_org name=Sales
```

## Update Organization `(update_org)` ##

Updates an organization unit with the settings specified.  Optional variable users\_to\_move contains a space-separated list of users to move to the organization.

**Usage:**

```
gas update_org name=<org> description=<description> [parent=<parent_org>] [block_inheritance=true] [users_to_move=<user_list>]
```

**Example:**

Updates the sales org with an updated description and moves a list of users to that organization.

```
gas update_org name=sales description="This org contains the sales users" users_to_move="jeff courtney jedd sarah mike tessa stephanie"
```


---



# Users #

## Creating a User `(create_user)` ##

Creates a user account named user\_name, with name first\_name and last\_name, and password password. These fields should be quoted if they contain spaces.
Optional parameter password\_hash\_function tells GAS that the password is being already given in an encrypted format, either SHA-1 or MD5.
Optional parameter suspended creates the account but marks it as suspended.
Optional parameter quota allows you to set the user's email quota.
Optional parameter change\_password will force the user to change their password after their first successful login.

**Usage:**

```
gas create_user user_name=<name> first_name=<First Name> last_name=<Last Name> password=<Password> [password_hash_function=SHA-1|MD5] [suspended=true|false] [quota_limit=<quota size>] [change_password=true|false]
```

**Example:**

This example creates a user account.

```
gas create_user user_name=monkey first_name=David last_name=Monkey password=ILikeBananas
```

This example creates a user in a secondary domain. This is useful when a Google Apps account has multiple domains.

```
gas create_user user_name=elephant@secondarydomain.com first_name=Big last_name=Ears password=ILikePeanuts
```

## Delete a User `(delete_user)` ##

Delete the given user's account. GAS will first rename the user with the current timestamp and then delete the account. This allows the user to be recreated immediately rather than waiting the 5 days that Google normally requires.

**Usage:**

```
gas delete_user user_name=<name> [no_rename=true]
```

**Example:**

This example will delete the account for user igotfired without first renaming the account.

```
gas delete_user user_name=igotfired no_rename=true
```

## Get User Info `(read_user)` ##

Retrieve details about the given user.

**Usage:**

```
gas read_user user_name=<name>
```

**Example:**

This example will show information on the user daniel.

```
gas read_user user_name=daniel
```

## Rename a User `(rename_user)` ##

> Renames the user\_name account to new\_user\_name. Note that the user's primary calendar name must still be changed manually.

**Usage:**

```
gas rename_user user_name=<name> new_user_name=<name>
```

**Example:**

This example renames the user christopher to chris.

```
gas rename_user user_name=christopher new_user_name=chris
```

## Restore a User `(restore_user)` ##

Restores a user (from a suspended user state).

**Usage:**

```
gas restore_user user_name=<name>
```

**Example:**

This example restores the user ihavereturned, in the case that ihavereturned was suspended earlier.

```
gas restore_user user_name=ihavereturned
```

## Suspend a User `(suspend_user)` ##

Suspends the given user's account.

**Usage:**

```
gas suspend_user user_name=<name>
```

**Example:**

This example suspend the account for user iamsuspended. Suspended accounts can be restored at a later date.

```
gas suspend_user user_name=iamsuspended
```

## Update (and Rename) a User `(update_user)` ##

Updates the user account for user\_name. All parameters except user\_name are optional. If you wish to rename the username for this user, set new\_user\_name.

**Usage:**

```
gas update_user user_name=<name> [new_user_name=<New Name>] [first_name=<First Name>] [last_name=<Last Name>] [password=<Password>] [password_hash_function=SHA-1|MD5] [suspended=true|false] [quota_limit=<quota size>] [change_password=true|false] [admin=true|false] [suspended=true|false] [ip_whitelisted=true|false]
```

**Example:**

This example updates a user account, setting the first\_name, last\_name and password and making them an administrator.

```
gam update_user user_name=jack first_name=Jack last_name=Johnson password=MovingOut admin=true suspended=false
```

This example renames the user jeffrey to jeff.

```
gam update_user user_name=jeffrey new_user_name=jeff
```