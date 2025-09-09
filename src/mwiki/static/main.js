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
        let windowI18NTitleTag = options.titleI18nTag || "";
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
        let code = `<h2 data-i18n="${windowI18NTitleTag}" class="window-title">${title}</h2> <button class="btn-window-close">[X]</button><hr>`;
        // console.log(" [TRACE] code = ", code);
        this._dom.innerHTML = code;
        this._dom.innerHTML += html; 
        let self = this;
        this.onClick(".btn-window-close", () => self.close());
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

// I18N Internationalization for the Website GUI - Graphics User Interface.
// It allows adding new localization without changing the UI code.
translationsi18n = 
{
    // NOTE: Actually, it is international English using US-English (American English)
    // spelling.
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
		, "menu-item-view-label":     "View"
		, "menu-item-edit-label":     "Edit"
		, "menu-item-new-label":      { "label": "New", "title": "Create new Wiki page" }
		, "tags-menu-item-label":     { "label": "Tags", "title": "Browse pages using tags." }
		, "menu-item-delete-label":   { "label": "Delete", "title": "Delete this wiki page" }
		, "menu-item-source-label":   { "label": "Source", "title": "Display source code of current wiki page." }
		, "links-menu-item-label":    { "label": "Links", "title": "Display all external and internal links of this wiki page." }
		, "login-button": 			  "LOGIN"
		, "username-label": 		  "User Name"
		, "username-placeholder": 	  "Enter your username"
        , "password-label": 		  "Password"
        , "password-placeholder":     "Enter your password"
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
		, "settings-update-button": "Update"
		, "settings-sitename-label": "Website Name"
		, "settings-website-description-label": "Website Description"
		, "settings-public-checkbox-label": "Public"
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
		, "settings-public-checkbox-description": "If enabled, everybody including non logged in users will be able to view the wiki content. Note that only logged in users can edit the wiki." 
		, "settings-default-locale-label":               "Default Locale"
		, "settings-use-default-locale-checkbox-label":  "Use default locale/language"
		, "settings-use-default-locale-description": "Always use the default locale (language) regardless of the user preferred language provided by the web browser."
		, "about-page-title":          "About"
		, "edit-page-title":           "Editing"
		, "edit-page-toolbar-title":   "Toolbar"
		, "edit-page-h3-insert-label": "Insert"
		, "edit-page-h3-actions-label": "Actions"
		, "edit-page-document-status-label": "Document not saved yet"
		, "edit-page-back-button": {  "label": "Back"
									, "title": "Switch to document view mode and exit editing mode."}

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
        , "upload-form-window-title": "File Upload"
        , "upload-form-file-link-label": "Link Label"
        , "upload-form-choose-file-label": "Choose a file"
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
        , "foldable-math-example-block-label":    "Example"
        , "admonition-math-defintion-label":      "DEFINITION"
        , "admonition-math-theorem-label":        "THEOREM"
        , "admonition-math-example-label":        "Example"
        , "abbreviation-window-title":            "Abbreviation"
        , "links-page-title":                     "Links of"
        , "links-page-strong-label":              "Page"
        , "links-page-internal-links-h2":         "Internal Links"
        , "links-page-external-links-h2":         "External Links"
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
		, "menu-item-view-label":     "Ver"
		, "menu-item-edit-label":     "Editar"
		, "menu-item-new-label":      { "label": "Nova", "title": "Criar nova página Wiki" }
		, "tags-menu-item-label":     { "label": "Tags", "title": "Navegar pelas páginas usando tags." }
		, "menu-item-delete-label":   { "label": "Deletar", "title":  "Excluir esta página wiki"}
		, "menu-item-source-label":   { "label": "Fonte", "title": "Exibir código-fonte da página wiki atual." }
		, "links-menu-item-label":    { "label": "Links", "title": "Exibir todos os links externos e internos desta página wiki." }
		, "login-button": 			  "LOGAR"
		, "username-label":			  "Nome de Usuário"
		, "username-placeholder":     "Entre com o nome de usuário"
        , "password-label": 	      "Senha"
        , "password-placeholder":     "Entre com a senha"
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
		, "settings-update-button": "Atualizar"
		, "settings-sitename-label": "Nome do Website"
		, "settings-website-description-label": "Descrição do Website"
		, "settings-public-checkbox-label": "Público"
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
		, "settings-use-default-locale-checkbox-label":  "Usar idioma/locale padrão"
		, "settings-use-default-locale-description": 	 "Sempre usar o idioma padrão (default locale), independentemente do idioma preferido do usuário fornecido pelo navegador da web."
		, "about-page-title":          "Sobre"
		, "edit-page-title":           "Editando"
		, "edit-page-toolbar-title":   "Barra de Ferramentas"
		, "edit-page-h3-insert-label": "Inserir"
		, "edit-page-h3-actions-label": "Ações"
		, "edit-page-document-status-label": "Document não salvo ainda."
		, "edit-page-back-button": {  "label": "Voltar"
									, "title": "Switch to document view mode and exit editing mode."}

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
		, "edit-page-upload-button": {   "label": "Link para Arquivo Subido"
									   , "title": "Sobe arquivo (faz upload) e insire link para ele na posição atual do cursor no editor."
									 }
		, "edit-page-insert-latex-equation": "Equação LateX"
		, "edit-page-insert-latex-non-numbered-button": "Equação LaTeX não numerada."
		, "edit-page-insert-theorem-button": "Teorema"
		, "edit-page-insert-details-button": "Detalhes"
		, "edit-page-clipboard-h3-label": "Opções da Área de Transferência"
		, "edit-page-p-clipobard": "Selecione o modo de colar da área de transferência"
        , "upload-form-window-title": "Subir Arquivo (Upload)"
        , "upload-form-file-link-label": "Rótulo do link."
        , "upload-form-choose-file-label": "Escolha um arquivo."
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
        , "foldable-math-example-block-label":    "Exemplo"
        , "admonition-math-defintion-label":      "DEFINIÇÃO"
        , "admonition-math-theorem-label":        "TEOREMA"
        , "admonition-math-example-label":        "Exemplo"
        , "abbreviation-window-title":            "Abreviação"
        , "links-page-title":                     "Links de"
        , "links-page-strong-label":              "Página"
        , "links-page-internal-links-h2":         "Links Internos"
        , "links-page-external-links-h2":         "Links Externos"
	}

};


