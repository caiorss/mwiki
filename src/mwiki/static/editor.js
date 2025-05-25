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

editor.getSession().setUseWrapMode(true)
editor.getSession().setWrapLimitRange(60, 60);

/** Vim Emulation */
editor.setKeyboardHandler("ace/keyboard/vim");

ace.config.loadModule("ace/keyboard/vim", function(m) {
    var VimApi = require("ace/keyboard/vim").CodeMirror.Vim
    VimApi.defineEx("write", "w", function(cm, input) {
        // cm.ace.execCommand("save")
        editorSaveDocument();
    })
})

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

async function editorSaveDocument()
{
    let code  = editor.getValue();
    // console.log("Current page ", page);
    // console.log("Editor content = \n", code);
    const urlParams = new URLSearchParams(window.location.search);
    const lineStart = urlParams.get('start');
    const lineEnd   = urlParams.get('end');
    const anchor    = urlParams.get('anchor');
    const page      = urlParams.get('page');
    let payload = {  "content": code
                   , "start":   lineStart
                   , "end":     lineEnd 
                };
    let out = await http_post(document.URL, payload);
    console.log(" [RESULT] of saving operation = ", out)
    let status = out["status"];
    let statusbar = document.querySelector("#status-info");

    let currentdate = new Date(); 
    let datetime = currentdate.getDate() + "/"
            + (currentdate.getMonth()+1)  + "/" 
            + currentdate.getFullYear() + " @ "  
            + currentdate.getHours() + ":"  
            + currentdate.getMinutes() + ":" 
            + currentdate.getSeconds();

    if(status == "ok"){
        // Note:  currentWikipage is global variable defined in edit.html template.
        let url = `/wiki/${currentWikiPage}#${anchor}`
        // Redirect to corresponding wiki page
        // and heading 
        document.location.href = url;
        statusbar.textContent = `Saved at ${datetime}.`
    } else {
        console.log("Status Error = ", out);
        statusbar.textContent = `Failed to reach the server at ${datetime}.`    }
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

let selectPageWindow = new PopupWindow({
       title: "Insert Link to Wiki Page"
    ,  height: "100px"
    ,  html: `
    <input id="prompt-select-page" name="select-page" list="pagelist">
    <datalist id="pagelist"></datalist>
    <button onclick="insertLinkToPageCallback();">Insert</button>
    `
});

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
          console.log(" [TRACE] Null payload");
          return;
        }
        console.log(" [TRACE] Payload = ", payload);
        let out = await http_post("/paste", payload);
        console.log(" Output = ", out);
        editorInsertTextArCursor(`![[${fileName}]]`);
        // Automatically save document after pasting any image.
        ///// editorSaveDocument();
      };
      // let b64blob =  URL.createObjectURL(blob);
      // console.log("blob = ", b64blob);
      // destinationImage.src = b64blob;
    }
  } catch (error) {
    console.log(error.message);
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
    ,  html: `

        <form id="uploadForm" action="/api/upload" method="POST">
            <input type="hidden" name="csrf_token" value="${CSRF_TOKEN}">
            <div class="field">
                <label for="fileLabel">Link Label</label>
                <input name="fileLabel" id="fileLabel" title="Enter label of file link. (Optional)"></fileLabel>
            </div>
            <div class="field">
                <label for="fileInput">Choose a file</label>
                <input type="file" id="fileInput" name="file" required>
            </div>
            <br>
            <div class="field">
                <button type="submit" name="submit">Upload</button>
            </div>
        </form>
        <p id="upload-status">Ready to upload file.</p>
        <p>
            This form allows uploading files and inserting 
            hyperlinkt to it at current cursor position in 
            the wiki code editor. NOTE: The file link label 
            is optional, if it is empty, it the file name will
            be used as the link label.
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
        
    console.log(" dom = ", dom);
    var result = null;
    // alert("Not implemented");
    if (!res.ok)
    {
        result = {
              "status": "error"
            , "error": httpErrorCodes[res.status]
        }
        console.log(" [TRACE] message = ", result);
        dom.innerText = 'ERROR: Failed to upload file';
    } else {
        dom.innerText = 'Upload successful';
        result = await res.json();
        let filename = result["file"];
        uploadWindow.hide();
        let fileLabel = document.querySelector("#fileLabel");
        let value = fileLabel.value;
        var output = "";
        if(value !== ""){
            output = `[[${filename}|${value}]]`
        } else {
            output = `[[${filename}]]`
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
  console.log("File(s) dropped");

  // Prevent default behavior (Prevent file from being opened)
  ev.preventDefault();

  if (ev.dataTransfer.items) {
    // Use DataTransferItemList interface to access the file(s)
    [...ev.dataTransfer.items].forEach((item, i) => {
      // If dropped items aren't files, reject them
      if (item.kind === "file") {
        const file = item.getAsFile();
        console.log(`… file[${i}].name = ${file.name}`);
      }
    });
  } else {
    // Use DataTransfer interface to access the file(s)
    [...ev.dataTransfer.files].forEach((file, i) => {
      console.log(`… file[${i}].name = ${file.name}`);
    });
  }
}

function dragOverHandler(ev) {
  console.log("File(s) in drop zone");

  // Prevent default behavior (Prevent file from being opened)
  ev.preventDefault();
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
          title: `Preview of: ${currentWikiPage}`
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

    previewWindow.show();
}


//// window.onpaste = onPasteEventHandler;
// window.addEventListener("paste", onPasteEventHandler, false);

// document.onpaste = onPasteEventHandler;

// let output = domToMarkdownCompiler(el);
// console.log("output \n", output);