# Changelog 

## Release v0.9

+ Add new fonts/typefaces choices  Averia, AveriaSans, Averia Gruesa, NotoSans, Space Groteske, EBGaramond, Jet Brains Mono (monospace font for source code listing), DMMono Regular.
+ Generate CSS font-face data dynamically instead of hardcoding them in the CSS file. This change improves the website loading speed.
+ Create custom markdown/JSON syntax for flashcard deck `{flashcard}`. NOTE that this feature is still under development.
+ Implement mastodon-like button for displaying alt text of figures, images with metadata defined with a `{figure}` block, in popup windows.
+ Implement LaTeX input window for the code editor.
  + Implement LaTeX input window (popup window) in which an user can type a LaTeX formula or code and get immediate feedback about how the formula looks like as the it is rendered immediately as the user types. This feature improves the usability, user experience (UX) by making it easier and faster to enter LaTeX formulas.
+ Add settings checkbox "Display alt text button", which enables or disables a mastodon-like button for displaying the alt text of figures in a popup-window.
+ Implement setting latex_renderer (allows switching to KaTeX).
  + Implement  website settings latex_renderer in the /settings form. The site configuration latex_renderer allows choosing MathJax or KaTeX JavaScript library for rendering LaTeX math formulas. KaTeX is newer and faster than MathJax, however it still does not have full feature parity with the later library, as a result the KaTeX support is still experimental.
+ Add checkbox use_cdn (default disabled) for the settings forms, that enables or disables loading JavaScript libraries from a CDN (Content Delivery Network). If this checkbox is enabled, MathJax or KaTeX will be loaded from a CDN instead of being loaded from the vendored libraries hosted by the MWiki server.
+ Implement settings checkbox "Allow language switch".
  + If the settings checkbox "allow language switch" is enabled, users can switch the user interface language during their sessions. If disabled, the users will not be  able to switch the user interface language and the main menu item "Language" will not be shown.
+ Create equation derivation `{derivation}` block, simular to `{proof}`. This block is intended to show how a equation or differential equation is derived. It was created as the terminology **derivation** is more popular in physics and engineering than the terminology **proof**, which is more popular in mathematics and statiscs.
+ Rename code block `{latex_macros}`for defining LaTeX macros to `{macros}`.
+ Rename frontmatter directive `equation_enumeration` to `equation_enumeration_style`, which has the choice "cont" or "continous" for continues enumeration 1, 2, 3, ...; "section" for section (default) enumeration 1.1, 1.2, 2.1, 2.2, ...; "subsection" for 1.2.3, 2.3.6.
+ Add frontmatter directive `equation_enumeration_enabled`, which has "on" or "off" possible values. If this directive is set to "on", all display-mode equations will be enumerated unless they have a `\notag` LaTeX command. If the directive is set to "off" (default value), only referenced with `\label{UNIQUE_LABEL}` equations by `\eqref{UNIQUE_LABEL}` will be eneumerated.
+ Implement global LaTeX macros and menu items for editing macros.
   + Implemented global LaTeX macros stored in the file *$MWIKI_REPOSITORY_PATH/macros.stye*. The menu item "Edit Macros" opens the file $MWIKI_REPOSITORY_PATH/macros.sty (Latex macro file extension). Macros defined in this file can be used in all MWiki pages. For a instance, if the LaTeX macro `\newcommand{\v}[1]{ \mathbf{#1} }` is defined in this file. It can be used for writing LaTeX formulas with vectors in all MWiki pages using `\v{r}_1` for position vector instead of `\mathbf{r}_1`.
+ Implement frontmatter directive latex_renderer for overriding the default LaTeX renderer.
  + The frontmatter directive latex_renderer allows overriding the default LaTeX renderer, that is set in the settings form page /settings
