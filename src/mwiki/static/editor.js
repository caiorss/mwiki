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

//// window.onpaste = onPasteEventHandler;
// window.addEventListener("paste", onPasteEventHandler, false);

// document.onpaste = onPasteEventHandler;

// let output = domToMarkdownCompiler(el);
// console.log("output \n", output);