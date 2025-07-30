import flask_wtf as fwt 
import wtforms as wt 
import wtforms.validators as wtfv 
from . constants import *


class SettingsForm(fwt.FlaskForm):
    """Form for changing Wiki Settings (Website settings)"""
    public =  wt.BooleanField("Public", 
                               description = "If enabled, everybody including non logged in users" 
                                             " will be able to view the wiki content. Note that "
                                             "only logged in users can edit the wiki."
                                             )
    show_source =  wt.BooleanField("Show Page Source", 
                               description = "Provides a button that allows vieweing the Markdown (wiki text) " 
                                             "source code a wiki"
                                             )
    display_edit_button = wt.BooleanField("Display edit button",
                                    description = ( 
                                          "Display the wiki edit button for all users [E]. If this setting is disabled,  "
                                          "only admin users or users with permission to edit pages will be able to view the edit button."
                                            ) 
                                          )
    sitename = wt.StringField("Wiki Name", validators = [ wtfv.DataRequired() ] )
    description = wt.TextAreaField("Wiki Description") 
    submit = wt.SubmitField("Submit")

        
class UserSettingsForm(fwt.FlaskForm):
    """Form that allows users to change their own account settings."""
    password = wt.PasswordField("Password", validators = [ wtfv.DataRequired() ] )
    submit   = wt.SubmitField("Update")

USER_TYPE_CHOICES = [(USER_MASTER_ADMIN, "Root Admin"), (USER_ADMIN, "Admin"), (USER_GUEST, "Guest") ]

class UserAddForm(fwt.FlaskForm):
    """Form for adding new user account manually."""
    username = wt.StringField("Username", validators = [ wtfv.DataRequired() ] )
    ## email    = wt.StringField("Email") 
    email    = wt.StringField("Email", validators = [ wtfv.DataRequired() ] )
    password = wt.PasswordField("Password", validators = [ wtfv.DataRequired() ] )
    ## password = wt.StringField("Password", validators = [ wtfv.DataRequired() ] )
    type     = wt.SelectField("Type", choices = USER_TYPE_CHOICES )
    ## active   = wt.BooleanField("Active", default = True) 
    submit   = wt.SubmitField("Update")

    def get_user_type(self):
        choice = dict(USER_TYPE_CHOICES).get(self.type.data)
        return choice
