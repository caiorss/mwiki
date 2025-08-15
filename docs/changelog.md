# Changelog 

## Release v0.5


+ Implement site settings for changing code font.
   + Implement settings form option that allows the admin to change the default code font (monospace font/typeface).
+ Implement caching of markdown-to-html compilation.
  + Implement caching of markdown-to-html compilation, which allows faster page response and less server load (CPU usage) as the markdown files of wiki pages (notes)  are recompiled only when they are modified or when some dependency changes.
+ Add new monospace fonts/typefaces, including Commint Mono, Julia Mono, Julia Mono Light, Libertinus Mono, Libertinus Sans and Libertinus Serif. In this version, the following code (monospace) fonts are available: IBM Plex Mono; Go mono; Logic Monospace Regular; Logic Monospace Medium; Commint Mono; Julia Mono; Julia Mono Light and Libertinus Mono.
+ The popup window "quick open" now search page if input does not match user input.
   + The popup window "Quick Open Wiki Page", that allows quickly switching to other wiki page by providing a user input text entry with title completion, now searches the terms entered by the user if they do not match any wiki page title.
+ Wiki pages (notes) with spaces in the file name are regarded as the same as pages with underline in the file name.
  + After this change, the files  'Cloud Computing.md' abd 'Cloud_Computing.md' are regarded as the same file, consequentely the wiki pages 'Cloud Computing' and 'Cloud_Computing' are also regarded as the wiki page (note). This approach improves compatibility with Wikis or note taking applications  that use underline in file name and Wikis that use space in the file name.
+  Bugfix - Fix datalist DOM elment of popup window "Quick Open Wiki Page".
+  Bugfix - Function openWikiPageCallback() now uses underline '_' characters in the url instead of spaces.
+  Bugfix - Fix the display of edit buttons (pencil icons) due to architecture changes.
   + Passing server data to the page via template no longer works because cached pages are served directly from the compilation output (html files). As a result, a rest api endpoint /api/auth was implemented for allowing the client-side to obtain the configuration data for modify the page without markdown recompilation on every request.

## Release v0.4

+ Use underline in URLs instead of whitespace.
  + URLs to internal wiki pages such as [[Linux Operating System]] are now rendered using underline character '_' instead of whistespaces ' ', which corresponds to '%20' URL enconding. This feature makes URL rendering look better and be easier to type. For instance, before this commit, the URL to the page file 'Linux Operating System.md' was '/wiki/Linux%20Operating%20System' now this URL is '/wiki/Linux_Operating_System'.
+ Settings Form Changes
  + Settings form allows changing fonts (typefaces) used by the website, including, main font and title font. 
  + Implement checkbox in settings form for enabling/disabling the display the wiki edit button (pencil icon) for all users. If this setting is disabled, only admin users or users with permission to edit pages will be able to view the edit button.
  + Implement hyperlink to go to previous page in the settings form.
  + implement VIM emulation checkbox in setting form.  This checkbox  (/settings relative URL) allows enabling or disabling VIM editor emulation in the wiki code editor (Ace9). After this commit, emulation of VIM editor keybindings is disabled by default as VIM keybindings are not familiar to most users. However, it can be enabled by the admin in the settings form. VIM keybindgs are highly recommended as they make easier to navigate in the text or code and do complex editing with few keystrokes.
