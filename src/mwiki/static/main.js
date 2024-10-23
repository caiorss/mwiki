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

document.addEventListener("DOMContentLoaded", function()
  {
    let toc = document.querySelector(".toc");
    // Event bubbling
    toc.addEventListener("click", (evt) => {
        let screenType = getComputedStyle(document.body).getPropertyValue("--screen-type");
        let isMobile = screenType === "mobile";
        if(isMobile && evt.target.className == "link-sidebar")
        { 
            toggle_sidebar();
        } 
    });

    let last = null;
    toc.addEventListener("click", (event) => {
        let tg = event.target;
        if(tg.className !== "link-sidebar"){ return; }
        if(last != null){  last.classList.remove("link-sidebar-clicked"); }
        tg.classList.add("link-sidebar-clicked");
        last = tg;
    });

          
});


    