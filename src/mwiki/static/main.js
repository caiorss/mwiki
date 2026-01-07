class PopupWindow
{
    constructor(options)
    {
        let title = options.title || "";
        let html  = options.html  || "";
        let width = options.width || "500px";
        // let height = options.height || "400px";
        let top = options.top || "10%";
        let left = options.left || "30%";
        let zIndex = options.zIndex || "1000";
        let visible = options.visible || false;
        let windowI18NTitleTag = options.titleI18nTag || "";
        this._html = html;
        this._dom = document.createElement("div");
        document.body.appendChild(this._dom);
        this._dom.classList.add("popup-window");
        this._dom.style.zIndex = zIndex;
        this._dom.style.position = "absolute";
        this._dom.style.width  = width;
        // if( options.height ){ this._dom.style.height = options.height; }
        this._dom.style.top    = top;
        this._dom.style.left   = left;
        this._dom.style.background = "aliceblue";
        this._dom.style.padding = "10px";
        this._dom.style.display = "inline-block";
        if(!visible){ this.hide() };
        let code = `<h2 data-i18n="${windowI18NTitleTag}" class="window-title">${title}</h2> <button class="btn-window-close">[X]</button><hr>`;
        // console.log(" [TRACE] code = ", code);
        this._dom.innerHTML = code;
        this._dom.innerHTML += html; 
        let self = this;
        this.onClick(".btn-window-close", () => self.close());
    }

    dom(){
      return this._dom;
    }

    setHeight(height)
    {
      this._dom.style.height = height;
    }

    /* Add a CSS Class name to change Window presentation. */
    addClass(cssClassNameStr)
    {
       this._dom.classList.add(cssClassNameStr);
    }

    querySelector(selector)
    {
      let dom = this._dom.querySelector(selector);
      return dom;
    }

    childElementByClass(cssClassSelector)
    {
      let dom = this._dom.querySelector("." + cssClassSelector);
      return dom;
    }

    setTitle(title)
    {
        let x= this._dom.querySelector(".window-title");
        if(!x){
            console.error(`DOM element of CSS class 'window-title' not found.`);
            return;
        }
        x.textContent = title;
    }

    setMessage(message)
    {
        let x =  this._dom.querySelector(".popup-message-text");
        if(!x)
        { 
            console.error(`Not found container of CSS class 'pupup-message-text'. 
                              Failed to set popup window messasge.`) ;
            return;
        }
        x.innerHTML = message;
    }

    /* Add event to DOM element of this window, given the DOM
     * element CSS selector. For instance, if this window has
     * a button <button class="btn-submit">Submit</button>
     *
     * pwindo.onEvent(".btn-submit", "click", () => console.log("Button clicked"));
     *------------------------------------------- */
    onEvent(cssSelector, eventName, handler)
    {
      
        let x =  this._dom.querySelector(cssSelector);
        if(!x)
        { 
            console.error(`PopUpWindow.onEvent(selector, eventName, handler) => Not found container of CSS class 'pupup-message-text'. 
                              Failed to set popup window messasge.`) ;
            return;
        }
        x.addEventListener(eventName, handler);
    }

    onWindowClick(handler)
    {
        this._dom.addEventListener("click", (event) => {
            let target = event.target;
            let className = target.className;
            handler(className);
        });
    }

    // Event triggered when window loses focus
    onBlur(handler)
    {
        this._dom.addEventListener("blur", handler);
    }

    onClick(query, handler)
    {
        let q = this._dom.querySelector(query);
        if(q == null){
            console.error(`DOM element '${query}' not found.`)
            return;
        }
        q.addEventListener('click', handler);
    }

    closeWindowOnClick(query)
    {
      self = this;
      this.onClick(query, () => self.close());
    }

    value(query)
    {
        let q = this._dom.querySelector(query);
        if(q == null){
            console.error(`DOM element '${query}' not found.`)
            return;
        }
        let out = q.value;
        return out;
    }
    
    show()
    {
        this._dom.style.visibility = "visible";
        return this;
    }

    hide()
    {
        this._dom.style.visibility = "hidden";
        return this;
    }

    toggle()
    {
        if(this._dom.style.visibility === "hidden")
        {
           this.show(); 
        } else {
            this.close();
        }
        return this;
    }

    close()
    {
        this.hide();
        // this.remove();
    }

    /** Demove _dom element from anchor (document.body) */
    remove()
    {
        this._dom.remove();
    }
}

function localStorageSet(key, value)
{
    localStorage.setItem(key, JSON.stringify(value));
}

function localStorageGet(key)
{
    let valueStr = localStorage.getItem(key);
    if(!valueStr){ return null; }
    let data = JSON.parse(valueStr);
    return data;
}

/** Unescape/decode Html code.*/
function htmlUnescape(htmlStr)
{
    htmlStr = htmlStr.replace(/&lt;/g , "<");
    htmlStr = htmlStr.replace(/&gt;/g , ">");
    htmlStr = htmlStr.replace(/&quot;/g , "\"");
    htmlStr = htmlStr.replace(/&#39;/g , "\'");
    htmlStr = htmlStr.replace(/&amp;/g , "&");
    return htmlStr;
}


function htmlEscape(htmlStr){

    htmlStr = htmlStr.replace("<",  "&lt;");
    htmlStr = htmlStr.replace(">",  "&gt;");
    htmlStr = htmlStr.replace("\"", "&quot;");
    htmlStr = htmlStr.replace("\'", "&#39;");
    htmlStr = htmlStr.replace("&",  "&amp;");
    return htmlStr;
}


// Function to encode a UTF-8 string to Base64
function utf8ToBase64(str) {
    const encoder = new TextEncoder();
    const data = encoder.encode(str);

    const binaryString = String.fromCharCode.apply(null, data);
    return btoa(binaryString);
}

// Function to decode a Base64 string to UTF-8
function base64ToUtf8(b64) {
    const binaryString = atob(b64);
    // Create a Uint8Array from the binary string.
    const bytes = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }
    const decoder = new TextDecoder();
    return decoder.decode(bytes);
}


/** Render a LaTeX formula in some DOM element obtained
  * with document.querySelector(...) API.
  *
  * @param {any}     domElement  - DOM element where the equation will be rendered.
  * @param {string}  latexCode   - LaTeX code of equation be rendered.
  * @param {boolean} displayMode - true if the formula is display mode.
  *
  **/
function katexRenderDOMLatexFormula(domElement, latexCode, displayMode = false)
{
  var macros = {};
  try {
    macros = JSON.parse(base64ToUtf8(KATEX_MACROS));
  } catch (error) {
    // console.log(" JSON Parsing error: ", error);
  }
  // console.log(" [TRACE] macros = ", macros);
  try {
    katex.render(latexCode, domElement
                  , { displayMode: displayMode, macros: macros });
  } catch (error) {
    domElement.textContent = prev + error;
  }
}


function katexRenderDOMLatex(domElement)
{
   const CSS_CLASS_DIV_LATEX_CODE = "div-latex-code";
   const CSS_CLASS_MATH_INLINE = "math-inline";
   if( !IS_LATEX_RENDERER_KATEX ){ return; }
   var macros = {};
   try {
     macros = JSON.parse(base64ToUtf8(KATEX_MACROS));
    } catch(error){
        console.log(" JSON Parsing error: ", error);
    }
    if ( domElement.classList.contains(CSS_CLASS_MATH_INLINE)
         || domElement.classList.contains(CSS_CLASS_DIV_LATEX_CODE) )
    {
      let prev = domElement.textContent;
      domElement.classList.remove("lazy-load-latex");
      try{
         let isDisplayMode = domElement.classList.contains(CSS_CLASS_DIV_LATEX_CODE);
         katex.render(domElement.textContent, domElement, { displayMode: isDisplayMode, macros: macros});
      } catch(error){
          domElement.textContent = prev + error;
      }
       return;
    }
   // console.log("Katex macros = ",macros);
   // Render inline nodes (non display math)
   let nodesInline = domElement.querySelectorAll(".math-inline");
   for(let n of nodesInline)
   {
     let prev = n.textContent;
     try{ 
       n.classList.remove("lazy-load-latex");
       katex.render(n.textContent, n, { displayMode: false, macros: macros});
    } catch(error){
        n.textContent = prev + error;
    }
   }
   // Render display math 
   let nodesDisplayMode = domElement.querySelectorAll(".div-latex-code");
   for(let n of nodesDisplayMode)
   {
      let prev = n.textContent;
      n.classList.remove("lazy-load-latex");
      try{
        katex.render(n.textContent, n, { displayMode: true, macros: macros });
      } catch(error) {
        n.textContent = prev + `\n${error}`;
      }
  }
}

function katexRenderDocumentLatex()
{
   katexRenderDOMLatex(document.body);
}

document.addEventListener("DOMContentLoaded", ()=> {
   let formulas = document.querySelectorAll(".lazy-load-latex");
   const MAX_FORMULAS = 300;
   
   if(formulas.length <= MAX_FORMULAS){
      // Render all LaTeX formulas in this document, otherwise do Lazy loading
      katexRenderDocumentLatex();
   } else {
     // Render only the first MAX_FORMULAS formulas
      for(i = 0; i < MAX_FORMULAS; i++){
        let dom = formulas[i];
        katexRenderDOMLatex(dom);
        dom.classList.remove("lazy-load-latex");
      }
   }
});

/** Render DOM (Document Object Model) node using either KaTeX or MathJax
 *
 *  Example:
 *  let dom = document.querySelect(".someDomElementCssSelector");
 *  renderDOMLatex(dom);
 */
function renderDOMLatex(domElementObject)
{
   if(IS_LATEX_RENDERER_KATEX)
   {
      katexRenderDOMLatex(domElementObject);
   }
   if(IS_LATEX_RENDERER_MATHJAX)
   {
     MathJax.typeset();
   }
}

/* Get the maximum random integer within the range (0, size - 1)
   without repetition
*/
function nextRandomInt(size, current)
{
  var out = current;
  while( out === current )
  {
    out = Math.floor(Math.random() * size);
  }
  return out;
}


