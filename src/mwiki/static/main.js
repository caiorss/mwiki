class PopupWindow
{
    constructor(options)
    {
        let title = options.title || "";
        let html  = options.html  || "";
        this._html = html;
        this._dom = document.createElement("div");
        document.body.appendChild(this._dom);
        this._dom.classList.add("popup-window");
        this._dom.style.zIndex = "1000";
        this._dom.style.position = "absolute";
        this._dom.style.width  = "400px";
        this._dom.style.height = "500px";
        this._dom.style.top    = "10%";
        this._dom.style.left   = "30%";
        this._dom.style.background = "aliceblue";
        this._dom.style.padding = "10px";
        this.hide();
        let code = `<h2 class="window-title">${title}</h2> <button class="btn-window-close">[X]</button><hr>`;
        console.log(" [TRACE] code = ", code);
        this._dom.innerHTML = code;
        this._dom.innerHTML += html; 
        let self = this;
        this.onClick(".btn-window-close", () => self.close());
    }

    onWindowClick(handler)
    {
        this._dom.addEventListener("click", (event) => {
            let target = event.target;
            let className = target.className;
            handler(className);
        });
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
        this.remove();
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
        <p>${message}</p>
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

function popupMessage(title, message)
{
    let html_ = `
        <p>${message}</p>
        <button class="btn-popup-close">Close</buttom>
    `;
    let pwindow = new PopupWindow({
          title: title 
        , html: html_
    });
    pwindow.onWindowClick( (className) => {
        if(className == "btn-popup-close"){ pwindow.close(); }
    });
    pwindow.show();
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

document.addEventListener("DOMContentLoaded", function()
  {
    // Event bubbling
    onClick(".toc", (evt) => {
        let screenType = getComputedStyle(document.body).getPropertyValue("--screen-type");
        let isMobile = screenType === "mobile";
        if(isMobile && evt.target.className == "link-sidebar")
        { 
            toggle_sidebar();
        } 
    });

    // onClick("#btn-scroll-top", () => scrollToTop());
    document.querySelector("#btn-scroll-top")
        .addEventListener("click", scrollToTop);

    let last = null;
    onClick(".toc", (event) => {
        let tg = event.target;
        if(tg.className !== "link-sidebar"){ return; }
        if(last != null){  last.classList.remove("link-sidebar-clicked"); }
        tg.classList.add("link-sidebar-clicked");
        last = tg;
    });


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
          
});


function scrollToTop()
{
    console.log(" [TRACE] I was called.");
    let domMain = document.querySelector(".main");
    domMain.scrollTo({top: 0});
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
