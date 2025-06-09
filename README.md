# MWiki - Markdown-Powered Wiki 

## Overview 

MWiki is a **wiki engine** and note taking web application software geared towards mathematics and research designed for scientific and technical communication. This wiki engine software has semantic-rich lightweight markup language based on MyST markdown, Obsidian markdown, and Media wiki engine markup language. 

This Python application is powered by Python Flask web framework and the extensible markdown-it parser used by MyST markdown and the Jupyter Book project. 


+ Note: This software is still **work in progress** and under early stage. However, it can already be used as a personal note taking application.
+ Note: Mediawiki is the wiki engine software that powers Wikipedia.

See also:

+ [README in Portuguese](./README-portuguese.md) - Portuguese language version of this document. The original documentation was written in English.


### Features Highlights

#### Wiki Features 

+ File-based Wiki: all Wiki pages are stored as Markdown files like Moin Moin wiki engine and Dokuwiki. However, it uses SQLite file database or a any full-featured database for system management purposes. 
 + Supports MyST Markdown, GFM (Github-Flavored Markdown Support), subset of Obsidian Markdown syntax, subset of Mediawiki markup language and inline HTML.
 + Pages written in Markdown-based markup language instead of HTML, which allows to any non programmers to write scientific and technical documents that are rendered to html. 
 + Buttons for editing specific document sections similar to Media wiki section editing buttons. 
 + File upload. Now the wiki code editor has a button for inserting a hyperlink to an uploaded file. When the button is clicked, a popup window for upload is shown. Once the user sends the file, the window is closed and a link to the file is inserted in the editor.
 + Embeddable pages. The contents of a wiki page can be embedded in another wiki page by using the syntax `![[Name of Wiki page to be embedded]]`
 + Document preview - allows users viewing how a wiki page markdown text will look like when rendered before saving it. The editor's preview button also allows viewing how a selected markdown code of a wiki page looks like when rendered.
 + Vendored third-party JavaScript dependencies for offline usage. For instance, MWiki has MathJax, pseudocode-JS, and Ace9 in the source code for offline usage even when no CDN is available due to lack of internet connectivity or if the Wiki is used in rescrited environment behind a firewall. 


#### Access control 

 + The wiki has the following types of users: *admin*, that can edit the Wiki pages; *guest* a registered used which can view pages even if the wiki is not public, but a guest user cannot edit any page; and *anonymous* users (non logged in users) that can only view pages if the **public** checkbox in the Wiki settings ('/settings' pages) is enabled.
 + Public/private wiki settings - if the **public** checkbox in MWiki settings page is disabled, only logged in users will be able to view the wiki pages and non logged in users will be redirected to the authentiation screen. If this checkbox is enabled, non logged in users can view the wiki. Note that: only users of type administrator can edit the wiki pages and make changes to any content.


#### Text Editor Features

+ Markdown **Code editor** built on top of Ace9 JavaScript code editor.
+ *Clipboard to markdown converter*, which allows turning html content copied from any other web page (aka web site) to MWiki markdown. This feature is similar to Obsidian's non-plain text copying and pasting. 
+ Upload images by pasting them from clipboard. 
     + Usage: Copy any image using the right click on any picture and past it on the text editor sesssion of some wiki page either by using the mouse or typing Ctrl + v.