+ Disable default equation enumeration within math code blocks such as `{solution}`, `{proof}` or `{derivation}` and `{example}`. LaTeX `\notag` directives are automatically added to formulas within those foldable sections. In order to enable enumeration in this section, add the directive `:enumeration: on`.
+ Render LaTeX math expression in popup windows of footnotes.
+ Implement popup window for displaying LaTeX equation referenced by `\eqref{EQUATION_LABEL}` links. A referenced equation is displayed when the mouse hoovers over a reference link to it. (Only Implemented for KaTeX renderer)
+ Implement unix shell script wrappers in the docker/podman container image.
+ Implement user account management.
   + Implement user account management, including:  list all users; create new user account;
    delete user account and edit user account. The user account panel can be accessed by
    opening the menu item Settings => User Accounts. The URL routes for user account management
    are: /users - List all users; /users/new - Create new user accoun); Edit user account /users/edit?user{USERNAME}.
+ Show a horizontal scroll bar if a display-mode LaTeX equation does not fit a mobile device screen.
+ Rename static websiste generator (compiler) command $ mwiki compile to $ mwiki export.
+ Add `--source` switch flag for the command $ mwiki export.
   + Add --source command line switch to MWiki static websiste generator. This option displays a menu item that shows the markdown (wikicode) source code of the current wiki page. This feature is useful for generating fully open source documents and allow users to view the document sources.
+ Add  command line switch `--latex-render` for `$ mwiki export` command. This swtich allows changing the LaTeX renderer to MathJax with `--latex-render=mathjax` or to KaTeX with `--latex-render=katex`.
+ Add development dependencies, pytest pytest-cov (test coverage) and parsel (html5 parser) for unit testing.
+ Rename command line swtich `--embed-mathjax` to `--embed-latex-render` for the command $ mwiki export. This command line switch is used for self-hosting the front-end javascript libraries Mathjax or KaTeX. The default behavior of this command is to load the LaTeX rendering library from a CDN (Content Delivery Network).
+ Implement compilation of markdown to self-contained html file.
   + Implement flag --self-contained for the command $ mwiki compile. This flag enables compilation of MWiki markdown files (wiki pages) to a self-contained html file, which contains all resourses, including icons, images, scripts and style sheets, encoded in base64 format. The self-contained html files are suitable to offline reading in a similar to PDF files.  In android mobile devices, the self-contained html files can be viewed just by opening them in any file browser and selecting the option to open with the Android built-in Html viewer.
+ Command $ mwiki export now can compile LaTeX on server side using KaTeX
   + Now the command $ mwiki export with the --compile-latex can build static websistes or self-contained html files with LaTeX formulas embedded as HTML fragments, compiled by KaTeX CLI - Command Line Interface. This feature requires a NodeJS (nodejs runtime) installation and the parent directory of the node executable to be listed in the $PATH environment variable. If nodeJS is not avaiable in or accessible in the command line, it is possible to set the environment variable MWIKI_NODE_PATH to nodejs path. The NPM package manager is not used sinece KaTeX is vendored by MWiki (the KaTeX source code is bundled with MWiki source code).
+ Remove rendundant command compile_latex from the module mwiki.cli.
  + The command removed was used for compiling all LaTeX formulas using xelatex, pdflatex, pdfcrop and pdf2svg. Now LaTeX formulas can be compiled and pre-rendered by using a vendored KaTeX javascript library.
+ Create Unit Test suite tests/test_ast.py, tests/test_render.py, tests/test_latex.py and
+ Add makefile rule "cov" for obtaining the test coverage report using pytest.
+ Bugfix - The pencil icon buttons for editing sections or the whole page are only visible to admins.
   + Before this commit, the pencil icon button for editing sections or a whole wiki page were not visible to anonymous users, but they were visible to guest users (without admin privilege). Now those buttons are only visible to admin users.
+ Bugfix - Action buttons of the search page /pages are only shown for admin users.
   + The page /pages list all wiki pages or pages matching the search results. Each search match has three buttons, edit, delete and view source. Now those buttons are only show to admin users. Anonymous and guest users do not view those buttons. Authorization (permission) for those action, including delete and edit are still enforced in the server side.


