class PopupWindow
{
    constructor(options)
    {
        let title = options.title || "";
        let html  = options.html  || "";
        let width = options.width || "500px";
        let height = options.height || "400px";
        let top = options.top || "10%";
        let left = options.left || "30%";
        let zIndex = options.zIndex || "1000";
        let visible = options.visible || false;
        this._html = html;
        this._dom = document.createElement("div");
        document.body.appendChild(this._dom);
        this._dom.classList.add("popup-window");
        this._dom.style.zIndex = zIndex;
        this._dom.style.position = "absolute";
        this._dom.style.width  = width;
        this._dom.style.height = height;
        this._dom.style.top    = top;
        this._dom.style.left   = left;
        this._dom.style.background = "aliceblue";
        this._dom.style.padding = "10px";
        if(!visible){ this.hide() };
        let code = `<h2 class="window-title">${title}</h2> <button class="btn-window-close">[X]</button><hr>`;
        console.log(" [TRACE] code = ", code);
        this._dom.innerHTML = code;
        this._dom.innerHTML += html; 
        let self = this;
        this.onClick(".btn-window-close", () => self.close());
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
        x.textContent = message;
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

function popupYesNo(title, message, handler)
{
    let html_ = `
        <p>${message}</p>
        <button class="btn-yes">Yes</button>
        <button class="btn-no">No</button>
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
    let html_ = `
        <p class="popup-message-text">${message}</p>
        <label>${label}</label><input type="text" class="popup-input" required="required" />
        <br><br>
        <button class="btn-yes">Yes</button>
        <button class="btn-no">No</button>
    `;
    let pwindow = new PopupWindow({
          title:  title
        , html: html_
    });
    pwindow.onWindowClick( (className) => {
        let entry = pwindow.value(".popup-input"); 
        if(className == "btn-yes" && entry)
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
    let width = (options.hidden || "80%");
    let height = (options.hidden || "90%");
    let html_ = `
        <iframe src="${url}" title="${title}" width="100%" height="100%" ></iframe> 
    `;
    let pwindow = new PopupWindow({
          title: title 
        , html: html_
        , width: width
        , height: height
        , top: "20px"
        , left: "50px" 
    });
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
                   // , 'X-CSRFToken': crfs_token
                    };
    const res = await fetch(url, { "method": method
                                    , "headers": headers 
                                    , body: JSON.stringify(body) })
                            .catch(networkErrorHandler)
                            ;
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
    console.log(" [TRACE] Toggle side bar");
    let sidebar = document.querySelector(".sidebar");
    sidebar.classList.toggle("sidebar-visibility");
    let main = document.querySelector(".main");
    main.classList.toggle("main-visiblity");
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

function isMobileScreen()
{
    let screenType = getComputedStyle(document.body).getPropertyValue("--screen-type");
    let isMobile = screenType === "mobile";
    return isMobile;
}

document.addEventListener("DOMContentLoaded", function()
  {
    // Event bubbling
    onClick(".toc", (evt) => {
        if(isMobileScreen() && evt.target.className == "link-sidebar")
        { 
            toggle_sidebar();
        } 
    });

    // onClick("#btn-scroll-top", () => scrollToTop());
    document.querySelector("#btn-scroll-top")
        .addEventListener("click", scrollToTop);

    document.querySelector("#btn-scroll-bottom")
        .addEventListener("click", scrollToBottom);

    let last = null;
    onClick(".toc", (event) => {
        let tg = event.target;
        if(tg.className !== "link-sidebar"){ return; }
        if(last != null){  last.classList.remove("link-sidebar-clicked"); }
        tg.classList.add("link-sidebar-clicked");
        last = tg;
    });

    tooltip_window = popupMessage("Abbreviation", "" 
                                  , {hidden: true, height: "100px", zIndex: "2000"});

    let btnCreateNote = document.querySelector("#btn-create-note");
    btnCreateNote.addEventListener("click", () => {
        popupInput(
                  "New Note"
                , "Enter the name of the note be created."
                , "Name"
                , async (noteName) => {
                    let resp = await http_post(`/api/wiki/${noteName}`);
                    if (resp.status === "error"){
                        popupMessage("Error", resp.error); 
                        return;
                    } 
                    redirect(`/edit/${noteName}`);
                });
    });

    if( isMobileScreen() ) { setHeadingsVisibility(false); }
    _visibilityFlag =  !isMobileScreen();
    // setHeadingsVisibility(false);
          
});

var refcard_window = null;

function showRefcard()
{
    if( !refcard_window)
    {
        // Lazy Initialization
        refcard_window =  popupIframe( "Reference Card"
                                     , "/wiki/special:refcard"
                                     , { width: "100%", height: null} );
    }
    refcard_window.show();
}


document.addEventListener("mouseover", (event) => {
    let target = event.target;


    if(target.tagName === "ABBR")
    {
        // Lazy Initialization
        if( tooltip_window == null )
        {
            tooltip_window = popupMessage("Abbreviation", "" 
                                      , {hidden: true, height: "100px", zIndex: "2000"});
        }
        let tooltip = `${target.innerText}: ${target.title}`; 
        tooltip_window.setMessage(tooltip);
        tooltip_window.show();
    } else {
        if(tooltip_window != null){ tooltip_window.close(); }
    }

});


_menus = new Set();

document.addEventListener("click", (event) => {
    let target = event.target; 
    // if(target.tagName === "ABBR")
    // {

    //     event.preventDefault();
    //     let tooltip = `${target.innerText}: ${target.title}`; 
    //     tooltip_window.setMessage(tooltip);
    //     tooltip_window.show();
    //     // popupMessage("Abbreviation", tooltip, { closeOnBlur: true });
    // } else {
    //     tooltip_window.close();
    // }
    if(target.classList[0] == "button-toggle-menu")
    {
        let dom = event.target.parentElement.querySelector(".menu-dropdown-content");
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
    }


});



function scrollToTop()
{
    console.log(" [TRACE] I was called.");
    let domMain = document.querySelector(".main");
    domMain.scrollTo({top: 0});
}

function scrollToBottom()
{
    console.log(" [TRACE] I was called.");
    let domMain = document.querySelector(".main");
    // domMain.scrollTo({top: 0});
    domMain.scrollTop = domMain.scrollHeight;
}

function deletePage(pagename)
{
    let message =  (  `Are you sure you really want to delete the page: "${pagename}"?` 
                    + "WARNING: This action cannot be reversed." );
    popupYesNo("Delete page?", message, async () => {
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
    console.log(" [TRACE] target = ", event.target);
    let parent = event.target.parentElement;
    console.log(" [TRACE] parent = ", parent);
    /** 
     *  CSS Class 
     * 
     * .show {
     *     visibility: visible;
     * }
     *------------------------------------------*/
    parent.classList.toggle("show");

    let href = target.href.split("#")[1];
    console.log(" [TRACE] target.href = ", href);

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
