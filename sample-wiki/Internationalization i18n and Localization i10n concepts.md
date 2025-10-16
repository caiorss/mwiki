---
title:       Internationalization i18n and Localization i10n concepts
label:       
description: 
keywords:    
---


## Terminology of Internationalization


ISO 
 : International Organization for Standardization
 
W3C 
 : World Wide Web Consortium

AE
 : American English
 
BE
 : British English 

**i10n** - Localization (AE) or Localisation (BE)
  : Adaptation of software or product to meet language and culture of a particular target market ou audience. Localization is not only language translation, but also cultural adaption, inclunding, country currency, parper size ISO A4 or Letter sizer, date time format, cultural conventions, legal requirements.

**i18n** - Internationalization (AE), Internationalisation (BE)
  : Process of building a software application capable of adapting to multiple languages and cultures without code changing. In other words, a internationalization is the process of building a software with localization infrastructure, that allows adding new localization without code changes.

**g11n** - Globalization
  : Combination of internationalization and localization. This terminology is used by IBM and Oracle.

Locale
  : Language ISO code for instance, en-US (American English), en-UK (British English), fr-CA (Canadian French) and so on.
  
CJK  Languages
  : Chinese, Japanese and Korean languages

RTL Languages
  : Right-To-Left Languages. Languages written from right to left. Examples: most languages using Latin Script, including, English, Greek and so on. 
  
LTR Languages
  : Left-To-Right Languages. Languages written from left to right. Example: Hebrew, Arabic, Persian, Urdu, Phoenician and so on.

NVL 
  : National Language Version
  
UTF-8
  : Unicode 8 bits. One "character" or symbol may use more than one byte. Unicode 8 bits is the most used text enconding format possibly due to the backward compatibility with the old ASCII text encoding. However, it makes programming harder since one cannot assume that i-th position of a unicode string corresponds to the i-th character because a single UTF-8 "character" may be represented by multiple bytes.
  
UTF-16
  : Unicode 16 bits. One "character" or symbol is represented by 2 bytes. The UTF-16 encoding is mostly used internally by programming languages implementations, including Java and Python. The Windows C API - Application Programming Interface also uses UTF-16 in its internal APIs. This text enconding format is easier to deal with in programming langues because the i-th position of a unicode array is the i-th symbol. 
  
QA Testing
  : EN - Quality Assurance Testing 
  : PT - Teste de Garantia de Qualidade
 
## Internationalization Issues

```{figure} ![[pasted-image-1755972975940.jpg]]
World Regional Languages
```

Brainstorm of Major Internationalization Issues


+ Initial Language
  + The website or application attempts to guess the user language based on http header or IP address.
  + Presents the web page in default language and provides a menu or form allowing the user to switch the language.
+ Language Switching (Processo de mundança de línguagem)
+ Optimization 
  + Localization strings (text) served or renderend in the front-end (client side).
  + Localization strigns (text) served or rendered in the backend (server side).
  + Lazy loading locatization strings.
  + Load only what is needed.
+ Language Issues
    + Date Format
    + Pluralization
    + Language Dialects
    + Gender-Specific Translations
    + A country may have more than one language or more than one official language. For instance, in Canada, English and French are official languages and in Switzerland, German, French and Italian are official languages.
    + Spelling of Specific dialect of a language (Ortografia de dialetos especificos de uma linguagem)
    + RTL - Right-To-Left Language Support (Suporte a Línguagens da Esquerda para direita), for instance Arabic and Hebrew are written from right to left.
+ Cultural Issues
    + Cultural Standards
    + Cultural Conventions
    + Cultural Assumptions
  
## Common Mistakes


