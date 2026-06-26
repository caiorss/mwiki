/* Settings for the JavaScript code editor Ace9
 *
 ********************************************************/


let editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
if( document.location.pathname.endsWith("/edit/special:macros") )
{
    editor.session.setMode("ace/mode/latex");
} else {
    editor.session.setMode("ace/mode/markdown");
}
// Enable VIM keybindings

editor.setOptions({
      selectionStyle:     "line"  // "line" | "text"
    , highlightActiveLine: true   // boolean
    , readOnly:            false  //
    , cursorStyle:        "ace"
    , showFoldWidgets:     true
    , showLineNumbers:     false
    , theme:               'ace/theme/textmate'
    , useSoftTabs:         true
    , wrap:                true
    , indentSoftWrap:      true
    , foldStyle:          'markbegin'

});

//editor.getSession().setUseWrapMode(true)
editor.getSession().setWrapLimitRange(60, 60);

let lineWrappingCheckbox = document.querySelector("#editor-line-wrapping-checkbox");
editor.getSession().setUseWrapMode(lineWrappingCheckbox.checked);

lineWrappingCheckbox.addEventListener("click", () => {
    editor.getSession().setUseWrapMode(lineWrappingCheckbox.checked);
});



const KEY_USER_VIM_EMULATED_ENABLED = "vim_emulation_enabled";
let vimEditorEmulation = document.querySelector("#editor-vim-emulation-checkbox");
let userVimEmulationEnabled = localStorageGet(KEY_USER_VIM_EMULATED_ENABLED);


let isVimEnabled = (VIM_EMULATION_ENABLED && userVimEmulationEnabled == null) || userVimEmulationEnabled;
vimEditorEmulation.checked = isVimEnabled;

if( isVimEnabled )
{
    editor.setKeyboardHandler("ace/keyboard/vim");
} else {
    editor.setKeyboardHandler("ace/keyboard/vscode");
}

vimEditorEmulation.addEventListener("click", (event) => {
    if( vimEditorEmulation.checked )
    {
        editor.setKeyboardHandler("ace/keyboard/vim");
    } else {
        editor.setKeyboardHandler("ace/keyboard/vscode");
    }
    localStorageSet(KEY_USER_VIM_EMULATED_ENABLED, vimEditorEmulation.checked);
});



ace.config.loadModule("ace/keyboard/vim", function(m) {
    let VimApi = require("ace/keyboard/vim").CodeMirror.Vim
    VimApi.defineEx("write", "w", function(cm, input) {
            // cm.ace.execCommand("save")
            editorSaveDocument();
    });
});


function disableControl(cssSelector)
{
    let dom = document.querySelector(cssSelector);
    if(!dom){
        console.error(`DOM element with selector ${cssSelector} not found.`);
        return;
    }
    dom.setAttribute("disabled", false);
}


if( document.location.pathname === "/edit/special:macros" )
{

    disableControl("[data-i18n='edit-page-back-button']");
    disableControl("[data-i18n='edit-page-preview-button']");
}


function editorRedo()
{
    editor.redo();
}

function editorUndo()
{
    editor.undo();
}

/** Redirect current page to a given URL */
function redirectUrl(url) { document.location.href = url; }


/** View document rendered html. */
function editorViewDocument()
{
    const urlParams = new URLSearchParams(window.location.search);
    const anchor    = urlParams.get('anchor');
    let url = `/wiki/${currentWikiPage}#${anchor}`
    redirectUrl(url);
}

function setStatusbarText(text)
{
    let statusbar = document.querySelector("#status-info");
    statusbar.textContent = text;

}

async function editorSaveDocument()
{
    // console.log(" [TRACE] Enter editorSaveDocument function.");
    let currentdate = new Date();
    let datetime = currentdate.getDate() + "/"
            + (currentdate.getMonth()+1)  + "/"
            + currentdate.getFullYear() + " @ "
            + currentdate.getHours() + ":"
            + currentdate.getMinutes() + ":"
            + currentdate.getSeconds();
    let code  = editor.getValue();
    // console.log("Current page ", page);
    // console.log("Editor content = \n", code);
    const urlParams = new URLSearchParams(window.location.search);
    const lineStart = urlParams.get('start');
    const lineEnd   = urlParams.get('end');
    const anchor    = urlParams.get('anchor');
    const page      = urlParams.get('page');
    const is_macro  = window.location.pathname.split("/")[2] === "special:macros";
    let payload = {  "content": code
                   , "start":   lineStart
                   , "end":     lineEnd
                };
    setStatusbarText(`Saving document at ${datetime}. Wait ...`);
    // Disable save buttons whiling saving the document and waiting a server response.
    let btn1 = document.querySelector("[data-i18n='edit-page-save-button']");
    let btn2 = document.querySelector("[data-i18n='edit-page-save-icon-button']");
    if(btn1 && !is_macro){ btn1.setAttribute("disabled", false); }
    if(btn2 && !is_macro){ btn2.setAttribute("onclick", ""); }
    // console.log(" [TRACE] Saving document. Wait ...");
    let out = await http_post(document.URL, payload);
    // console.log(" [RESULT] of saving operation = ", out);
    let status = out["status"];
    if(status == "ok"){
        // Note:  currentWikipage is global variable defined in edit.html template.
        let url = `/wiki/${currentWikiPage}#${anchor}`
        // Redirect to corresponding wiki page
        // and heading
        if(!is_macro){
            document.location.href = url;
        }
        setStatusbarText(`Saved at ${datetime}.`);
    } else {
        console.log("Status Error = ", out);
        setStatusbarText(`Failed to reach the server at ${datetime}.`);
        // Enable save buttons again
        if(btn1){ btn1.setAttribute("disabled", true); }
        if(btn2){ btn2.setAttribute("onclick", "editorSaveDocument();"); }
    }
}


function editorInsertTextArCursor(text)
{
    let cursorPosition = editor.getCursorPosition();
    editor.session.insert(cursorPosition, text)
    editor.focus();
}

function editorInsertLatexEquation()
{
    editorInsertTextArCursor(`$$\n%Latex Equation here\n\n$$`);
    // editor.moveCursorTo(cursorPosition);
}

