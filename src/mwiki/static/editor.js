/* Settings for the JavaScript code editor Ace9
 *
 ********************************************************/


let editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.session.setMode("ace/mode/markdown");
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
 
    /// console.log(" [TRACE] out.html = ", out.html);
    // let src = 'data:text/html;charset=utf-8,' + encodeURI(out.html); 

    let previewWindow = new PopupWindow({
          title: `Preview of: ${currentWikiPageTitle}`
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

    //// window.onpaste = onPasteEventHandler;
    // window.addEventListener("paste", onPasteEventHandler, false);

    // document.onpaste = onPasteEventHandler;

    // let output = domToMarkdownCompiler(el);
    // console.log("output \n", output);