class FlashCard
{
  constructor(root)
  {
     this._handlers = {}; 
     this._root = root;
     this._visible = false;
     // Number of flashcards in this deck of flashcards
     this._size = JSON.parse(root.dataset.size);
     // Current visible flashcard in practice mode (when all cards are hidden)
     this._current = 0;
     let self = this;
     this.bindClick("btn-flashcard-next", (target) => self.next(target));
     this.bindClick("btn-flashcard-prev", (target) => self.prev(target));
     this.bindClick("btn-flashcard-view", (target) => self.toggle(target));
     this.bindClick("btn-show-card", (target) => self.showAnswer(target));
     this.bindClick("btn-flashcard-reset", (target) => {
        this._current = 0;
        let entries = this._root.querySelectorAll(".card-entry");
        for(let x of entries)
        {
           x.classList.add("hidden");    
           let backside = x.querySelector(".card-answer");
           backside.classList.add("hidden");
           x.querySelector(".btn-show-card").textContent = "open";
        }
        this.toggleCard(0);
        let checkbox = this._root.querySelector(".display-backside-checkbox");
        // checkbox.checkbox = false;
        let displayBackSide = checkbox.checked;
        if(displayBackSide){
          checkbox.click();  
        }
     });
     let toggleBackSide = () => {
        //this.toggleBackside(this._current);
        let entries = this._root.querySelectorAll(".card-entry");
        for(let x of entries)
        {
           // x.classList.remove("hidden");    
           let backside = x.querySelector(".card-answer");
           backside.classList.toggle("hidden");
           let label = backside.classList.contains("hidden") ? "open" : "close";
           x.querySelector(".btn-show-card").textContent = label;
        }
     };
    this.bindClick("display-backside-checkbox", toggleBackSide);
    let displayBackside = this.checkboxValue(".display-backside-checkbox");
    if(displayBackside){ toggleBackSide(); }
  }
  
  toggle(target)
  {
    if(this._visible){ this.hide(); } 
    else 						 { this.show(); }
  }

  /** Toggle visibility of the the it-th flashcard
    * @param {number} index
    */
  toggleCard(index)
  {
    
    let card = this._root.querySelectorAll(".card-entry")[index];
    card.classList.toggle("hidden");
  }

  /** Tooggle visibility of the backside of the i-th flashcard
    * @param {number} index
    */
  toggleBackside(index)
  {
    let card = this._root.querySelectorAll(".card-entry")[index];
    let backside = card.querySelector(".card-answer");
    backside.classList.toggle("hidden");
  }

  
  /** Display the backside of the i-th flashcard
    * @param {number} index
    */
  displayBackside(index)
  {
    let card = this._root.querySelectorAll(".card-entry")[index];
    let backside = card.querySelector(".card-answer");
    backside.classList.remove("hidden");
  }
  
  show(target)
  {
    	this._visible = true;
      let entries = this._root.querySelectorAll(".card-entry");
      for(let x of entries)
      {
         x.classList.remove("hidden");    
         x.querySelector(".card-answer").classList.remove("hidden");
      }
  }
  
  hide(target)
  {
    	this._visible = false;
      let entries = this._root.querySelectorAll(".card-entry");
      for(let x of entries)
      {
         x.classList.add("hidden");    
         x.querySelector(".card-answer").classList.add("hidden");
      }
    	// entries[0].classList.remove("hidden");
      this._root.querySelectorAll(".card-entry")[this._current].classList.remove("hidden");
  }
  
  /* Switch to next flashcard in the current cardset. */
  next(target)
  {
    if(this._visible){ return; }
    //this._root.querySelectorAll(".card-entry")[this._current].classList.toggle("hidden");
    this.toggleCard(this._current);
    let randomMode = this.checkboxValue(".random-mode-checkbox");
    let displayBackside = this.checkboxValue(".display-backside-checkbox");
    if(randomMode){
      this._current = nextRandomInt(this._size, this._current);
    } else {
      this._current = this._current + 1;
      if(this._current >= this._size){ this._current = this._size - 1}
    }
    this.toggleCard(this._current);
    if(displayBackside){
      this.displayBackside(this._current);
    }
    //this._root.querySelectorAll(".card-entry")[this._current].classList.toggle("hidden");
    // alert("Error not implementd");
  }

  /** Get value of a checkbox, given its CSS selector. 
    * @param {string} selector 
    * @return {boolean}
    */   
  checkboxValue(selector)
  {
    let dom = this._root.querySelector(selector)
    if(!dom){ console.error(`DOM element with selector ${selector} not found.`)}
    let out = dom.checked;
    return out;
  }
  
  /* Switch to previous flashcard of the cardset. */
  prev(target)
  {
    if(this._visible){ return; }
    this._root.querySelectorAll(".card-entry")[this._current].classList.toggle("hidden");
    this._current = this._current - 1;
    if(this._current <= 0){ this._current = 0; }
    this._root.querySelectorAll(".card-entry")[this._current].classList.toggle("hidden");
  
  }

  /* Show back side of the current flashcard. */
  showAnswer(target)
  {
      let answer = target.parentElement.querySelector(".card-answer");
      let label  = answer.classList.contains("hidden") ? "close" : "open";
      target.textContent = label;
      answer.classList.toggle("hidden");
  }
 
  bindClick(buttonClassNameTarget, handler)
  {
    this._handlers[buttonClassNameTarget] = handler;
  }
  
  dispatchClick(targetClass, target)
  {
     let action = this._handlers[targetClass];
     if(!action){
       console.error(`Button class target not found: ${targetClass}`);
       return;
     }
     action(target);
  }
}

let flashcardObjects = {};

function cardHandler(event)
{
   let cardset = this;
   let obj = flashcardObjects[this.dataset.id];
   //console.log(" [TRACE] obj ", obj);
   let targetClass = event.target.classList[0];
   //console.log(" [TRACE] target = ", event.target);
   
   obj.dispatchClick(targetClass, event.target);
}



