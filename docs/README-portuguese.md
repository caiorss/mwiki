# MWiki - Wiki impulsionada por Markdown

## Visão Geral

O MWiki é um **motor wiki** *(wiki engine)* e um software de aplicação web para anotações, voltado para matemática e pesquisa, projetado para comunicação científica e técnica. Este software de motor wiki possui uma linguagem de marcação leve e rica em semântica, baseada em MyST Markdown, Obsidian Markdown e na linguagem de marcação do motor Media Wiki.

Este aplicativo Python é suportado pelo framework web Python Flask e pelo parser extensível Markdown-it usado pelo MyST Markdown e pelo projeto Jupyter Book.

Aplicações:
+ Documentação
+ Redação Técnica/Científica, especialmente nas áreas STEM (Ciências, Tecnologia, Engenharia e Matemática).
+ Base de Conhecimento Pessoal
+ Preservação do Conhecimento e da Informação


**Registro de Mudanças (Changelog):**

+ [./docs/changelog.md](./docs/changelog.md)


**NOTAS:**

+ Observação: Este software ainda está **em progresso** e em estágio inicial. No entanto, ele já pode ser usado como um aplicativo de anotações pessoais.
+ Observação: o Mediawiki é o software de motor wiki usado pela Wikipédia.


### Destaques de Funcionalidades

#### Funcionalidades Wiki

+ Wiki baseado em arquivo: todas as páginas Wiki são armazenadas como arquivos Markdown, como o motor wiki Moin Moin e o Dokuwiki. No entanto, ele usa um banco de dados de arquivos SQLite ou qualquer banco de dados completo para fins de gerenciamento do sistema.
+ Suporta MyST Markdown, GFM (Github-Flavored Markdown Support), subconjunto da sintaxe Obsidian Markdown, subconjunto da linguagem de marcação Mediawiki e HTML embutido.
+ Páginas escritas em linguagem de marcação baseada em Markdown em vez de HTML, o que permite que qualquer pessoa não programadora escreva documentos científicos e técnicos que são renderizados em HTML.
+ Botões para editar seções específicas do documento, semelhantes aos botões de edição de seções do Mediawiki.
+ Upload de arquivo. Agora, o editor de código wiki possui um botão para inserir um hiperlink para um arquivo carregado. Ao clicar no botão, uma janela pop-up para upload é exibida. Assim que o usuário envia o arquivo, a janela é fechada e um link para o arquivo é inserido no editor.
+ Páginas embutiveis. O conteúdo de uma página wiki pode ser incorporado em outra página wiki usando a sintaxe `![[Nome da página Wiki a ser incorporada]]`
+ Visualização do documento - permite que os usuários visualizem como o texto em markdown de uma página wiki ficará quando renderizado antes de salvá-lo. O botão de pré-visualização do editor também permite visualizar a aparência de um código markdown selecionado de uma página wiki quando renderizado.
+ Dependências JavaScript de terceiros para uso offline. Por exemplo, o MWiki possui MathJax, pseudocode-JS e Ace9 embutidos *(vendored)* no código-fonte para uso offline, mesmo quando não há CDN disponível devido à falta de conectividade com a internet ou se o Wiki for usado em um ambiente restrito protegido por firewall.

#### Controle de acesso

+ O Wiki possui os seguintes tipos de usuários: *admin*, que pode editar as páginas do Wiki; *guest* (visitante), um usuário registrado que pode visualizar páginas mesmo que o Wiki não seja público, mas um usuário convidado não pode editar nenhuma página; e usuários *anonymous* (anônimos - usuários não logados/autenticados) que só podem visualizar páginas se a caixa de seleção **público** nas configurações do Wiki (páginas '/settings') estiver habilitada.

+ Configurações do wiki público/privado - se a caixa de seleção **público** na página de configurações do MWiki estiver desabilitada, apenas usuários logados poderão visualizar as páginas do wiki e usuários não logados serão redirecionados para a tela de autenticação. Se esta caixa de seleção estiver habilitada, usuários não logados poderão visualizar o wiki. Observe que: somente usuários do tipo administrador podem editar as páginas do wiki e fazer alterações em qualquer conteúdo.

#### Funcionalidades do Editor de Texto

