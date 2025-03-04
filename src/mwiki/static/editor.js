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
        save_document();
    })
})

async function save_document()
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
    if(status == "ok"){
        statusbar.textContent = "Document saved ok.";
        // Note:  currentWikipage is global variable defined in edit.html template.
        let url = `/wiki/${currentWikiPage}#${anchor}`
        // Redirect to corresponding wiki page
        // and heading 
        document.location.href= url;
    } else {
        console.log("Status Error = ", out);
        statusbar.textContent = "Failed to save document."
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
        let fileName = `pasted-image-${timestamp}.png`
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
      };
      // let b64blob =  URL.createObjectURL(blob);
      // console.log("blob = ", b64blob);
      // destinationImage.src = b64blob;
    }
  } catch (error) {
    log(error.message);
  }
}

document.onpaste = pasteImage;



