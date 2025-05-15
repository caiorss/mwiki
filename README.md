# MWiki - Markdown-Powered Wiki 
## Overview 

MWiki is a **wiki engine** and note taking web application software geared towards mathematics and research designed for scientific and technical communication. This wiki engine software has semantic-rich lightweight markup language based on MyST markdown, Obsidian markdown, and Media wiki engine markup language. 

This Python application is powered by Python Flask web framework and the extensible markdown-it parser used by MyST markdown and the Jupyter Book project. 


+ Note: This software is still **work in progress** and under early stage. However, it can already be used as a personal note taking application.
+ Note: Mediawiki is the wiki engine software that powers Wikipedia.


### Features Highlights

File-based Wiki 

+ All Wiki pages are stored as Markdown files like Moin Moin wiki engine and Dokuwiki. However, it uses SQLite file database or a any full-featured database for system management purposes. 

Wiki Features:  

 + Supports MyST Markdown, GFM (Github-Flavored Markdown Support), subset of Obsidian Markdown syntax, subset of Mediawiki markup language and inline HTML.
 + Pages written in Markdown-based markup language instead of HTML, which allows to any non programmers to write scientific and technical documents that are rendered to html. 
 + Buttons for editing specific document sections similar to Media wiki section editing buttons. 
 + File upload. Now the wiki code editor has a button for inserting a hyperlink to an uploaded file. When the button is clicked, a popup window for upload is shown. Once the user sends the file, the window is closed and a link to the file is inserted in the editor.
 + Embeddable pages. The contents of a wiki page can be embedded in another wiki page by using the syntax `![[Name of Wiki page to be embedded]]`
 + Vendored third-party JavaScript dependencies for offline usage. For instance, MWiki has MathJax, pseudocode-JS, and Ace9 in the source code for offline usage even when no CDN is available due to lack of internet connectivity or if the Wiki is used in rescrited environment behind a firewall. 

Text Editor Features

 + Markdown **Code editor** built on top of Ace9 JavaScript code editor.
 + *Clipboard to markdown converter*, which allows turning html content copied from any other web page (aka web site) to MWiki markdown. This feature is similar to Obsidian's non-plain text copying and pasting. 
 + Upload images by pasting them from clipboard. 
     + Usage: Copy any image using the right click on any picture and past it on the text editor sesssion of some wiki page either by using the mouse or typing Ctrl + v.
+ NOTE: The clipboard features rely on Clibpboard Html5 API, which only is available on [secure contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts). Therefore pasting images from clipboard to the wiki text editor only works if the wiki is served on local host or from a domain with https (HTTP + TLS), which may require a reverse proxy such as Caddy or NGinx for TLS/SSL encryption and server authentication.


Access control 

 + The wiki has the following types of users: *admin*, that can edit the Wiki pages; *guest* a registered used which can view pages even if the wiki is not public, but a guest user cannot edit any page; and *anonymous* users (non logged in users) that can only view pages if the **public** checkbox in the Wiki settings ('/settings' pages) is enabled.
 + Public/private wiki settings - if the **public** checkbox in MWiki settings page is disabled, only logged in users will be able to view the wiki pages and non logged in users will be redirected to the authentiation screen. If this checkbox is enabled, non logged in users can view the wiki. Note that: only users of type administrator can edit the wiki pages and make changes to any content.

Features of the Wiki Markup Language

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

### Companion Software and Tools

The following set of companion sotfware or apps are recommended for MWiki as they can provide additional features and improve usage.

**Online Tools**

+ *Table Generator for Markdown, LaTeX and MediaWiki*
  + https://www.tablesgenerator.com/markdown_table
+ *Detexify*
  + https://detexify.kirelabs.org/classify.html
  + *Allows to recognize LaTeX symbols by drawing them by hand.*
+ *LaTeX Equation Editor*  
  + https://editor.codecogs.com/
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
   + *Ksnip is a Qt based cross-platform screenshot tool that provides many annotation features for your screenshots.*
- *KSnip - Flathub*  (KDE/QT Flatpak App)
   + https://flathub.org/apps/org.ksnip.ksnip
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


**Site-To-Site Mesh VPN**

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


## Demonstration 

### GIF Animations 

**Usage GIF animation**

![](images/mwiki-animation-usage1.gif)

**Copying and pasting images**

![](images/mwiki-animation-usage2.gif)

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

### Installation using Pipx

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

Install Mwiki using  Pipx and a different version of Python. This command is useful if the default versuion of Python in the current system is 3.8 or a non supported version.

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

Change site name using the built-in CLI management tool.

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


## MWiki Markdown/Markup Language Features 

This section describes the MWiki markup language features, which is based on MyST markdown, Obsidian markdown and Media Wiki markup language.

TODO: Add screenshot of wiki syntax code examples.