## Release v0.8.1

+ Display root URL in the compilation output.
+ The command $ mwiki compile displays all compilation settings.
+ Display value of boolean compilation settings as on/off instead of True/False.
+ Display information about mathjax self-hosting in the '$ mwiki compile' output.
+ Add command line switch --author to the static generator command.
   + Add command line switch --author="Author Name" to the subcommand $ mwiki compile. This command line option allows overriding the author attribute in the frontmatter of all MWiki pages if they are not set. This command line option only makes sense if all pages have the same author.  The author field is compiled to the html meta tag `<meta name="author" content="Author Name">`.
+ Add flag --embed-mathjax to the command $ mwiki compile.
   + Add command line switch --embed-mathjax to the static website generator subcommand $ mwiki compile for self hosting mathjax in the static websiste instead of loading the library from a CDN (Content Delivery Network). If this command line switch is enabled, mathjax is copied from the module mwiki to the static websiste output directory. The drawback of this approach is the larger disk space and bandwidth usage.
+ Bugfix - Fix popup window for creating new MWiki page/note.
+ Bugfix - Fix edge case of the static websiste compile when root URL is /.
+ Bugfix - Fix the display of LaTeX algorithms in the static website generator.
+ Bugfix - Fix the style of .admonition-title css class on mobile devices.
+ Bugix - Fix relative URL of admonitions' SVG icons when using a different root URL than /.
   + Fix static websiste generator that did not resolved the path of admonitions' SVG icons when using a different root URL than the default root URL.

## Release v0.8


+ Created checkbox for toggling password display in the login form. dth usage.
+ Created editor line wrapping checkbox.
   + Implement editor checkbox for toggling line wrapping which, may be desirable when editing long lines that needs alignment, such as wide tables.
+ Added editor checkbox that allows users to override Vim emulation default settings.
   + The settings form has a checkbox that alllows enabling or disabling emulation for all users. The checkbox added to the editor page allows users to override the default Vim emulation settings and persist the user-specific configuration in the browser's local storage. The checkbox makes toggling Vim emulation faster as users no longer have to lose their focus to enable or disabling Vim keybindings by opening the settings form page.
+ Implemented popup window that allows users to override the current locale.
    + This change improves the i18n internationalizatioin infrastructure by  addding the item "Language" to the main menu for opening a form that allows users to quickly switch the current user interface language. The user language setting is unique for each user and persisted in the browser local storage. If there is no user locale/language setting in the local storage, then the system attempts to get the user locale from the JavaScript navigator.language API when the checkbox "always use default language/locale" is disabled. When the previous checkbox is enabled, the UI language is the default one set by the admin in the settings form. Note that even if the checkbox "always use the default language" is enabled, each user is still able to switch the user interface language during his or her session
+ Implement file uploading by dragging and dropping.
   + Implement file upload by dragging and dropping files from the desktop to the Wiki editor. When a file is dragged and dropped on the editor, the upload popup window is shown and the user can click at the button upload, change the file name or cancel the operation.
+ Disable save buttons while saving the document.
  + Save buttons are disabled while saving the document in order to avoid multiple concurrent request and idempotency issues that could cause data loss in  aslow connection if an user attempted to click any save button multiple times. If the http post request fails, the save buttons are enabled again.
+ Improve portuguese localization related to edit-page-upload-button i18n key.
+ Implemented magic link for passwordless authentication.
  + The command $ mwiki auth generates a sign in link that also allows authentication without password by copying and pasting the link. The magic login link is valid for 1 minute and uses HMAC signature to ensure its authenticity and integrity.  This feature is similar to Jupyter server token URL login, that allows logging in to a Jupyter Lab server by pasting the magic link in some web browser.