function editorInsertLatexEquationNonNumered()
{
    editorInsertTextArCursor(`$$\n%Latex Equation here\n\\notag\n\n$$`);
    // editor.moveCursorTo(cursorPosition);
}

function editorInsertTheorem()
{
    let text = (":::{theorem} Theorem-name"
                + "\n:label: theorem-label-unique-id-optional"
                + "\n"
                + "\n % theorem content"
                + "\n:::"
                + "\n% -- End theorem --- %"
               );
    editorInsertTextArCursor(text);
    // editor.moveCursorTo(cursorPosition);
}

function editorInsertDetails()
{
    let text = (":::{details} $Details-Block-Name"
                + "\n:label: details-label-unique-id-optional"
                + "\n"
                + "\n % content"
                + "\n:::"
                + "\n% -- End defauls --- %"
               );
    editorInsertTextArCursor(text);
    // editor.moveCursorTo(cursorPosition);
}

async function insertLinkToPage()
{
    let pages = await httpRequest("GET", "/api/wiki");
    console.log(" [TRCCE] pages = ", pages);
    let datalist = document.querySelector("#pagelist");
    for(let p of pages)
    {
        let option = document.createElement("option");
        option.value = p;
        datalist.appendChild(option);
    }
    selectPageWindow.show();
}

function insertCodeBlock()
{
  let text = "```\n\n```";
  editorInsertTextArCursor(text);
}

function insertPythonCodeBlock()
{
  let text = "```python\n\n```";
  editorInsertTextArCursor(text);
}

function insertMatlabCodeBlock()
{
  let text = "```matlab\n\n```";
  editorInsertTextArCursor(text);
}

function insertJuliaCodeBlock()
{
  let text = "```julia\n\n```";
  editorInsertTextArCursor(text);
}

function noSubmitForm(event)
{
    console.log(" [TRACE] noSubmitForm called ok.")
    event.preventDefault();
    insertLinkToPageCallback();
    return false;
}

// "Insert Link to Wiki Page"
let insertPageWindowTitle = geti18nTranslation("insert-link-popup-window-title");
// "Insert"
let insertPageButtonLabel = geti18nTranslation("insert-link-popup-window-insert-button");

let selectPageWindow = new PopupWindow({
       title:  insertPageWindowTitle
    ,  height: "100px"
    ,  html: `
    <form class="insert-link-form">
        <fieldset>
            <input type="search" id="prompt-select-page" name="select-page" list="pagelist">
            <datalist id="pagelist"></datalist>
        </fieldset>
        <fieldset>
            <button class="primary-button" type="button" onclick="insertLinkToPageCallback();">${insertPageButtonLabel}</button>
        </fieldset>
   </form>
   `
});

document.querySelector(".insert-link-form").addEventListener("submit", noSubmitForm)


function insertLinkToPageCallback()
{
    let input = document.querySelector("#prompt-select-page");
    let selectedPage = input.value;
    input.value = "";
    let text = `[[${selectedPage}]]`;
    editorInsertTextArCursor(text);
    selectPageWindow.close();
}

function notImplemented()
{
    alert("ERROR: Not implemented yet.");
}

var uploadImageFlag = false;
// English message:  `Uploading image to server. Wait ...`
const StatusbarMessageImageUploadWaiting  = geti18nTranslation("statusbar-upload-image-waiting-text");
const StatusBarMessageImageUploadFinished = geti18nTranslation("statusbar-upload-image-finished-text");
const StatusBarMessageImageUploadError    = geti18nTranslation("statusbar-upload-image-error-text");



/** Note: It only works on secure context with HTTPS or localhost */
async function pasteImage(event) {
  try {
    const clipboardContents = await navigator.clipboard.read();
    for (const item of clipboardContents) {
      if (!item.types.includes("image/png")) {
        throw new Error("Clipboard does not contain PNG image data.");
      }
      const blob = await item.getType("image/png");
      //console.log(" [TRACE] blob = ", blob);

      let fr = new FileReader();
      fr.readAsDataURL(blob);
      fr.onload = async (event) => {
        let timestamp = new Date().valueOf();
        let fileName = `pasted-image-${timestamp}.jpg`
        let payload = {
                fileName: fileName
              , data: event.target.result
        };
        if(payload.data == null){
          // console.log(" [TRACE] Null payload");
          return;
        }
        setStatusbarText(StatusbarMessageImageUploadWaiting);
        let out = await http_post("/paste", payload);
        /// console.log(" Output = ", out);
        setStatusbarText(StatusBarMessageImageUploadFinished);
        editorInsertTextArCursor(`\`\`\`{figure} ![[${fileName}]]`
                                + "\n```"
                                );
        // Automatically save document after pasting any image.
        ///// editorSaveDocument();
      };
      // let b64blob =  URL.createObjectURL(blob);
      // console.log("blob = ", b64blob);
      // destinationImage.src = b64blob;
    }
  } catch (error) {
        console.log(error.message);
        // setStatusbarText(StatusBarMessageImageUploadError);
  }
}



/** Compiles AST of html5 nodes (DOM) to MWiki markdown.
 *
 * + AST => Abstract Syntax Tree
 * + DOM => Domain Object Model
 ********************************************/
