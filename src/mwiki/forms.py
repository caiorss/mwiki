import flask_wtf as fwt 
import wtforms as wt 
import wtforms.validators as wtfv 
import mwiki.models as models
import mwiki.constants as const 


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
    latex_renderer = wt.SelectField("LaTeX Renderer"
                                    , choices = [ ("mathjax", "MathJax"), ("katex", "KaTeX") ]
                                    , description = ("Client-side JavaScript library used for rendering math formulas"
                                                    " and equations written in LaTeX. Note that the use of KaTeX "
                                                    "is still experimental."
                                                       ))
    use_cdn = wt.BooleanField("Use a CDN",
                              description = (
                                  "Load JavaScript libraries from a CDN (Content Delivery Network)"
                                  "Instead of loading them from this server."
                              ))

    language = wt.SelectField("Default Document Language"
                              , choices = [(lang_code, lang_name)
                                              for (lang_name, lang_code) in models.LanguagesDatabase])
    language_switch = wt.BooleanField("Language Swich")
    display_alt_button = wt.BooleanField("Display alt text button")
    vim_emulation = wt.BooleanField("VIM Emulation", description="Enable VIM editor emulation in the Wiki code editor (Ace9).")
    show_licenses = wt.BooleanField("Show Licenses", description="Displays menu option showing 'Licenses' that shows all open"
																 "Source licenses used by this project.")
    use_default_locale = wt.BooleanField("Default Locale", description=("Always use default locale regardless of" " user's preferred locale provided by the web browser.") )
    default_locale = wt.SelectField("default_locale", choices = [ ("en-US", "en-US - American English")
															     ,("pt-BR", "pt-BR - Português Brasileiro (Brazilian Portuguese) ") ]
															     )
    main_font = wt.SelectField("Main Font", choices = [(ch.value, ch.value) for ch  in models.FontFamiliyEnum])
    code_font = wt.SelectField("Code Font", choices = [(ch.value, ch.value) for ch  in models.CodeFontFamily])
    title_font = wt.SelectField("Title Font", choices = [(ch.value, ch.value) for ch  in models.TitleFontFamily])
    sitename = wt.StringField("Website Name", validators = [ wtfv.DataRequired() ] )
    description = wt.TextAreaField("Website Description") 
    submit = wt.SubmitField("Update")

        
class UserSettingsForm(fwt.FlaskForm):
    """Form that allows users to change their own account settings."""
    password = wt.PasswordField("Password", validators = [ wtfv.DataRequired() ] )
    submit   = wt.SubmitField("Update")

USER_TYPE_CHOICES = [(const.USER_MASTER_ADMIN, "Root Admin")
                    , (const.USER_ADMIN, "Admin")
                    , (const.USER_GUEST, "Guest")
                    , (const.USER_EDITOR, "Editor")
                ]
            

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

class UserEditForm(fwt.FlaskForm):
    """Form for adding new user account manually."""
    username = wt.StringField("Username", validators = [ wtfv.DataRequired() ] )
    active   = wt.BooleanField("Active")
    ## email    = wt.StringField("Email") 
    email    = wt.StringField("Email" )
    password = wt.PasswordField("Password",  )
    ## password = wt.StringField("Password", validators = [ wtfv.DataRequired() ] )
    type     = wt.SelectField("Type", choices = USER_TYPE_CHOICES )
    ## active   = wt.BooleanField("Active", default = True) 
    submit   = wt.SubmitField("Update")

    def get_user_type(self):
        choice = dict(USER_TYPE_CHOICES).get(self.type.data)
        return choice

class UserCreateForm(fwt.FlaskForm):
    """Form for adding new user account manually."""
    username = wt.StringField("Username", validators = [ wtfv.DataRequired() ] )
    active   = wt.BooleanField("Active")
    ## email    = wt.StringField("Email") 
    email    = wt.StringField("Email" )
    password = wt.PasswordField("Password", validators = [ wtfv.DataRequired() ] )
    ## password = wt.StringField("Password", validators = [ wtfv.DataRequired() ] )
    type     = wt.SelectField("Type", choices = USER_TYPE_CHOICES )
    ## active   = wt.BooleanField("Active", default = True) 
    submit   = wt.SubmitField("Create")

    def get_user_type(self):
        choice = dict(USER_TYPE_CHOICES).get(self.type.data)
        return choice