+ Added flag --auth to the command $ mwiki server command for passwordless login.
  + When the flag --auth is added to the command $ mwiki server, a login token and login URL for passwordless authentication are printed in ther terminal before starting the server. Both the token and the URL are valid for 20 seconds and can be used for fast authentication as admin without password. The authentication is endpoint cannot be manipulated be non authorized users as it uses a random numer salt and HMAC digital signature. +  Secret key is now stored in the wiki repository.
    + Before this change, the secret key was stored in special folders for application data sepecific for each operating system. Now the secret key is stored in the file $WIKI_REPOSITORY/.data/appkey.txt. The key is a uniquely generated random hexadecimal string during the wiki initialization and is unique per MWiki deployment.
+ Implemented lazy loading of the library pseudocodeJS.
   + Now the library pseudocodeJS, for rendering LaTeX pseudocode blocks of algorithms, is only loaded when there is at least one pseudocode block in the markdown code. This code change improves the page loading speed and reduces bandwidth.
+ Implemented Graphviz lazy loading.
   + The graphviz library, for redering graph diagrams written in graphviz dot language, is now loaded only when needed. This modification ensures faster page speed loading and less bandwidth costs.
+ Created static website generator.
  + Implement comamnd line $ mwiki compile that compiles the whole MWiki markdown repository to a static website that can be easily deployed by copying and pasting files to a static file web server. Static files can also be served using Caddy, NGinx, github or gitlab repository.
+ Implemented rendering of "author" attribute in the YAML frontmatter to html `<meta>` tag. The author attribute in  the YAML frontmatter `athor: John Doe` is rendered to `<meta name="author" content="John Doe">`.
+  Page description attribute in the YAML frontmater, for instance `description description here.` is compiled to the html meta tag `<meta name="description>description here">`.
+ Added new fonts (typefaces) choices in the settings form: Jackwrite, Jackwrite Bold (font that mimics typewriter text with leaked ink in an old sheet of paper), medieval font Fondamento, DINWeb, CMU Concrete, CMU Sans Serif, peachi medium, saira thin and saira thin bold. Added Epson dotmatrix 1980's/80's nostalgia fonts, that mimics Epson dotmatrix fonts popular in the 1980s for printing code in computer magazines.
+ Improve search - normalize Romanian and Istro-Romanian alphabets letters to English alphabet. 
+ Improve search - normalize Maltese Alphabet letters to English alphabet.
+ Improve search - normalize letters of the Czesh alphabet to English alphabet.
+ Bugfix - Fix the label of the login button.
+ Bugfix - Add missing required html attributes in the login form.
+ Bugfix - Fix menu button for creating new note.
+ Bugfix - display warning for AST element without renderer function.  
    + A "Rendering not implementd" warning is issued instead of throwing an exception when there is no implementation of renderer method for a markdown element.
    


## Release v0.7

+ Update Python minimum required version to 3.9 and remove version pinning for updating dependencies. Note that the version of depedencies are still fixed in the lockfiles for supply chain security purposes. 
+ Delete poetry.lock - lock file of poetry package manager because now this project will only use UV package manager.
+ Improve upload form style.
+ Improve usability - use pointer cursor for section headings.
+ Add new fonts/typeface choices in the settings form: Crimson, Muson,  Bricolage Grotesque, range and range mono fonts/typefaces.
+ Enhance user feedback when uploading pasted image.
  + Improve user feedback by showing in the status bar whether the system is still uploading the pasted image from clipboard and also whether the upload was successful.
+ Insert figure block `{figure}` (images with metadata) upon upload of other image formats including webp, apng, bmp, avif, ico and svg.
+ Refresh page if its timestamp is greater than the edit button timestamp.
  + When the user clicks at the pencil icon,  on the left side of a wiki page section header, and the timestamp provided in the pencion icon hyperlink is older than the page timestamp, the page is reloaded in order to ensure that the user is always editing the most up-to-date wiki page file.