+ Country Flag does not represent a language. For instance, the Brazilian flag should not be used for representing the Portuguese language.
+ There are more than one dialect and spelling of the same language. For instance, some words in American English and British English have different spellings, i.e *internationalization* (American English) and *internationalisation* (British English). That is the reason why country flags should not be used for representing  languages.
+ Localization must not only specific for a particular language. It should also be specific for each country and **standardized dialect of a language**, such as American English, British English, European Portuguese or Brazilian Portuguese. For instance, despite the American English be ubiuitous on the internet, most English speaking countries other than USA or Phillipines use British English spelling and languages contructs derived from this English dialect. The British English spelling is also widely used on continental Europe by non English speaking countries, including Germany, France, Portugal, Netherlands and so on.
+ Do not use IP address or user geographic location for selecting the language or locale used by a website. The language should be selected based on the user preference indicated by the http header [Accept-Language](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Accept-Language) and the graphicsuser interface should always have a button or selection box allowing the user to switch the language. On Linux Desktop applications, the environment variable LANG is commonly used for obtaining the user desired language. This variable is set during Linux installation of Linux desktop distributions to the language chosen by the user.
+ Some reasons to avoid using IP address, geographic location or country for choosing the UI - User Interface language are: some countries may have multiple official languages or multiple spoken languages; nowadays, people travels and may not be able speak the local language; even a native speakers may not want read in his or her own native language. 
   
  
## Common Locales

| Country      | Locale Code          | Language Name                                   | 
|------------- | -------------------- | ----------------------------------------------- |
| UK           | en-UK                | British English (UK - United Kingdom)           |
| USA          | en-US                | American/USA English                            |
| Ireland      | en-IE                | Irish English                                   |
| Canada       | en-CA                | Canadian English                                |
| Canada       | ca_FR                | Canadian French (Français Canadien)             |
| Australia    | en-AU                | Australian English                              | 
| New Zealand  | en-NZ                | New Zealand English                             |
| Singapore    | en-SG                | Singaporean English                             |
| Hong Kong    | en-HK                | Hong Kong English                               |
| South Africa | en-ZA                | South African English                           |  
| South Africa | af-ZA                | Afrikaans (based on Dutch language)             |
| Phillipines  | en-PH                | Phillipines English (based on American English) |
| India        | en-IN                | Indian English                                  |
| India        | hi_IN                | Hindi (Hindustani)                              |
| Germany      | de_DE                | German (Deutsch)                                |
| Austria      | de_AT                | Austrian German (Österreichisches Deutsch)      |
| Switzerland  | de_CH                | Switzerland German (Schweizerdeutsch)           |
| Switzerland  | fr_CH                | Switzerland French  (Suisse français)           |
| Switzerland  | it_CH                | Switzerland Italian                             |
| France       | fr_FR                | French (Français)                               |
| Italy        | it_IT                | Italian (Italiano)                              |
| Greece       | el_GR                | Modern Greek                                    | 
| Cyprus       | el_CY                | Modern Greek of Cyprus                          |
| Spain        | es_ES                | Spanish (Español)                               |
| Spain        | ca_ES                | Catalan (Catalán in Spanish)                    |   
| Spain        | eu-ES                | Basque (Non indo-european language)             |
| Spain        | gl-ES                | Galician (Sister language of Portuguese)        |
| Mexico       | es_MX                | Mexican Spanish (Español mexicano)              |
| USA          | es-US                | American/USA Spanish                            |
| Puerto Rico  | es_PR                | Puerto Rico Spanish (USA)                       |
| Argentina    | es_AR                | Argentinian Spanish (Español argentino)         |
| Uruguay      | es_UY                | Uruguayian Spanish (Español uruguayo)           |
| Chile        | es_CL                | Chilean Spanish (Español chileno)                |
| Colombia     | es_CO                | Colombian Spanish (Español colombiano)          |
| Peru         | es_PE                | Peruvian Spanish (Español peruano)              |
| Ecuador      | es_EC                | Ecuadorian Spanish (Español ecuatoriano)        |
| Panama       | es_PA                | Panamenian Spanish (Español panameño)           |
| Venezuela    | es_VE                | Venezuelan Spanish (Español venezolano)         |
| Portugal     | pt_PT                | European Portuguese (Português Europeu)         |
| Brasil       | pt_BR                | Brazilian Portuguese (Português Brasileiro)     |                    
| Capte Verde  | pt_CV                | Cape Verde Portuguese (Português de Cabo Verde) |                                        |
| China        | zh_CN                | Chinese (Mandarin Chinese of Mainland China)    | 
| Hong Kong    | zh_HK                | Hong Kong Chinese                               |
| Taiwan       | zh_TW                | Taiwan Chinese                                  |
  