function domToMarkdownCompiler(dom)
{
    var out = "";
    let ntype = dom.nodeName;
    const arrayNodeTypes = [ "DIV",  "BODY", "P", "LI", "UL", "EM", "STRONG"
                             , "H1", "H2", "H3", "H4", "H5", "H6" ];
    if(ntype === "HTML"){
        // Iterate over body

        let nextDom = dom.childNodes[1];
        console.assert(nextDom.nodeName === "BODY");
        out = domToMarkdownCompiler(nextDom);
    }
    // else if (ntype === "BODY" || ntype == "P" || ntype === "LI" || ntype == "UL" || ntype == "EM" || ntype == "H3")
    else if ( arrayNodeTypes.includes(ntype) )
    {
       for(let ch of dom.childNodes)
       {
            let nodeMarkdown = domToMarkdownCompiler(ch);
            if(ch.nodeName == "LI"){
                out += "+ ";
            }
            out += nodeMarkdown;
            if     (ntype === "P"  ){ out += " ";  }
            else if(ntype === "LI" ){ out += "\n"; }
            // if(ch.nodeName == "LI"){ out += "\n"; }
       }
       if (ntype === "P") // || ntype === "UL")
       {
         out += "\n\n";
       } else if(ntype == "UL")
       {
         out += "\n";
       } else if (ntype == "EM")
       {
          out = "*" + out.replace("’", "") + "*";
       } else if (ntype == "STRONG")
       {
          out = "**" + out.replace("’", "") + "**";
       } else if(ntype === "H1"){
          out = "# " + out + "\n\n";
       } else if(ntype === "H2"){
          out = "## " + out + "\n\n";
       } else if(ntype === "H3"){
          out = "### " + out + "\n\n";
       } else if(ntype === "H4"){
          out = "#### " + out + "\n\n";
       } else if(ntype === "H5"){
          out = "##### " + out + "\n\n";
       } else if(ntype === "H6"){
          out = "###### " + out + "\n\n";
       }


    } else if (ntype === "#text")
    {
        let text = dom.data.trim().replace("’", "'")
                                  .replace("“", "\"")
                                  .replace("”", "\"");
        out = text.split("\n").map(x => x.trim()).join();
        //text.split("\n").map(x => " " + x.trim()).join().trim();
        console.log(" [TRACE] ntype - #text => out = \n", out);
    } else if (ntype === "A")
    {
        if(dom.innerText === ""){
            out = "";
        } else {
            out = `[${dom.innerText}](${dom.href})`;
        }
    } else if (ntype === "PRE")
    {
        if(  dom.childNodes[0].type === "CODE" )
        {
            out = dom.childNodes[0].innerText;
        } else {
            out = dom.innerText;
        }
        out = "```\n" + out + "\n```\n\n";
    }  else if (ntype === "CODE")
    {
        out = "`" + dom.innerText + "`";
    }
    else {
        console.error(`Not implemented for element of type ${ntype}`);
   }
    return out;
}

/** Transpiler from html to MWiki markdown (markup language) */
function htmlToMarkdown(htmlSourceCodeString)
{

    let el = document.createElement("html");
    el.innerHTML = htmlSourceCodeString;
    let out = domToMarkdownCompiler(el);
    return out;
}



function onPasteEventHandler (text, event)
{
    // event.preventDefault();
    // event.stopPropagation();

    let choice = document.querySelector('input[name="clipboardChoice"]:checked').value;
    console.log(" Clipboard Choice = ", choice);

    console.log("event = ", event);
    let clipboard = event.clipboardData;
    console.log(" clipboard = ", clipboard);
    let types = clipboard.types;
    var out = "";

    if( types.includes("image/png") )
    {
        console.error("Not implemented pasting for images/png");

    } else if( types.includes("text/html") && choice == "html" )
    {
        out = clipboard.getData("text/html");

    }
    else if( types.includes("text/html") && choice == "markdown" )
    {
        let html = clipboard.getData("text/html");
        out  = htmlToMarkdown(html);
    }
    else if( types.includes("text/plain") )
    {
        console.log("Pasting text =", clipboard.getData("text/plain"));
        out = clipboard.getData("text/plain");

    } else
    {
        console.error("Not implemented pasting this type");
    }
    editorInsertTextArCursor(out);
}


// editor.container.addEventListener("paste", onPasteEventHandler);

editor.onPaste = onPasteEventHandler;
document.onpaste = pasteImage;

uploadWindow = new PopupWindow({
       title: "Upload File"
    ,  titleI18nTag: "upload-form-window-title"
    ,  html: `

        <form id="uploadForm" action="/api/upload" method="POST">
            <input type="hidden" name="csrf_token" value="${CSRF_TOKEN}">
            <fieldset">
                <label data-i18n="upload-form-file-link-label" for="fileLabel">Link Label</label>
                <input type="text" name="fileLabel" id="fileLabel" title="Enter label of file link. (Optional)"></fileLabel>
            </fieldset>
            <fieldset>
                <label data-i18n="upload-form-choose-file-label" for="file">Choose a file</label>
                <input type="file" id="fileInput" name="file" required>
            </fieldset>
            <fieldset>
                <input type="checkbox" name="convert-jpeg">
                <label data-i18n="upload-form-convert-jpeg-checkbox-label" for="convert-jpeg">Convert Images to JPEG</label>
                <p data-i18n="upload-form-convert-jpeg-checkbox-description">
                    Reduce image file size by converting uploaded image to JPEG
                </p>
            </fieldset>
            <fielset>
                <button class="primary-button" data-i18n="upload-form-submit-button" type="submit" name="submit">Upload</button>
            </fieldset>
        </form>
        <p data-i18n="upload-status-label" id="upload-status">Ready to upload file.</p>
        <p data-i18n="upload-form-instruction">
            This form allows uploading files and inserting link to it at current cursor position in the wiki code editor. NOTE: The file link label is optional. If it is empty, the file name will be used as the link label.
        </p>
    `
});

function openUploadWindow()
{
    uploadWindow.show();
}