// I18N Internationalization for the Website GUI - Graphics User Interface.
// It allows adding new localization without changing the UI code.
translationsi18n = 
{
    // NOTE: Actually, it is international English using US-English (American English)
    // spelling. By international English, it means English without idiomatic expression
    // and local regional expressions.
    "en-US": {
		  "locale": 				  "English"
		, "locale-name-native":       "American (USA) English"
        , "button-yes-label":         "Yes"
        , "button-no-label":          "No"
		, "settings-page-title":      "Wiki Settings" 
		, "source-page-title":        "Source Code"
		, "sidebar-toggle-button":    { "title": "Toggle sidebar." }
		, "button-toggle-sections":   { "title": "Fold/Unfold all sections." }
		, "main-menu":                { "title": "Main menu" }
		, "pages-menu":               { "title": "Menu containing actions for current page." } 
		, "home-page-button":         { "title": "Go to the initial page (index)" }
		, "button-quick-switch-to-page": { "title": "Quick switch to page. Open a window that allows switching to Wiki page by typing its name or search all pages for the user entry." }
		, "user-accounts-menu-item-label": { "label": "Accounts", "title": "User accounts management." }
		, "menu-item-view-label":     "View"
		, "menu-item-edit-label":     "Edit"
		, "menu-item-new-label":      { "label": "New", "title": "Create new Wiki page" }
		, "tags-menu-item-label":     { "label": "Tags", "title": "Browse pages using tags." }
		, "menu-item-delete-label":   { "label": "Delete", "title": "Delete this wiki page" }
		, "menu-item-source-label":   { "label": "Source", "title": "Display source code of current wiki page." }
		, "links-menu-item-label":    { "label": "Links", "title": "Display all external and internal links of this wiki page." }
		, "menu-item-print-label":    { "label": "Print", "title": "Print current page or export it to PDF."}
		, "menu-item-print-icon":     { "title": "Print current page or export it to PDF."}
		, "login-button": 			  "LOG IN"
		, "username-label": 		  "User Name"
		, "username-placeholder": 	  "Enter your username"
        , "password-label": 		  "Password"
        , "password-placeholder":     "Enter your password"
        , "login-form-show-password-label": "Display password"
        , "login-form-show-password-checkbox": { "title": "Toggle password display." }
        , "login-form-token-auth-summary-label": "Token Authentication"
        , "login-form-token-label":              "Authentication token"
        , "login-form-token-input":              "Paste the authentication token"
        , "keybindings-menu-item":    
			{  "label": "Keybindings"
			 , "title": "Display a window showing all keyboard shortcuts, also known as keybindings."
			}
		, "login-menu-item-label": 	  "Log in"
		, "logoff-menu-item-label":   "Log off"
      , "settings-menu-item-label": {  "label": "Settings"
										,"title": "Form for changing web site settings, including description and site name."
									  }
      , "about-menu-item-label":    "About"
      , "new-account-menu-item-label": "New Account"
      , "user-settings-item-label": "My Account"
      , "licenses-menu-item-label": 
				{  "label": "Licenses"
				 , "title": "Licenses of open source libraries used by this project."
				}
		, "edit-section-button": { "title": "Edit section" }
		, "search-entry-placeholder": "Search"
		, "search-menu-item-label" :  "Search"
    , "sidebar-search-label":     "Search"
    , "sidebar-table-of-contentes-label": "Contents"    
		, "figure-prefix-label": "Figure"
        , "video-prefix-label":   "Video"
		, "title-listing-all-pages":   "All pages"
		, "title-search-results-page": "Search results for"
		, "search-form-label":  "Search pages"
		, "search-form-search-button-label": "Search"
		, "search-form-clear-button-label": "Clear"
		, "search-form-all-button-label":  "All"
		, "search-results-sort-by-label":  "Sort by"
		, "search-results-h2-label":  "Pages"
		, "number-of-search-results-label": "Results"
		, "sort-by-score-link-button":          { "label": "Score", "title": "Sort by score." }
		, "sort-by-name-link-button":           { "label": "Name",  "title": "Sort by name (alphabetic order)" }
		, "sort-by-modified-time-link-buttton": { "label": "Modified", "title": "Sort by modified time" }
		, "sort-by-created-time-link-button":   { "label": "Created", "title": "Sort by created time" }
		, "search-matches-label": "Search matches"
		, "settings-page-go-back-label": "Go back to"
        , "settings-page-successful-update-message": "Wiki settings updated successfully."
		, "settings-update-button": "Update"
		, "settings-sitename-label": "Website Name"
		, "settings-website-description-label": "Website Description"
		, "settings-public-checkbox-label": "Public"
		, "settings-language-switch-checkbox-label":     "Allow language switch "
		, "settings-language-switch-description":        "Allow users to switch the user interface language."
		, "settings-display-alt-button-checkbox-label":  "Display alt text button"
		, "settings-display-alt-button-description":     "Display a Mastodon-like alt text button for figures, which shows the alt text in a popup window when clicked."
		, "settings-display-edit-button-checkbox-label": "Diplay edit button"
		, "settings-vim-emulation-checkbox-label":       "Vim Emulation"
		, "settings-show-source-checkbox-label":         "Show Page Source"
		, "settings-show-licenses-checkbox-label":       "Show Licenses"
		, "settings-main-font-label":  					 "Main Font"
		, "settings-title-font-label": 					 "Title Font"
		, "settings-code-font-label":  					 "Code Font"
		, "settings-show-licenses-checkbox-description": "Displays menu option showing 'Licenses' that shows all open Source licenses used by this project."
		, "settings-show-source-checkbox-description":   "Provides a button that allows viewing the Markdown (wiki text) source code a wiki"
		, "settings-vim-emulation-checkbox-description": "Enable VIM editor emulation in the Wiki code editor (Ace9)"
		, "settings-display-edit-button-checkbox-description": "Display the wiki edit button for all users [E]. If this setting is disabled,  only admin users or users with permission to edit pages will be able to view the edit button."
		, "settings-default-locale-label":               "Default locale"
		, "settings-default-content-locale-label":       "Default content language"
		, "settings-use-default-locale-checkbox-label":  "Use Default Locale"
		, "settings-use-default-locale-description": 	   "Always use the default locale (language) regardless of the user preferred language provided by the web browser."
		
		, "settings-public-checkbox-description": "If enabled, everybody including non logged in users will be able to view the wiki content. Note that only logged in users can edit the wiki." 
    , "settings-use-cdn-checkbox-label":      "Use CDN"
		, "settings-use-cdn-description":         "Load JavaScript libraries from a CDN Content-Delivery Network instead of loading them from this server."
    , "settings-latex-renderer-label":        "LaTeX Renderer"
    , "settings-latex-renderer-description":  "JavaScript library used for rendering LaTeX math formulas. Note that the support for KaTeX is still experimental. "
    , "settings-h2-general-settings":        "General Settings"
    , "settings-h2-math-rendering-settings": "Math Rendering Settings"
    , "settings-h2-editor-settings":         "Editor Settings"
    , "settings-h2-language-settings":       "Language Settings"
    , "settings-h2-font-settings":           "Font/Typeface Settings"
        , "popup-window-change-language-menu-launcher": { "label": "Language"
                                                          , "title": "Open form that allows overriding the current user interface language." }
        , "popup-window-change-language": "Change the User Interface Language"
        , "popup-window-change-language-label1": "Set the user interface language."
        , "popup-window-change-language-label2": "This form allows overriding the current UI - User Interface language."
        , "popup-window-change-language-change-button": "Change"
        , "popup-window-change-language-close-button":  "Close"

        , "about-page-title":          "About"
		, "edit-page-title":           "Editing"
		, "edit-page-toolbar-title":   "Toolbar"
		, "edit-page-h3-insert-label": "Insert"
		, "edit-page-h3-actions-label": "Actions"
		, "edit-page-document-status-label": "Document not saved yet"
		, "edit-page-back-button": {  "label": "Back"
									, "title": "Switch to document view mode and exit editing mode."}

		, "edit-page-preview-popup-window": "Preview of"
		, "edit-page-preview-button": { 
									      "label": "Preview"
										, "title": "View how page will look like before saving."
									  }
		, "edit-page-save-button":  {
										  "label": "Save"
										, "title": "Save document and switch to view mode."
									}
    , "edit-page-save-icon-button": { "title": "Save document and switch to view mode." }
		, "edit-page-undo-button": "Undo"
		, "edit-page-redo-button": "Redo"
		, "edit-page-refcard-button": {
										  "label": "Reference Card"
										, "title": "Displays reference card containing examples about the markdown syntax."
									  }
		, "edit-page-insert-link-button": {
											  "label": "Link to Wiki page" 
											 ,"title": "Insert hyperlink to existing wiki page at current cursor position."

											}
		, "edit-page-upload-button": {  "label": "Link to Uploaded File"
									   , "title": "Upload file and insert link to it at current cursor position in the editor."
									 }
		, "edit-page-insert-latex-equation": "LateX Equation"
		, "edit-page-insert-latex-non-numbered-button": "Non Numbered LaTex Equation"
		, "edit-page-insert-theorem-button": "Theorem"
		, "edit-page-insert-details-button": "Details"
		, "edit-page-clipboard-h3-label": "Clipboard Options"
		, "edit-page-p-clipobard": "Select the clipboard pasting mode"
        , "edit-page-line-wrapping-checkbox":  { "title": "Toggle editor line wrapping." }
        , "edit-page-line-wrapping-checkbox-label":  "Line wrapping."
        , "edit-page-vim-emulation-checkbox":     { "title": "Toggle emulation of Vim editor keybindings." }
        , "edit-page-vim-emulation-checkbox-label": "Vim editor emulation"
        , "upload-form-window-title": "File Upload"
        , "upload-form-file-link-label": "Link Label"
        , "upload-form-choose-file-label": "Choose a file"
        , "upload-form-convert-jpeg-checkbox-label": "Convert Images to JPEG"
        , "upload-form-convert-jpeg-checkbox-description": "Reduce image file size by converting uploaded image to JPEG"
        , "upload-form-submit-button":  "Upload"
        , "upload-status-label": "Ready to upload file."
        , "upload-form-instruction": "This form allows uploading files and inserting link to it at current cursor position in the wiki code editor. NOTE: The file link label is optional. If it is empty, the file name will be used as the link label."
        , "delete-page-form-title":    "Delete page."
        , "delete-page-form-question": "Are you really sure you want to delete the page"
        , "delete-page-form-warning":  "WARNING: This action cannot be reversed."
        , "creating-page-title": "Creating page"
        , "create-page-form-legend":         "Create new page"
        , "create-page-form-optional-label": "Label (Optional)"
        , "create-page-form-description":    "Description (Optional)"
        , "create-page-form-keywords-label": "keywords (Optional)"
        , "create-page-form-create-button":  "Create"
        , "create-page-form-cancel-button":  "Cancel"
        , "quick-open-window-title":         "Quick Open Wiki Page"
        , "quick-open-page-open-button":     "Open"
        , "popup-window-note-myst-role-title":    "Note"
        , "foldable-math-solution-block-label":   "Solution"
        , "foldable-math-proof-block-label":      "Proof"
        , "foldable-math-derivation-block-label": "Derivation"
        , "foldable-math-example-block-label":    "Example"
        , "admonition-math-defintion-label":      "DEFINITION"
        , "admonition-math-theorem-label":        "THEOREM"
        , "admonition-math-example-label":        "Example"
        , "abbreviation-window-title":            "Abbreviation"
        , "links-page-title":                     "Links of"
        , "links-page-strong-label":              "Page"
        , "links-page-internal-links-h2":         "Internal Links"
        , "links-page-external-links-h2":         "External Links"
        , "new-note-popup-window-title":          "New Note"
        , "new-note-popup-window-label":          "Name"
        , "new-note-popup-window-instruction":    "Enter the name of the note be created."
        , "insert-link-popup-window-title":          "Insert Link to a Wiki Page"
        , "insert-link-popup-window-insert-button": "Insert"
        , "statusbar-upload-image-waiting-text": "Uploading image to server. Wait ..."
        , "statusbar-upload-image-finished-text": "Imagem uploaded successfully."
        , "statusbar-upload-image-error-text": "Error: failed to upload image."
        , "popup-window-footnote-title":          "Footnote"
        , "popup-window-equation-display-title":  "Equation"

        , "edit-page-latex-input-window":
          {
              "label": "LaTeX Input Window"
            , "title": "Open a LaTeX input popup window that allows typing LaTeX equations and getting immediate feedback about how the formula looks like when rendered."
          }
        
        , "latex-input-window-title": "LaTeX Input Window"
        , "latex-input-window-btn-insert": {  "label": "Insert"
                                            , "title": "Close this window and insert LaTeX formula at current cursor position. Keyboard shortcut: Alt + Enter"
                                           }
        , "latex-input-window-btn-clear": { "label":  "Clear"
                                          , "title":  "Clear LaTeX code entry. Keyboard shortcut: Ctrl + l" 
                                          }
        , "latex-input-window-btn-close": {
                                              "label": "Close"
                                            , "title": "Close this window."
                                          }
        , "latex-input-window-p": "Output:"
        , "btn-copy-source-code": { "title": "Copy the source code." }
        , "download-jupyter-notebook-icon-tooltip": { "title": "Download this Jupyter Notebook." }
        , "label-copy-source-code": "copied!"
	}
   ,"pt-BR": {
		  "locale":                   "Brazilian Portuguese"
		, "locale-name-native": 	  "Português Brasileiro"
        , "button-yes-label":         "Sim"
        , "button-no-label":          "Não"
		, "settings-page-title":      "Configurações da Wiki" 
		, "source-page-title":        "Código Fonte"
		, "sidebar-toggle-button":    { "title": "Abre ou fecha barra lateral." }
		, "button-toggle-sections":   { "title": "Dobrar/Desdobrar todas as seções." }
		, "main-menu":                { "title": "Menu principal" }
		, "pages-menu":               { "title": "Menu contendo ações para a página atual." } 
		, "home-page-button":         { "title": "Ir para a página inicial (Index)" }
		, "button-quick-switch-to-page": { "title": "Troca rápida de página. Abra uma janela que permite alternar para a página Wiki digitando seu nome ou buscar a entrada do usuário." }
		, "user-accounts-menu-item-label": { "label": "Contas", "title": "Gerenciamento de contas de usuário." }
		, "menu-item-view-label":     "Ver"
		, "menu-item-edit-label":     "Editar"
		, "menu-item-new-label":      { "label": "Nova", "title": "Criar nova página Wiki" }
		, "tags-menu-item-label":     { "label": "Tags", "title": "Navegar pelas páginas usando tags." }
		, "menu-item-delete-label":   { "label": "Deletar", "title":  "Excluir esta página wiki"}
		, "menu-item-source-label":   { "label": "Código", "title": "Exibir código-fonte da página wiki atual." }
		, "links-menu-item-label":    { "label": "Links", "title": "Exibir todos os links externos e internos desta página wiki." }
		, "menu-item-print-label":    { "label": "Imprimir", "title": "Imprimir página atual ou exporte-a para PDF."}
		, "menu-item-print-icon":     { "title": "Imprimir página atual ou exporte-a para PDF."}
		, "login-button": 			  "LOGAR"
		, "username-label":			  "Nome de Usuário"
		, "username-placeholder":     "Entre com o nome de usuário"
        , "password-label": 	      "Senha"
        , "password-placeholder":     "Entre com a senha"
        , "login-form-show-password-label": "Mostrar senha"
        , "login-form-show-password-checkbox": { "title": "Alternar exibição de senha." }
        , "login-form-token-auth-summary-label": "Autenticação com Token"
        , "login-form-token-label": "Token de autenticação"
        , "login-form-token-input": "Cole o token de autenticação"
        , "keybindings-menu-item":    
				{   "label": "Altalhos"
				  , "title": "Exibe uma janela mostrando todos os atalhos de teclado, também conhecidos como combinações de teclas (keybindings)."
				 }
		, "login-menu-item-label":    "Autenticar"
        , "settings-menu-item-label": 
			{   "label": "Configurações"
			  , "title": "Formulário para alterar as configurações do site, incluindo descrição e nome do site."
			}
		, "logoff-menu-item-label":   "Sair"
        , "about-menu-item-label":    "Sobre"
        , "new-account-menu-item-label": "Nova Conta"
        , "user-settings-item-label": "Minha Conta"
        , "licenses-menu-item-label": 
			{ 
			    "label": "Licenças"
			  , "title": "Licenças de bibliotecas de código aberto usadas por este projeto."
			}
		, "edit-section-button": 	  { "title": "Editar seção" }
		, "search-entry-placeholder": "Buscar"
		, "search-menu-item-label":   "Buscar"
        , "sidebar-search-label":     "Buscar"
        , "sidebar-table-of-contentes-label": "Conteúdo"
		, "figure-prefix-label":  "Figura"
        , "video-prefix-label":   "Vídeo"
        , "title-listing-all-pages":   "Todas Páginas"
		, "title-search-results-page": "Resultados de busca para"
		, "search-form-label":  "Buscar páginas"
		, "search-form-search-button-label": "Buscar"
		, "search-form-clear-button-label": "Limpar"
		, "search-form-all-button-label":  "Todas"
		, "search-results-sort-by-label":  "Ordenar por"
		, "search-results-h2-label":  "Páginas"
		, "number-of-search-results-label": "Resultados"
		, "sort-by-score-link-button":          { "label": "Pontuação",  "title": "Ordenar por pontuação." }
		, "sort-by-name-link-button":           { "label": "Nome",       "title": "Ordenar por nome (ordem alfabetica)" }
		, "sort-by-modified-time-link-buttton": { "label": "Modificado", "title": "Ordernar por tempo modificado." }
		, "sort-by-created-time-link-button":   { "label": "Criado",    "title": "Ordenar por tempo criado." }
		, "search-matches-label": "Correspondências de pesquisa"
		, "settings-page-go-back-label": "Voltar para"
        , "settings-page-successful-update-message": "Configurações da Wiki atualizadas com sucesso."
		, "settings-update-button": "Atualizar"
		, "settings-sitename-label": "Nome do Website"
		, "settings-website-description-label": "Descrição do Website"
		, "settings-public-checkbox-label": "Público"
		, "settings-language-switch-checkbox-label": "Permitir troca de idioma"
		, "settings-language-switch-description":    "Permitir que os usuários mudem o idioma da interface do usuário."
		, "settings-display-alt-button-checkbox-label":  "Exibir botão de texto alternativo"
		, "settings-display-alt-button-description":     "Exibir um botão de texto alternativo semelhante ao do Mastodon para as figuras, que mostre o texto alternativo em uma janela pop-up ao ser clicado."
		, "settings-display-edit-button-checkbox-label": "Mostrar botão editar"
		, "settings-vim-emulation-checkbox-label":       "Emulação do Vim"
		, "settings-show-source-checkbox-label":         "Mostrar Código de Fonte de Página"
		, "settings-show-licenses-checkbox-label":       "Mostrar Licenças"
		, "settings-main-font-label":  					 "Fonte Principal"
		, "settings-title-font-label": 					 "Fonte de Título"
		, "settings-code-font-label": 					 "Fonte de Código"
		, "settings-show-licenses-checkbox-description": "Exibe a opção de menu 'Licenças' que mostra todas as licenças de código aberto usadas por este projeto."
		, "settings-show-source-checkbox-description":   "Fornece um botão que permite visualizar o código-fonte Markdown (texto wiki) de um wiki"
		, "settings-vim-emulation-checkbox-description": "Habilitar emulação do editor VIM no editor de código Wiki (Ace9)."
		, "settings-display-edit-button-checkbox-description": "Exibir o botão de edição do wiki para todos os usuários [E]. Se esta configuração estiver desabilitada, somente usuários administradores ou usuários com permissão para editar páginas poderão visualizar o botão de edição."
		, "settings-public-checkbox-description": 		 "Se habilitado, todos, incluindo usuários não logados, poderão visualizar o conteúdo do wiki. Observe que somente usuários logados podem editar o wiki."
		, "settings-default-locale-label":               "Idioma/locale padrão"
		, "settings-default-content-locale-label":       "Idioma padrão do conteúdo"
		, "settings-use-default-locale-checkbox-label":  "Usar idioma/locale padrão"
		, "settings-use-default-locale-description": 	 "Sempre usar o idioma padrão (default locale), independentemente do idioma preferido do usuário fornecido pelo navegador da web."
    , "settings-use-cdn-checkbox-label": "Usar CDN"
		, "settings-use-cdn-description":   "Carregar as bibliotecas JavaScript de uma CDN (Rede de Distribuição de Conteúdo) em vez de carregá-las deste servidor."
    , "settings-latex-renderer-label":  "Renderizador LaTeX"
    , "settings-latex-renderer-description":  "Biblioteca JavaScript usada para renderizar fórmulas matemáticas em LaTeX. Observe que o suporte para KaTeX ainda é experimental."
    , "settings-h2-general-settings": "Configurações Gerais"
    , "settings-h2-math-rendering-settings": "Configurações de Renderização Matemática"    , "settings-h2-editor-settings": "Configurações do Editor"
    , "settings-h2-language-settings": "Configurações de Idioma"
    , "settings-h2-font-settings": "Configurações de Fonte/Tipo de Letra (Typeface)"
        , "popup-window-change-language-menu-launcher": { "label": "Idioma"
                                                          , "title": "Formulário que permite sobrepor/mudar o idioma atual da interface do usuário." }
        , "popup-window-change-language": "Alterar o idioma da interface do usuário"
        , "popup-window-change-language-label1": "Definir o Idioma da Interface do usuário."
        , "popup-window-change-language-label2": "Este formulário permite substituir/sobrepor o idioma atual da interface do usuário."
        , "popup-window-change-language-change-button": "Mudar"
        , "popup-window-change-language-close-button":  "Fechar"
        , "about-page-title":          "Sobre"
		, "edit-page-title":           "Editando"
		, "edit-page-toolbar-title":   "Barra de Ferramentas"
		, "edit-page-h3-insert-label": "Inserir"
		, "edit-page-h3-actions-label": "Ações"
		, "edit-page-document-status-label": "Documento não salvo ainda."
		, "edit-page-back-button": {  "label": "Voltar"
									, "title": "Alternar para o modo de visualização de documento e sair do modo de edição."}

		, "edit-page-preview-popup-window": "Visualização de"
		, "edit-page-preview-button": { 
									      "label": "Visualização"
										  , "title": "Veja como a página ficará antes de salvar."
									  }
		, "edit-page-save-button":  {
										  "label": "Salvar"
										, "title": "Salvar o documento e alternar para o modo de visualização."
									}
        , "edit-page-save-icon-button": { "title": "Salvar o documento e alternar para o modo de visualização." }
		, "edit-page-undo-button": "Desfazer"
		, "edit-page-redo-button": "Refazer"
		, "edit-page-refcard-button": {
										  "label": "Cartão de Referência"
										, "title": "Exibe um cartão de referência contendo exemplos sobre a sintaxe do markdown."
									  }
		, "edit-page-insert-link-button": {
											  "label": "Link para página da Wiki" 
											 ,"title": "Inserir hiperlink para uma página wiki existente na posição atual do cursor."

											}
		, "edit-page-upload-button": {   "label": "Link para arquivo enviado"
									   , "title": "Envia/sobe arquivo (faz upload) e insire link para ele na posição atual do cursor no editor."
									 }
		, "edit-page-insert-latex-equation": "Equação LateX"
		, "edit-page-insert-latex-non-numbered-button": "Equação LaTeX não numerada."
		, "edit-page-insert-theorem-button": "Teorema"
		, "edit-page-insert-details-button": "Detalhes"
		, "edit-page-clipboard-h3-label": "Opções da Área de Transferência"
		, "edit-page-p-clipobard": "Selecione o modo de colar da área de transferência"
        , "edit-page-line-wrapping-checkbox":  { "title": "Alternar quebra de linha do editor." }
        , "edit-page-line-wrapping-checkbox-label":  "Quebra de linha"
        , "edit-page-vim-emulation-checkbox":   { "title": "Alternar (ativa/desativa) a emulação de atalhos de teclado do editor Vim." }
        , "edit-page-vim-emulation-checkbox-label": "Emulação do editor Vim"
        , "upload-form-window-title": "Subir Arquivo (Upload)"
        , "upload-form-file-link-label": "Rótulo do link."
        , "upload-form-choose-file-label": "Escolha um arquivo."
        , "upload-form-convert-jpeg-checkbox-label": "Converter imagens para JPEG"
        , "upload-form-convert-jpeg-checkbox-description": "Reduzir o tamanho do arquivo de imagem convertendo a imagem enviada para JPEG"
        , "upload-form-submit-button":  "Enviar"
        , "upload-status-label": "Pronto para enviar arquivo."
        , "upload-form-instruction": "Este formulário permite o upload de arquivos e a inserção de um link para eles na posição atual do cursor no editor de código wiki. NOTA: O rótulo do link do arquivo é opcional. Se estiver vazio, o nome do arquivo será usado como rótulo do link."
        , "delete-page-form-title": "Excluir página."
        , "delete-page-form-question": "Você tem certeza de que deseja excluir a página?"
        , "delete-page-form-warning": "AVISO: Esta ação não pode ser revertida."
        , "creating-page-title": "Criando página"
        , "create-page-form-legend":           "Criar nova página"
        , "create-page-form-optional-label":   "Rótulo (Opcional)"
        , "create-page-form-description":      "Descrição (Opcional)"
        , "create-page-form-keywords-label":   "Palavras-chave (Opcional)"
        , "create-page-form-create-button":    "Criar"
        , "create-page-form-cancel-button":    "Cancelar"
        , "quick-open-window-title":         "Abertura rápida de Página Wiki"
        , "quick-open-page-open-button":     "Abrir"
        , "popup-window-note-myst-role-title":    "Nota"
        , "foldable-math-solution-block-label":   "Solução"
        , "foldable-math-proof-block-label":      "Prova"
        , "foldable-math-derivation-block-label": "Derivação"
        , "foldable-math-example-block-label":    "Exemplo"
        , "admonition-math-defintion-label":      "DEFINIÇÃO"
        , "admonition-math-theorem-label":        "TEOREMA"
        , "admonition-math-example-label":        "Exemplo"
        , "abbreviation-window-title":            "Abreviação"
        , "links-page-title":                     "Links de"
        , "links-page-strong-label":              "Página"
        , "links-page-internal-links-h2":         "Links Internos"
        , "links-page-external-links-h2":         "Links Externos"
        , "new-note-popup-window-title":          "Nova Nota"
        , "new-note-popup-window-label":          "Nome"
        , "new-note-popup-window-instruction":    "Digite o nome da nota a ser criada."
        , "insert-link-popup-window-title":          "Inserir Link para uma Página Wiki"
        , "insert-link-popup-window-insert-button": "Inserir"
        , "statusbar-upload-image-waiting-text": "Enviando imagem ao servidor. Esper..."
        , "statusbar-upload-image-finished-text": "Imagem enviada com sucesso."
        , "statusbar-upload-image-error-text":    "Error: falha de envio de imagem."
        , "popup-window-footnote-title":          "Nota de Rodapé"
        , "popup-window-equation-display-title":  "Equação"

        , "edit-page-latex-input-window":
            {
                "label": "Janela de Entrada LaTeX"
              , "title": "Abre uma janela pop-up de entrada LaTeX que permite digitar equações LaTeX e obter feedback imediato sobre a aparência da fórmula quando renderizada."

            }

        , "latex-input-window-title": "Janela de Entrada LaTeX"
        , "latex-input-window-btn-insert":
            { "label": "Inserir"
            , "title": "Fecha esta janela e insere a fórmula LaTeX na posição atual do cursor. Atalho de teclado: Alt + Enter"
            }
        , "latex-input-window-btn-clear":
          { "label": "Limpar"
          ,"title": "Limpar a entrada de código LaTeX. Atalho de teclado: Ctrl + l"
          }
        , "latex-input-window-btn-close":
          {
            "label": "Fechar"
           ,"title": "Fecha esta janela."
          }
        , "latex-input-window-p": "Saída:"
        , "btn-copy-source-code": { "title": "Copiar o código de fonte." }
        , "label-copy-source-code": "copiado!"
        , "download-jupyter-notebook-icon-tooltip": { "title": "Baixar este Jupyter Notebook." }
  }
        

};