NOTE:
1. Most English variants around the world are based on the British English and uses the British spelling. The American English spelling is only used by USA and Phillipines.
2. India does not have any official language and Hindi is not the official language of India. Moreover, the majority of Indian population does not speak Hindi.
3. Hong Kong is not country. It is a SAR - Special Administrative Region of mainland China. 
4. Puerto Rico is USA non incorporated territory. So, it is not a country.

**Change User Interface Language on Linux**

It is possible to change the UI interface language of some application on Linux on command line by setting the environment variable LANG to the desired locale code. For instance, the following temporarily changes the Kwrite KDE text editor language to Swiss German even if the default language used during the Linux distribution installation was not German. This feature is useful for language learners for obtaining the common terminology used for localizing applications to a particular language.

```sh
env LANG=de_CH kwrite
```

Lanch kwite with language set to Swiss German detached from terminal (without blocking the terminal emulator).

```sh
$ env LANG=de_US.UTF-8 kwrite 1> /dev/null 2> /dev/null & disown
```

Explanation:

+ `1> /dev/null` redirects the kwrite process' stdout (standard output) to Linux pseudo file /dev/null.
+ `2> /dev/null` redirects the kwrite process' stderr (standard error output) to Linux pseudo file /dev/null.
+ `& disown` => Detach kwrite process from the terminal in order run this application as a daemon (background process/service) and to avoid blocking the terminal emulator and terminating the kwrite process if the terminal is closed.

**See**

+ *Country Code Language List*
  + https://www.fincher.org/Utilities/CountryLanguageList.shtml
+ *ISO-3166 Country Codes and ISO-639 Language Codes*, Oracle Docs
  + https://docs.oracle.com/cd/E13214_01/wli/docs92/xref/xqisocodes.html
+ *Standard locale names*, Microsoft
  + https://learn.microsoft.com/en-us/globalization/locale/standard-locale-names
+ *ISO Country and Language Codes: The Definitive Guide*
  + https://centus.com/blog/iso-language-codes
            
## Falsehoods Many Programmers Believe About Names