+  Feature - Extend syntax of {comment} block for toggling rendering of enclosed code. The `{comment}` block syntax was extended with commands "on" and "off" for toggling the rendering/display of the enclosed markdown code without needing the removal of the backticks and tag `{comment}`. This feature is useful for toggling the display of content that is not ready to be published.
+ Recompile markdown if the version of metadata file does not match the expected version.
+ Implement MyST role raw ````{r}`text```` and ````{raw}`text`````. Due to compatibility with Github Flavored Markdown, angle brackets may be interpreted as html tags which may not be desirable. MyST raw role ```{r}`enclosed text```` or ```{raw}`enclosed text```` solves this issue by rendering the text to iself. For instance the markdown ```{r}`<a href="https://site.com">label</a>```` code is rendered to `<a href="https://site.com">label</a>` without monospace font/typeafce instead of being rendered to a html hyperlink.
+ Implement footnote reference `term1^[footnote here]` - syntax compatible with MyST markdown and Obsidian.
+ Implement footnote reference `term^{footnote here}` - custom MWiki syntax. However, the advantage of this syntax is the lack of conflict with markdown constructs such as hyperlinks `[label](http://some-site.com).` 
+ Implement footnotes listing syntax using code blocks with tag `{footnotes}`. This construct lists all footnotes of current page and hyperlinks to the corresponding footnotes references in the document.
+ Implement `{video}` blocks for embeding videos with metadata, such as caption below the video with enumeration.
+ Improve rendering of embedded pages.
+ Add i18n internationalization of the form successful update message.
+ Only load mathjax in the template base.html when necessary for making page loading faster.
+ Improve sytle of foldable blocks such as `{example}`, `{solution}` and `{proof}`.
+ Improve search - normalize escape characters `\.` and `\:`.
   + The domain name of websites such as somedomain.org is parsed as URL by default. When this behavior is not desirable, the URL is written as `somedomain\.org`. However, this breaks the search as searching for somedomain.org yields no result. The solution for this issue added by this commit is to to turn the escaped character `"\."` into `"."` and `"\:"` into `":"` when storing the text in the search index database for full text search.
+ Improve search - Normalize spanish diactric (ñ) n tilde to n.
+ Improve search - normalize diactrics and ligatures of french latin alphabet.
  + Letters, ligatures and diactrics of French latin alphabet are now normalized to equivalent letters of English alphabet in order to enhance for french words with an english keyboard layout or a non french keyboard layout.
+ Improve search by normalizing diactrics, accents and chracters from Old English, Old Norse, Icelandic and Sweedish alphabets to corresponding letters of the English Alphabet.
+ Improve search - normalize Vietnamese latin alphabet to English Alphabet.
  + Normalize letters, symbols and diactrics of the Vietnamese latin alphabet to English alphabet for improving the search engine. This feature allows searching for vietnamese words using an English keyboard layout. For instance, the vietnamese word "người" is stored in the search index database as "nguoi" instead of being stored as "người". So, searching for "nguoi" or "người" yields the same search results. As a result, this approach makes it easier to search for vietnamese words using an English keyboard layout or non vietnamese keyboard layouts.
+ Bugfix - Fix regex of markdown_it_parser plugin for wiki links.
  + The parser failed to recognize wiki internal links
    when there were two wiki links in the same line, for instance, the
    parser failed to recognize `See about [[Unix]] and [[Linux]]` due to use of greedy regex quantifier star `(*)` instead of star  followed by question mark `(*?)`.
+ Bugfix - Fix pencil hyperlinks in section headers for editing corresponding sections.

## Release v0.6


+ Refactor watcher module for using polling instead watchdog module for improving realibility.
  + This refactoring was needed due to the buggy behavior of watchdog module (library). In addition, there are many reports that this module may not work well on Micrsoft Windows and sometimes fail to work on Linux.
+ Implement normalization of other latin alphabets to english Alphabet (Improve Search).
   + This commit implements normalization of other latin alphabets variants to English latin alphabet, including Polish latin alphabet, Turkish Latin Alphabet and Serbo-Croatian alphabet. This feature allows searching for words written in other latin alphabet variants using only letters of English alphabet. For instance, it is possible to search for the Polish word Władysław by typing "Wladyslaw" instead "Władysław", whose letters are not available in an english keyboard layout. If a Wiki page contains a word such as "Władysław" or other words written using letters of Polish, Turkish or Serbo-croatian alphaet, the letters are not available in English are turned into English equivalent letters. For example, the word "Władysław" is recorded as "Wladyslaw" in the search index database. If the user types the word in Polish letters "Władysław" in the search form, the word it is turned into "Wladyslaw". As a result, the search results will contain all pages with "Wladyslaw" or "Władysław" word.
+ Improve search - Normalize Danish and Norwegian alphabets to English alphabet.
+ Implement internationalization (i18n) infrastructure for adding multiple locales to the UI - User Interface without changing any part of the code. The UI - User Interface supports the following locales, en-US (American English) and pt-BR (Brazilian Portuguese). But, it is possible to add new languages by editing only a JSON global variable.
+ Implement UI localization to Portuguese language (Brazilian Portuguese). The default language of the user interface is English (American English spelling). However, it is possible to change the default locale/language in the settings form.
+ Normalize English locales to en-US (American English) and Portuguese locales to pt-BR (Brazilian Portuguese).
    + Map all english locales provided by the web browser to en-US ) and all portuguese locales to pt-BR (Brazilian Portuguese). In the future, more locales of other languages or different dialects of the same language can be added. 