const KEY_USER_LOCALE = "user_locale";

function setLocaleI18n(locale)
{
	var translations = translationsi18n[locale];
	if( !translations )
	{
        // Fallback to the primary locale
        translations = translationsi18n["en-US"];
	}
	/* let oldLocale = localStorage.getItem("locale");
	if(oldLocale !== locale )
	{
		localStorage.setItem("locale", locale);
		// if(oldLocale){ location.reload(); }
	}
	*/
	
	let elements = document.querySelectorAll("[data-i18n]");
	for(let elem of elements)
	{
		let tag = elem.getAttribute("data-i18n");
		if( elem.textContent.includes("[i18n]") && !elem.dataset.textContentI18N )
		{
		  elem.dataset.textContentI18N = elem.textContent;
		}
		let value_ = translations[tag];
		if( !value_){ continue; }
		let value = value_.label || value_;
		// console.log(`tag = ${tag} ; value = "${value}" ; elem = `, elem);
		if( value_.title )
		{
			if( elem.title.includes("[i18n]") )
			{

        let out = elem.textContent.replace("[i18n]", value._title);
        elem.title = out;
				// elem.title = elem.title.replace("[i18n]", value_.title);
			} else {
				elem.title = value_.title;
			}
		}
		if( elem.tagName === "INPUT" 
			&& (elem.type === "password" || elem.type === "text"
                || elem.type === "search"))
		{
			elem.placeholder = value;
			continue;
		}
		if( elem.tagName === "INPUT" && (elem.type === "submit" || elem.type == "button"))
		{
			elem.value = value;
			continue;
		}
		if( value_.title && !value_.label ){ continue; }
		// elem.textContent = value;
//		if( elem.textContent.includes("[i18n]") )
    if( elem.dataset.textContentI18N && elem.dataset.textContentI18N.includes("[i18n]") )
		{
		  let out =  elem.dataset.textContentI18N.replace("[i18n]", value);
		  // let out = elem.textContent.replace("[i18n]", value);
			elem.textContent = out;
		} else {
			elem.textContent = value;
		}
	}
	
}