1. Names are only written using ascii characters. Counterexample: "João".
2. Names does not contain hyphen (-) or apostrophe (') characters. Counterexample: O'neil - common irish surname.
3. A person may have only two names, a given name and surname (family name). Counterexample: the full name of Brazil's emperor [Pedro II of Brazil](https://en.wikipedia.org/wiki/Pedro_II_of_Brazil) was "Pedro de Alcântara João Carlos Leopoldo Salvador Bibiano Francisco Xavier de Paula Leocádio Miguel Gabriel Rafael".
4. People do not change their names, surnames or email. 
5. People will never have identical names.
6. The name or surname has at least 3 characters. Counterexample: "Wu".
7. The full name is limited to 100 characters length.
8. I will never need to deal with foreign names in my database.
9. Names with the same spelling are always written in the same way with the same spelling. Counterexample: There are several different Japanese names that sounds as ["Akira"](<https://en.wikipedia.org/wiki/Akira_(given_name)>) and are romanized (written in latin script) as that, although they are written using different Kanji symbols and have different meanings. 
10. People have at least one surname. Countereraxmple: In some countries, such as Indonesia and Japan some people may have a single given name and no surname. Members of Japanese royalty do not have surnames or family names. Sukarno, the first president of Indonesia did not have any surname. His full name was just "Sukarno".

**See also:**

+ *Personal names around the world*, W3C
  + https://www.w3.org/International/questions/qa-personal-names
  + *How do people's names differ around the world, and what are the implications of those differences on the design of forms, databases, ontologies, etc. for the Web?*
+ *Legal name*, Wikipedia
  + https://en.wikipedia.org/wiki/Legal_name
+ *Middle name*, Wikipedia
  + https://en.wikipedia.org/wiki/Middle_name
+ *Name change*, Wikipedia
  + https://en.wikipedia.org/wiki/Name_change
+ *Surname*, Wikipedia
  + https://en.wikipedia.org/wiki/Surname
+ *Maiden and married names*, Wikipedia
  + https://en.wikipedia.org/wiki/Maiden_and_married_names
+ *Patronymic surname*, Wikipedia
  + https://en.wikipedia.org/wiki/Patronymic_surname
+ *A basic guide to using Asian names*, Asia Media Centre
  + https://www.asiamediacentre.org.nz/features/a-guide-to-using-asian-names
+ *Chinese Naming Conventions - Chinese Culture*, Cultural Atlas
  + https://culturalatlas.sbs.com.au/chinese-culture/chinese-culture-naming
+ *Japanese Naming Conventions - Japanese Culture*, Cultural Atlas
  + https://culturalatlas.sbs.com.au/japanese-culture/japanese-culture-naming
+ *Wikipedia:Naming conventions (Chinese)*
  + https://en.wikipedia.org/wiki/Wikipedia:Naming_conventions_(Chinese)
+ *East Slavic name*, Wikipedia
  + https://en.wikipedia.org/wiki/East_Slavic_name
+ *Spanish naming customs*, Wikipedia
  + https://en.wikipedia.org/wiki/Spanish_naming_customs
+ *Naming customs of Hispanic America*, Wikipedia
  + https://en.wikipedia.org/wiki/Naming_customs_of_Hispanic_America
+ *Arabic name*, Wikipedia
  + https://en.wikipedia.org/wiki/Arabic_name
+ *How Arabic Names Work: A Guide to Ism, Nasab, Laqab, Nisba, and Kunya*
  + https://arabic-for-nerds.com/translation/how-are-family-names-constructed-in-arabic/
+ *Mononym*, Wikipedia (People with no surname, just a single name)
  + https://en.wikipedia.org/wiki/Mononym
+ *List of legally mononymous people*, Wikipedia (List of people whose full legal name does not have surname or family name such as members of Japanese royal family)
  + <https://en.wikipedia.org/wiki/List_of_legally_mononymous_people>
+ *O'Neill (surname)*, Wikipedia
  + https://en.wikipedia.org/wiki/O%27Neill_(surname)
+ *Akira (given Japanese name)*, Wikipedia
  + <https://en.wikipedia.org/wiki/Akira_(given_name)>   
## American English Vs British English 

| American English    | British English      |
| ------------------- | -------------------- |
| internalization     | internationalisation |
| localization        | localisation         |
| program             | programme            |
| center              | centre               |
| color               | colour               |
| favor               | favour               |
| favorite            | favourite            |
| labor               | labour               |
| defense             | defence              |
| ofense              | ofence               |
| shop                | shoppe               |
| shopping mall, mall | shopping centre      |
| tires               | tyres                |
| while               | while, whilst        |  
| football            | American football    |   
| soccer              | football             |  
| roomates            | rommates, flatmates  |  
| fall                | autumn               | 
## Software Libraries

JavaScript
 + i18Next

Python
+ Gettext
    

## See also

+ *Internationalization and localization*, Wikipedia
  + https://en.wikipedia.org/wiki/Internationalization_and_localization
+ *Personal names around the world*, W3C
  + https://www.w3.org/International/questions/qa-personal-names
  + *How do people's names differ around the world, and what are the implications of those differences on the design of forms, databases, ontologies, etc. for the Web?*
+ *Internationalization and Localization in Flask Apps*, Reintech Media
  + https://reintech.io/blog/internationalization-localization-flask-apps
+ *The Flask Mega-Tutorial, Part XIII: I18n and L10n*, Miguel Grinberg
  + https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiii-i18n-and-l10n
+ *How to Internationalize Your Flask App Like a Pro*, Oksana Tkach - Metamova
  + https://medium.com/@oksanatkach/how-to-internationalize-your-flask-app-like-a-champ-e57535185893
  + *How to tweak the Babel library for large i18n projects to enable pseudotranslation and iterative localization*
+ *Localization vs. Internationalization*, W3C
  + https://www.w3.org/International/questions/qa-i18n
+ *Mastering Localisation (l10n) and Internationalisation (i18n) in Modern Frontend Development*, Nitin Mangrule
  + https://medium.com/@ndmangrule/mastering-localisation-l10n-and-internationalisation-i18n-in-modern-frontend-development-3ec3c6751e58
+ *GNU gettext Manual*
  + https://www.gnu.org/software/gettext/manual/gettext.html
  + *This manual documents the GNU gettext tools and the GNU libintl library, version 0.26.*
+ *GNU gettext*, GNU Project
  + https://www.gnu.org/software/gettext/
  + Brief: * Usually, programs are written and documented in English, and use English at execution time for interacting with users. This is true not only from within GNU, but also in a great deal of proprietary and free software. Using a common language is quite handy for communication between developers, maintainers and users from all countries. On the other hand, most people are less comfortable with English than with their own native language, and would rather be using their mother tongue for day to day's work, as far as possible. Many would simply love seeing their computer screen showing a lot less of English, and far more of their own language. GNU gettext is an important step for the GNU Translation Project, as it is an asset on which we may build many other steps. This package offers to programmers, translators, and even users, a well integrated set of tools and documentation. Specifically, the GNU gettext utilities are a set of tools that provides a framework to help other GNU packages produce multi-lingual messages. These tools include a set of conventions about how programs should be written to support message catalogs, a directory and file naming organization for the message catalogs themselves, a runtime library supporting the retrieval of translated messages, and a few stand-alone programs to massage in various ways the sets of translatable strings, or already translated strings. A special GNU Emacs mode also helps interested parties in preparing these sets, or bringing them up to date.*
+ *Guide to the ECMAScript Internationalization API*, W3C Interationalization
  + https://w3c.github.io/i18n-drafts/articles/intl/index.en.html
  + *For years, developers relied on JavaScript libraries, string manipulation, or server-side logic to ensure that users around the world see dates, numbers, and text formatted in a way that is natural and correct for them. These solutions, while functional, often added significant weight to web pages and created maintenance challenges. Fortunately, modern browsers now have a built-in, standardized solution: the ECMAScript Internationalization API, available globally in JavaScript via the Intl object. This API provides a native way to handle locale- and culture-sensitive data and operations, ensuring your application speaks your user's language correctly and efficiently. This article will serve as a practical overview of the most essential parts of the Intl API, providing actionable examples you can use to internationalize your web applications today.*
+ *Implement a strategy to select the language/culture for each request in a localized ASP.NET Core app*, Microsft Learn - Dotnet core
  + https://learn.microsoft.com/en-us/aspnet/core/fundamentals/localization/select-language-culture?view=aspnetcore-9.0
 + *Accept-Language header*, MDN - Mozilla Development Network
   + https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Accept-Language
   + *The HTTP Accept-Language request header indicates the natural language and locale that the client prefers. The server uses content negotiation to select one of the proposals and informs the client of the choice with the Content-Language response header. Browsers set required values for this header according to their active user interface language. Users can also configure additional preferred languages through browser settings. The Accept-Language header generally lists the same locales as the navigator.languages property, with decreasing q values (quality values). Some browsers, like Chrome and Safari, add language-only fallback tags in Accept-Language. For example, en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7 when navigator.languages is ["en-US", "zh-CN"]. For privacy purposes (reducing fingerprinting), both Accept-Language and navigator.languages may not include the full list of user preferences. For example, in Safari (always) and Chrome's incognito mode, only one language is listed.*
+ *Accept-Language used for locale setting*, W3C (2003)
  + https://www.w3.org/International/questions/qa-accept-lang-locales
+ *Accept-Language Documentation*, Fastly 
  + https://www.fastly.com/documentation/reference/http/http-headers/Accept-Language/
+ *Internationalization and localization*, Django Docs
  + https://docs.djangoproject.com/en/5.2/topics/i18n/
+ *Translation*, Django Docs
  + https://docs.djangoproject.com/en/5.2/topics/i18n/translation/
+ *Localization / Internationalization*
  + https://frontend.turing.edu/lessons/module-4/localization.html
+ *Introduction - I18N Best Practices*
  + https://internationalization-guide.readthedocs.io/en/latest/introduction.html
+ *Internationalize your API*, The Rest API Cookbook
  + https://octo-woapi.github.io/cookbook/internationalization.html
+ *Internationaliazation*, Django Rest Framework Docs
  + https://www.django-rest-framework.org/topics/internationalization/
+ *Django Internationalization and Localization Best Practices*, Codezup
  + https://codezup.com/django-i18n-l10n-best-practices/
+ *Globalization and localization in ASP\.NET Core*, Documentation ASP\.NET Core
  + https://learn.microsoft.com/en-us/aspnet/core/fundamentals/localization?view=aspnetcore-9.0
+ *Vue.js and Vue Router with Internationalization and Localization*, Codez Up (2024)
  + https://codezup.com/vuejs-vuerouter-internationalization-localization/
+ *Where should I do localization (server-side or client-side)?*
  + https://softwareengineering.stackexchange.com/questions/313726/where-should-i-do-localization-server-side-or-client-side
+ *Internationalization, localization, and input methods in Fuchsia*
  + https://fuchsia.dev/fuchsia-src/development/internationalization
+ *RFC 9839 and Bad Unicode*, TBray (See <rfc:9839>)
  + https://www.tbray.org/ongoing/When/202x/2025/08/14/RFC9839
  + *Unicode is good. If you’re designing a data structure or protocol that has text fields, they should contain Unicode characters encoded in UTF-8. There’s another question, though: “Which Unicode characters?” The answer is “Not all of them, please exclude some.” This issue keeps coming up, so Paul Hoffman and I put together an individual-submission draft to the IETF and now (where by “now” I mean “two years later”) it’s been published as RFC 9839. It explains which characters are bad, and why, then offers three plausible less-bad subsets that you might want to use. Herewith a bit of background, but…*
+ *A step-by-step guide to effective website localization*, Webflow
  + https://webflow.com/blog/website-localization
  + *Discover the benefits of website localization and learn how to modify your content and marketing strategy to cater to local audiences effectively.*       
+ *Internationalization And Localization For Static Sites*, Sam Richard, Smash Magazine (2020)
  + https://www.smashingmagazine.com/2020/11/internationalization-localization-static-sites/
+ *Building a Multilingual Static Website: A Step-by-Step Guide*, Noha Nabil (2023)
  + https://medium.com/@nohanabil/building-a-multilingual-static-website-a-step-by-step-guide-7af238cc8505 
+ *Internationalization*, NextJS
  + https://nextjs.org/docs/app/guides/internationalization
  + *Next.js enables you to configure the routing and rendering of content to support multiple languages. Making your site adaptive to different locales includes translated content (localization) and internationalized routes.*
+ *k-yak / stati18n Public* (2014)
  + https://github.com/k-yak/stati18n
    