+ Fix css style of the log in form for mobile devices.
+ Improve look and feel of the login form (also known as sig in or authentication form).
+ Improve appearance of the settings form.
+ Improve look and feel of the popup window for insert link to a wiki page.
+ Accessibility improvement - Use figure caption as alt text if no alt text is provided.
+ Performance improvment - Recompile markdown file if any link depency is changed.
  + Details: If a page contains an internal to hyperlink to a Wiki page `[Mass Moment of Internetia Tensor]]` and the corresponding     markdown page does not exist yet the link will be red. If this page corresponding to this link is created and the page referencing this link is refreshed, it will be recompiled for updating the cached html. After recompilation the link will become green.
+ Implement custom MyST role for adding notes to text.
+ implement save icon button in the editor page header.
   + This diskette icon allows quickly saving a Wiki page document in a mobile device with small screen.
+ Update reference card - add example about  Note MyST role.
+ Bugfix - Create search index directory if it does not exist yet.
+ Bugfix - Fix equation enumeration undefined javascript bug in the preview window.
+ Bugfix - Fix the behavior of the popup window for displaying abbreviations of `<abbr>` htm5 elements in mobile devices. 
+ Bugfix - Fix back link of the settings page.



## Release v0.5.1

+ Implement fast and efficient full text search.
  + Implement fast and efficient full text search, similar to web search engine using Python Whoosh library.  + Improve full text search by normalizing words and adding the fuzzy match plugin.
+ Update search index outside the http request-response transaction.
  + Now the Python Woosh search index is updated outside the request-response cycle for speeding up the server response.  The module mwiki.watcher watches the file system and detects modified markdown files and updates the search index database of Python Woosh full-text search engine.
+ Implement checkbox show licenses (enabled by default) in the settings form.
  + If this checkbox is eanbled, a menu option whith the label 'Licenses' is added to the main menu. When clicked this menu option redirects to a page showin the license of this project AGPL (GNU Afero) and the licenses of all depedencies used by this project giving credit to other projects and open source developers.
+ Change code for {figure} block of pasted image inserted in the editor.
+ The http route /licenses is only available if show_licenses flags is enabled.
+ Add Python Whoosh to open source licenses template page.

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

## Release v0.3.1

+ Implement optional section enumeration.
+ Implement Keyboard shortcuts for quick navigation.
+ Disable annoying pull-down-to-refresh behavior in mobile browsers.


## Release v0.2

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


## Release v0.1

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