function normalizeI18nLocale(userLocale)
{
    var locale = "";
	// Set all English locales to en-US (US English) as this
	// is the only English locale available. However, more
    // english locales can be added later if it is required.
	if( userLocale.startsWith("en-") ){
		locale = "en-US";
	}
	// Set all portuguese locales to pt-BR (Brazilian Portuguese)
	if( userLocale.startsWith("pt-") ){
		locale = "pt-BR";
	}
	return locale;
}

function getCurrentLocale()
{
    let locale = localStorageGet(KEY_USER_LOCALE)
                || DEFAULT_LOCALE
                || normalizeI18nLocale(navigator.language);
    return locale;
}

function doTranslationI18N()
{
    let locale = getCurrentLocale();
    setLocaleI18n(locale);
}

function geti18nTranslation(key) {
  let userLocale = getCurrentLocale();
  let value = translationsi18n[userLocale][key];
  return value;
}


function popupYesNo(title, message, handler)
{
    let buttonYesLabel = geti18nTranslation("button-yes-label");
    let buttonNoLabel = geti18nTranslation("button-no-label");
    let html_ = `
        <p>${message}</p>
        <button class="btn-yes">${buttonYesLabel}</button>
        <button class="btn-no">${buttonNoLabel}</button>
    `;
    let pwindow = new PopupWindow({
          title:  title
        , html: html_
    });
    pwindow.onWindowClick( (className) => {
        if(className == "btn-yes"){ handler(); pwindow.close(); }
        if(className == "btn-no" ){ pwindow.close(); }
    });
    pwindow.show();
}

function popupInput(title, message, label, handler)
{
    let buttonYesLabel = geti18nTranslation("button-yes-label");
    let buttonNoLabel = geti18nTranslation("button-no-label");
    let html_ = `
        <form>
          <fieldset>
                <p class="popup-message-text">${message}</p>
                <label>${label}</label><input type="text" class="popup-input" required="required" />
                </fieldset>
            <fieldset>
                <button class="primary-button btn-yes">${buttonYesLabel}</button>
                <button class="primary-button btn-no">${buttonNoLabel}</button>
            </fieldset>
        </form>
    `;
    let pwindow = new PopupWindow({
          title:  title
        , html: html_
    });
    pwindow.onWindowClick( (className) => {
        let entry = pwindow.value(".popup-input"); 
        if(className.includes("btn-yes") && entry)
        { 
            handler(entry); 
            pwindow.close(); 
        }
        if(className == "btn-no" ){ pwindow.close(); }
    });
    pwindow.show();
}


function popupMessage(title, message, options)
{
    let html_ = `
        <p class="popup-message-text">${message}</p>
    `;
    let pwindow = new PopupWindow({
          title: title 
        , html: html_
        , height: options.height
        , zIndex: options.zIndex
    });
    pwindow.onWindowClick( (className) => {
        if(className == "btn-popup-close"){ pwindow.close(); }
    });
    let hidden = options.hidden || false;
    // let closeOnBlur = options.closeOnBlur || false;
    // if(closeOnBlur)
    // {  
    //     //console.log(" [TRACE] Install close on Blur");
    //     pwindow.onBlur((event) => pwindow.remove()); 
    // }
    if(!hidden){ pwindow.show(); }
    return pwindow;
}

function popupIframe (title, url, options)
{
    if( options == undefined ){ 
        options = {};
    }
    let hidden = (options.hidden || false);
    let width = (options.width || "80%");
    // let minHeight = (options.minHeight || "90%");
    let html_ = `
        <iframe src="${url}" title="${title}" width="100%" height="100%" ></iframe> 
    `;
    let options_ =  {
          title: title 
        , html: html_
        , width: width
        // , height: height
        , top: "20px"
        , left: "50px" 
        , zIndex: "1000"
    };
    let pwindow = new PopupWindow(options_);
    // pwindow.addClass("popup-window-iframe");
    pwindow.setHeight("90%");
    pwindow.onWindowClick( (className) => {
        if(className == "btn-popup-close"){ pwindow.close(); }
    });
    // let closeOnBlur = options.closeOnBlur || false;
    // if(closeOnBlur)
    // {  
    //     //console.log(" [TRACE] Install close on Blur");
    //     pwindow.onBlur((event) => pwindow.remove()); 
    // }
    if(!hidden){ pwindow.show(); }
    return pwindow;
}