+ NOTE: The clipboard features rely on Clibpboard Html5 API, which only is available on [secure contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts). Therefore pasting images from clipboard to the wiki text editor only works if the wiki is served on local host or from a domain with https (HTTP + TLS), which may require a reverse proxy such as Caddy or NGinx for TLS/SSL encryption and server authentication.
+ [VIM](<https://en.wikipedia.org/wiki/Vim_(text_editor)>) Editor Keybindings: The Wiki editor uses VIM keybindings by default.

See also:

+ *VIM dot ORG* - Official Website
  + https://www.vim.org
+ *Vim (text editor)*
  + https://en.wikipedia.org/wiki/Vim_(text_editor)
+ *A Great Vim Cheat Sheet*
  + https://vimsheet.com/
+ *Vim Cheat Sheet*
  + https://vim.rtorr.com
+ *Vim Key Bindings – Vim Keys List Reference*
  + https://www.freecodecamp.org/news/vim-key-bindings-reference/
+ *vi Complete Key Binding List*
  + https://hea-www.harvard.edu/~fine/Tech/vi.html


#### Wiki Markup Language

+ Text formatting:
   + Italic Text 
   + Bold Text 
   + Strikethrough text (also known as deleted text)
   + Colored text 
   + Abbreviation, which corresponds to the `<abbr>` html5 tag.
   + Superscript text 
   + Subscript text 
+ Code blocks with syntax highlight
+ Tables 
+ List 
   + Bullet List 
   + Ordered Lists 
   + Definition Lists 
+ Scientific and Technical Communication 
   + Built-in inline LaTeX formula (powered by MathJaX)
   + Built-in LaTeX formula (display mode) with automatic enumeration
   + Special code blocks for adding custom LaTeX macros
   + Pseudocode code block 
   + Admonition (also known callout box) for mathematical definition 
   + Admonition for mathematical theorem 
   + Admonition for solved exercise examples 
   + Foldable section for solution of solved exercise 
   + Foldable section for theorem proofs, used in theorem admonition.
+ Admonitions 
  + Tip Admonition 
  + Note Admonition
  + Information Admonition
  + Warning Admonition 
  + Foldable Admonition   

View detailed documentation and examples at: 

+ [Markup Language](./README-Markup-Language.md)

## Demonstration 

### GIF Animations 

**Usage GIF animation**

![](images/mwiki-animation-usage1.gif)

**Copying and pasting images**

![](images/mwiki-animation-usage2.gif)

**Markdown preview feature**

+ The editor button preview allows viewing how a wiki page will look like before saving it. The preview feature also allows viewing how a selected markdown text will look like before saving it.

![](images/wiki-markdown-preview.gif)


### Screenshots

**Wiki Screenshot 1**

This Wiki page, whose relative URL is /wiki/Linear%20Algebra%20New is generated by processing the file 'Linear Algebra New.md'.

![](images/screen1.png)


**Wiki Screenshot 2**

![](images/screen2.png)

**Wiki Screenshot 3**

![](images/screen3.png)

**Wiki Screenshot 4**

MWiki code editor powered by Ace9 Javascript code editor.

![](images/screen4.png)

**Wiki Screenshot 5**

MWiki settings page.

![](images/screen5.png)

**Wiki Screenshot 6**

Global menu screenshot.

![](images/screen6.png)

**Wiki Screenshot 7**

Screenshot of page menu that allows to perform actions on the current Wiki page.

![](images/screen7.png)

**Wiki Screenshot 8**

It is possible to fold all Wiki headings for fast navigation on mobile devices or desktop by clicking at the '(F)' button on the top navigation bar.

![](images/screen8.png)


**Wiki Screenshot 9**

![](images/screen9.png)

**Wiki Screenshot 10**

The Wiki has built-in search engine that allows searching for keywords in all Markdown files used for rendering the wiki pages.

![](images/screen10.png)

**Wiki Screenshot 11 - Reference Card**

This wiki provides a reference card popup windown that provides examples of the MWiki markup language (custom markdown).

(1) Open the reference card.

![](images/refcard1.png)

(2) Reference card with all sections folded.

![](images/refcard2.png)

(3) Reference card with a section unfolded.

![](images/refcard3.png)


## Installation 

### Installation using UV package manager

[UV](https://github.com/astral-sh/uv) is a newer blazing fast package manager for Python, that can even install multiple specific versions of the Python interpreter without disrupting Python installation used by the system. UV can also install Python tools in isolated environment without breaking the current Python installation. 

**STEP 1**

```sh
$ uv tool install git+https://github.com/caiorss/mwiki
  ... ... ... ... ... ... ... ... ..
  Installed 2 executables: mwiki, mwiki-convert
```

**STEP 2** Run executable mwiki:

```sh
$ mwiki 

Usage: mwiki [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  compile  Compile Latex Formulas of .md file or folder to SVG images.
  convert  Convert from org-mode markup to markdown
  manage   Manage MWiki settings, including accounts, passwords and etc.
  server   Run the mwiki server.
```

**Inspect Executable Files**

```sh
$ which mwiki
/home/username/.local/bin/mwiki

$ whereis mwiki
mwiki: /var/home/username/.local/bin/mwiki

$ file $(which mwiki)
/home/username/.local/bin/mwiki: symbolic link to /home/username/.local/share/uv/tools/mwiki/bin/mwiki

$ file $(readlink $(which mwiki))
/home/username/.local/share/uv/tools/mwiki/bin/mwiki: Python script, ASCII text executable
```

**Uninstall**

```sh
$ uv tool uninstall mwiki 
Uninstalled 2 executables: mwiki, mwiki-convert
```

### Installation using Pipx pacakge manager 

**STEP 1:** Pip and Python are assumed to be already installed.

Install [pipx](https://github.com/pypa/pipx) tool.

```sh
$ pip install pipx 
```

**STEP 2:** Install using Pipx

Install Mwiki using Pipx (MWiki requires Python >= 3.9)

```sh
$ pipx install git+https://github.com/caiorss/mwiki 
  installed package mwiki 0.1, installed using Python 3.9.19
  These apps are now globally available
    - mwiki
    - mwiki-convert
    - mwiki_convert
done! ✨ 🌟 ✨

```

Install Mwiki using Pipx and a different version of Python. This command is useful if the default version of Python in the current system is 3.8 or a non supported version.

```
$ pipx install --python=3.9 git+https://github.com/caiorss/mwiki 
```

### Installation using Docker 

Docker is the most realibable way to install Python application since it is reproducible and helps to avoid the Python and Pip dependency hell (also knowns as "works-on-machine problem"). 

**STEP 1:** Clone the repository

```sh 
$ git clone https://github.com/caiorss/mwiki mwiki

# Enter source code directory
$ cd mwiki
```

**STEP 2:** Build the docker image.

```sh
$ docker build --tag mwiki-server .
```

or run the Makefile (only supported on Unix-like systems with GNU Make)

```sh
$ make docker 
```

**STEP 3:** Run MWiki docker image. The $WIKIPATH environment variable is set to any directory containing markdown files, including Obsidian vaults.

Create a .env file in the current directory containing the initial configuration of MWiki passed as environment variables. (Optional)


File: .env

```
MWIKI_ADMIN_PASSWORD=u2afb5ck69
MWIKI_SITENAME=WBook
WIKI_PUBLIC=
```

Run docker passing the .env configuration file.

```sh
$ docker run --rm -it  --privileged \
            --network=host --env-file=$PWD/.env \
            --volume="$WIKIPATH:/wiki" mwiki-server
 [TRACE] Admin user created OK
 [INFO] Enter the username: admin and password: 'SN81N87JZ6' to log in.
[2025-01-09 20:00:40 +0000] [1] [INFO] Starting gunicorn 23.0.0
[2025-01-09 20:00:40 +0000] [1] [INFO] Listening at: http://0.0.0.0:9090 (1)
[2025-01-09 20:00:40 +0000] [1] [INFO] Using worker: sync
[2025-01-09 20:00:40 +0000] [7] [INFO] Booting worker with pid: 7
[2025-01-09 20:00:40 +0000] [8] [INFO] Booting worker with pid: 8
[2025-01-09 20:00:40 +0000] [9] [INFO] Booting worker with pid: 9
[2025-01-09 20:00:40 +0000] [10] [INFO] Booting worker with pid: 10
[2025-01-09 20:00:40 +0000] [11] [INFO] Booting worker with pid: 11
[2025-01-09 20:00:40 +0000] [12] [INFO] Booting worker with pid: 12
[2025-01-09 20:00:40 +0000] [13] [INFO] Booting worker with pid: 13
[2025-01-09 20:00:40 +0000] [14] [INFO] Booting worker with pid: 14
[2025-01-09 20:00:40 +0000] [15] [INFO] Booting worker with pid: 15
 [TRACE] _username = admin ; _password = SN81N87JZ6
 [WARNING] Note implemented html rendering for foot_note_block =  SyntaxTreeNode(footnote_ref)
 [WARNING] Note implemented html rendering for foot_note_block =  SyntaxTreeNode(footnote_block)

```

Run as a daemon (background service detached from terminal):

```sh
$ docker run --detach \
           --name=mwiki  \
           --network=host \
           --env-file=$PWD/.env \
           --privileged \
           --volume="$PWD/pages:/wiki" mwiki-server
a6f0838f5159ff75aa25228fafdbd2f4fe1432c3359a9dc5d3ec84b10d801577
 
```

View logs from mwiki container:

```sh
$ docker logs -f mwiki
[2025-01-09 20:06:23 +0000] [1] [INFO] Starting gunicorn 23.0.0
[2025-01-09 20:06:23 +0000] [1] [INFO] Listening at: http://0.0.0.0:9090 (1)
[2025-01-09 20:06:23 +0000] [1] [INFO] Using worker: sync
[2025-01-09 20:06:23 +0000] [7] [INFO] Booting worker with pid: 7
[2025-01-09 20:06:23 +0000] [8] [INFO] Booting worker with pid: 8
[2025-01-09 20:06:23 +0000] [9] [INFO] Booting worker with pid: 9
[2025-01-09 20:06:23 +0000] [10] [INFO] Booting worker with pid: 10
[2025-01-09 20:06:23 +0000] [11] [INFO] Booting worker with pid: 11
[2025-01-09 20:06:23 +0000] [12] [INFO] Booting worker with pid: 12
[2025-01-09 20:06:23 +0000] [13] [INFO] Booting worker with pid: 13
[2025-01-09 20:06:23 +0000] [14] [INFO] Booting worker with pid: 14
[2025-01-09 20:06:24 +0000] [15] [INFO] Booting worker with pid: 15

```

Stop MWiki container:

```
$ docker stop mwiki 
mwiki
```

Start MWiki container 

```sh
$ docker start mwiki 
```

Restart MWiki container software.

```sh
$ docker restart mwiki
```

Change site name using the built-in CLI (Command Line Interface)


```sh
$ docker exec -it mwiki python -m mwiki  manage --sitename=WNotes
 [*] Site name changed to: WNotes
```

Change admin password.

```sh
$ docker exec -it mwiki python -m mwiki  manage --admin-password=somePassNewPassword
```

**STEP 5:** 

Open MWiki in the web browser, in the port 8080 by copying and pasting the URL http://localhost:8000 and enter 'admin' in the username entry and the initial admin password in the password field. The initial admin password is provided in the previous command output. In this password is '0JAJ6UAMUA', which is a random generated string unique per MWiki installation.

**STEP 6:**

Open the settings page http://localhost:8000/admin and change the Wiki settings. Then go the URL http://localhost:8000/user and change the admin password. Note that user passwords are never stored in plaintext, they are always stored in hashed form for security reasons.


### Installation via Docker-Compose or Podman-Compose 


**STEP 1:** Clone the repository

```sh 
$ git clone https://github.com/caiorss/mwiki mwiki

# Enter source code directory
$ cd mwiki
```

**STEP 2:** Edit the config.env file.

File: config.env

```sh
# MWiki configuration files 
#----------------------------------#

MWIKI_SERVER_ADDR=mwiki 
MWIKI_SERVER_PORT=9090

# Path to wiki folder, where *.md markdown files, images and other 
# files will be stored.
MWIKI_PATH=./sample-wiki

# Password of main admin
MWIKI_ADMIN_PASSWORD=mypasswd

# Name of the Wiki (Name of the website)
MWIKI_SITENAME=MyNoteBook

# URL which the website is hosted or just domain name 
MWIKI_WEBSITE=localhost sbox.ts 

# Configure MWiki as a private Wiki. 
# => Only logged in users can view wiki pages. 
# MWIKI_PUBLIC=   

# Configure MWiki  as a public Wiki.
# => Anonymous users can view wiki pages, however only 
# admin users can edit.
MWIKI_PUBLIC=true

# Server static files using Caddy or NGinx 
MWIKI_X_ACCEL_REDIRECT=true

#----------------------------------------------------##
##      Less common Settings for certificate         ##
#----------------------------------------------------##
# They are not needed if the server is hosted in a machine
# with static and public IP address. Those settings are only
# required when hosting in internal networks (LANs).
#
MWIKI_INTERNAL_CA=
MWIKI_ACME_CA_URL=
```


**STEP 3:** Run docker-compose or podman compose for the deployment.

Deploy with docker-compose.

```sh
$ docker-compose --env-file=./config.env up -d 
```

Deploy with podman-compose.

```sh
$ podman-compose --env-file=./config.env up -d 
```

**STEP 4:** TLS/SSL Certificates

If the MWiki is hosted in a machine with static and public IP address reacheable from anywhere on the internet and MWiki domain points to this IP address, Caddy will automatically obtain the TLS/SSL certificate from Let's Encrypt CA - Certificate authority. 

If this application is hosted on local network or site-to-site VPN, such as tailscale and using Let's Encrypt CA is not possible, Caddy can be turned into a local CA - Certificate Authority by editing the config.env and changing 

```
MWIKI_INTERNAL_CA=true
```

This step creates an endpoint 

+ `https://<mwiki-website-domain>/root.crt`

where the user can download the root CA certificate and install it on web browsers or phones. This root CA cerfiticate can be downloaded using curl. This procedure is useful for self-hosting MWiki on home labs.

```sh
$ curl -O -k --silent https://<mwiki-website-domain>/root.crt
```

See also:

+ *Set up Certificate Authorities (CAs) in Firefox*
  + https://support.mozilla.org/en-US/kb/setting-certificate-authorities-firefox
+ *Installing a Root Certificate Authority in Firefox* 
  + https://chewett.co.uk/blog/854/installing-root-certificate-authority-firefox/
+ *How to Add a Certificate on Android? Step by Step*
  + https://www.airdroid.com/mdm/add-certificate-android/

## Development 

**STEP 1:** Clone the repository

```sh
$ git clone <REPOSITORY-URL>  mwiki
$ cd mwiki
```

**STEP 2:** Install [Poetry](https://python-poetry.org/) package manager if it is not installed yet.

```sh
$ pip install poetry 
```

**STEP 2:** Install dependencies with Poetry.

```sh
$ poetry install 
```

**STEP 3:** Generate VScode JSON files .vscode/settings.json and .vscode/launch.json for integrating Poetry, Virtualenv and VSCode editor.

```
$ make vscode
```

or run

```sh
$ pythopn vscode.py

## OR 

$ ./vscode.py # On Unix-like operating system (Linux, BSD or MacOSX)
```

**STEP 4:** Run MWiki in development mode.

```sh
 $ poetry run mwiki  server  --debug \
                              --host=0.0.0.0 \
                              --port=8000  \
                              --wikipath=/path/to/wiki-markdon-files/directory/notes
 [TRACE] Admin user created OK
 [INFO] Enter the username: admin and password: '0JAJ6UAMUA' to log in.
 * Serving Flask app 'mwiki.server'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8000
 * Running on http://192.168.0.103:8000
Press CTRL+C to quit
 * Restarting with stat
 [INFO] Enter the username: admin and password: '0JAJ6UAMUA' to log in.
 * Debugger is active!
 * Debugger PIN: 795-641-657
```

The notes folder, in this case '/path/to/wiki-markdon-files/directory/notes', is just a folder containing markdown files and images. This folder can also be a *Obisdian Vault*, a repository of markdown files and images.

```sh
 $ ls notes/
'Android OS for Mobile Devices.md'
'APL - Programming Languages.md'
 articles/
'Authoring Tools.md'
 AWS_Cloud.md
 aws.org
'Backend Design and Scalability.md'
'Backup and Digital Preservation.md'
 Bookmarks.md
 books/
'Books and Files.md'
'Business News.md'
'Caching Algorithms and Synchronization.md'
'Collected Info.md'
'Command Line.md'
'Compiler Design.md'
'Computer Architecture.md'
   ... ... ...  ... ... ... ... ...
   ... ... ...  ... ... ... ... ...

```

Every markdown file is rendered as wiki page. For instance the file 'Business News.md' corresponds to the wiki page 

+ `http://<PAGE-DOMAIN>/wiki/Business%20News`

or

+ `http://localhost/wiki/Business%20News`


**STEP 5:** 

Open MWiki in the web browser, in the port 8080 by copying and pasting the URL http://localhost:8000 and enter 'admin' in the username entry and the initial admin password in the password field. The initial admin password is provided in the previous command output. In this password is '0JAJ6UAMUA', which is a random generated string unique per MWiki installation.

**STEP 6:**

Open the settings page http://localhost:8000/admin and change the Wiki settings. Then go the URL http://localhost:8000/user and change the admin password. Note that user passwords are never stored in plaintext, they are always stored in hashed form for security reasons.



## Companion Software and Tools

The following set of companion sotfware or apps are recommended for MWiki as they can provide additional features and improve usage.

**Online Tools**

+ *Table Generator for Markdown, LaTeX and MediaWiki*
  + https://www.tablesgenerator.com
+ *Detexify*
  + https://detexify.kirelabs.org/classify.html
  + *Allows to recognize LaTeX symbols by drawing them by hand.*
+ *LaTeX Equation Editor*  
  + https://editor.codecogs.com/
+ *Mathcha.io*
  + https://www.mathcha.io
  + *Online tool for scientific/technical illustration drawing, which supports LaTeX symbols and has many building blocks for drawing geometric, electrical, mechanical and computer science diagrams or schemas. 
+ *How to write algorithm in Latex*
  + https://shantoroy.com/latex/how-to-write-algorithm-in-latex
+ *LaTeX/Algorithms - Wikibooks*
  + https://en.wikibooks.org/wiki/LaTeX/Algorithms


**Browser Addons**

+ *LibreWolf* - Fork of Firefox Web Browser
  + https://librewolf.net/
  + *Modified Firefox web browser hardened for better security, privacy and protection against tracking.*
+ *Obsidian Web Clipper* (Firefox Addon)* \[BEST\]
  + https://addons.mozilla.org/en-US/firefox/addon/web-clipper-obsidian
  + Extension that lets users to save web pages in markdown format or turn selected parts of the web page into markdown. This tool can be used with MWiki for extracting information from web pages as MWiki markup language is compatible with Obsidian markdown. 
+ *Web Archives* - Search for older versions of current URL win Web Archiver, archive.is and other sites.
  + https://addons.mozilla.org/en-US/firefox/addon/view-page-archive/
  + *View archived and cached versions of web pages on various search engines, such as the Wayback Machine and Archive․is.*
+ *Allow Right Click - Re-enable right-click on websites that overwrite it* (Firefox)
  + https://addons.mozilla.org/en-US/firefox/addon/re-enable-right-click/
  + *The "Allow Right-Click" extension modifies some JavaScript methods to enable the original right-click context menu when a web page intentionally blocks right-clicking on its content. Most modern browsers permit JavaScript to disable the default context menu when a web page provides its custom context menu for its content (such as in Google Docs). However, this ability can also allow website owners to disable the right-click context menu without providing any useful functionality. The extension adds a button to the toolbar area of the user's browser. Clicking the extension's icon injects a small script into the current page to remove the context menu blockage. It is important to note that the extension does not inject any code by default on any web page; it only does so on user action. Users can click the extension button to release the restriction when a website blocks the right-click context menu without offering a custom context menu.*
+ *Script Blocker Ultimate* - (NoScript, Disable JS)
  + https://addons.mozilla.org/en-US/firefox/addon/script-blocker-ultimate/
  + *Extension for toggling execution of Javascript, which allows disabling and enabling JavaScript.*
+ *Tree Style Tabs for Firefox*
  + https://addons.mozilla.org/en-US/firefox/addon/tree-style-tab



**Translation and Text-to-speak**

+ *Speech Note - Flathub* \[Linux Flatpak APP\] (Offline "G00gl3 Translator")
  + https://flathub.org/apps/net.mkiol.SpeechNote
  + Brief: *Speech Note let you take, read and translate notes in multiple languages. It uses Speech to Text, Text to Speech and Machine Translation to do so. Text and voice processing take place entirely offline, locally on your computer, without using a network connection. Your privacy is always respected. No data is sent to the Internet.*


**Screenshot Tools**

Note: These tools allows taking screenshots of select part of the screen and pasting the screenshot image at the target application or MWiki editor by typing Ctrl + v.


- *Spetacle* \[BEST\]
   + https://apps.kde.org/spectacle/
   + *KDE Plasma tool for taking screenshots. It also allows selecting rectangular are of the screen and adding texts and annotations. This app is available in any Linux distribution with KDE plasma desktop environment.*
- *Flameshot*
   + https://flameshot.org
   + *Cross platform screenshot tool available for Microsoft Windows, Linux distributions and Apple's MacOSX.*
- *Flameshot - Flatpak*  
   + https://flathub.org/apps/org.flameshot.Flameshot
- *KSnip - Flathub*  (KDE/QT Flatpak App)
   + https://flathub.org/apps/org.ksnip.ksnip
   + *Ksnip is a Qt based cross-platform screenshot tool that provides many annotation features for your screenshots.*
- *Shutter Screenshot tool* \[BEST\]
   + https://shutter-project.org
   + => Note: Note available as AppImage or flatpak app. It is easier to install Shutter in Debian-based or Ubuntu-based Linux distributions.


**Video Recorder**

+ *Peek - Flathub* (Screen Recorder - can create GIF animation or WebM and MP4 videos)
  + https://flathub.org/apps/com.uploadedlobster.peek
  + Brief: * Peek makes it easy to create short screencasts of a screen area. It was built for the specific use case of recording screen areas, e.g. for easily showing UI features of your own apps or for showing a bug in bug reports. With Peek you simply place the Peek window over the area you want to record and press "Record". Peek is optimized for generating animated GIFs, but you can also directly record to WebM or MP4 if you prefer.*

**Container Orchestration Tools**

+ *Docker Compose*, Docker Company Official Docs
  + https://docs.docker.com/compose/
+ *Podman Compose*, Red Hat 
  + https://docs.podman.io/en/latest/markdown/podman-compose.1.html


**Site-To-Site Mesh VPN (Virtual Private Network)**

A site-to-site mesh VPN such as **tailscale** can be helpful for self hosting this application in a private local network and accessing it from anywhere around the world without exposing any TCP or UDP ports to the internet.

+ *Tailscale* - Official Website
  + https://tailscale.com
  + Note: Only some tailscale clients are open source, the default tailscale server provided as SAAS (Software-As-Service) is not open source, although there exists the **Headscale** open source implementation of tailscale server.
+ *Tailscale Client Download*
  + https://tailscale.com/download
+ *Tailscale Client for Android on F-Droid App Store* (App Store for Open Source Android apps compiled with reproducible build)
  + https://f-droid.org/packages/com.tailscale.ipn
+ *Headscale Server* (Open source, suitable for homelabs and self-hosting)
  + https://headscale.net/stable
+ *Headscale Server - Github Repository* (Written in GO - Golang)
  + https://github.com/juanfont/headscale