async function handleUploadFormSubmit(event)
{
    event.preventDefault();
    const form = event.currentTarget;
    const formData = new FormData(form);
    const url = new URL(form.action);

    const headers = {
        'X-CSRFToken': CSRF_TOKEN
       ,'X-Requested-With': 'XMLHttpRequest'
    };
    const fetchOptions = {
        'method':  form.method,
        'headers': headers,
        'body':    formData,
    };
    let networkErrorHandler = function(err){
        console.warn("Network error ", err);
        let response = new Response(JSON.stringify({
               status: "error"
            ,  message: "Failed to reach server. A network error happenned."
        }));
        return response;
    };
    let httpErrorCodes = {
          404: "404 - Not found"
        , 403: "403 - Forbidden (Autorization)"
        , 401: "401 - Unauthorized (Athentication)"
        , 405: "405 - Http Method POST Not Allowed"
        , 500: "500 - Internal Server Error"
    };
    let dom = document.querySelector("#upload-status");
    dom.innerText = 'Uploading file wait ...';
    const res = await fetch(url, fetchOptions)
                            .catch(networkErrorHandler);

    // console.log(" dom = ", dom);
    var result = null;
    // alert("Not implemented");
    if (!res.ok)
    {
        result = {
              "status": "error"
            , "error": httpErrorCodes[res.status]
        }
        // console.log(" [TRACE] message = ", result);
        dom.innerText = 'ERROR: Failed to upload file';
    } else {
        dom.innerText = 'Upload successful';
        result = await res.json();
        let filename = result["file"];
        uploadWindow.hide();
        let fileLabel = document.querySelector("#fileLabel");
        let value = fileLabel.value;
        var output = "";
        if( filename.endsWith(".png")
            || filename.endsWith(".apng")
            || filename.endsWith(".jpg")
            || filename.endsWith(".jpeg")
            || filename.endsWith(".webp")
            || filename.endsWith(".bmp")
            || filename.endsWith(".avif")
            || filename.endsWith(".ico")
            || filename.endsWith(".svg")
            )

        {
            output =   `\`\`\`{figure} ![[${filename}]]`
                                + "\n:name: "
                                + "\n:alt: "
                                + "\n"
                                + `\n${value}`
                                + "\n```"
                       ;
        } else if( filename.endsWith(".webm") || filename.endsWith(".mp4") )
        {
            output =   `\`\`\`{video} ![[${filename}]]`
                                + "\n:name: "
                                + "\n:alt: "
                                + "\n"
                                + `\n${value}`
                                + "\n```";
        } else {
            if (value !== "") {
                output = `[[${filename}|${value}]]`
            } else {
                output = `[[${filename}]]`
            }
        }
        editorInsertTextArCursor(output);
        // Automatically save document after uploading file
        //// editorSaveDocument();

    }

    return result;

}


const form = document.querySelector('#uploadForm');
form.addEventListener('submit', handleUploadFormSubmit);


function dropHandler(ev) {
    // Prevent default behavior (Prevent file from being opened)
    ev.preventDefault();
    console.log("File(s) dropped");

    let file = (ev.dataTransfer.items)
                ? ev.dataTransfer.items[0].getAsFile() : ev.dataTransfer.files[0].getAsFile();
    let dt = new DataTransfer();
    //console.log(" dt = ", dt);
    dt.items.add(file);
    let fileInput = document.querySelector("#fileInput");
    if(!fileInput){
        // If this message is shown, it means that there is a bug.
        alert(`Error file input #fileInput not found.`)
        return;
    }
    fileInput.files = dt.files;
    uploadWindow.show();
}

// Prevent default behavior (Prevent file from being opened)
function dragOverHandler(ev) {
  ev.preventDefault();
  //console.log("File(s) in drop zone");
}


async function editorPreviewDocument()
{
    let selection = editor.getSelectedText();
    let code = selection !== "" ? selection : editor.getValue();
    // Note:  currentWikipage is global variable defined in edit.html template.
    let payload = { "code": code, "page": currentWikiPage };
    let out = await http_post("/api/preview", payload);
    if( out.status != "ok" ){ return;}
    // Default value: "Preview of"
    let localizedTitlePrefix = geti18nTranslation("edit-page-preview-popup-window") || "Preview of";
    let previewWindow = new PopupWindow({
          title: `${localizedTitlePrefix} ${currentWikiPageTitle}`
        , html:   `<iframe id="iframe-preview"
                           sandbox="allow-scripts allow-same-origin allow-forms allow-top-navigation-by-user-activation"
                           srcdoc="${out.html}"
                           width="100%"
                           height="100%"
                           ></iframe> `
        , width:  "95%"
        , height: "98%"
        , top: "0px"
        , left: "0px"
    });
    previewWindow.setHeight("98%");
    previewWindow.show();
}

latexEntryWindow = null;
latexRenderingUpdateFunc = null;

document.addEventListener("DOMContentLoaded", function(){

    latexEntryWindow = new PopupWindow({
           title: "LaTeX Input Window"
        ,  titleI18nTag: "latex-input-window-title"
        ,  width: "600px"
        ,  height: "500px"
        ,  html: `
          <div class="latex-input-window">
            <textarea class="latex-input" name="latex-input" rows="4" cols="50"
                      autocomplete="off"
                      autocorrect="off"
                      autocapitalize="off"
                      spellcheck="false">
            </textarea>
            <div class="latex-input-window-buttons">
                <button class="btn-insert-latex primary-button" data-i18n="latex-input-window-btn-insert" title="Close this window and insert LaTeX formula at current cursor position. Keyboard shortcut: Alt + Enter">Insert</button>
                <button class="btn-clear-latex  primary-button" data-i18n="latex-input-window-btn-clear" title="Clear LaTeX code entry. Keyboard shortcut: Ctrl + l">Clear</button>
                <button class="btn-cancel-latex primary-button" data-i18n="latex-input-window-btn-close"
                    title="Close this window." >Close</button>
            </div>

            <p data-i18n="latex-input-window-p">Output:</p>
            <div class="div-latex-code"></div>
        </div>
    `});
    // Function called from file main.js
    doTranslationI18N();

    latexEntryWindow.setHeight("500px");
    let btnInsertLatex = latexEntryWindow.querySelector(".btn-insert-latex");
    let latexEntry = latexEntryWindow.querySelector(".latex-input");
    let latexOutput = latexEntryWindow.querySelector(".div-latex-code");
    latexEntry.value =   "% Type ctrl + l to clear this LaTeX code entry "
                       + "\n% Type Alt + Enter to insert this formula and close this window."
                       + "\n% The sum of all angles of a tringle is 180 degrees or pi."
                       + "\n\\alpha + \\beta + \\theta = \\pi";

    function updateLatexRendering()
    {
        let latexCode = latexEntry.value;
        latexOutput.textContent =
                IS_LATEX_RENDERER_KATEX ? latexCode : "$$\n" + latexCode + "\n$$";
        renderDOMLatex(latexEntryWindow.dom());
    }

    latexRenderingUpdateFunc = updateLatexRendering;

    function insertLatexCode()
    {
        let latexCode = latexEntry.value;
        latexEntryWindow.close();
        editorInsertTextArCursor("\n$$\n" + latexCode + "\n$$\n");
    }

    function clear()
    {
        latexEntry.value = "";
        updateLatexRendering();
    }


    function handleKeyDown(e) {
        console.log(" [TRACE] e = ", e);
        if (e.key === "Enter" && e.altKey)
        {
            e.preventDefault();
            insertLatexCode();
            return;
        }
        if (e.key === "q" && e.altKey)
        {
            e.preventDefault();
            latexInputWindow.close();
            return;
        }
        if (e.key === "l" && e.ctrlKey)
        {
            e.preventDefault();
            clear();
            return;
        }
        if (e.key !== "Tab") { return; }
        e.preventDefault();
        const start = this.selectionStart;
        const end = this.selectionEnd;
        this.value = this.value.substring(0, start) + "\t" + this.value.substring(end);
        this.selectionStart = this.selectionEnd = start + 1;
    }

    // updateLatexRendering();
    //btnCancelLatex.addEventListener("click", latexEntryWindow.close);
    latexEntry.addEventListener("input", updateLatexRendering);
    latexEntryWindow.closeWindowOnClick(".btn-cancel-latex");
    latexEntryWindow.onClick(".btn-insert-latex", insertLatexCode);
    latexEntryWindow.onClick(".btn-clear-latex",  clear);
    latexEntryWindow.onEvent(".latex-input", "keydown", handleKeyDown);
});