async function copyContentToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    console.log('Success! content copied to clipboard');
    /* Resolved - text copied to clipboard successfully */
  } catch (err) {
    console.error('Failed to copy: ', err);
    /* Rejected - text failed to copy to the clipboard */
  }
}


/** Send an Http request to a Rest API */
async function httpRequest(method, url, body)
{
    function networkErrorHandler(err){
        console.warn("Network error ", err);
        let response = new Response(JSON.stringify({
               status: "error"
            ,  message: "Failed to reach server. A network error happenned."
        }));
        return response;
    }

    let headers =  {  'Content-Type':     'application/json'
                    , 'X-Requested-With': 'XMLHttpRequest'
                    // Defined in based.html template as 
                    //  const CSRF_TOKEN = "{{ csrf_token() }}";
                    , 'X-CSRFToken':       CSRF_TOKEN
                    };
    var payload  ={  "method": method
     , "headers": headers
    };
    if(body !== null ){
        payload["body"] = JSON.stringify(body);
    }
    const res = await fetch(url, payload)
                            .catch(networkErrorHandler);
    let httpErrorCodes = {
          404: "404 - Not found"
        , 403: "403 - Forbidden (Autorization)"
        , 401: "401 - Unauthorized (Athentication)"
        , 405: "405 - Http Method POST Not Allowed"
        , 500: "500 - Internal Server Error"
    };
    if (!res.ok)
    {
        // console.log(" [TRACE] message = ", message);
        let result = {
              "status": "error"
            , "error": httpErrorCodes[res.status]
        }
        return result;
    }
    let result = await res.json();
    return result;

}

async function httpPutRequest(url, body)
{
    let result = await httpRequest("PUT", url, body);
    return result;
}

async function http_post(url, body) 
{
    let result = await httpRequest("POST", url, body);
    return result;
}


function linkify(inputText) 
{
    var replacedText, replacePattern1, replacePattern2, replacePattern3;

    //URLs starting with http://, https://, or ftp://
    replacePattern1 = /(\b(https?|ftp):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/gim;
    replacedText = inputText.replace(replacePattern1, 
    '<a href="$1" target="_blank" class="link-external" rel="noreferrer noopener nofollow">$1</a>');

    //URLs starting with "www." (without // before it, or it'd re-link the ones done above).
    replacePattern2 = /(^|[^\/])(www\.[\S]+(\b|$))/gim;
    replacedText = replacedText.replace(replacePattern2, 
    '$1<a href="http://$2" target="_blank" class="link-external" rel="noreferrer noopener nofollow">$2</a>');

    //Change email addresses to mailto:: links.
    replacePattern3 = /(([a-zA-Z0-9\-\_\.])+@[a-zA-Z\_]+?(\.[a-zA-Z]{2,6})+)/gim;
    replacedText = replacedText.replace(replacePattern3, '<a href="mailto:$1">$1</a>');

    return replacedText;
}

function linkfyDom(domElement)
{
    let html = linkify(domElement.innerHTML);
    domElement.innerHTML = html;
}

function redirect(url)
{
    document.location.href = url;
}

addEventListener("DOMContentLoaded", (ev) => {
        let entries = document.querySelectorAll(".search-item");
        for(let x of entries){ linkfyDom(x); }
});




function toggle_sidebar()
{
    /// console.log(" [TRACE] Toggle side bar");
    let sidebar = document.querySelector(".sidebar");
    sidebar.classList.toggle("sidebar-visibility");
    let main = document.querySelector(".main");
    main.classList.toggle("main-visiblity");
}

function toggleShortcutKeybindingWinodw()
{
    keybindDisplayWindow.toggle();
}

function onClick(anchor, handler)
{
    let dom = document.querySelector(".toc");
    if (!dom){ 
        console.warn(`DOM element ${anchor} not found.`);
        return; 
    }
    dom.addEventListener("click", handler);
}

var tooltip_window = null;
var quickOpenWindow = null;
var keybindDisplayWindow = null;

var changeLanguageForm = null;


function displayPageSourceWindow()
{
    // let html = document.querySelector("#template-page-source").innerHTML;
    // let html = base64ToUtf8(PageSource);
    let srcWindow= new PopupWindow({
          title: `Source:`
        , html:   `<iframe class="iframe-preview" 
                           sandbox="allow-scripts allow-same-origin allow-forms allow-top-navigation-by-user-activation"
                           src="${PAGE_SOURCE_URL}"
                           width="100%" 
                           height="100%" 
                           ></iframe> `
        , width:  "95%"
        , height: "98%"
        , top: "0px"
        , left: "0px" 
    });


    let dom = srcWindow.childElementByClass("iframe-page-source");
    // dom.srcdoc = html;
    srcWindow.setHeight("90%");
    srcWindow.show();
}



function isMobileScreen()
{
    let screenType = getComputedStyle(document.body).getPropertyValue("--screen-type");
    let isMobile = screenType === "mobile";
    return isMobile;
}

function printPage()
{
  if( isMobileScreen() ){
    // Open document in new table in printing mode
    let url = document.location.href.replace("#", "") + "?print=true";
    window.open(url, "_blank");
  } else {
    // print current wiki page
    window.print();
  }
}


var timerId = -1;

function lazyLoadImages()
{
    // console.log(" [TRACE] Enter function lazyLoadImages(). ");
    let imgs = document.querySelectorAll(".lazy-load");
    let videos = document.querySelectorAll(".lazy-load-video");
    let formulas = document.querySelectorAll(".lazy-load-latex");

    if( imgs.length === 0 && videos.length === 0 && formulas.length === 0)
    {
        clearInterval(timerId);
        // console.log(' [TRACE] Shutdown image lazy loader');
        return;
    }


    for(let x of imgs )
    {

        if( isElementInViewport(x) &&  x.parentElement.style.display !== "none")
        {
            // console.log(`[TRACE] loading image ${x.dataset.src}`);
            x.src = x.dataset.src;
            x.classList.remove("lazy-load");
        }
    }

    for(let v of videos)
    {
        if( isElementInViewport(v) && v.parentElement.style.display !== "none")
        {
            let src = v.dataset.src;
            let videoType = v.dataset.type;
            let video = document.createElement("video");
            video.setAttribute("width", "80%");
            video.setAttribute("controls", "");
            video.setAttribute("src", src);
            video.setAttribute("type", videoType);
            v.appendChild(video);
            v.classList.remove("lazy-load-video");
        }
    }

    for(let f of formulas)
    {
      if(isElementInViewport(f) && f.parentElement.style.display !== "none")
      {
         renderDOMLatex(f);
         f.classList.remove("lazy-load-latex");
      }
    }
}


var user_data = null;

async function displayEditButtons()
{
    if(!IS_USER_ADMIN){ return; }
    // Make all edit  buttons (pencil icons) of wiki sections visible
    for(let q of document.querySelectorAll(".link-edit"))
    { q.style.display = ""; }
}

var equationPopupWindow = null;

document.addEventListener("DOMContentLoaded", async function()
{
     
    lazyLoadImages();
    // Call function every 500 ms
    timerId = setInterval(lazyLoadImages, 500);

    // NOTE the cosntant variable FONT_FAMILY_MAIN is defined in the template base.html
    document.documentElement.style.setProperty('--font-family-main', FONT_FAMILY_MAIN);
    // set code font (typeface). NOte: this constant is defined in the file base.html
    document.documentElement.style.setProperty('--font-family-code', FONT_FAMILY_CODE);
    // Set font of document headings (title) 
    document.documentElement.style.setProperty('--font-family-title', FONT_FAMILY_TITLE);

    displayEditButtons();


    let cardsets = document.querySelectorAll(".div-flashcard");
    var id = 0;
    for(let x of cardsets)
    {
      
       flashcardObjects[id] = new FlashCard(x);
       x.dataset.id = id;
       x.addEventListener("click", cardHandler);
       id = id + 1;
    }
  

    // Event bubbling
    onClick(".toc", (evt) => {
        if(isMobileScreen() && evt.target.className == "link-sidebar")
        { 
            toggle_sidebar();
        } 
    });

    // onClick("#btn-scroll-top", () => scrollToTop());
    /// document.querySelector("#btn-scroll-top")
    ///     .addEventListener("click", scrollToTop);

    /// document.querySelector("#btn-scroll-bottom")
    ///     .addEventListener("click", scrollToBottom);

    let last = null;
    onClick(".toc", (event) => {
        let tg = event.target;
        if(tg.className !== "link-sidebar"){ return; }
        if(last != null){  last.classList.remove("link-sidebar-clicked"); }
        tg.classList.add("link-sidebar-clicked");
        last = tg;
    });

    let tooltipWindowTitle = geti18nTranslation("abbreviation-window-title");
    tooltip_window = popupMessage(tooltipWindowTitle, ""
                                  , {hidden: true, height: "100px", zIndex: "2000"});
    // English Label: "Quick Open Wiki Page"
    let windowTitle = geti18nTranslation("quick-open-window-title");
    // English Label: "Open"
    let openButtonLabel = geti18nTranslation("quick-open-page-open-button");
    quickOpenWindow = new PopupWindow({
           title: windowTitle
        ,  titleI18nTag: "quick-open-window-title"
        ,  height: "100px"
        ,  html: `
        <input type="search" id="prompt-open-page" name="select-page"
              list="quick-pagelist" >
        <datalist id="quick-pagelist"></datalist>
        <button class="primary-button" data-i18n="quick-open-page-open-button" onclick="openWikiPageCallback();">${openButtonLabel}</button>
        `
    });
    // console.log(" [TRACE] quickOpenWindow = ", quickOpenWindow);

    changeLanguageForm = new PopupWindow({
       title: "Change the User Interface Language"
    ,  titleI18nTag: "popup-window-change-language"
    ,  html: `
        <p data-i18n="popup-window-change-language-label1">Set the user interface language.</p>
        <fieldset>
            <select id="select-user-locale" name="user_locale">
                <option selected="" value="en-US">en-US - American English</option>
                <option value="pt-BR">pt-BR - Português Brasileiro (Brazilian Portuguese) </option>
            </select>
        </fieldset>
        <fieldset>
            <button data-i18n="popup-window-change-language-change-button"
                    id="btn-change-ui-language" class="primary-button">Change</button>
            <button  data-i18n="popup-window-change-language-close-button"
                     id="btn-close-ui-language" class="primary-button" onclick="changeLanguageForm.toggle();">Close</button>
        </fieldset>
        <p data-i18n="popup-window-change-language-label2">
        This form allows overriding the current UI - User Interface language.
        </p>
    `
    });

    equationPopupWindow = new PopupWindow({
         title:        ""
       , titleI18nTag: "popup-window-equation-display"
       , html: `
            <div class="equation-view">
            <div>
          `
       , width: "500px"
       , height: "95px"
    });

    let localeEntry = document.querySelector("#select-user-locale");
    let locale = getCurrentLocale();
    localeEntry.value = locale;

    let btnSetLanguage = document.querySelector("#btn-change-ui-language");
    btnSetLanguage.addEventListener("click", function(event){
        let item = localeEntry.item(localeEntry.selectedIndex);
        let locale = item.value;
        setLocaleI18n(locale);
        // Persist user locale
        localStorageSet(KEY_USER_LOCALE, locale);
    });

    keybindDisplayWindow = new PopupWindow({
          title: "Keybindings"
        , height: "300px"
        , html: `
            <table>
                <tr>
                    <th>Shortcut</th>
                    <th>Description</th>
                </tr>
            
                <tr>
                    <td>?</td>
                    <td>Toggle keybind (shortcut) helper window.  </td>
                </tr>
                 <tr>
                    <td>?</td>
                    <td>Type ? Question mark again to close this window.</td>
                </tr>               
                <tr>
                    <td>Ctrl /</td>
                    <td>Jump to search form.</td>
                </tr>
                <tr>
                    <td>Ctrl e</td>
                    <td>Toggle for quick jumpo to Wiki page.</td>
                </tr>
                <tr>
                    <td>Ctrl 1</td>
                    <td>Go to Index page '/' URL</td>
                </tr>
                <tr>
                    <td>Ctrl 2</td>
                    <td>Go to /pages - list of all Wiki pages.</td>
                </tr>
                <tr>
                    <td>Ctrl 3</td>
                    <td>Go to /tags - list of all tags.</td>
                </tr>
                <tr>
                    <td>Ctrl 5</td>
                    <td>Toggle headings of current Wiki page.</td>
                </tr>
                <tr>
                    <td>Ctrl 9</td>
                    <td>Toggle display all links of current wiki page.</td>
                </tr>
    

            </table>
        `
    });

    let inputQuickOpen = document.querySelector("#prompt-open-page");
    inputQuickOpen.addEventListener("keydown", openWikiPageCallbackKeyDown);


    let btnCreateNote = document.querySelector("#btn-create-note");
    if( btnCreateNote )
    {
        // New Note
        let title = geti18nTranslation("new-note-popup-window-title");
        // Name
        let label = geti18nTranslation("new-note-popup-window-label");
        // Enter the name of the note be created.
        let instruction = geti18nTranslation("new-note-popup-window-instruction");
		    btnCreateNote.addEventListener("click", () => {
            popupInput(
                  title
                , instruction
                , label
                , (noteName) => {
                    let url =  `/create/${noteName}`;
                    document.location.href = url;
		            });
	    });
    }

    // Translate user interface I18N
    doTranslationI18N();

    // Force Desktop CSS layout if the page was loaded with the URL
    // parameter ?printer=true	
    let params = new URLSearchParams(window.location.search);
    if( params.get("print") === "true" )
    {
       document.body.classList.add("force-desktop");
       renderDOMLatex(document.body);
       window.print();
    } else {
      if( isMobileScreen() ) { setHeadingsVisibility(false); }
      _visibilityFlag =  !isMobileScreen();
    }
    // setHeadingsVisibility(false);

});


var pageList = [];

async function quickOpenPage()
{
    let pages = await httpRequest("GET", "/api/wiki");
    // console.log(" [TRCCE] pages = ", pages);
    let datalist = document.querySelector("#quick-pagelist");
    datalist.replaceChildren();
    pageListt = [];
    for(let p of pages)
    {
        let option = document.createElement("option");
        option.value = p;
        pageList.push(p);
        datalist.appendChild(option);
    }
    quickOpenWindow.toggle();
}

function openWikiPageCallback()
{
    let input = document.querySelector("#prompt-open-page");
    let selectedPage = input.value;
    input.value = "";
    quickOpenWindow.close();
    if( pageList.find(x => x === selectedPage) )
    {
        let page = selectedPage.replaceAll(" ", "_");
        redirect(`/wiki/${page}`);
    } else {
        redirect(`/pages?search=` + encodeURI(selectedPage))
    }
}


function openWikiPageCallbackKeyDown(event)
{
    //console.log(" [TRACE] openWikipageCallbackKeyDown called. ");
    if(event.key !== "Enter"){ return; }
    openWikiPageCallback();
}

function isElementInViewport (el) {

    // Special bonus for those using jQuery
    if (typeof jQuery === "function" && el instanceof jQuery) {
        el = el[0];
    }

    var rect = el.getBoundingClientRect();

    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) && /* or $(window).height() */
        rect.right <= (window.innerWidth || document.documentElement.clientWidth) /* or $(window).width() */
    );
}