### Text Formatting 

#### Italic Text 

```
  + *text in italic*
```

Rendering:


+ *text in italic*

#### Bold Text 

Syntax: 

```
**Bold text here**
```

Example:

```
+ Example of syntax of a **bold text**.
```

Rendering:

+ Example of syntax of a **bold text**.


#### Strikethrough Text (Deleted Text) 

Example:

```
+ Example of ~~Deleted text~~ syntax.  
```

Rendering: 

+ Example of ~~Deleted text~~ syntax.  


#### Highlighted Text 

A highlighted text must be enclosed by `==`. Example:

```
this ==text will be higlighted== and remaining of the text.  
```

Rendering:

this ==text will be higlighted== and remaining of the text.



### Typographic Notation 

MWiki can convert ascii notation, such as `(C)` to the copyright unicode symbol, `(TM)` to trademark unicode symbol and other notations to the equivalent unicode symbol.

Example:

```
+ Copyright Symbol (C)
+ Copyright Symbol {C}
+ Registered Symbol (R)
+ Registered Symbol (C)
+ Trademark(TM) symbol
+ Trademark{TM} symbol
+ The angle is 60{deg} degrees 
+ The angle is 60{degrees} degrees 
+ The price is 30 {euros}
+ The price is 50 {pounds}
+ The price is 50 {gbp}  (British Pounds)
+ The price is 20 {yens}
+ Pilcrow Symbol {pilcrow} or {pagraph}
+ Section Symbol  {section}
```

Rendering:

+ Copyright Symbol ©
+ Copyright Symbol ©
+ Registered Symbol ®
+ Registered Symbol ©
+ Trademark™ symbol
+ Trademark™ symbol
+ The angle is 60° degrees
+ The angle is 60° degrees
+ The price is 30 €
+ The price is 50 £
+ The price is 50 £ (British Pounds)
+ The price is 20 ¥
+ Pilcrow Symbol ¶ or {pagraph}
+ Section Symbol §


### Hyperlinks

#### Internal Hyperlinks Links (WikiLinks)

Links to Wiki Pages (also called notes)

```
+ [[Link to internal page]]
```

Rendering: 

+ [[Link to internal page]]


#### External Inline Hyperlinks

**Raw External Link (1)**

```
+ <https://www.site.com/some/page>
```

Rendering:

+ https://www.site.com/some/page


**Raw External Link (2)**

```
+ <https://www.site.com/some/page>
```

Rendering:

+ <https://www.site.com/some/page>


**External Link with Label**

```
+ [Link label](https://www.site.com/some/page)
```
Rendering:

+ [Link label](https://www.site.com/some/page)


#### External Reference-Style Hyperlinks

Example:

```markdown

+ This page presents a study of [control][ceng] engineering and [state-space][ssmodel] models.

[ceng]: https://en.wikipedia.org/wiki/Control_engineering 

[ssmodel]: <https://en.wikipedia.org/wiki/State-space_representation>
      "In control engineering and system identification, a state-space representation is a mathematical model of a physical system specified as a set of input, output, and variables related by first-order differential equations or difference equations. Such variables, called state variables, evolve over time in a way that depends on the values they have at any given instant and on the externally imposed values of input variables. Output variables’ values depend on the state variable values and may also depend on the input variable values."
```

Rendering:


+ This page presents a study of [control][ceng] engineering and [state-space][ssmodel] models.

[ceng]: https://en.wikipedia.org/wiki/Control_engineering 

[ssmodel]: <https://en.wikipedia.org/wiki/State-space_representation>
      "In control engineering and system identification, a state-space representation is a mathematical model of a physical system specified as a set of input, output, and variables related by first-order differential equations or difference equations. Such variables, called state variables, evolve over time in a way that depends on the values they have at any given instant and on the externally imposed values of input variables. Output variables’ values depend on the state variable values and may also depend on the input variable values."

#### Special Hyperlinks

 **Hyperlink to Mastodon Handles (User Accounts)**

Syntax:
 
 ```
   @<USERNAME>@<SERVER>
 ```

Creates a hyperlink to a Mastodon user account. For instance, the Mastodon handle (user account)

```
+ @kde@floss.social
```

is rendered to HTML as

```
+  <a href="https://floss.social/@kde" class="link-esternal" ...  >@kde@floss.social</a>
```

In other words, @kde@floss.social is rendered as hyperlink (link for short) to the [Mastodon](https://en.wikipedia.org/wiki/Mastodon_(social_network)) user account of the [KDE project](https://en.wikipedia.org/wiki/KDE) project.

+ [@kde@floss.social](https://floss.social/@kde)


 **Hyperlink to DOI - Digital Object Identifier (1)**

Syntax:

```
  <doi:$DOI-BIBLIOGRAPHIC-REFERENCE>
```

Example:

```
+ Reference: Time Aware Least Recent Used (TLRU) cache management policy in ICN  <doi:10.1109/ICACT.2014.6779016> 
```

Rendering:

+ Reference: Time Aware Least Recent Used (TLRU) cache management policy in ICN  <doi:10.1109/ICACT.2014.6779016> 

When this DOI hyperlink is rendered, it is expanded to:

```
https://doi.org/10.1109/ICACT.2014.6779016
```

 **Hyperlink to DOI - Digital Object Identifier (2)**

This syntax when rendered yields the raw hyperlink, whose label is the DOI URL.

Syntax:

```
  <r-doi:$DOI-BIBLIOGRAPHIC-REFERENCE>
```

Example:

```
+ Paper: *Time Aware Least Recent Used (TLRU) cache management policy in ICN*
  + <r-doi:10.1109/ICACT.2014.6779016> 
```

Rendering:

+ Paper: *Time Aware Least Recent Used (TLRU) cache management policy in ICN*
  + <r-doi:10.1109/ICACT.2014.6779016> 

**Hyperlink to ArXiv paper**

Syntax:

```
  <arxiv:$ArXivID>
OR:
  <arXiv:$ArXivID>
```

Example:

```
+ See this paper:  <arxiv:1609.06088> - *Time Derivative of Rotation Matrices: a Tutorial*, shiyu zhao, (2016)  
```

Rendering:

+ see this paper:  <arxiv:1609.06088> - *time derivative of rotation matrices: a tutorial*, shiyu zhao, (2016)  


The hyperlink `<arxiv:1609.06088>` when rendered is expanded to following hyperlink.

```
https://arxiv.org/abs/1609.06088
```

**Hyperlink to ArXiv paper (Full Hyperlink)**

Example: 

```
+ *Time Derivative of Rotation Matrices: a Tutorial*, Shiyu Zhao, (2016)  
  + <r-arxiv:1609.06088>
```

Rendering:

+ *Time Derivative of Rotation Matrices: a Tutorial*, Shiyu Zhao, (2016)  
  + <r-arxiv:1609.06088>


**Hyperlink to Semantic Scholar** 

This syntax generates a hyperlink to a research paper listed in Semantic Scholar by its Semantic-Scholar Identifier (ID).

```
<S2CID:$SEMANTIC-SCHOLAR-ID> 

  OR:
 
<r-S2CID:$SEMANTIC-SCHOLAR-ID>  
   => Display hyperlink as Link label
```

Example: 

```

+ See this article: *Secure Distribution of Protected Content in Information-Centric Networking* - <S2CID:198967720>

```

Rendering:

+ See this article: *Secure Distribution of Protected Content in Information-Centric Networking* - <S2CID:198967720>


**Hyperlink to PubMed Paper by PubMed Id (Pmid)**

This type of special short hyperlink allows to create a link to research papers in PubMed Central database by using the PMID - PubMed of the research paper.

Syntax: 

```
  <pmid:$PUB-MED-ID-HERE>
```

Example: 

```
+ Reference: *Teaching population health: a competency map approach to education* <pmid:23524919>
```

Rendering:

+ Reference: *Teaching population health: a competency map approach to education* <pmid:23524919>

The special hyperlink `<pmid:23524919>` is expanded to:

```
https://pubmed.ncbi.nlm.nih.gov/23524919
```

**Hyperlink to PubMed Paper by PubMed Id (Pmid) - (Full Link)**


Example: 

```
+ *Teaching population health: a competency map approach to education* 
  + <r-pmid:23524919>
```

Rendering:

+ *Teaching population health: a competency map approach to education* 
  + <r-pmid:23524919>

 **Hyperlink to Patents**

Syntax:

```
  <patent:$PATENT-NUMBER>
OR
  <r-patent:$PATENT-NUMBER>

```

Exaple:

```markdown
+ Short Link 1: <patent:US9906369>
+ Full Link 1:  <r-patent:US9906369>
+ Short Link 2: <patent:7,139,686>
+ Full Link 2:  <r-patent:7,139,686>
```

Rendering: 


+ Short Link: [Patent USUS9906369](https://patents.google.com/patent/USUS9906369)
+ Full Link: https://patents.google.com/patent/USUS9906369
+ Short Link 2: [Patent US7139686](https://patents.google.com/patent/US7139686)
+ Full Link 2: https://patents.google.com/patent/US7139686



 **Hyperlink to RFC Standard**

Special link to RFC (Request for Comment) technical standards proposed by the IETF (Internet Engineering Task Force).

Syntax: 

```
    <rfc:$RFC-NUMBER> => Short Link
  <r-rfc:$RFC-NUMBER> => Link as label 
```


Example:

```
+ See <rfc:7231> - Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content

+ See <r-rfc:7231> - Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content
```

Rendering:

+ See <rfc:7231> - Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content

+ See <r-rfc:7231> - Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content


 **Hyperlink to PEP (Pyhton Enhancement Proposal)**

Syntax: 

 ```
   <pep:$PEP-NUMBER>
OR:
   <r-pep:$PEP-NUMBER>
 ```

Example:

```
+ See: Python WSGI - Webserver Gateway Interface  <pep:333> 
+ See: Python WSGI - Webserver Gateway Interface  <r-pep:333> 
```

Rendering:

+ See:  Python WSGI - Webserver Gateway Interface  <pep:333> 
+ See: Python WSGI - Webserver Gateway Interface  <r-pep:333> 

 **Hyperlink to Python Package**

Syntax: 

 ```
   <pypi:$PACKAGE-NAME>
OR:
   <r-pypi:$PACKAGE-NAME>
 ```

Example:

```
+ Pyhton <pypi:sqlitedict> package 
+ Python sqltedict package, available at <r-pypi:sqlitedict>
```

Rendering:

+ Pyhton <pypi:sqlitedict> package 
+ Python sqltedict package, available at <r-pypi:sqlitedict>


 **Hyperlink to CVE - Common Vulnerability Exposures**

This special link syntax allows creating hyperlinks to the CVE (Common Vunerability Exposures) database given a CVE identifier.

Syntax:

```md
 <cve:$CVE_NUMBER>
or
 <CVE:$CVE_NUMBER>
```

Example: the link shortcut

```md
+  <cve:CVE-2024-53104> 
```

is equivalent to the hyperlink 

```md
+ [CVE-2024-53104](https://www.cve.org/CVERecord?id=CVE-2024-53104) 
```

and is rendered to html as 

+  [CVE-2024-53104](https://www.cve.org/CVERecord?id=CVE-2024-53104) 


**Hyperlink to Subreddit**

Syntax:

```
<rd:/r/$NAME-OF-SUBREDDIT>

or

<reddit:/r/$NAME-OF-SUBREDDIT>
```

Example:

```markdown
+ C++ Subreddit <rd:/r/cpp> 
+ <reddit:/r/smalltalk>
```

Rendering:

+ C++ Subreddit [/r/cpp](https://old.reddit.com/r/cpp)
+ [/r/smalltalk](https://old.reddit.com/r/smalltalk) 

The hyperlink `<rd:/r/cpp>` is a hyperlink to

+ https://old.reddit.com/r/cpp 

### Image 
#### Internal Image 

The syntax for internal Wiki images is based on Obsidian's markdown syntax for embedding files on pages. It is not necessary to specify the full path or relative path of an image file as it will be displayed regardless of the sub directory it is located within the wiki pages repository. 

Syntax:

```
![[image_file.png]]

Or 

![[relative/path/to/images/image_file_name.png]]
```

#### External Image 

Hyperlink to external image. The image URL can be a relative URL as shown in the example below or a URL of type `https://www.site.com/files/image.png `.

Syntax:

```
![$IMAGE-ALT-TEXT-DESCRIPTION]($IMAGE-URL)
```

Example:

```
![Java's Duke Mascot](/static/example_java_duke_mascot.svg)
```

Rendering: 

![Java's Duke Mascot](/static/example_java_duke_mascot.svg)


### Code Blocks 
#### Inline code 

Inline code must be surrounded by backtick character (\`).

Example:

```
+ The wiki syntax `<rfc:7231>` is rendered to a hyperlink to 
http 1.1 standard from IETF <rfc:7231>
```

Rendering:

+ The wiki syntax `<rfc:7231>` is rendered to a hyperlink to 
http 1.1 standard from IETF <rfc:7231>

#### Code Block 

Example python source code block:

````markdown
```python
# Code for listing root directory 
import os 
for x in os.listdir("/"):
    print(x)
```
````

Rendering:

```python
# Code for listing root directory 
import os 
for x in os.listdir("/"):
    print(x)
```

### Quotes 

 **Quotion Syntax**

Example:

```markdown
> Let us change our traditional attitude to the construction of programs: Instead of imagining that our main task is to instruct a computer what to do, let us concentrate rather on explaining to humans what we want the computer to do.
> - -- Donald E. Knuth, Literate Programming, 1984
```

Rendering:

> Let us change our traditional attitude to the construction of programs: Instead of imagining that our main task is to instruct a computer what to do, let us concentrate rather on explaining to humans what we want the computer to do.
> - -- Donald E. Knuth, Literate Programming, 1984

 **Quotation Syntax Using Code Block**

Example:


````
```{quote}
Let us change our traditional attitude to the 
construction of programs: Instead of imagining that 
our main task is to instruct a computer what to do, 
let us concentrate rather on explaining to humans 
what we want the computer to do.
  -- Donald E. Knuth, Literate Programming, 1984
```
````

Rendering:

```{quote}
Let us change our traditional attitude to the 
construction of programs: Instead of imagining that 
our main task is to instruct a computer what to do, 
let us concentrate rather on explaining to humans 
what we want the computer to do.
  -- Donald E. Knuth, Literate Programming, 1984
```


### LaTeX Math Equations
#### Inline 

```
Let $x \in \mathbb{R}$ be a real number and $f(x) = \sqrt{x^2 - 10}$.
```

Rendering:

Let $x \in \mathbb{R}$ be a real number and $f(x) = \sqrt{x^2 - 10}$.

#### Display Mode 

```
$$
    A = \begin{bmatrix} 
              \alpha &  \beta 
          \\  \gamma &  \zeta 
        \end{bmatrix}
$$
```

Rendering:

$$
    A = \begin{bmatrix} 
              \alpha &  \beta 
          \\  \gamma &  \zeta 
        \end{bmatrix}
$$

#### Display Mode Without Enumeration 

```
$$
  \notag 
    A = \begin{bmatrix} 
              \alpha &  \beta 
          \\  \gamma &  \zeta 
        \end{bmatrix}
$$
```

Rendering:

$$
  \notag 
    A = \begin{bmatrix} 
              \alpha &  \beta 
          \\  \gamma &  \zeta 
        \end{bmatrix}
$$

#### Display Mode using Code Block Syntax 

Example:

````markdown
```{math}
  \notag 
    A = \begin{bmatrix} 
              \alpha &  \beta 
          \\  \gamma &  \zeta 
        \end{bmatrix}
```
````

Rendering:

```{math}
  \notag 
    A = \begin{bmatrix} 
              \alpha &  \beta 
          \\  \gamma &  \zeta 
        \end{bmatrix}
```

#### Latex Macros

It is possible to define LaTeX macros for writing math expressions in a more concise way
by using a code block similar to the example below on the top of the page. This special 
code block is not rendered, it is processed by MathJax or other LaTeX rendering engines.


````markdown
```{latex_macro}
% Logical AND 
\DeclareMathOperator{\\and}{ \\wedge }
% Logical OR
\DeclareMathOperator{\\or}{ \\vee }

 % ---- OR add your OWN LaTeX Macros here ------%%

```
````

After adding the previous macro to the top of the page, one can write logical expressions $\neg (p \wedge q)$, which means not (p and q) or NAND(p, q), in the following form:

```
$$
\neg (p \and q) \equiv \neg p \or q
$$
```


### Pseudocode of Algorithm

This wiki also supports LaTeX pseudocode of algorithms compatible with LaTeX algorithmic package. The implementation of this feature relies on [pseudocode-js](https://saswat.padhi.me/pseudocode.js/) and [MathJax](https://www.mathjax.org/) JavaScript libraries.

Example:

````latex
```{pseudo}
\begin{algorithm}
\caption{Buble Sort Algorithm}
\begin{algorithmic}
\PROCEDURE{BubbleSort}{$A, n$}
   \STATE $B = $ \CALL{CopyArray}{$A, n$}
   \STATE $\:$ \textit{// i = 0, 1, ..., n - 1}
   \FOR{$i = 0$ \TO  $i < n$}
       \STATE $\:$ \textit{// j = 0, 1, ..., n - 2 }
       \FOR{$j = 0$ \TO $j < n - 1$}
           \IF{$B[j] > B[j+1]$}
               \STATE swap $B[j]$ with $B[j+1]$
           \ENDIF
       \ENDFOR
   \ENDFOR
   \RETURN{$B$}
\ENDPROCEDURE
\end{algorithmic}
\end{algorithm}
```
````

Rendering:

```{pseudo}
\begin{algorithm}
\caption{Buble Sort Algorithm}
\begin{algorithmic}
\PROCEDURE{BubbleSort}{$A, n$}
   \STATE $B = $ \CALL{CopyArray}{$A, n$}
   \STATE $\:$ \textit{// i = 0, 1, ..., n - 1}
   \FOR{$i = 0$ \TO  $i < n$}
       \STATE $\:$ \textit{// j = 0, 1, ..., n - 2 }
       \FOR{$j = 0$ \TO $j < n - 1$}
           \IF{$B[j] > B[j+1]$}
               \STATE swap $B[j]$ with $B[j+1]$
           \ENDIF
       \ENDFOR
   \ENDFOR
   \RETURN{$B$}
\ENDPROCEDURE
\end{algorithmic}
\end{algorithm}
```


### Tables 

Example:

```
|  German          |   English         |
|------------------|-------------------|
| Deutsch          | German            |
| ja               | yes               |
| jetzt            | now               |
| nein             | no or not         | 
| hallo Welt       | hello World       |
| hallo Leute      | hello people      |
| willkomen        | welcome           |
| Hilfe            | Help              |
| die Zeit         | time              | 
| die Einstellugen | settings (plural) |
| die Kunst        | art               |
| die Freiheit     | freedom, liberty  |
| die Menschen     | people            |
| die Wirtschaft   | the economy       |
| das Ding         | thing, stuff      |
| das Miteglied    | member            | 
```

Rendering: 

|  German          |   English         |
|------------------|-------------------|
| Deutsch          | German            |
| ja               | yes               |
| jetzt            | now               |
| nein             | no or not         | 
| hallo Welt       | hello World       |
| hallo Leute      | hello people      |
| willkomen        | welcome           |
| Hilfe            | Help              |
| die Zeit         | time              | 
| die Einstellugen | settings (plural) |
| die Kunst        | art               |
| die Freiheit     | freedom, liberty  |
| die Menschen     | people            |
| die Wirtschaft   | the economy       |
| das Ding         | thing, stuff      |
| das Miteglied    | member            | 


### Lists 
#### Bullet Lists 

Example: 

```
+ Element 1 
+ Element 2 
  + Element 2.1
  + Element 2.2
+ Element 3
  + Element 3.1
  + Element 3.2
     + Element 3.2.1
     + Element 3.3.1
```

Rendering: 

+ Element 1 
+ Element 2 
  + Element 2.1
  + Element 2.2
+ Element 3
  + Element 3.1
  + Element 3.2
     + Element 3.2.1
     + Element 3.3.1

#### Ordered List 

Example:

```
1. Element 1
2. Element 2
   1. Element 2.1
   2. Element 2.2 
3. Element 3
   1. Element 3.1
   2. Element 3.2
   3. Element 3.3
      + Element 3.3.1
      + Element 3.3.2
   4. Element 3.4
4. Element 4
```

Rendering:

1. Element 1
2. Element 2
   1. Element 2.1
   2. Element 2.2 
3. Element 3
   1. Element 3.1
   2. Element 3.2
   3. Element 3.3
      + Element 3.3.1
      + Element 3.3.2
   4. Element 3.4
4. Element 4


#### Definition Lists 

Example: 

```
HTML 
   : Hypertext Markup Language 

DOM 
   : Domain Object Model 
   : Object that represents a parsed HTML tag in the memory.

WWW
   : World Wide Web 
```

Rendering: 


HTML 
   : Hypertext Markup Language 

DOM 
   : Domain Object Model 
   : Object that represents a parsed HTML tag in the memory.

WWW
   : World Wide Web 


### Admonitions (Callout Boxes) 
#### Info Admonition 


```markdown
:::{info}
Give some information to the user.
:::
```

Rendering:

:::{info}
Give some information to the user.
:::


#### Tip Admonition 

```
:::{tip}
Try changing `tip` to `warning`!
:::
```

Rendering:

:::{tip}
Try changing `tip` to `warning`!
:::

#### Note Admonition 

```
:::{note}
Make sure to check the relative error before stopping 
the iterations.
:::
```

Rendering:

:::{note}
Make sure to check the relative error before stopping 
the iterations.
:::

#### Warning Admonition 

```
:::{warning}

Make sure that device is fully charged before installing the firmware. Otherwise, it the device **may not be able to reboot**.
:::
```

Rendering:

:::{warning}

Make sure that device is fully charged before installing the firmware. Otherwise, it the device may not be able to reboot.
:::


#### Foldable Admonition

```
:::{note}
:class: dropdown

This is initially hidden, and can be clicked to be opened when you are viewing the content.
:::
```

Rendering:

:::{note}
:class: dropdown

This is initially hidden, and can be clicked to be opened when you are viewing the content.
:::

#### Mathematical Definition Admonition 

Example: 

```
:::{def} Inverse Matrix 
:label: inverse-matrix

The inverse matrix $A^{-1}$ of a matrix $A: n \times n$ is defined as a matrix that when multiplied by the square matrix A yields the identity matrix. Note that not always an inverse matrix of a square matrix Q exists. 

$$
  \notag
   A^{-1} A \triangleq A^{-1} \triangleq \mathbf{I}
$$

:::
```

Rendering:

:::{def} Inverse Matrix 
:label: inverse-matrix

The inverse matrix $A^{-1}$ of a matrix $A: n \times n$ is defined as a matrix that when multiplied by the square matrix A yields the identity matrix. Note that not always an inverse matrix of a square matrix Q exists. 

$$
  \notag
   A^{-1} A \triangleq A^{-1} \triangleq \mathbf{I}
$$

:::

#### Mathematical Theorem Admonition 

Example:

````markdown
:::{theorem} Determinant of Orthogonal Matrix  

The determinant of a **orthogonal matrix** $Q \in \mathbb{R}^{n \times n}$ of n rows and n columns is always 1.

$$
 \notag 
  \det(Q) = 1
$$


```{proof}

$$
\notag 
\begin{split}
      \det (Q Q^T)      &= \det(Q) \det(Q^{T}) 
   \\ \det (Q Q^T)      &= \det(Q) \det(Q) 
   \\ \det (Q Q^{-1})   &= \det(Q) \det(Q) 
   \\ \det (\mathbf{I}) &= \det(Q)^2
   \\  1                &= \det{Q}^2
   \\  \det(Q)          &= 1
\end{split}
$$
```
% --- end determinant proof ---

:::
````

Rendering:


:::{theorem} Determinant of Orthogonal Matrix  

The determinant of a **orthogonal matrix** $Q \in \mathbb{R}^{n \times n}$ of n rows and n columns is always 1.

$$
 \notag 
  \det(Q) = 1
$$


```{proof}

$$
\notag 
\begin{split}
      \det (Q Q^T)      &= \det(Q) \det(Q^{T}) 
   \\ \det (Q Q^T)      &= \det(Q) \det(Q) 
   \\ \det (Q Q^{-1})   &= \det(Q) \det(Q) 
   \\ \det (\mathbf{I}) &= \det(Q)^2
   \\  1                &= \det{Q}^2
   \\  \det(Q)          &= 1
\end{split}
$$
```
% --- end determinant proof ---

:::

#### Example of solved exercise 

````{markdown}
:::{example} Chain Rule for Derivative Multi-Variate Functions

Let the function f be $f(x, y) = x^2/A^2 + y^2/B^2 - C$.  Find the derivative of f with respect to t. And x and y are functions of t, $x = x(t) = A \cos t$ and $y = y(t) = B \sin t$. 


```{solution}   
$$
 \notag 
\begin{split}
  \frac{df}{dt} 
    &= \frac{\partial f}{\partial x} \frac{dx}{dt}  
    + \frac{\partial f}{\partial y} \frac{dy}{dt}  \\

    &=  \frac{\partial}{\partial x} (x^2/A^2 + y^2/B^2 - C) 
           \frac{d}{dt} ( A \cos t)
       \\ & +  \frac{\partial}{\partial y} (x^2/A^2 + y^2/B^2 - C) 
           \frac{d}{dt} ( A \sin t)  \\

    &=  (2x/A^2) (-A \sin t) + (2y/B^2) (A \cos t) \\ 
    &=  -2x \sin(t) / A + 2y \cos(t) / B \\
    &=  -2(A  \cos(t)) \sin(t) / A + 2(B  \sin(t)) \cos(t) / B \\
    &=  -2 \cos t  \sin t  + 2 \sin t  \cos t \\ 
    &=  0 
\end{split}
$$
```
:::
````

Rendering:

:::{example} Chain Rule for Derivative Multi-Variate Functions

Let the function f be $f(x, y) = x^2/A^2 + y^2/B^2 - C$.  Find the derivative of f with respect to t. And x and y are functions of t, $x = x(t) = A \cos t$ and $y = y(t) = B \sin t$. 


```{solution}   
$$
 \notag 
\begin{split}
  \frac{df}{dt} 
    &= \frac{\partial f}{\partial x} \frac{dx}{dt}  
    + \frac{\partial f}{\partial y} \frac{dy}{dt}  \\

    &=  \frac{\partial}{\partial x} (x^2/A^2 + y^2/B^2 - C) 
           \frac{d}{dt} ( A \cos t)
       \\ & +  \frac{\partial}{\partial y} (x^2/A^2 + y^2/B^2 - C) 
           \frac{d}{dt} ( A \sin t)  \\

    &=  (2x/A^2) (-A \sin t) + (2y/B^2) (A \cos t) \\ 
    &=  -2x \sin(t) / A + 2y \cos(t) / B \\
    &=  -2(A  \cos(t)) \sin(t) / A + 2(B  \sin(t)) \cos(t) / B \\
    &=  -2 \cos t  \sin t  + 2 \sin t  \cos t \\ 
    &=  0 
\end{split}
$$
```
:::

### MyST Roles 

The MyST Roles are similar to MyST directives, but they are single line. Exmaple:

Syntax:

```
{rolename}`text content here`
```

#### Underline text 

Makes a any text underline.

Example:

```
{u}`underline text`
```

Rendering:

+ {u}`underline text`


#### Abbreviation 

This syntax defines abbreviation of acronyms, that is rendered to an `<abbr>` html5 tag. The description of the acronym is shown in a popup window that appears when the user hoovers the mouse on the the abbreviation element.

Syntax:

```
 {abbr}`$ACRONYM  ($DESCRIPTION)`
```

Example:

```markdown
+ This wiki engine provides a syntax closer to {abbr}`MyST (Markedly Structured Text)`.
+ {abbr}`HTML (Hypertext Markup Language)` is a declarative language.
```

Rendering: 

+ This wiki engine provides a syntax closer to {abbr}`MyST (Markedly Structured Text)`.
+ {abbr}`HTML (Hypertext Markup Language)` is a declarative language.


#### Math Role for Inline LaTeX

```
+ The math expression  {math}`x^2 - 10x + 20` the previous function.
```

Rendering:

+ The math expression  {math}`x^2 - 10x + 20` the previous function.

####  Subscript  Role  

```
+ Water: H{sub}`2`O 
```

Rendering:

+ Water: H{sub}`2`O

#### Superscript Role 

Superscript Roles:

```
+ The 7{sup}`th` element.
```

Rendering:

+ The 7{sup}`th` element.

#### Embed Youtube Youtube Video

Embed Youtube video given its ID (Unique Identifier) or URL.

Syntax: 

```
{youtube}`<VIDEO-URL-OR-ID>`
```

Example: Embed video [3 Hours of Most Common Logical Fallacies to Fall Asleep To](https://www.youtube.com/watch?v=bNE4uBMsnP0&t=30s)

```
{youtube}`https://www.youtube.com/watch?v=bNE4uBMsnP0`

or

{youtube}`bNE4uBMsnP0`
```


### Frontmatter (Page Metadata)

The frontmatter is a YAML section at the beginning of MWiki *.md page file within two triple dashes (---), which contains machine-readable metadata of the current wiki page, including, authors, tags, date, description, abbreviations, page settings and other data.


Example: consider the wiki page file

+ 'NAS - Network Attached Storage Device.md'

whose content is

```md
---
author:  John Doe
date:    2022-06-10
description: Survey of NAS - Network Attached Storage devices for reliable backup, data replication and file sharing.

---

Describe what is a NAS 

+ S.M.A.R.T monitoring of disks.
+ SMB file sharing - SAMBA implementation 

...

![[picture-of-synology-nas.png]]

```

#### Abbreviations

The frontmatter can be used for defining abbreviations of common words. Consider a wiki page whose the frontmatter is

```
---
author:      John Doe
date:        2022-06-10
description: Survey of NAS - Network Attached Storage devices for reliable backup, data replication and file sharing.
abbreviations:
   NAS:  Network Attached Storage Device
   RAID: Redudant Array of Inexpensive Disks
   NFS:  Network File System 
   SMB:  Server Message Block (Windows shares, also known as network shares)
---
```

Any word defined in the 'abbreviations' section of a YAML frontmatter of a particular wiki page file, it is replaced by the `<abbr>` html5 element. 

For instance if a text of this wiki page is 

```
Most NAS devides provide Web UI for quickly 
creating SMB network shares, windows shared folders.
```

Then, it will be rendered to html as 

```html
Most <abbr title="Network Attached Storage Device">NAS</abbr>  
devides provide Web UI for quickly creating 
<abbr title="Server Message Block">SMB</abbr> network shares, 
windows shared folders.
```

When the mouse is over any abbr text, which has black dashes below it, a pop up window is appears displaying the meaning of the abbreviation. This feature also works on mobile devices, including phones and tablets.

#### Wordlinks

The wordlinks feature allows quickly creating hyperlinks for words defined in the **wordlinks** section of a frontmatter of a wiki page. This feature is useful for creating hyperlinks to dictionry definitions or Wikipedia articles related to a particular word. For instance consider the following frontmatter of a Wiki page *.md file.


```md
---
description: Wiki page (note) description here.

abbreviations:
    GUI: Graphics User Interface

wordlinks:
   ZFS:      https://hyperlink-to-wikipedia-of-ZFS
   TrueNAS:  https://link-to-wikipedia-of-TrueNAS

---
```

Whenever the word ZFS appears in any MWiki, paragraph, quote or bullet list, it is replaced by a hyperlink whose label is the word 'ZFS' and the URL is the corresponding URL to this word defined wordlist YAML dictionary. 

For instance, the wiki text 

```md
The file system ZFS is awesome!
```

is rendered to HTML as 

```html
The file system
<a href=" https://hyperlink-to-wikipedia-of-ZFS" ...>ZFS</a>
is awesome.
```

The advantage of this feature allows users to turn words of a MWiki page into hyperlinks without modifying the text or defining the hyperlink multiple times as 

+  `[word](http://hyperlink-of-this-word)`

### Further Reading 

+ https://mystmd.org/guide/admonitions
+ https://mystmd.org/sandbox
   + => Allows testing MyST online without installation.
+ https://myst-parser.readthedocs.io/en/latest/syntax/math.html
+ https://markdown-it-py.readthedocs.io/en/latest/architecture.html
+ https://mystmd.org/guide/glossaries-and-terms