function openLatexInputWindow()
{
    latexEntryWindow.show();
    latexRenderingUpdateFunc();
}


let spellCheckWindow = new PopupWindow({
       title: "Spell Checker"
    ,  titleI18nTag: "spell-checker-window-title"
    ,  width: "600px"
    ,  height: "500px"
    ,  html: `
      <div class="">
        <textarea class="spell-check-input" name="spell-check-input" rows="10" cols="20"
                  autocomplete="on"
                  autocorrect="on"
                  autocapitalize="off"
                  spellcheck="true"
                  wrap="hard"
                  style="word-wrap: break-word; width: 100%; height: 80%;"
                  ></textarea>
        <div class="latex-input-window-buttons">
            <button class="btn-insert primary-button" data-i18n=""
                title="Insert text at current cursor position and close this window.">Insert</button>
            <button class="btn-copy primary-button" data-i18n=""
                title="Copy text to clipboard.">Copy</button>
            <button class="btn-clear  primary-button" data-i18n=""
                title="Clear text.">Clear</button>
        </div>
    </div>
`});


spellCheckWindow.onClick(".btn-insert", () => {
     let input = spellCheckWindow.querySelector(".spell-check-input");
     editorInsertTextArCursor(input.value);
     input.value = "";
     spellCheckWindow.close();
});
spellCheckWindow.onClick(".btn-copy", () => {
     let input = spellCheckWindow.querySelector(".spell-check-input");
     navigator.clipboard.writeText(input.value);
});
spellCheckWindow.onClick(".btn-clear", () => spellCheckWindow
                                                .querySelector(".spell-check-input")
                                                .value = "" );

//// window.onpaste = onPasteEventHandler;
    // window.addEventListener("paste", onPasteEventHandler, false);

    // document.onpaste = onPasteEventHandler;

    // let output = domToMarkdownCompiler(el);
    // console.log("output \n", output);