var refcard_window = null;


function showRefcard()
{
    if( !refcard_window)
    {
        // Lazy Initialization
        refcard_window =  popupIframe( "Reference Card"
                                     , "/wiki/special:refcard"
                                     , { width: "90%" } );
        refcard_window.setHeight("90%");
    }
    refcard_window.show();
}


var lastToolTipTarget = "";

document.addEventListener("mouseover", (event) => {
    let target = event.target;

    if(target.tagName === "ABBR")
    {
        lastToolTipTarget = "ABBR";
        // Lazy Initialization
        if( tooltip_window == null )
        {
            // English title "Abrreviation"
            let title = geti18nTranslation("abbreviation-window-title");
            tooltip_window = popupMessage(title, ""
                                      , {hidden: true, height: "100px", zIndex: "2000"});
        }
        let title = geti18nTranslation("abbreviation-window-title");
        let tooltip = `${target.innerText}: ${target.title}`; 
        tooltip_window.setTitle(title);
        tooltip_window.setMessage(tooltip);
        tooltip_window.show();
    } else {
        if(tooltip_window != null && lastToolTipTarget === "ABBR")
        {
            tooltip_window.close();
        }
    }
    
    if( target.classList.contains("citation-link") )
    {
      let key = target.dataset.citekey;
      let html = REFERENCES[key];
      tooltip_window.setTitle("");
      tooltip_window.setMessage(html);
      tooltip_window.show();
      // console.log(" [TRACE] Render html = ", html);
      return;  
    }

    // Hyperlink to equation 
    // NOTE: It is only supported for KaTeX. 
    if( target.classList.contains("eqref") )
    {
       let div = document.querySelector(".equation-view");
       // katex.render(target.dataset.equation, div, { throwOnError: false });
       katexRenderDOMLatexFormula(div, target.dataset.equation, true);
       equationPopupWindow.show();
       let title = geti18nTranslation("popup-window-equation-display-title") || "Equation";
       // console.log(` [TRACE] Title = ${title}`);
       equationPopupWindow.setTitle(`${title} ${target.innerText}`);
    } else {
        // equationPopupWindow.close();
    }



});


_menus = new Set();

const REFERENCES = (() => {
  var data = {}; 
  try{
      inner = base64ToUtf8(CITATION_REFERENCES);
      //console.trace(" inner = ", inner);
      data = JSON.parse(inner);
      // console.trace(" data = ", data);
  } catch(error){
  }
  return data; 
})();