+ **Editor de código** Markdown desenvolvido sobre o editor de código JavaScript Ace9.
+ *Conversor de área de transferência para Markdown*, que permite converter conteúdo HTML copiado de qualquer outra página da web (também conhecida como site) para Markdown do MWiki. Este recurso é semelhante à cópia e colagem de texto não simples do Obsidian.
+ Carregue imagens colando-as da área de transferência.
+ Uso: Copie qualquer imagem clicando com o botão direito do mouse e cole-a na sessão do editor de texto de alguma página wiki usando o mouse ou pressionando Ctrl + V.
+ NOTA: Os recursos da área de transferência dependem da API HTML5 do Clibpboard, disponível apenas em [contextos seguros](https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts). Portanto, colar imagens da área de transferência para o editor de texto wiki só funciona se o wiki for servido em um host local ou em um domínio com https (HTTP + TLS), o que pode exigir um proxy reverso, como Caddy ou NGinx, para criptografia TLS/SSL e autenticação do servidor.
+ [VIM](<https://en.wikipedia.org/wiki/Vim_(text_editor)>) Atalhos de Tecla do Editor: O editor Wiki usa atalhos de tecla do VIM por padrão.

Veja também:

+ *VIM dot/ponto ORG* - Official Website
  + https://www.vim.org
+ *Vim (text editor)*
  + https://en.wikipedia.org/wiki/Vim_(text_editor)
+ *A Great Vim Cheat Sheet*
  + https://vimsheet.com/
+ *Vim Cheat Sheet*
  + https://vim.rtorr.com
+ *Vim Key Bindings – Vim Keys List Reference*
  + https://www.freecodecamp.org/news/vim-key-bindings-reference/
+ *vi Complete Key Binding List*
  + https://hea-www.harvard.edu/~fine/Tech/vi.html


  #### Linguagem de Markup(Marcação/Formatação) da MWiki

+ Formatação de texto:
+ Texto em itálico
+ Texto em negrito
+ Texto tachado (também conhecido como texto excluído)
+ Texto colorido
+ Abreviação, que corresponde à tag HTML5 `<abbr>`.
+ Texto sobrescrito
+ Texto subscrito
+ Blocos de código com destaque de sintaxe
+ Tabelas
+ Lista
+ Lista com marcadores
+ Listas ordenadas
+ Listas de definições
+ Comunicação científica e técnica
+ Fórmula LaTeX embutida (com tecnologia MathJaX)
+ Fórmula LaTeX embutida (modo de exibição) com enumeração automática
+ Blocos de código especiais para adicionar macros LaTeX personalizadas
+ Bloco de código em pseudocódigo
+ Advertência (também conhecida como caixa de chamada - *admonition*) para definição matemática
+ Advertência para teorema matemático
+ Advertência para exemplos de exercícios resolvidos
+ Seção dobrável para solução de exercícios resolvidos
+ Seção dobrável para provas de teoremas, usada em advertências de teoremas (*theorem admonition*).
+ Advertências
+ Advertência de Dica
+ Advertência de Nota
+ Advertência de Informação
+ Advertência de Aviso
+ Advertência Dobrável

Veja documentação detalhada e exemplos em:

+ [Linguagem de Marcação](./README-Markup-Language.md)


## Atalhos de Teclado (Atalhos de Tecla)

+ NOTA: Não é necessário lembrar dessas combinações de teclas, pois há um botão de menu no menu **[Main]** (principal em inglês), que permite abrir a janela auxiliar de combinações de teclas (atalho) exibindo todas as atalhose de teclados.
+ NOTA: Disponível desde de a versão v0.3.1

| Atalho | Descrição |
| --------- | ------------------------------------------------ |
| ? | Alterna a janela auxiliar de atalhos de teclado. |
| ? | Digite ? Ponto de interrogação novamente para fechar esta janela. |
| Ctrl / | Ir para o formulário de pesquisa. |
| Ctrl e | Alterna para um salto rápido para a página Wiki. |
| Ctrl 1 | Ir para a página de índice '/' URL |
| Ctrl 2 | Ir para /pages - lista de todas as páginas Wiki. |
| Ctrl 3 | Ir para /tags - lista de todas as tags. |
| Ctrl 5 | Alterna os títulos da página Wiki atual. |
| Ctrl 9 | Alterna a exibição de todos os links da página Wiki atual. |


## Demonstração

### Animações GIF

NOTA: Embora as animações GIF estejam desatualizadas devido às principais mudanças no layout e na interface do usuário, as funcionalidades apresentadas permanecem as mesmas.


**Animação GIF mostrando usdo do MWiki**

![](images/mwiki-animation-usage1.gif)

**Copiando e colando imagens**

![](images/mwiki-animation-usage2.gif)

**Recurso de visualização do Markdown**

+ O botão de visualização do editor permite visualizar a aparência de uma página wiki antes de salvá-la. O recurso de visualização também permite visualizar a aparência de um texto Markdown selecionado antes de salvá-lo.

![](images/wiki-markdown-preview.gif)


### Capturas de Tela (Screenshot)

**Captura de Tela 1 do Wiki**

Esta página do Wiki, cujo URL relativo é /wiki/Linear%20Algebra%20New, é gerada pelo processamento do arquivo 'Linear Algebra New.md'.

![](images/screen1.png)

**Captura de Tela 2 do Wiki**

![](images/screen2.png)

**Captura de Tela 3 do Wiki**

![](images/screen3.png)

**Captura de Tela 4 do Wiki**

Editor de código MWiki com tecnologia Javascript Ace9.

![](images/screen4.png)

**Captura de Tela 5 do Wiki**

Página de configurações do MWiki.

![](images/screen5.png)

**Captura de Tela 6 do Wiki**

Captura de tela do menu principal *(main menu)*.

![](images/screen6.png)

**Captura de tela 7 do Wiki**

Captura de tela do menu de página *(page menu)*.

![](images/screen7.png)

**Captura de tela 8 do Wiki**

É possível ocultar todos os títulos do Wiki para uma navegação rápida em dispositivos móveis ou desktop clicando no botão "(F)" na barra de navegação superior.

![](images/screen8.png)

**Captura de tela 9 do Wiki**

![](images/screen9.png)

**Captura de tela 10 do Wiki**

O Wiki possui um mecanismo de busca integrado que permite a busca por palavras-chave em todos os arquivos Markdown usados ​​para renderizar as páginas do Wiki.

![](images/screen10.png)

**Captura de Tela 11 do Wiki - Cartão de Referência**

Este wiki fornece uma janela pop-up de cartão de referência que fornece exemplos da linguagem de marcação MWiki (markdown personalizado).

(1) O cartão de referência pode ser aberto clicando no botão 'Reference Card' na barra de ferramentas do editor.

![](images/refcard1.png)

(2) Cartão de referência com todas as seções dobradas.

![](images/refcard2.png)

(3) Cartão de referência com uma seção desdobrada.

![](images/refcard3.png)


## Instalação

### Instalação usando o gerenciador de pacotes UV (1)

[UV](https://github.com/astral-sh/uv) é um gerenciador de pacotes para Python extremamente rápido e recente, que pode até instalar várias versões específicas do interpretador Python sem interromper a instalação do Python usada pelo sistema. O UV também pode instalar ferramentas Python em ambientes isolados sem quebrar a instalação atual do Python.

**PASSO 1**

Instalar versão instável *(Unstable Release)*.

```sh
$ uv tool install git+https://github.com/caiorss/mwiki
... ... ... ... ... ... ... ..
Instalou 2 executáveis: mwiki, mwiki-convert
```

Instalar a versão estável mais recente: versão v0.4

```sh
$ uv tool install https://github.com/caiorss/mwiki/archive/refs/tags/v0.4.zip
```

Instalar a versão estável mais recente (usando o hash do commit que não tem como ser mudado após o commit ser publico): versão v0.4


```sh
$ uv tool install https://github.com/caiorss/mwiki/archive/a7d898080f8549d82fd8eb2766822cefeb776e1e.zip
``` 

Instalar a versão estável mais recente: versão v0.3.1

```sh
$ uv tool install https://github.com/caiorss/mwiki/archive/refs/tags/v0.3.1.zip

## ou

$ uv tool install https://github.com/caiorss/mwiki/archive/3f4d38a8bc103dee8f89230c6b0a9eefb3083766.zip
```


Instalar a versão estável mais recente: versão v0.2

```sh
$ uv tool install https://github.com/caiorss/mwiki/archive/refs/tags/v0.2.zip

## OU 

$ uv tool install https://github.com/caiorss/mwiki/archive/1a3388679af0a6abaec83f6a88415b617e580c83.zip
```

Instalar a versão de lançamento v0.1

```sh
$ uv tool install https://github.com/caiorss/mwiki/archive/refs/tags/v0.1.zip
```


**PASSO 2** Execute o arquivo/ficheiro executável mwiki:


```sh
$ mwiki 

Usage: mwiki [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  compile  Compile Latex Formulas of .md file or folder to SVG images.
  convert  Convert from org-mode markup to markdown
  manage   Manage MWiki settings, including accounts, passwords and etc.
  server   Run the mwiki server.
```

**Inspecionar Arquivos/Ficheiros Executáveis**

```sh
$ which mwiki
/home/username/.local/bin/mwiki

$ whereis mwiki
mwiki: /var/home/username/.local/bin/mwiki

$ file $(which mwiki)
/home/username/.local/bin/mwiki: symbolic link to /home/username/.local/share/uv/tools/mwiki/bin/mwiki

$ file $(readlink $(which mwiki))
/home/username/.local/share/uv/tools/mwiki/bin/mwiki: Python script, ASCII text executable
```

**Desinstalar**

```sh
$ uv tool uninstall mwiki 
Uninstalled 2 executables: mwiki, mwiki-convert
```

### Instalação usando o gerenciador de pacotes UV (2)

Este procedimento de instalação utiliza o gerenciador de pacotes UV para instalar a partir do código-fonte em vez da URL do GitHub.

**PASSO 1:** Clone o repositório.

```sh
$  git clone https://github.com/caiorss/mwiki 
```

Entre no diretório do código-fonte.

```sh
$ cd mwiki
```

**PASSO 2:** Instalar MWIKI usando UV.

```sh
$ uv tool install . 

Resolved 36 packages in 1.07s
Installed 36 packages in 119ms
 + blinker==1.9.0
 + cachelib==0.13.0
 + cffi==1.17.1
 + click==8.1.8
 + cryptography==45.0.4
 + flask==3.1.1
 + flask-session==0.8.0
 + flask-sqlalchemy==3.1.1
 + flask-wtf==1.2.2
 + frontmatter==3.0.8
 + greenlet==3.2.3
 + importlib-metadata==8.7.0
 + itsdangerous==2.2.0
 + jinja2==3.1.6
 + linkify-it-py==2.0.3
 + markdown-it-py==3.0.0
 + markupsafe==3.0.2
 + mdit-py-plugins==0.4.2
 + mdurl==0.1.2
 + msgspec==0.19.0
 + mwiki==0.1 
 + pillow==11.2.1
 + pycparser==2.22
 + pygments==2.19.2
 + python-dateutil==2.9.0.post0
 + pyyaml==5.1
 + six==1.17.0
 + sqlalchemy==2.0.41
 + tomli==2.2.1
 + typing-extensions==4.14.0
 + uc-micro-py==1.0.3
 + waitress==3.0.2
 + watchdog==6.0.0
 + werkzeug==3.1.3
 + wtforms==3.2.1
 + zipp==3.23.0
Installed 2 executables: mwiki, mwiki-convert

```

**Desinstalar**


```sh
$ uv tool uninstall mwiki 
Uninstalled 2 executables: mwiki, mwiki-convert
```


### Instalação usando o gerenciador de pacotes Pipx

**PASSO 1:** Presume-se que Pip e Python já estejam instalados.

```sh
$ pip install pipx 
```

**PASSO 2:** Instalar usando Pipx

Instale o Mwiki usando Pipx (o MWiki requer Python >= 3.9)


```sh
$ pipx install git+https://github.com/caiorss/mwiki 
  installed package mwiki 0.1, installed using Python 3.9.19
  These apps are now globally available
    - mwiki
    - mwiki-convert
    - mwiki_convert
done! ✨ 🌟 ✨

```

Instale o Mwiki usando o Pipx e uma versão diferente do Python. Este comando é útil se a versão padrão do Python no sistema atual for 3.8 ou uma versão não suportada.


```
$ pipx install --python=3.9 git+https://github.com/caiorss/mwiki 
```


### Instalação usando Docker

O Docker é a maneira mais confiável de instalar aplicativos Python, pois é reproduzível e ajuda a evitar o problema das dependências entre Python e Pip (também conhecido como "problema de execução na máquina").

**PASSO 1:** Clonar o repositório

```sh 
$ git clone https://github.com/caiorss/mwiki mwiki

# Enter source code directory
$ cd mwiki
```

**PASSO 2:** Crie a imagem do docker.

```sh
$ docker build --tag mwiki-server .
```

ou execute o Makefile (suportado apenas em sistemas do tipo Unix com GNU Make)

```sh
$ make docker 
```

**PASSO 3:** Execute a imagem do Docker do MWiki. A variável de ambiente $WIKIPATH é definida para qualquer diretório que contenha arquivos Markdown, incluindo os cofres Obsidian.

Crie um arquivo .env no diretório atual contendo a configuração inicial do MWiki passada como variáveis ​​de ambiente. (Opcional)

Arquivo: .env

```
MWIKI_ADMIN_PASSWORD=u2afb5ck69
MWIKI_SITENAME=WBook
WIKI_PUBLIC=
```

Execute o docker passando o arquivo de configuração .env.


```sh
$ docker run --rm -it  --privileged \
            --network=host --env-file=$PWD/.env \
            --volume="$WIKIPATH:/wiki" mwiki-server
 [TRACE] Admin user created OK
 [INFO] Enter the username: admin and password: 'SN81N87JZ6' to log in.
[2025-01-09 20:00:40 +0000] [1] [INFO] Starting gunicorn 23.0.0
[2025-01-09 20:00:40 +0000] [1] [INFO] Listening at: http://0.0.0.0:9090 (1)
[2025-01-09 20:00:40 +0000] [1] [INFO] Using worker: sync
[2025-01-09 20:00:40 +0000] [7] [INFO] Booting worker with pid: 7
[2025-01-09 20:00:40 +0000] [8] [INFO] Booting worker with pid: 8
[2025-01-09 20:00:40 +0000] [9] [INFO] Booting worker with pid: 9
[2025-01-09 20:00:40 +0000] [10] [INFO] Booting worker with pid: 10
[2025-01-09 20:00:40 +0000] [11] [INFO] Booting worker with pid: 11
[2025-01-09 20:00:40 +0000] [12] [INFO] Booting worker with pid: 12
[2025-01-09 20:00:40 +0000] [13] [INFO] Booting worker with pid: 13
[2025-01-09 20:00:40 +0000] [14] [INFO] Booting worker with pid: 14
[2025-01-09 20:00:40 +0000] [15] [INFO] Booting worker with pid: 15
 [TRACE] _username = admin ; _password = SN81N87JZ6
 [WARNING] Note implemented html rendering for foot_note_block =  SyntaxTreeNode(footnote_ref)
 [WARNING] Note implemented html rendering for foot_note_block =  SyntaxTreeNode(footnote_block)

```

Executar como um daemon (serviço em segundo plano desacoplado do terminal):


```sh
$ docker run --detach \
           --name=mwiki  \
           --network=host \
           --env-file=$PWD/.env \
           --privileged \
           --volume="$PWD/pages:/wiki" mwiki-server
a6f0838f5159ff75aa25228fafdbd2f4fe1432c3359a9dc5d3ec84b10d801577
 
```

Ver logs do contêiner mwiki:

```sh
$ docker logs -f mwiki
[2025-01-09 20:06:23 +0000] [1] [INFO] Starting gunicorn 23.0.0
[2025-01-09 20:06:23 +0000] [1] [INFO] Listening at: http://0.0.0.0:9090 (1)
[2025-01-09 20:06:23 +0000] [1] [INFO] Using worker: sync
[2025-01-09 20:06:23 +0000] [7] [INFO] Booting worker with pid: 7
[2025-01-09 20:06:23 +0000] [8] [INFO] Booting worker with pid: 8
[2025-01-09 20:06:23 +0000] [9] [INFO] Booting worker with pid: 9
[2025-01-09 20:06:23 +0000] [10] [INFO] Booting worker with pid: 10
[2025-01-09 20:06:23 +0000] [11] [INFO] Booting worker with pid: 11
[2025-01-09 20:06:23 +0000] [12] [INFO] Booting worker with pid: 12
[2025-01-09 20:06:23 +0000] [13] [INFO] Booting worker with pid: 13
[2025-01-09 20:06:23 +0000] [14] [INFO] Booting worker with pid: 14
[2025-01-09 20:06:24 +0000] [15] [INFO] Booting worker with pid: 15

```

Parar o contêiner MWiki:

```
$ docker stop mwiki 
mwiki
```

Iniciar contêiner MWiki


```sh
$ docker start mwiki 
```

Reinicie o software contêiner MWiki.


```sh
$ docker restart mwiki
```

Alterar o nome do site usando a CLI (Interface de Linha de Comando) integrada/nativa.

```sh
$ docker exec -it mwiki python -m mwiki  manage --sitename=WNotes
 [*] Site name changed to: WNotes
```

Alterar senha do administrador.

```sh
$ docker exec -it mwiki python -m mwiki  manage --admin-password=somePassNewPassword
```

**PASSO 5:**

Abra o MWiki no navegador web, na porta 8080, copiando e colando a URL http://localhost:8000 e digite "admin" no campo de nome de usuário e a senha inicial do administrador no campo de senha. A senha inicial do administrador foi fornecida na saída do comando anterior. A senha é "0JAJ6UAMUA", que é uma string gerada aleatoriamente e exclusiva para cada instalação do MWiki.

**PASSO 6:**

Abra a página de configurações http://localhost:8000/admin e altere as configurações do Wiki. Em seguida, acesse a URL http://localhost:8000/user e altere a senha do administrador. Observe que as senhas dos usuários nunca são armazenadas em texto simples, elas são sempre armazenadas em formato hash por motivos de segurança.


### Instalação via Docker-Compose ou Podman-Compose

**PASSO 1:** Clonar o repositório

```sh 
$ git clone https://github.com/caiorss/mwiki mwiki

# Enter source code directory
$ cd mwiki
```

Se o repositório já estiver clonado, é possível obter as últimas alterações executando

```sh
$ git pull
```

**PASSO 3:** Mude para uma versão estável

```sh
$ git checkout <<RELASE-VERSION>>

# Por exemplo

$ git checkout v0.31
```

**PASSO 3:** Edite o arquivo config.env.


Arquivo: config.env

```sh
# MWiki configuration files 
#----------------------------------#

MWIKI_SERVER_ADDR=mwiki 
MWIKI_SERVER_PORT=9090

# Path to wiki folder, where *.md markdown files, images and other 
# files will be stored.
MWIKI_PATH=./sample-wiki

# Password of main admin
MWIKI_ADMIN_PASSWORD=mypasswd

# Name of the Wiki (Name of the website)
MWIKI_SITENAME=MyNoteBook

# URL which the website is hosted or just domain name 
MWIKI_WEBSITE=localhost sbox.ts 

# Configure MWiki as a private Wiki. 
# => Only logged in users can view wiki pages. 
# MWIKI_PUBLIC=   

# Configure MWiki  as a public Wiki.
# => Anonymous users can view wiki pages, however only 
# admin users can edit.
MWIKI_PUBLIC=true

# Server static files using Caddy or NGinx 
MWIKI_X_ACCEL_REDIRECT=true

#----------------------------------------------------##
##      Less common Settings for certificate         ##
#----------------------------------------------------##
# They are not needed if the server is hosted in a machine
# with static and public IP address. Those settings are only
# required when hosting in internal networks (LANs).
#
MWIKI_INTERNAL_CA=
MWIKI_ACME_CA_URL=
```

**PASSO 4:** Execute docker-compose ou podman compose para por o sistem no ar (online).

por o sistem no ar (online) com docker-compose.

```sh
$ docker-compose --env-file=./config.env up -d 
```

Por o sistem no ar (online).

```sh
$ podman-compose --env-file=./config.env up -d 
```

**PASSO 5:** Certificados TLS/SSL

Se o MWiki estiver hospedado em uma máquina com endereço IP estático e público acessível de qualquer lugar na internet e o domínio MWiki apontar para esse endereço IP, o Caddy obterá automaticamente o certificado TLS/SSL da Autoridade Certificadora Let's Encrypt CA.

Se este aplicativo estiver hospedado em uma rede local ou VPN site a site, como tailscale, e não for possível usar a Autoridade Certificadora Let's Encrypt CA, o Caddy pode ser transformado em uma Autoridade Certificadora CA local editando o arquivo config.env e alterando


```
MWIKI_INTERNAL_CA=true
```

Esta etapa cria uma URL

+ `https://<mwiki-website-domain>/root.crt`

onde o usuário pode baixar o certificado da CA raiz e instalá-lo em navegadores da web ou celulares. Este certificado da CA raiz pode ser baixado usando o curl. Este procedimento é útil para auto-hospedar o MWiki em laboratórios domésticos.

```sh
$ curl -O -k --silent https://<mwiki-website-domain>/root.crt
```

Veja também:

+ *Set up Certificate Authorities (CAs) in Firefox (Configurar Autoridades de Certificação (ACs) no Firefox)*
  + https://support.mozilla.org/en-US/kb/setting-certificate-authorities-firefox
+ *Installing a Root Certificate Authority in Firefox (Instalando uma Autoridade de Certificação Raiz no Firefox)* 
  + https://chewett.co.uk/blog/854/installing-root-certificate-authority-firefox/
+ *How to Add a Certificate on Android? Step by Step (Como adicionar um certificado no Android? Passo a passo)*
  + https://www.airdroid.com/mdm/add-certificate-android/


## Pós-instalação 

### Acesse o MWiki na rede local

**PASSO 1:**

Obtenha o nome do host do computador onde o mDNS está instalado no Linux, MacOSX ou Windows executando o seguinte comando em um emulador de terminal. No Microsoft Windows, um emulador de terminal pode ser aberto digitando Windows-Key + R e digitando "cmd".


```sh
$ hostname 
```

e também obter o endereço IP do computador no Microsoft Windows para fins de diagnostico de problemas *(debugging)*.


```sh
$ ipconfig
```

no Linux, o endereço IP do servidor na rede local pode ser obtido executando.


```sh
# Versões mais antigas de distribuições Linux, BSD e MacOS
$ ifconfig

## Versões mais recentes de distribuições Linux.
$ ip addr
```

**PASSO 2:**

Se o servidor MWiki estiver instalado e em execução e for possível acessá-lo de qualquer computador na rede local com mDSN - Multicast DNS habilitado, abra uma das seguintes URLs em qualquer navegador da web a partir de qualquer dispositivo ou computador na rede local, incluindo smartphones ou tablets.

+ http://dummy.local:8080 se o MWiki estiver escutando na porta TCP 8080
+ http://dummy.local se o MWiki estiver escutando na porta 80 (porta HTTP TCP padrão)
+ http://192.168.0.106:8080 se o endereço IP do servidor obtido na etapa 1 for 192.168.0.106 e o MWiki estiver escutando na porta 8080
+ http://192.168.0.106 se o endereço IP do servidor obtido na etapa 1 for 192.168.0.106 e o MWiki estiver escutando na porta 80.

Observações:

1. Observe que *dummy* é o nome do host (nome da rede) do computador que executa o MWiki, obtido na etapa 1 com o comando `$hostname`.
2. Na maioria das redes corporativas, o tráfego de rede multicast é desabilitado por padrão, enquanto na maioria das redes domésticas, o tráfego de rede multicast, incluindo o DNS multicast, é habilitado por padrão.

O MWiki pode ser iniciado com o comando

```
$ mwiki server  --wsgi --port=9010 --wikipath=/home/user/path/to/wiki/repository
```

É recomendável executar o aplicativo usando servidores proxy reversos Caddy ou NGinx, pois eles fornecem criptografia TLS e melhor desempenho para servir arquivos estáticos e lidar com alto tráfego de rede.

### Abrir Portas de Firewall

**PASSO 3:**

Para acessar o MWiki ou qualquer outro servidor web de outros computadores ou dispositivos, pode ser necessário abrir portas TCP no firewall do sistema operacional.

Abra a porta 8080 no Microsoft Windows (requer a abertura de um terminal com privilégios de administrador).

```sh
$ netsh firewall add portopening TCP 8080 "MWIki server port"
```

Abra a porta 8080 no Linux com o Iptables (firewall padrão do Linux, todos os outros firewalls do Linux são wrappers do Iptables).

```sh
$ sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
```

Abra a porta 8080 no Linux com UFW (Uncomplicated Firewall), usado principalmente por distribuições Linux derivadas do Debian e do Ubuntu.

```sh
$ sudo ufw allow 8080/tcp
```

Abra a porta 8080 no Linux com firewalld.


```sh
$ sudo firewall-cmd --add-port=8080/tcp --permanent
$ sudo firewall-cmd --reload
```

### Encaminhamento de Porta SSH (SSH Port Forwarding)

O recurso para colar imagens da área de transferência requer um contexto seguro do navegador, que pode ser obtido executando o servidor MWiki usando um proxy reverso TLS (Transport Layer Security), como o Caddy, ou executando-o em um host local. Uma maneira alternativa de obter um [contexto seguro]((https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts)) sem precisar instalar o NGinx ou o Caddy é usar o encaminhamento de porta local SSH para redirecionar o tráfego de rede da porta TCP local para a porta TCP de uma máquina remota, qualquer computador com um servidor ssh instalado. Por exemplo, se o MWiki estiver executando uma máquina remota cujo nome de host é dummy.local (endereço IPv4 da rede local 192.168.0.115) e que escuta a porta TCP 9090, é possível redirecionar o tráfego de rede da porta local 8080 para a porta 9090 da máquina fictícia com o comando ssh


```sh
$ ssh  -o StrictHostKeyChecking=no  -v -f -N -L  8080:127.0.0.1:9090  myuser@dummy.local
```

ou

```sh
$ ssh  -o StrictHostKeyChecking=no  -v -f -N -L  8080:127.0.0.1:9090  myuser@dummy.local -p 2022
```

Onde:
+ `-v`
- Significa verboso para melhor diagnóstico de erros.
+ `-f` significa executar ssh em segundo plano sem bloquear o emulador de terminal atual.
+ `-N`
- Significa sessão não interativa apenas para encaminhamento de porta.
+ `-L 8080:127.0.0.1:9090`
- Encaminhamento de porta local da porta TCP 8080 da máquina atual para a porta 9090 da máquina remota.
+ `o StrictHostKeyChecking=no`
- O objetivo desta opção de linha de comando é ignorar a verificação estrita de host (opcional).
+ `-p 2022`
- Usar a porta ssh 2022 em vez da porta ssh padrão 222.

Após executar este comando, será possível acessar o servidor MWiki abrindo qualquer uma das seguintes URLs em qualquer navegador da web, incluindo Firefox, Safari, Microsoft Edge e etc.

+ http://localhost:8080

ou

+ http://127.0.0.1:8080

A vantagem dessa abordagem é permitir o acesso ao servidor Wiki mesmo que ele não esteja exposto à internet e todas as portas TCP estejam bloqueadas por qualquer aplicativo de firewall. Este procedimento também é útil para fornecer [contexto seguro](https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts), o que permite o uso das APIs da área de transferência [*(clipboard)*](https://developer.mozilla.org/en-US/docs/Web/API/Clipboard_API) dos navegadores da web sem lidar com certificados TLS (Transport Layer Security - PT: Camada de Segurança de Transportes), anteriormente SSL (Secure Socket Layer). Observe que o tráfego de rede entre a máquina remota e a máquina local é criptografado por SSH. Vale mencionar também que um cliente SSH integrado está disponível no Microsoft Windows 10 e no Microsoft Windows 11.

Observe que o nome do host SSH myuser@dummy.local também pode ser:

1. Nome de domínio, por exemplo, my-dummy-machine.net, se este domínio hipotético apontar para o endereço IPv4 público da máquina fictícia.
2. Nome de domínio mDNS (Multi-cast DNS). Exemplo: dummy.local se o nome do host da máquina for fictício e a rede local permitir DNS multicast. A maioria das redes domésticas permite DNS multicast, porém ele está desabilitado na maioria das redes corporativas.
3. Nome de domínio DNS mágico da VPN Tailscale (Site-to-Site).
4. Endereço IPv4 externo, por exemplo, 172.168.115.125 se o MWiki estiver sendo executado em qualquer máquina com endereço IPv4 público (fixo/estático), geralmente uma máquina virtual VPS (Virtual Private Server) em nuvem. Todos os VPS (Virtual Private Server), máquinas virtuais em nuvem, fornecidos pelo Google Cloud, AWS, Digital Ocean e outros provedores de nuvem, têm endereço IPv4 público acessível de qualquer lugar do mundo.
5. Ipv4 interno para acesso na rede local, por exemplo 192.168.0.115


### Leitura adicional


**Configurações de Firewalll**

+ *Open TCP Port 80 in Windows Firewall Using Netsh* 
  + https://www.wiki.mcneel.com/zoo/homenetsh
+ *Linux Open Port 80 (HTTP Web Server Port)*, Vivek Gite (2022), Cyberciti
  + https://www.cyberciti.biz/faq/linux-iptables-firewall-open-port-80/
+ *5 ways to open a port in Linux explained with examples*, Arun Kumar (2023), FOSS Linux
  + https://www.fosslinux.com/111811/5-ways-to-open-a-port-in-linux-explained-with-examples.htm
+ *Linux .local domain*
  + https://en.wikipedia.org/wiki/.local
+ *Linux Open Port: Step-by-Step Guide to Managing Firewall Ports*, Vijaykrishna Ram and Anish Singh Walia, Digital Ocean
  + https://www.digitalocean.com/community/tutorials/opening-a-port-on-linux


**mDNS - Multicast DNS and Network Discovery - Zeroconf/Bonjour**

+ *Using mDNS aliases within your home network*, Andrew Dupont (2022)
  + https://andrewdupont.net/2022/01/27/using-mdns-aliases-within-your-home-network/
+ *How to set up mDNS on an ESP32*
  + https://lastminuteengineers.com/esp32-mdns-tutorial/
+ *mDNS, hostname.local, and WSL2*, Nelsons' log
  + https://nelsonslog.wordpress.com/2022/01/06/mdns-hostname-local-and-wsl2/
+ *Multicast DNS (MDNS) on Home Networks*
  + https://stevessmarthomeguide.com/multicast-dns/
+ *Pros and Cons of Using Multicast DNS*, Networking Interview
  + https://networkinterview.com/pros-and-cons-of-using-multicast-dns/
+ *Android silently picks up long-awaited mDNS feature*, Anroid Policy
  + https://www.androidpolice.com/android-mdns-local-hostname/
+ *Use network service discovery*, Android Developers
  + https://developer.android.com/develop/connectivity/wifi/use-nsd
+ *Multicast Application Protocol mDNS for Local Discovery*, Expressif (ESP32) Docs
  + https://espressif.github.io/esp32-c3-book-en/chapter_8/8.2/8.2.4.html#multicast-application-protocol-mdns-for-local-discovery
+ *Avahi (software)*, Wikipedia
  + https://en.wikipedia.org/wiki/Avahi_%28software%29
  + Brief: *Avahi is a free zero-configuration networking (zeroconf) implementation, including a system for multicast DNS and DNS Service Discovery. It is licensed under the GNU Lesser General Public License (LGPL). Avahi is a system that enables programs to publish and discover services and hosts running on a local network. For example, a user can plug a computer into a network and have Avahi automatically advertise the network services running on its machine, facilitating user access to those services.* (Wikipedia)
+ *Avahi*, ArchLinux Wiki
  + https://wiki.archlinux.org/title/Avahi
  + Brief: *Avahi is a free Zero-configuration networking (zeroconf) implementation, including a system for multicast DNS/DNS-SD service discovery. It allows programs to publish and discover services and hosts running on a local network with no specific configuration. For example you can plug into a network and instantly find printers to print to, files to look at and people to talk to. It is licensed under the GNU Lesser General Public License (LGPL).* (ArchLinux Wiki)
+ *How to Properly Disable Avahi-Daemon*, Ashish Khadka (2024), Baeldung
  + https://www.baeldung.com/linux/avahi-daemon-disable
+ *Network service discovery with an Avahi container*, Radu Zaharia (2022)
  + https://blog.raduzaharia.com/network-service-discovery-with-an-avahi-container-3dfdce4f1c75
+ *Avahi - Daemon - WebOS Internals*
  + https://www.webos-internals.org/wiki/Avahi
+ *Unveiling Linux Avahi: A Comprehensive Guide*, LinuxVox (2025)
  + https://linuxvox.com/blog/linux-avahi/



**SSH - Secure Shell Server**

+ *Tutorial: SSH in Windows Terminal*, Microsoft MSFT
  + https://learn.microsoft.com/en-us/windows/terminal/tutorials/ssh
+ *Get started with OpenSSH for Windows*, Microsoft MSFT
  +  https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse?tabs=gui&pivots=windows-server-2025
+ *How to Enable and Use Windows 10's New Built-in SSH Commands*, Chris Hoffman (2017), How-To-Geek
  + https://www.howtogeek.com/336775/how-to-enable-and-use-windows-10s-built-in-ssh-commands/
+ *How to Enable SSH in Windows 10: A Step-by-Step Guide for Beginners*, Matt Jacobs (2024), SupportYourTech
  + https://www.supportyourtech.com/articles/how-to-enable-ssh-in-windows-10-a-step-by-step-guide-for-beginners/
+ *How to Set up SSH Tunneling (Port Forwarding)*, Linuxise (2020)
  + https://linuxize.com/post/how-to-setup-ssh-tunneling/
+ *SSH Port Forwarding (SSH Tunneling) Explained*, Vladmir Kaplarevic (2024)
  + https://phoenixnap.com/kb/ssh-port-forwarding
+ *A Visual Guide to SSH Tunnels: Local and Remote Port Forwarding*, Ixmiuz (2022)
  + https://iximiuz.com/en/posts/ssh-tunnels/
+ *Tunneling and Port Forwarding*, SSH Handbook
  + https://www.sshhandbook.com/overview-of-ssh-tunneling/



## Software e ferramentas complementares 

O seguinte conjunto de softwares ou aplicativos complementares são recomendados para o MWiki, pois podem fornecer recursos adicionais e melhorar o uso.

**Motores de Busca (Buscadores)**

+ https://noai.duckduckgo.com 
  + Motor de busca *(search engine)* sem resumo de IA falso e enganoso.

**Ferramentas Online**

+ *QuickLatex* 
  + https://www.quicklatex.com 
  + Esta ferramenta online permite visualizar e renderizar rapidamente expressões matemáticas LaTeX sem precisar instalar nada.
+ *Table Generator for Markdown, LaTeX and MediaWiki*
  + https://www.tablesgenerator.com
+ *Detexify*
  + https://detexify.kirelabs.org/classify.html
  + *Mostra código LaTeX para escrever símbolo matemático desenhado manualmente seja com o mouse/cursor ou com o dedo em navegadoes de dispositivos móveis.*
+ *LaTeX Equation Editor*  
  + https://editor.codecogs.com
+ *Mathcha.io*
+ https://www.mathcha.io
+ *Ferramenta online para desenho de ilustrações científicas/técnicas, que suporta símbolos LaTeX e possui vários blocos de construção para desenhar diagramas ou esquemas geométricos, elétricos, mecânicos e de ciência da computação.
+ *Plurimath - Converte entre múltiplas linguagens de representação matemática*
  + https://www.plurimath.org/
+ *How to write algorithm in Latex (Como escrever algoritmos em LaTeX)*
  + https://shantoroy.com/latex/how-to-write-algorithm-in-latex
+ *LaTeX/Algorithms - Wikibooks*
  + https://en.wikibooks.org/wiki/LaTeX/Algorithms

**Complementos/extensões do Navegadores Web**

+ *LibreWolf* - Fork (versão modificada) do navegador Firefox
    + https://librewolf.net/
    + *Navegador Firefox modificado e reforçado para maior segurança, privacidade e proteção contra rastreamento.*
+ *Obsidian Web Clipper* (Addon do Firefox)* \[MELHOR\]
    + https://addons.mozilla.org/en-US/firefox/addon/web-clipper-obsidian
    + Extensão que permite aos usuários salvar páginas da web em formato markdown ou transformar partes selecionadas da página em markdown. Esta ferramenta pode ser usada com o MWiki para extrair informações de páginas da web, já que a linguagem de marcação MWiki é compatível com o markdown Obsidian.
+ *Web Archive* - Busca por versões mais antigas do URL atual do Win Web Archiver, archive.is e outros sites.
    + https://addons.mozilla.org/en-US/firefox/addon/view-page-archive/
    + *Visualize versões arquivadas e em cache de páginas da web em vários mecanismos de busca, como Wayback Machine e Archive․is.*
+ *Permitir Clique com o Botão Direito - Reative o clique com o botão direito em sites que o sobrescrevem* (Firefox)
    + https://addons.mozilla.org/en-US/firefox/addon/re-enable-right-click/
    + *A extensão "Permitir Clique com o Botão Direito" modifica alguns métodos do JavaScript para habilitar o menu de contexto original do botão direito quando uma página da web bloqueia intencionalmente o clique com o botão direito em seu conteúdo. A maioria dos navegadores modernos permite que o JavaScript desabilite o menu de contexto padrão quando uma página da web fornece seu próprio menu de contexto personalizado para seu conteúdo (como no Google Docs). No entanto, esse recurso também pode permitir que proprietários de sites desabilitem o menu de contexto do botão direito sem fornecer nenhuma funcionalidade útil. A extensão adiciona um botão à área da barra de ferramentas do navegador do usuário. Clicar no ícone da extensão injeta um pequeno script na página atual para remover o bloqueio do menu de contexto. É importante observar que a extensão não injeta nenhum código por padrão em nenhuma página da web; ela só o faz mediante ação do usuário. Os usuários podem clicar no botão da extensão para liberar a restrição quando um site bloqueia o menu de contexto do botão direito sem oferecer um menu de contexto personalizado.* (Sem Script, Desativar JS, NOTA: Traduzido da descrição original em inglês.) 
+ *Script Blocker Ultimate*  
    + https://addons.mozilla.org/en-US/firefox/addon/script-blocker-ultimate/
    + *Extensão para alternar a execução de Javascript, que permite desativar e ativar JavaScript.*
+ *NoScript* 
    + https://noscript.net/
    + *Browser extension that blocks scripts by default.*
    + *Extensão do navegador que bloqueia scripts por padrão.*
+ *Árvore de Tabs para Firefox* (melhor navegação em muitas tabs)
    + https://addons.mozilla.org/en-US/firefox/addon/tree-style-tab



**Tradução e Conversão de Texto em Fala**

+ *Speech Note - Flathub* \[Aplicativo Flatpak Linux\] (Tradutor "G00gl3" Offline)
    + https://flathub.org/apps/net.mkiol.SpeechNote
    + Resumo: *O Speech Note permite que você faça, leia e traduza notas em vários idiomas. Ele utiliza Conversão de Texto em Fala, Conversão de Texto em Fala e Tradução Automática para isso. O processamento de texto e voz ocorre totalmente offline, localmente no seu computador, sem usar uma conexão de rede. Sua privacidade é sempre respeitada. Nenhum dado é enviado para a internet.*
    + NOTA: Requer uso de GPU, o software tem melhor performance/desempenho com GPUs da NVIDIA com CUDA.
    + AVISO: Ferramentas de tradução automatizada de texto baseiam-se na probabilidade de palavras, assim como os tão badalados LLM (Modelos de Grandes Linguagens). Como resultado, elas podem não ser capazes de traduzir com precisão gírias, jargões, ditados populares e nuances linguísticas. Além disso, elas têm maior probabilidade de falhar em idiomas distantes das línguas europeias e do inglês. Também vale a pena notar que algumas variedades linguísticas ou dialetos, como o dialeto alemão da Baviera, podem existir principalmente na forma falada e, infelizmente, não existir em quantidade significativa na forma escrita, o que dificulta a tradução das informações por ferramentas automatizadas.




**Ferramentas de Captura de Tela**

Observação: Essas ferramentas permitem tirar capturas de tela de uma parte selecionada da tela e colá-las no aplicativo de destino ou no editor MWiki pressionando Ctrl + v.

- *Spetacle* \[MELHOR\]
    + https://apps.kde.org/spectacle/
    + *Ferramenta do KDE Plasma para tirar capturas de tela. Também permite selecionar áreas retangulares da tela e adicionar textos e anotações. Este aplicativo está disponível em qualquer distribuição Linux com ambiente de trabalho KDE Plasma.*
- *Flameshot*
    + https://flameshot.org
    + *Ferramenta de captura de tela multiplataforma disponível para Microsoft Windows, distribuições Linux e MacOSX da Apple.*
- *Flameshot - Flatpak*
    + https://flathub.org/apps/org.flameshot.Flameshot
- *KSnip - Flathub* (Aplicativo Flatpak KDE/QT)
    + https://flathub.org/apps/org.ksnip.ksnip
    + *Ksnip é uma ferramenta de captura de tela multiplataforma baseada em Qt que oferece diversos recursos de anotação para suas capturas de tela.*
- *Ferramenta de Captura de Tela do Shutter* \[MELHOR\]
    + https://shutter-project.org
    + => Observação: Nota disponível como AppImage ou aplicativo flatpak. É mais fácil instalar o Shutter em distribuições Linux baseadas em Debian ou Ubuntu.

**Gravador de Vídeo**

+ *Peek - Flathub* (Gravador de Tela - pode criar animações GIF ou vídeos WebM e MP4)
    + https://flathub.org/apps/com.uploadedlobster.peek
    + Resumo: * O Peek facilita a criação de screencasts curtos de uma área da tela. Ele foi desenvolvido para o uso específico de gravação de áreas da tela, por exemplo, para mostrar facilmente os recursos de interface dos seus próprios aplicativos ou para mostrar um bug em relatórios de bugs. Com o Peek, basta posicionar a janela do Peek sobre a área que deseja gravar e clicar em "Gravar". O Peek é otimizado para gerar GIFs animados, mas você também pode gravar diretamente em WebM ou MP4, se preferir.*

**Ferramentas de Orquestração de Contêineres**

+ *Docker Compose*, Documentação Oficial da Docker Company
    + https://docs.docker.com/compose/
+ *Podman Compose*, Red Hat
    + https://docs.podman.io/en/latest/markdown/podman-compose.1.html 


**VPN Mesh Site-to-Site (Virtual Private Network / Rede Privada Virtual)**


Uma VPN Mesh Site-to-Site, como a **tailscale**, pode ser útil para hospedar este aplicativo em uma rede local privada e acessá-lo de qualquer lugar do mundo sem expor nenhuma porta TCP ou UDP à internet.

+ *Tailscale* - Site Oficial
    + https://tailscale.com
    + Observação: Apenas alguns clientes Tailscale são de código aberto. O servidor Tailscale padrão fornecido como SAAS (Software como Serviço) não é de código aberto, embora exista a implementação de código aberto **Headscale** do servidor Tailscale.
+ *Download do Cliente Tailscale*
    + https://tailscale.com/download
+ *Cliente Tailscale para Android na App Store do F-Droid* (App Store para aplicativos Android de código aberto compilados com build reproduzível)
    + https://f-droid.org/packages/com.tailscale.ipn
+ *Servidor Headscale* (código aberto, adequado para homelabs e auto-hospedagem)
    + https://headscale.net/stable
+ *Servidor Headscale - Repositório Github* (Escrito em GO - Golang)
    + https://github.com/juanfont/headscale

## Leitura Adicional 

+ *If it is worth keeping, save it in Markdown (Se vale a pena manter, salve em Markdown)*
  + https://p.migdal.pl/blog/2025/02/markdown-saves
+ *Exposing a web service with Cloudflare Tunnel (Expondo um serviço web com o Tunnel Cloudflare)*, Erissa A (2022)
  + https://erisa.dev/exposing-a-web-service-with-cloudflare-tunnel/
  + *What if you could host a web service with no ports exposed? With Cloudflare Tunnel, you can!*
  + COMENTÁRIO: Para quem não confia na Cloudflare, uma VPN mesh Tailscale auto-hospedada é uma escolha melhor. A Tailscale permite estabelecer um túnel criptografado direto de ponta a ponta entre nós clientes Tailscale (máquinas com o cliente Tailscale instalado). Como resultado, qualquer nó em uma rede Tailscale pode acessar qualquer serviço web exposto por outros nós Tailscale. Por exemplo, se um Android ou iPhone tiver um aplicativo cliente Taiscale instalado, é possível navegar em um host web na rede local, possivelmente por trás de um NAT (Network Address Translator), que bloqueia conexões de entrada por padrão, abrindo a URL http://dummy:8080 ou http://dummy.net.ts:8080, onde dummy é o nome do host ou nome Tailscale do computador que hospeda o servidor web. O Tailscale não é útil apenas para acessar servidores web locais de qualquer lugar sem expor nenhuma porta TCP ou UDP à internet, mas também é útil para acessar pastas compartilhadas do Windows (SAMBA/SMB), às vezes chamadas de compartilhamentos do Windows, e máquinas Windows remotamente por meio de VNC ou remote desktop.
  + COMENTÁRIO: Expor um servidor web local à internet com Taiscale requer a instalação de um cliente tailscale no computador local que hospeda o servidor web e um cliente tailscale no VPS - Virtual Private Server, uma máquina virtual hospedada na nuvem com endereço IP público. Tudo o que é necessário é adicionar uma configuração ao caddy ou nging na máquina remota para encaminhar o tráfego de rede das portas 80 (http) e 443 (https) para o endereço IP tailscale ou nome do host do computador local, por exemplo, dummy.net.ts é o nome do host ou o nome tailscale do computador local é dummy. A função de um servidor tailscale, que deve ser instalado em uma máquina com endereço IP estático e público, é apenas coordenar as conexões entre os clientes. Uma vez estabelecida uma conexão de cliente para cliente, o tráfego de rede entre os clientes não passa pelo servidor.
+ *Scientific Articles*, MyST 
  + https://mystmd.org/guide/quickstart-myst-documents
+ *R Markdown* 
  + https://rmarkdown.rstudio.com/
  + *R Markdown documents are fully reproducible. Use a productive notebook interface to weave together narrative text and code to produce elegantly formatted output. Use multiple languages including R, Python, and SQL.*
+ *MyST syntax cheat sheet*, Jupyter Book
  + https://jupyterbook.org/en/stable/reference/cheatsheet.html
  + NOTE: MWiki syntax is mostly compatible with MyST syntax because it uses the same markdown parser developed by Jupyter Book project. Credits should be given to MyST markdown project.
+ *Working with MyST Markdown*, MyST 
  + https://mystmd.org/guide/quickstart-myst-markdown
+ *Export Static Documents*, MyST 
  + https://mystmd.org/guide/quickstart-static-exports
+ *Try MyST*, MyST 
  + https://mystmd.org/sandbox
+ *CommonMark*, MyST 
  + https://mystmd.org/guide/commonmark
+ *CommonMark Spec*, CommonMark
  + https://spec.commonmark.org/0.31.2/#introduction
+ *reStructuredText* (Python RST syntax)
  + https://docutils.sourceforge.io/rst.html
+ *Documentation Audiences*, OpenEdx
  + <https://docs.openedx.org/en/latest/documentors/concepts/about_doc_audiences.html>
+ *Rendering Math in HTML: MathML, MathML Core, and AsciiMath*, Andrew Lock (2024)
  + https://andrewlock.net/rendering-math-in-html-mathml-mathml-core-and-asciimath/
+ *Latex, MATHML, and tex4ht: Tools for Creating Accessible Documents (a brief tutorial)*, Jacek Polewczak 
  + https://www.csun.edu/~hcmth008/mathml/acc_tutorial.html
+ *MathML in Web Browsers - A joint effort to add native MathML-Core support to web browsers*, Igalia
  + https://mathml.igalia.com/
+ *MathJax - render math on the Web on all browsers*, Murray Bourne (2011), Interactive Mathematics
  + https://www.intmath.com/blog/mathematics/mathjax-render-math-on-the-web-on-all-browsers-5703
+ *Exploring cross-browser math equations using MathML or LaTeX with MathJax*, Scott Hanselman (2014)
  + https://www.hanselman.com/blog/exploring-crossbrowser-math-equations-using-mathml-or-latex-with-mathjax