unicodeWindow = new PopupWindow({
       title: "Insert unicode or emoji symbol"
    ,  titleI18nTag: "unicode-emoji-dialog-title"
    ,  html: `
        <div class="div-unicode-emoji-symbol">
            <div>
                <h3>Symbols</h3>
                <button title="Section symbol">§</button>
                <button title="Pillcrow sign, paragrapha mark, paragraph sign also known as pargraph symbol or blind P">¶</button>
                <button title="Copyright symbol">©</button>
                <button title="Sound Record Copyright">℗</button>
                <button title="Registered Trademark Symbol">®</button>
                <button title="Official Mark (Canada)">Ⓜ</button>
                <button title="Trademark symbol">™</button>
                <button title="Service mark">℠</button>
                <button title="Raised MC sign">🅪</button>
                <button title="Warenzeichen grapheme (Germany)">🄮</button>
                <button title="Euro currency sign">£</button>
                <button title="Pound currency sign">€</button>
                <button title="Yen (Japan) and Yuan (China) Sign">¥</button>
                <button>—</button>
                <button>’</button>
                <button>“</button>
                <button>”</button>
                <button>«</button>
                <button>»</button>
                <button>💯</button>
                <button>⚠️</button>
                <button>‼️</button>
                <button>🚫</button>
                <button>⭕️️</button>
                <button>🔴</button>
                <button>⛔️️</button>
                <button>❌️</button>
                <button>🚨</button>
                <button title="Bookmark">🔖</button>
                <button>🔎</button>
                <button>🔗</button>
                <button title="Chi Rho">☧</button>
                <button title="Chi Rho Coptic">⳩</button>
                <button>·</button>
                <button>°</button>
                <button>→</button>
                <button>√</button>
                <button>π</button>
                <button>×</button>
                <button>∆</button>
                <button>▼</button>
                <button>🜃</button>
                <button>✓</button>
                <button>√</button>
                <button>∞</button>
                <button title="Per mile sign">‰</button>
                <button title="Per thousands sign (basis points)">‱</button>
                <button title="Prime">′</button>
                <button title="Double prime">″</button>
                <button title="Triple prime">‴</button>
                <button title="Set of complex numbers">ℂ</button>
                <button title="Hilbert Space">ℋ </button>
                <button title="Set of quaternions">ℍ</button>
                <button title="Laplace transform operator \mathcal{L}">ℒ</button>
                <button title="Ell \ell">ℓ</button>
                <button title="Set of Natural Numbers">ℕ</button>
                <button title="Integers set">ℤ</button>
                <button title="Fourier Transform Operator">ℱ </button>
                <button title="Integral operator">∫</button>
                <button title="Double Integral Operator">∬</button>
                <button title="Triple Integral Operator">∭</button>
                <button title="Contour Integral Operator">∮</button>
                <button titlte="Oplus">⊕</button>
                <button title="Ominus">⊖</button>
                <button title="Otimes or outer product operator">⊗</button>
                <button title="Odot">⊙</button>
                <button title="Iota">⍳</button>
                <button title="LEQ - Less or Equal Than">≤</button>
                <button title="GEQ - Greater or Equal Than">≥</button>
                <button title="Not equal">≠</button>
                <button>≡</button>
                <button>≢</button>
                <button>∊</button>
                <button>⍷</button>
                <button title="Greek letter rho or shape operator in APL.">⍴</button>
                <button title="Greek letter phi or transpose operator in APL">⌽</button>
                <button>⍉</button>
                <button>↑</button>
                <button>↓</button>
                <button>⊥</button>
                <button>⊤</button>
                <button>⊂</button>
                <button>∩</button>
                <button>∪</button>
                <button>⊢</button>
                <button>⊣</button>
                <button>⍋</button>
                <button>⍒</button>
                <button>⎕</button>
                <button>⍞</button>
                <button>◊</button>
                <button title="Symbol used for comment in APL.">⍝</button>
                <button>⍎</button>
                <button>⍕</button>
                <button>⌷</button>
                <button>⍬</button>
                <button>⍨</button>
                <button title="APL - Slash bar operator">⌿</button>
                <button title="APL - Backslash bar operator">⍀</button>
                <button title="APL Outer Product">∘.</button>
                <button title="APL symbol for matrix inversion.">⌹</button>
                <button title="Box drawing character">╔</button>
                <button title="Box drawing character">═</button>
                <button title="Box drawing character">╦</button>
                <button title="Box drawing character">╗</button>
                <button title="Box drawing character">╠</button>
                <button title="Box drawing character">╣</button>
                <button title="Box drawing character">║</button>
                <button title="Box drawing character">╚</button>
                <button title="Box drawing character">╩</button>
                <button title="Box drawing character">╝</button>
                <button title="Box drawing character">┏</button>
                <button title="Box drawing character">━</button>
                <button title="Box drawing character">┳</button>
                <button title="Box drawing character">┓</button>
                <button title="Box drawing character">┣</button>
                <button title="Box drawing character">╋</button>
                <button title="Box drawing character">┫</button>
                <button title="Box drawing character">┃</button>
                <button title="Box drawing character">┗</button>
                <button title="Box drawing character">┻</button>
                <button title="Box drawing character">┛</button>
            </div>
            <div>
                <h3>Stuffs</h3>
                <button>☀</button>
                <button title="Mailbox">📬</button>
                <button>⏰</button>
                <button>🕙️</button>
                <button title="Dice">🎲</button>
                <button>📍</button>
                <button>🎟️</button>
                <button>💡</button>
                <button>🔌</button>
                <button>✂️</button>
                <button>⚛️</button>
                <button>♾️</button>
                <button>🔍</button>
                <button>💾</button>
                <button>🖋</button>
                <button>📝</button>
                <button title="A stack of books">📚️</button>
                <button title="Scroll">📜</button>
                <button title="Opened book">📖</button>
                <button>Ⓥ</button>
                <button>🚨</button>
                <button>📍</button>
                <button>📢</button>
                <button>🎧️</button>
                <button>🎼</button>
                <button>💻️</button><button>🧰</button>
                <button>📱</button><button>🎮</button>
                <button>✅️</button>
                <button>💊</button><button>👑</button>
                <button>🎮</button>
                <button>🕹️</button>
                <button>🔭</button>
                <button>🧵</button>
                <button>🎞️</button>
                <button>🚴</button>
                <button>📺️</button>
                <button>🎵</button>
                <button>⛔️️</button>
                <button>🎞️</button>
                <button>🛒</button>
                <button>🎨</button>
                <button>🔔</button>
                <button>🎁</button>
                <button>🤖</button>
                <button>🚧</button>
                <button>💼</button>
                <button>🧱</button>
                <button>🚀</button>
                <button>🔧</button>
                <button>🗜</button>
                <button>🔩</button>
                <button>⚙</button>
                <button>🔨</button>
                <button>📡</button>
                <button>✍🏼</button>
                <button>✈️</button>
                </button><button>⚒</button>
                <button>🛠</button>
                <button>☢️</button>
                <button>⧖</button>
                <button>Ⓥ</button>
                <button>💰</button>
                <button>🔒</button>
                <button>📁</button>
                <button title="Battery level indicator">🔋</button>
                <button title="Bookmark">🔖</button>
            </div>
            <div>
                <h3>Emojis</h3>
                <button>🎅</button>
                <button>👨🏻‍💼</button>
                <button>🚶</button>
                <button>🚶🏻‍♂️</button>
                <button>👀</button>
                <button>👁️</button>
                <button>😎</button>
                <button>🤓</button>
                <button>😃</button>
                <button>🥳</button>
                <button>😊</button>
                <button>👻</button>
                <button>🤡</button>
                <button>🫣</button>
                <button>🙀</button>
                <button>😹</button>
                <button>😼</button>
                <button>😵‍💫</button>
                <button>😵</button>
                <button>☣️</button>
                <button>✊️</button>
                <button>🥋</button>
                <button>🙇‍♂️</button>
                <button>🙇</button>
                <button>🫡</button>
                <button>😔</button>
                <button>🤔</button>
                <button>🤞</button>
                <button>😬</button>
                <button>😭</button>
                <button>🤗</button>
                <button>🫶</button>
                <button>🫂</button>
                <button>🎃</button>
                <button>🤷</button>
                <button>✨️</button>
                <button>⚽️</button>
                <button>👾</button>
                <button>👽️</button>
                <button>💀</button>
                <button>😷</button>
                <button>😱</button>
                <button>☃️</button>
                <button>🙏🏼</button>
                <button>🕯️</button>
                <button>👉</button>
                <button>✌️</button>
                <button>🖖</button>
                <button>👇</button>
                <button>👍</button>
                <button>👏</button>
                <button>🙌</button>
                <button>✋</.button>
                <button>👌</button>
                <button>👋🏼<button>
                <button>👏🏾</button>
                <button>🤏🏾</button>
                <button>👏🏾</button>
                <button>👊🏾</button>
                <button>🙌🏻</button>
                <button>💯</button>
                <button>🎉</button>
                <button>😑</button>
                <button>🗣</button>
                <button>😍</button>
                <button>😻</button>
                <button>😅</button>
                <button>🤣</button>
                <button>😂</button>
                <button>😢</button>
                <button>😤</button>
                <button>👨🏻‍💻</button>
                <button>🤯</button>
                <button>💪</button>
                <button>🤬</button>
                <button>😡</button>
                <button>👿</button>
                <button title="Soldier's helmet, serviceman helmet">🪖</button>
                <button>⚔️</button>
                <button>🛡️</button>
                <button>☠️ </button>
                <button>🏴‍☠️</button>
                <button>🔥</button>
                <button>💥</button>
            </div>
            <div>
                <h3>Nature</h3>
                <button>🍁</button>
                <button>🍀</button>
                <button>🌿</button>
                <button>🍂</button>
                <button>🎄</button>
                <button>🌴</button>
                <button>🌳</button>
                <button>🌱</button>
                <button>🌾</button>
                <button>🍁</button>
                <button>🌻</button>
                <button>🌹</button>
                <button>🍄</button>
                <button>🪹</button>
                <button>❄️</button>
                <button>💭</button>
                <button>💦</button>
                <button>🌎️</button>
                <button>🌍️</button>
                <button>🌏️</button>
                <button title="Volcano">🌋</button>
            </div>
            <div>
                <h3>Animals</h3>
                <button title="Dragon">🐉</button>
                <button title="blue bird">🐦</button>
                <button>🦊</button>
                <button>🐇</button>
                <button>🦉</button>
                <button>🦅</button>
                <button title="bat">🦇</button>
                <button>🐘</button>
                <button>🦣</button>
                <button>🦏</button>
                <button>🐻</button>
                <button>🦧</button>
                <button>🐒</button>
                <button>🐍</button>
                <button>🐀</button>
                <button>🦃</button>
                <button>🦦</button>
                <button>🐧</button>
                <button>🐈️</button>
                <button>🐄</button>
                <button>🐾</button>
                <button>🦮</button>
                <button>🐕️</button>
                <button>🐿 </button>
                <button>🐇</button>
                <button>🕊 </button>
                <button>🐝</button>
                <button>🦋</button>
                <button>🦌</button>
                <button>🐐</button>
                <button>🐦️</button>
                <button>🐂</button>
                <button>🦜</button>
                <button>🍃</button>
                <button>🕷️</button>
                <button>🐖</button>
                <button>🐃</button>
                <button>🐄</button>
                <button>🐮</button>
                <button>🦇</button>
                <button>🦝</button>
                <button>🕊️</button>
                <button>🦅</button>
                <button>🐿️</button>
                <button>🦛</button>
                <button>🦦</button>
                <button>🦀</button>
                <button>🦄</button>
                <button>🐊</button>
                <button>🕷</button>️
                <button>🪲</button>
                <button>🐞</button>
            </div>
            <div>
                <h3>Science</h3>
                <button>🎓</button>
                <button title="Abacus">🧮</button>
                <button title="compass">🧭</button>
                <button>💬</button>
                <button>📊</button>
                <button>🪐</button>
                <button>🛰️</button>
                <button>📡</button>
                <button>🔭</button>
                <button>🧪</button>
                <button>🧬</button>
                <button title="Brain">🧠</button>
                <button>🌎️</button>
                <button>🌍️</button>
                <button>🌏️</button>
            </div>
            <div>
                <h3>Space</h3>
                <button>🪐</button>
                <button>☀️</button>
                <button>🌟</button>
                <button>🌒</button>
                <button>🌔</button>
                <button>🚀</button>
                <button>🔭</button>
                <button>🛰️</button>
                <button>📡</button>
                <button>⚡️</button>
                <button>✨</button>
                <button>✧</button>
                <button>✦</button>
                <button>🌐</button>
                <button>🌎️</button>
                <button>🌍️</button>
                <button>🌏️</button>
            </div>
            <div>
                <h3>Food and Beverage</h3>
                <button title="A cup of coffee">☕️️</button>
                <button title="A glass of beer - beverage">🍺</button>
                <button>🍮</button>
                <button>🍞</button>
                <button>🍜</button>
                <button>🥗</button>
                <button>🍸</button>
                <button>🍓</button>
                <button>🍎</button>
                <button title="carrot">🥕</button>
                <button>🍊</button>
                <button>🍍</button>
                <button>🍉</button>
                <button>🥦</button>
                <button>🍆</button>
                <button title="Onion">🧅</button>
                <button>🌙</button>
                <button>🍋</button>
                <button>🍔</button>
                <button>🍕</button>
                <button>🍣</button>
                <button>🍗</button>
                <button title="Bancon">🥓</button>
            </div>
            <div>
                <h3>Flags</h3>
                <button title="Flag of United Nations (UN)">🇺🇳</button>
                <button title="Flag of European Union">🇪🇺</button>
                <button title="Vatican's flag">🇻🇦</button>
                <button title="Italy's flag">🇮🇹</button>
                <button title="Spain's flag, Spanish flag">🇪🇸</button>
                <button title="Portugal's flag, Flag of Portugal, Portuguese Flag">🇵🇹</button>
                <button title="Flag of France">🇫🇷</button>
                <button title="Germany's flag">🇩🇪</button>
                <button title="Austria's flag, Austrian flag">🇦🇹</button>
                <button title="Flag of Switzerland, Swiss flag">🇨🇭</button>
                <button title="Belgian flag">🇧🇪</button>
                <button title="Netherlands">🇳🇱</button>
                <button title="Denmark's flag">🇩🇰</button>
                <button title="Poland's flag">🇵🇱</button>
                <button title="Bulgaria's flag">🏴󠁧󠁢󠁷󠁬󠁳󠁿</button>
                <button title="Greece's flag">🇬🇷</button>
                <button title="Cyprus' flag">🇨🇾</button>
                <button title="Hungrary">🇭🇺</button>
                <button title="Croacia's flag">🇭🇷</button>
                <button title="Ireland's flag, Irish flag">🇮🇪</button>
                <button title="Flag of United Kingdom">🇬🇧</button>
                <button title="England's flag">🏴󠁧󠁢󠁥󠁮󠁧󠁿</button>
                <button title="Scotland's flag">🏴󠁧󠁢󠁳󠁣󠁴󠁿</button>
                <button title="Wale's flag">🏴󠁧󠁢󠁷󠁬󠁳󠁿</button>
                <button title="Canadian flag" >🇨🇦</button>
                <button title="Australian flag">🇦🇺</button>
                <button title="New Zelanda">🇳🇿</button>
                <button title="American/USA flag">🇺🇲</button>
                <button title="South Africa's flag, South African flag">🇿🇦</button>
                <button title="Cape Verde's flag">🇨🇻</button>
                <button tilte="Nigeria's flag">🇳🇬</button>
                <button title="Flag of India, Indian flag">🇮🇳</button>
                <button title="Bangladesh flag">🇧🇩</button>
                <button title="Turkish flag">🇹🇷</button>
                <button titte="Azebaijan's flag">🇦🇿</button>
                <button title="Armenia flag">🇦🇲</button>
                <button title="Japanese flag">🇯🇵</button>
                <button title="Ukraine's flag">🇺🇦</button>
                <button title="Belarus">🇧🇾</button>
                <button>🇷🇺</button>
                <button title="Bahamas' flag">🇧🇸</button>
                <button title="Jamaican flag">🇯🇲</button>
                <button title="Mexico's flag, Mexican flag">🇲🇽</button>
                <button title="Flag of Argentina">🇦🇷</button>
                <button title="Uruguay's flag">🇺🇾</button>
                <button title="Chile's flag">🇨🇱</button>
                <button title="Peru's flag, Peruvian flag">🇵🇪</button>
                <button title="Colombia's flag">🇨🇴</button>
                <button title="Venezuela's flag, Venezuelan flag">🇻🇪</button>
                <button title="Puerto Rico's flag">🇵🇷</button>
                <button tilte="Hondura's flag">🇭🇳</button>
                <button title="Bolivia's flag">🇧🇴</button>
                <button title="Flag of Costa Rica">🇨🇷</button>
                <button title="Suriname">🇸🇷</button>
                <button title="El Salvador">🇸🇻</button>
                <button title="Dominican Republic's flag">🇩🇴</button>
                <button title="Flag of Brazil, Brazilian flag">🇧🇷</button>
                <button title="Japan's flag, Japanese flag">🇯🇵</button>
                <button title="Vietnan's flag, Vietnamese flag">🇻🇳</button>
                <button title="Flag of South Korea">🇰🇷</button>
                <button title="Singapore's flag">🇸🇬</button>
                <button title="Taiwan's flag, Taiwanese flag">🇹🇼</button>
                <button title="China's flag">🇨🇳</button>
                <button title="Hong Kong (China's SAR - Special Administrative Region)">🇭🇰</button>
                <button title="Macao (China's SAR)">🇲🇴</button>
                <button title="Mongolia flag">🇲🇳</button>
                <button title="Leabanon's flag">🇱🇧</button>
                <button title="Flag of Syria, Syrian Flag">🇸🇾</button>
                <button title="Flag of Morocco">🇲🇦</button>
                <button title="Algeria's flag">🇩🇿</button>
                <button title="Tunisia's flag">🇹🇳</button>
                <button title="Egypt's flag">🇪🇬</button>
                <button>🇾🇪</button>
                <button title="Flag of UAE - United Arabs Emirates">🇦🇪</button>
                <button title="Jordan's flag">🇯🇴</button>
                <button title="Qatar">🇶🇦</button>
                <button title="Saudi Arabia">🇸🇦</button>
                <button title="Bahrain flag">🇧🇭</button>
                <button>🇮🇷</button>
                <button tilte="Pirate flag, used by pirate ships (funny)">🏴‍☠️</button>
                <button title="Chequered flag">🏁</button>
                <button title="Triangular flag">🚩</button>
                <button title="Crossed flags">🎌</button>
                <button title="Black flag">🏴</button>
                <button title="White flag">🏳</button>
            </div>
            <div>
                <h3>Non Categorized</h3>
                <button>🛻</button>
                <button>🏆</button>️
                <button>🥇</button>
                <button>🥈</button>
                <button>🥉</button>
                <button title="Letter">✉️</button>
                <button title="Newspaper>📰</button>
                <button>️💲</button>
                <button>🕟</button>
                <button>📬</button>
                <button>⛏️</button>
                <button>🚲</button>
                <button title="Canoe - boat">🛶</button>
                <button>🪑</button>
                <button>▶</button>
                <button>🔗</button>
                <button>❌️</button>
                <button>🔙</button>
                <button>💤</button>
                <button>✊🏽</button>
                <button>🏘️</button>
                <button>🖋</button>
                <button>✍</button>️
                <button>✉️</button>
                <button>🖼️</button>
                <button>🃏</button>
                <button>📷️</button>
                <button title="Vehicle - bus">🚍</button>️
                <button>🏵</button>
                <button>🕸️</button>
                <button>📸</button>
                <button>🦡</button>
                <button>👀</button>
                <button>⤵️</button>
                <button>🚂</button>
                <button>🏳 </button>
                <button>🔡</button>
                <button>🌍️</button>
                <button>🏆️</button>
                <button>🏭️</button>
                <button>📖</button>
                <button>🔁</button>
                <button>⚖️</button>
                <button>🍉</button>
                <button>↕️</button>
                <button>🎉</button>
                <button>🔒</button>
                <button>🗽</button>
                <button title="Bank">🏦</button>
            </div>
            <div>
                <h3>Funny Ascii/Unicode Art</h3>
                <button>(^_^)</button>
                <button>ᕕ( ᐛ )ᕗ</button>
                <button>ᕕ(ツ)ᕗ</button>
                <button>( = ⩊ = )</button>
                <button>乁_ツ_ㄏ</button>
                <button>乁_益_ㄏ</button>
            </div>
      </div>

<button>





    `
});

unicodeWindow.querySelector(".div-unicode-emoji-symbol")
             .addEventListener("click", (event) => {
                 if(event.target.tagName !== "BUTTON"){
                     return;
                 }
                 console.log(" [TRACE] insert unicode symbol = ", event.target.textContent);
                 editorInsertTextArCursor(event.target.textContent);
             });


function openUnicodeWindow()
{
    unicodeWindow.show();
}

async function updateCSRFToken()
{
    let resp = await httpRequest("GET", "/api/token", null);
    if(resp.status === "ok")
    {
        CSRF_TOKEN = resp.token;
    }
}

// Update CSRF token every 30 minutes
//   = 30 minutes * 60 seconds/minutes * 1000 milliseconds/seconds
//   = 1,800,000
let INTERVAL_30_MINUTES = 1800000;
setInterval(updateCSRFToken, INTERVAL_30_MINUTES);