document.addEventListener("click", (event) => {
    let target = event.target; 

    if(target.classList.contains("btn-copy-button"))
    {
      let code = target.parentElement
                       .parentElement
                       .parentElement
                       .childNodes[1].textContent.trim();
      // Display copied message
      let copiedLabel = target.parentElement.parentElement.childNodes[0];
      copiedLabel.classList.toggle("hidden");
      // Hide the copied label again after 1 second
      setTimeout(() => copiedLabel.classList.toggle("hidden"), 1000);
      copyContentToClipboard(code);
      return;
    }

    
    if(target.tagName === "ABBR")
    {
         let tooltip = `${target.innerText}: ${target.title}`;
         let title = geti18nTranslation("abbreviation-window-title");
         tooltip_window.setTitle(title);
         tooltip_window.setMessage(tooltip);
         tooltip_window.show();
         return;
    }

    if(target.classList[0] === "myst-note-role")
    {
        let term = target.innerText;
        let note = target.dataset.note;
        // English title: "Note"
        let title = geti18nTranslation("popup-window-note-myst-role-title") || "Note";
        tooltip_window.setTitle(title)
        tooltip_window.setMessage(note);
        tooltip_window.show();
    }

    if(target.classList[0] === "footnote-reference")
    {
        lastToolTipTarget = "footnote-reference";
        let note = htmlUnescape(target.dataset.footnote);
        let counter = target.dataset.counter;
        // English title: "Note"
        var title = geti18nTranslation("popup-window-footnote-title") || "Footnote";
        title = title + " " + counter;
        tooltip_window.setTitle(title)
        tooltip_window.setMessage(note);
        tooltip_window.show();
        let dom = tooltip_window.childElementByClass("popup-message-text");
        renderDOMLatex(dom);
        return;
    }

    if(target.classList[0] === "btn-show-alt-text")
    {
       let title = "Alt text";
       let text = target.previousElementSibling.alt;
       tooltip_window.setTitle(title);
       tooltip_window.setMessage(text);
       tooltip_window.show();
       return;
    }
    
    // Toggle zoom images (expand to 100% width) when they are clicked
    if(target.classList[0] == "wiki-image")
    {
        // console.log(' [TRACE] toggle css class wiki-image-full');
        event.target.classList.toggle("wiki-image-full");
    }

    if(target.classList[0] === "button-toggle-menu" || target.classList[0] === "header-icon" )
    {
        var dom = null;
        if( event.target.tagName === "IMG" )
        {
            dom = event.target.parentElement.parentElement.querySelector(".menu-dropdown-content");
            console.trace("Image clicked");
        } else {
            dom = event.target.parentElement.querySelector(".menu-dropdown-content");
        }
        // Show menu 
        dom.classList.toggle("menu-hidden");
        _menus.add(dom);
    } else {
        for(let x of _menus)
        {
            // Hide menu
            x.classList.add("menu-hidden")
        } 
    }

    if(target.tagName == "H2" && target.parentElement.classList[0] == "div-heading")
    {
        // Fold all other headings 
        setHeadingsVisibility(false);
        // Iterate over the siblings
        // The purpose of .nextElementSibling is to skip
        // the next DOM node, an horizontal line below the heading
        var sibling = target.parentElement.nextElementSibling;
        while(true)
        {
            sibling = sibling.nextElementSibling;
            if(sibling == null || (sibling.className === "div-heading"  
                                    /* && sibling.children[0].tagName == "H2" */ ))
            { break; }
            // Alternate viisibility
            // when the display CSS property is set to none,
            // the DOM node becomes non visible. 
            let display =  sibling.style.display === "none" ? "" : "none";
            sibling.style.display = display; 
        }
        // Click on link programatically in order to set focus
        // on this heading
        let link = target.parentElement.querySelector("a");
        link.click();
        lazyLoadImages();
    }
    if(target.tagName == "H3" && target.parentElement.classList[0] == "div-heading")
    {
        // Fold all other headings
        setHeadingsVisibility(false);
        // Iterate over the siblings
        // The purpose of .nextElementSibling is to skip
        // the next DOM node, an horizontal line below the heading
        var sibling = target.parentElement;
        while(true)
        {
            sibling = sibling.nextElementSibling;
            if(sibling == null || sibling.className === "div-heading" )
                                    
            { break; }
            // Alternate viisibility
            // when the display CSS property is set to none,
            // the DOM node becomes non visible. 
            let display =  sibling.style.display === "none" ? "" : "none";
            sibling.style.display = display; 
        }
        // Click on link programatically in order to set focus
        // on this heading
        let link = target.parentElement.querySelector("a");
        link.click();
        lazyLoadImages();
    }

  tooltip_window.close();

  if(equationPopupWindow){
     equationPopupWindow.close();
  }   
});



function scrollToTop()
{
    /// console.log(" [TRACE] I was called.");
    let domMain = document.querySelector(".main");
    domMain.scrollTo({top: 0});
}

function scrollToBottom()
{
    /// console.log(" [TRACE] I was called.");
    let domMain = document.querySelector(".main");
    // domMain.scrollTo({top: 0});
    domMain.scrollTop = domMain.scrollHeight;
}

function deletePage(pagename)
{
    const deletePageFormTitle = geti18nTranslation("delete-page-form-title");
    const deleteFormQuestion = geti18nTranslation("delete-page-form-question");
    const deleteFormWarning = geti18nTranslation("delete-page-form-warning");
    let message =  (  `${deleteFormQuestion}: "${pagename}"?`
                    + deleteFormWarning );
    popupYesNo(deletePageFormTitle, message, async () => {
           let resp = await httpRequest("DELETE", `/api/wiki/${pagename}`);
           if (resp.status === "error"){
               popupMessage("Error", resp.error); 
               return;
           } 
           // Refresh/Reload current page
           document.location.reload();
       });   
}

function generateUUID() { // Public Domain/MIT
    var d = new Date().getTime();//Timestamp
    var d2 = ((typeof performance !== 'undefined') && performance.now && (performance.now()*1000)) || 0;//Time in microseconds since page-load or 0 if unsupported
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16;//random number between 0 and 16
        if(d > 0){//Use timestamp until depleted
            r = (d + r)%16 | 0;
            d = Math.floor(d/16);
        } else {//Use microseconds since page-load if supported
            r = (d2 + r)%16 | 0;
            d2 = Math.floor(d2/16);
        }
        return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
}


function btnClickHandler(event) {
    // let dom = document.querySelector("#myDropdown");
    let dom = event.target.parentElement.querySelector(".menu-dropdown-content");
    dom.classList.toggle("menu-hidden");
}

function menuClicked(event) {
    let target = event.target;
    /// console.log(" [TRACE] target = ", event.target);
    // let parent = event.target.parentElement;
        // console.log(" [TRACE] parent = ", parent);
    /** 
     *  CSS Class 
     * 
     * .show {
     *     visibility: visible;
     * }
     *------------------------------------------*/
    parent.classList.toggle("show");

    let href = target.href.split("#")[1];
    // console.log(" [TRACE] target.href = ", href);

    // if( href === "home" )
    // {  
    //    alert("Button Home was clicked");
    // } else if( href === "about" )
    // {
    //    alert("Button About was clicked");   
    // }

}

function clearFormEntries(formID)
{
    let form = document.querySelector(formID);
    if(!form){ return; }
    let entries = form.querySelectorAll("input");
    for(let q of entries)
    {
        if(q.type == "search" || q.type == "text")
        {
            q.value = "";
        }
    }
}

var _visibilityFlag = true; 

function toggleHeadings()
{

    _visibilityFlag = !_visibilityFlag;
    setHeadingsVisibility(_visibilityFlag);
}




function setHeadingsVisibility(visibility)
{
    let nodes_ =  document.querySelectorAll(".div-heading");
    let nodesh2 = Array.from(nodes_)
        .filter(n => n.children[0].tagName == "H2");
    let nodesh3 = Array.from(nodes_)
        .filter(n => n.children[0].tagName == "H3");

    for(let n of nodesh2)
    {
        // Iterate over the siblings
        // The purpose of .nextElementSibling is to skip
        // the next DOM node, an horizontal line below the heading
        var sibling = n.nextElementSibling;
        while(true)
        {
            sibling = sibling.nextElementSibling;
            if(sibling == null || (sibling.className === "div-heading"  
                                    && sibling.children[0].tagName == "H2" ))
            { break; }
            // Alternate viisibility
            // when the display CSS property is set to none,
            // the DOM node becomes non visible. 
            //// let display =  sibling.style.display === "none" ? "" : "none";
            //////let display =  _visiblityFlag && (sibling.className !== "div-heading") ? "" : "none";
            var display = "";
            if( visibility ){
                display = "";
            } else {
                if(sibling.className !== "div-heading"){ display = "none"; }
            }
            sibling.style.display = display; 
        }
    }
}

// document.addEventListener("click", (event) => {
//     let target = event.target; 
//     let className = target.classList[0];
//     if(className === "link-internal-missing")
//     {
//         event.preventDefault();
//         let noteName = target.innerText;
//         let message =  `The note/page "${noteName}" does not exist yet. Do you wish to create it?`;
//         popupYesNo("Create Note?", message, async () => {
//             let resp = await http_post(`/api/wiki/${noteName}`);
//             if (resp.status === "error"){
//                 popupMessage("Error", resp.error); 
//                 return;
//             } 
//             redirect(`/edit/${noteName}`);
//         });
//     }
// });

/** ----- Keyboard Shortcuts ------------------ **/

document.addEventListener("keydown", (event) => {

    // console.log(" [TRACE] Keydown Event = ", event);

    // Keybind: '?' toggle keybind/shortcut reminder Window
    if (event.key == "?")
    {
        if(event.target.tagName === "INPUT") { return; }
        let url = new  URL(document.URL); 
        // Skip wiki editor page 
        if( url.pathname.startsWith("/edit/") ){ return; }
        keybindDisplayWindow.toggle();
    }

    // Focus on search bar after user types Ctrl+/
    if (event.ctrlKey && event.key === "/") {
        /// console.log(" [TRACE] Ctrl + / pressed Ok. ");
        let sform = document.querySelector("#search-form")
        var dom = null;
        if (sform) {
            dom = sform.querySelector("#site-search-bar");
        } else {
            dom = document.querySelector("#site-search-bar");
        }
        dom.focus();
    }
    // Open window within current that allows quick switching
    // to a Wiki page by typing its title.
    if (event.ctrlKey && event.key === "e") {
        quickOp
        let dom = document.querySelector("#prompt-open-page");
        setTimeout(() => { dom.focus(); }, 500);

    }

    // Keybind Ctrl+2
    // Open Index page 
    if (event.ctrlKey && event.key === "1") {
        // Redirect browser to root URL 
        window.location.href = "/";
    }

    // Keybind: Ctrl+2
    // Open Search Page, containing a search form and 
    // listing all wiki pages
    if (event.ctrlKey && event.key === "2") {
        // Redirect browser to /pages URL
        window.location.href = "/pages";
    }

    // Keybind: Ctrl+3
    // Open Pages that allows navigating by tags 
    if (event.ctrlKey && event.key === "3") {
        // Redirect browser to /pages URL
        window.location.href = "/tags";
    }
    
    
    // Keybind: Ctrl+5
    // Toggle headings off current section 
    // NOTE: Headings are titles of sections or subsections.
    // This keybinding allows quick navigation in a given Wiki page.
    if (event.ctrlKey && event.key === "5") {
        toggleHeadings();
    }


    // Keybind: Ctrl+9
    // View all links (hyperlinks) URLs of current wiki page
    if (event.ctrlKey && event.key === "9") {
        let urlObj = new URL(document.URL);
        let paths =  urlObj.pathname.split('/')
        let pageType = paths[1];
        if(pageType !== "wiki" && pageType !== "links"){
            return;
        }
        let pageType_ =  pageType === "wiki" ? "links" : "wiki";
        let wikiPageName = paths[2];
        let url = `/${pageType_}/${wikiPageName}`;
        window.location.href = url;

    }


});