+ Provide the following fonts typefaces options in the settings form: 
  + Computer Modern, Neo Euler, Chicago (used by older versions of Apple Inc's MacOSX), IBM Plex Mono, Comorant Light, Literata (font used by Google Books),  Logic Monospace Regular, Logic Monospace Medium, Garamond Pro Regular, GO Mono, NewsReader, Graphik Regular,  Textura Modern and Bastarda.
+ Implement image and video lazy loading. 
  + This feature allows faster page loading loading as only images visible in the current window viewport are loaded. As a result, the load on the server is reduced.
+ UI - User Interface Improvement.
  + Replace text buttons including '[E]' and text menus with SVG icons
  + Improve user interface UI of the settings form.
  + Remove search button in the left toolbar due to its redundancy.
  + Rename label of editor button 'view' to 'back'.
+ Remove (C) and (R) from the typographic convention database.
+ Implement figure syntax for images with metadata, including caption/label, alt text (alternative text) for better accessibility, unique identifier and automatic enumeration. It is similar to MyST markdown figure syntax.
+  Editor now uses figure syntax when pasting an image instead of the old image syntax.

### Release v0.3.1

+ Implement optional section enumeration.
+ Implement Keyboard shortcuts for quick navigation.
+ Disable annoying pull-down-to-refresh behavior in mobile browsers.


### Release v0.2

+  Centralize document title heading h1.
+ Bugfix - Display Links menu items of Page menu for all users, including anonymous users.  
  + NOTE: No change of permission model has been introduced, anonymous users can only view the wiki page if the checkbox 'Public Wiki' of  /settings menu is enabled.
+ Move 'Search' and 'Tags' menu items from Main menu to Page menu.
+ Rename 'Wiki Settings' menu item label to 'Settings'.
+ Move create new page menu item from Main menu to Page menu.
+ Bugfix - Fix missing CRSF token of create user form.
+ Implement checkbox for enabling/disable menu item for showing page source.
  + This commits implements a Web Site setting checkbox at URL endpoint /settings, which allows enabling or disabling menu option in [Page] menu for showing markdown source of current wiki page.
+ Refactor page_menu.html only displaying editing menus for logged in users.
+ Move button show reference card from Main menu to Page menu.
+ Add button show reference card to editor toolbar.
+ Bugfix - Fix frontmatter rendering - AttributeError: 'NoneType' object has no attribute 'get'.
+ About page shows information from site settings.  
  + Move MWiki AGPL license to /licenses listing all open source licenses.
  + About page now displays information about the website or website description that can be changed by user in the URL endpoint /settings. A form where the user can change web site name, description and whether it is public or not.
+ Allow changing document title in wiki page frontmatter with title directive.
+ Implement adjustable LaTeX equation enumeration.  Implement 'equation_enumeration' directive for a front-matter of a MWiki page (markdown file). This directive allows enabling/disabling LaTeX equation enumeration and changing equation enumeration style. If the directive is set to 'none', automatic equation enumeration is disabled. If the directive is set to 'section' the enumeration schema becomes `<section-number>.<equation-number>` (default style). If the directive is set to to 'subsection' , the enumeration style is set to  `<section>.<subsection>.<eqnum>`.  For instance, if a LaTeX (MathJaX) equation is numbered as 2.4.10, it means that is the 10th equation of the 4th subsection of the section 2 of the current wiki page.
+ Implement continous equation enumeration.   
  + Create continous equation enumeration style for Mathjax/LaTeX equations, where equation are enumerated as 1, 2, 3, ..., in the order that they are defined. This enumeration style might be useful for short documents.
+ Implement MyST role syntax for embeding youtube videos.
+ Rename Global menu to Main.
+ Create editor button for saving document.
+ Bugfix - Fix path traversal vulnerability - do not serve hidden folders or database.sqlite.
+ Implement CSRF protection. 
  + Implement protection against CSRF - Cross-Site Request Forgery attacks by requiring the CSRF token in forms and Ajax requests.
+ Upload pasted images from clipboard in JPEG instead of PNG format.
  + Now images pasted from clipboard are saved in JPEG format (.jpg extension) instead of PNG format. This feature significantly reduces image size, saves bandwidth and loads them faster in a web browser. The images are converted in the server side using Python pillow package
+ Create edit buttton on top of wiki h1 section header.
   + Create [E] edit button on top of wiki h1 section header, which
    allows editing the whole page without going to the menu [Global].
+ Implement actions of Do and Redo editor buttons.
+ Implement special hyperlink to subreddits using the `<rd:/r/smalltalk> syntax.
+ Use database as default session storage instead of file system.
+ Implement hyperlink to patent numbers with comma.
+ Implement system management command line switches.
+ Initial settings can be defined through environment variables.  Initial settings of the Wiki web app now can be defined using environment variables, which is useful for automated installation via docker-compose or other container orchestration tools. MWIKI_ADMIN_PASSWORD => Defines default admin password.  MWIKI_PUBLIC => Enable or disable initial login form. MWIKI_SITENAME => Allows changing the web site name.
+ Allow defining admin password using environment variable.
+ mplement {u} MyST role syntax for underline markup.
+ Imlement clipboard to markdown converter.
+ Implement short hyperlink syntax to CVE database and update docs, example `<cve:CVE-2024-53104>`.
+ Implement wordlinks for frontmatter.
+ Bugfix - catch yaml.parser.ParserError exception.
+ Replace hardcoded status codes by constants.
+ Implement special hyperlink syntax for mastdon user account handle. For instance, the handle (akin to Twitter user account) `@kde@floss.social` is rendered as the link https://floss.social/@kde with  label `@kde@floss.social` In this case, `@kde@floss.social` is rendered to html as `<a href="https://floss.social/@kde" ...>@kde@foss.social</a>`.
+ Update README.md  - add pipx install instructions. 
+Bugfix - Solve dependency hell issue by replacing gunicorn with waitress WSGI server.
  + This commit makes it possible to install this application with pipx and Poetry with newer versions of Python.  In addition, unlike Gunicorn, waitress WSGI sever also works on Microsoft Windows.


### Release v0.1

+ First release.
+ Implement of MyST comments.
+ Allow markdown folder to be set through environment variable.
+ Implement Obsididian markdown  syntax for text highlight.
+ Implement this MyST syntax for math code block with directives.
+ Add noreferrer noopener nofollow rel properties to all external hyperlinks in order to improve privacy and avoid leaking data.
+ Implement HTML rendering of MyST math role.
+ Implement html rendering of sup and sup MyST roles.
+ Implement rest API endpoint /api/logged.
+ Refactor - replace string-replacement template with flask built-in template system (Jinja2).
+ Implement display of frontmatter metadata.
+ Implement latex macros for MathJax.
+ Change style - set default font to Computer Modern and make the page look like a LaTeX document.
+ Change style - use monospace ttf font IBM Plex Mono in code blocks.
+ Improve search by removing accents from queries.  Some languages such as Portuguese, Spanish and French uses accents. Now it is possible to search for words with accents without typing all accents since the accents are now remove from queries. For instance, the Portuguese word 'industrialização' is turned into the word 'industrializacao', which provides more search results.
+ Implement Obsidian-like feature for embeding a note within another note by using the syntax: `![[Note name]]` , that embeds the file 'Note Name.md' within the current note.
+ Render link to non existing notes (wiki pages) in red color.
+ Implement button for creating new note (Wiki page).
+ Implement Obsidian's tag syntax, that uses number sign '#'.
+ Change MathJax settings to enumerate all latex equations by default.
+ Implement automatic heading enumeration.
+ Implement navitgation menus.
+ Create button for scrolling to top.
+ Create button for scrolling to bottom.
+ Create command utility to convert from org-mode to MWiki markdown. Note that this feature is still experimental and unstable.
+ Create html5/js modal window for displaying abbreviation `<abbr>` html5 elements.
+ Create popup window for displaying MWiki markup language reference card.
+ Implement short hyperlink expansion and short link to Python packages.
+  Feature - implement custom wiki markup syntax for creating html `<details>` foldable element.
+ Create syntax for mathematica proof foldable block.
+ Implement code block syntax for drawing graphs using  graphviz dot language.
+ Load ace9 JS code editor in edit.html from self-hosted static files.
+ Implement database login.
+ Add flask-wtf Python dependency for handling forms.
+ Implement settings form page.
+ Improve security - enforce authorization on server-side.