function setLocaleI18n(locale)
{
	let translations = translationsi18n[locale];
	if( !translations )
	{
		console.error(`Locale ${locale} not found in the i18n translation database.`);
		return;
	}
	let oldLocale = localStorage.getItem("locale");
	if(oldLocale !== locale )
	{
		localStorage.setItem("locale", locale);
		// if(oldLocale){ location.reload(); }
	}
	
	let elements = document.querySelectorAll("[data-i18n]");
	for(let elem of elements)
	{
		let tag = elem.getAttribute("data-i18n");
		let value_ = translations[tag];
		if( !value_){ continue; }
		let value = value_.label || value_;
		// console.log(`tag = ${tag} ; value = "${value}" ; elem = `, elem);
		if( value_.title )
		{
			if( elem.title.includes("[i18n]") )
			{
				elem.title = elem.title.replace("[i18n]", value_.title);
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
		if( elem.textContent.includes("[i18n]") )
		{
			elem.textContent = elem.textContent.replace("[i18n]", value);
		} else {
			elem.textContent = value;
		}
	}
	
}


function doTranslationI18N()
{
	// var locale = localStorage.getItem("locale");
	if( USE_DEFAULT_LOCALE ){
		// alert("Use default locale");
		setLocaleI18n(DEFAULT_LOCALE);
		return;
	} 
	// Attempt to get locale from navigator
	var userLocale = navigator.language;
	// Set all English locales to en-US (US English) as this 
	// is the only English locale available
	if( userLocale.startsWith("en-") ){
		userLocale = "en-US";
	} 
	// Set all portuguese locales to pt-BR (Brazilian Portuguese)
	if( userLocale.startsWith("pt-") ){
		userLocale = "pt-BR";
	}
	if( translationsi18n[userLocale] ){
		setLocaleI18n(userLocale); 
	} else {
		setLocaleI18n(DEFAULT_LOCALE);
	}
}

function geti18nTranslation(key)
{
	var userLocale = navigator.language;
	// Set all English locales to en-US (US English) as this
	// is the only English locale available
	if( userLocale.startsWith("en-") ){
		userLocale = "en-US";
	}
	// Set all portuguese locales to pt-BR (Brazilian Portuguese)
	if( userLocale.startsWith("pt-") ){
		userLocale = "pt-BR";
	}
	if( USE_DEFAULT_LOCALE ){
		// alert("Use default locale");
		userLocale = DEFAULT_LOCALE;
	}
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

function isMobileScreen()
{
    let screenType = getComputedStyle(document.body).getPropertyValue("--screen-type");
    let isMobile = screenType === "mobile";
    return isMobile;
}


var timerId = -1;

function lazyLoadImages()
{
    // console.log(" [TRACE] Enter function lazyLoadImages(). ");
    let imgs = document.querySelectorAll(".lazy-load");
    let videos = document.querySelectorAll(".lazy-load-video");

    if( imgs.length === 0 && videos.length === 0)
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
}


var user_data = null;

async function displayEditButtons()
{
    let data = await httpRequest("GET", "/api/auth", null);
    user_data = data;
    if( data.show_buttons )
    {
        /// console.log(" [TRACE] show buttons ok. ");
        // Make all edit  buttons (pencil icons) of wiki sections visible
        for(let q of document.querySelectorAll(".link-edit"))
        { q.style.display = ""; }
    }
}


document.addEventListener("DOMContentLoaded", async function()
  {
    
    doTranslationI18N();
    
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
	}
	
    if( isMobileScreen() ) { setHeadingsVisibility(false); }
    _visibilityFlag =  !isMobileScreen();
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
        if(tooltip_window != null){ tooltip_window.close(); }
    }



});


_menus = new Set();

document.addEventListener("click", (event) => {
    let target = event.target; 

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
        quickOpenPage();

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
