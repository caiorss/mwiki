# Changelog 


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

