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
  
[ICU](https://icu.unicode.org/)
  : International Components for Unicode 
  
[ICU4J](https://unicode-org.github.io/icu/userguide/icu4j/)
  : Java implementatijon of the ICU library.
  
[CLDR](https://cldr.unicode.org/)
  : Common Locale Data Repository (from ICU project)

LMDL
  : Locale Data Markup Language (XML-based language - ICU project).
  
UTF-8
  : Unicode 8 bits. One "character" or symbol may use more than one byte. Unicode 8 bits is the most used text enconding format possibly due to the backward compatibility with the old ASCII text encoding. However, it makes programming harder since one cannot assume that i-th position of a unicode string corresponds to the i-th character because a single UTF-8 "character" may be represented by multiple bytes.
  
UTF-16
  : Unicode 16 bits. One "character" or symbol is represented by 2 bytes. The UTF-16 encoding is mostly used internally by programming languages implementations, including Java and Python. The Windows C API - Application Programming Interface also uses UTF-16 in its internal APIs. This text enconding format is easier to deal with in programming langues because the i-th position of a unicode array is the i-th symbol. 
  
QA Testing
  : EN - Quality Assurance Testing 
  : PT - Teste de Garantia de Qualidade
    
## Internationalization Issues

```{figure} ![[pasted-image-1760618396013.jpg]]
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

Locale codes follow the convention {raw}`<language-code>-<countery-code>` with (-) dash character or {raw}`<language-code>_<country-code>` with the underline character (_).

| Country      | Locale Code          | Language Name                                   | 
|------------- | -------------------- | ----------------------------------------------- |
| USA          | en-US                | American/USA English                            |
| UK           | en-UK                | British English (UK - United Kingdom)           |
| Ireland      | en-IE                | Irish English                                   |
| Ireland      | ga-IE                | Irish language (Irish Gaelic)                   |
| Canada       | en-CA                | Canadian English                                |
| Canada       | fr-CA                | Canadian French (Français Canadien)             |
| Australia    | en-AU                | Australian English                              | 
| New Zealand  | en-NZ                | New Zealand English                             |
| Singapore    | en-SG                | Singaporean English                             |
| Hong Kong    | en-HK                | Hong Kong English                               |
| South Africa | en-ZA                | South African English                           |  
| South Africa | af-ZA                | Afrikaans (based on Dutch language)             |
| Phillipines  | en-PH                | Phillipines English (based on American English) |
| India        | en-IN                | English (India)                                 |
| India        | hi-IN                | Hindi^{Hindustani} (India)                      |
| India        | ta-IN                | Tamil (India)                                   |
| Germany      | de-DE                | German (Deutsch)                                |
| Austria      | de-AT                | Austrian German (Österreichisches Deutsch)      |
| Switzerland  | de-CH                | Switzerland German (Schweizerdeutsch)           |
| Switzerland  | fr-CH                | Switzerland French  (Suisse français)           |
| Switzerland  | it-CH                | Switzerland Italian                             |
| France       | fr-FR                | French (Français)                               |
| Italy        | it-IT                | Italian (Italiano)                              |
| Greece       | el-GR                | Modern Greek                                    | 
| Türkiye      | tr-TR                | Turkish^{The country is formely known as Turkey.} |
| Cyprus       | el-CY                | Modern Greek of Cyprus                          |
| Cyprus       | tr-CY                | Turkish language (Cyprus)                       |
| Spain        | es-ES                | Spanish (Español)                               |
| Spain        | ca-ES                | Catalan (Catalán in Spanish)                    |   
| Spain        | eu-ES                | Basque (Non indo-european language)             |
| Spain        | gl-ES                | Galician (Sister language of Portuguese)        |
| Mexico       | es-MX                | Mexican Spanish (Español mexicano)              |
| USA          | es-US                | American/USA Spanish                            |
| Puerto Rico  | es-PR                | Puerto Rico Spanish (USA)                       |
| Argentina    | es-AR                | Argentinian Spanish (Español argentino)         |
| Uruguay      | es-UY                | Uruguayian Spanish (Español uruguayo)           |
| Chile        | es-CL                | Chilean Spanish (Español chileno)               |
| Colombia     | es-CO                | Colombian Spanish (Español colombiano)          |
| Peru         | es-PE                | Peruvian Spanish (Español peruano)              |
| Ecuador      | es-EC                | Ecuadorian Spanish (Español ecuatoriano)        |
| Panama       | es-PA                | Panamenian Spanish (Español panameño)           |
| Venezuela    | es-VE                | Venezuelan Spanish (Español venezolano)         |
| Portugal     | pt-PT                | European Portuguese (Português Europeu)         |
| Angolar      | pt-AO                | Portuguese (Angola)                             |
| Capte Verde  | pt-CV                | Portuguese (Português de Cabo Verde)            |                                        |
| Brasil       | pt-BR                | Brazilian Portuguese (Português Brasileiro)     |                    
| Japan        | ja-JP                | Japanese language                               |
| Singapore    | zh-SG                | Chinese (Singapore)                             |
| Taiwan       | zh-TW                | Taiwan Chinese                                  |
| Hong Kong    | zh-HK                | Hong Kong Chinese                               |
| China        | zh-CN                | Chinese (Mandarin Chinese of Mainland China)    | 
  
NOTE:
1. Most English variants around the world are based on the British English and uses the British spelling. The American English spelling is only used by USA and Phillipines.
2. India does not have any official language and Hindi is not the official language of India. Moreover, the majority of Indian population does not speak Hindi.
3. Hong Kong is not country. It is a SAR - Special Administrative Region of mainland China. Hong Kong has its own currency and onlympic team. In addition, in sports matches Hong Kong uses its own flag. 
4. Puerto Rico is not a country. The island is USA non incorporated territory, even though the island has its own olympic team.
5. Spanish locales don't have much difference other than country code, currency and paper size since most Spanish countries follows the [Royal Spanish Academy](https://en.wikipedia.org/wiki/Royal_Spanish_Academy)^{Spanish: Real Academia Española}

**Change User Interface Language on Linux**

It is possible to change the UI interface language of some application on Linux on command line by setting the environment variable LANG to the desired locale code. The default system locale on Linux can be obtained by reading the environment variable $LANG.

In bash shell or any other POSIX shell.

```sh
$ echo $LANG
en_US.UTF-8
```

In Python, 

```sh
>>> import os 

>>> os.getenv("LANG", "")
'en_US.UTF-8'
```

The following command temporarily changes the Kwrite KDE text editor language to Swiss German even if the default language used during the Linux distribution installation was not German. This feature is useful for learning new vocabulary of other languages.

```sh
env LANG=de_CH kwrite
```

Lanch kwite with language set to Swiss German detached from terminal (without blocking the terminal emulator).

```sh
$ env LANG=de_CH.UTF-8 kwrite 1> /dev/null 2> /dev/null & disown
```

Explanation:

+ `1> /dev/null` redirects the kwrite process' stdout (standard output) to Linux pseudo file /dev/null.
+ `2> /dev/null` redirects the kwrite process' stderr (standard error output) to Linux pseudo file /dev/null.
+ `& disown` => Detach kwrite process from the terminal in order run this application as a daemon (background process/service) and to avoid blocking the terminal emulator and terminating the kwrite process if the terminal is closed.


**Screenshot of KWrite using different locales**

```{figure} ![[pasted-image-1760611139235.jpg]]

KWrite started with en_US American English locale 
```

```{figure} ![[pasted-image-1760611027216.jpg]]

KWrite started with de_DE German locale for Switzerland
```

```{figure} ![[pasted-image-1760610949514.jpg]]

KWrite started with es_ES Spanish locale for Spain
```






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

1. Names are only written using ascii characters. Counterexample: "João" (portuguese version of John) or " Björk" (Icelandic given name).
2. Names does not contain hyphen (-) or apostrophe (') characters. Counterexample: O'neil - common irish surname.
3. A person may have only two names, a given name and surname (family name). Counterexample: the full name of Brazil's emperor [Pedro II of Brazil](https://en.wikipedia.org/wiki/Pedro_II_of_Brazil) was "Pedro de Alcântara João Carlos Leopoldo Salvador Bibiano Francisco Xavier de Paula Leocádio Miguel Gabriel Rafael".
4. People do not change their names, surnames or email. 
5. People will never have identical names.
6. The name or surname has at least 3 characters. Counterexample: "Wu".
7. The full name is limited to 100 characters length.
8. I will never need to deal with foreign names in my database.
9. Names with the same spelling are always written in the same way with the same spelling. Counterexample: There are several different Japanese names that sounds as ["Akira"](<https://en.wikipedia.org/wiki/Akira_(given_name)>) and are romanized (written in latin script) as that, although they are written using different Kanji symbols and have different meanings. 
10. People have at least one surname. Countereraxmple: In some countries, such as Indonesia and Japan some people may have a single given name and no surname. Members of Japanese royalty do not have surnames or family names. Sukarno, the first president of Indonesia did not have any surname. His full name was just "Sukarno".
11. People only a have a single given name and there is no whitespace within a given name. Counterexample:  Hector Marίa GONZALEZ LÓPEZ. The given name is "Hector Marίa". The patronymic surname is Gonzalez and the mather's family name is López. Many Spanish given names have the suffix Maria in compound given names. Female hispanic given often have the suffix "de dolores", "soledad" and etc. 


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
+ *Roman naming conventions*, Wikipedia
  + https://en.wikipedia.org/wiki/Roman_naming_conventions
+ *Nomen gentilicium*, Wikipedia
  + https://en.wikipedia.org/wiki/Nomen_gentilicium
+ *Cognomen*, Wikipedia
  + https://en.wikipedia.org/wiki/Cognomen
+ *Praenomen*, Wikipedia
  + https://en.wikipedia.org/wiki/Praenomen
+ *Italian name*, Wikipedia
  + https://en.wikipedia.org/wiki/Italian_name
+ *Spanish naming customs*, Wikipedia
  + https://en.wikipedia.org/wiki/Spanish_naming_customs
+ *Spanish Names: A Beginner’s Guide to Naming Customs and Traditions*, ESLZubzz
  + https://eslbuzz.com/spanish-names/
+ *Spanish proper names and their cultural secrets: More than just a name*, WOrldsAcross
  + https://blog.worldsacross.com/index/spanish-proper-names-and-their-cultural-secrets-more-than-just-a-name
+ *Naming - Spanish Culture*, Cultural Atlas
  + https://culturalatlas.sbs.com.au/spanish-culture/spanish-culture-naming
+ *Naming customs of Hispanic America*, Wikipedia
  + https://en.wikipedia.org/wiki/Naming_customs_of_Hispanic_America
+ *Portuguese name*, Wikipedia
  + https://en.wikipedia.org/wiki/Portuguese_name
  + *A Portuguese name, or Lusophone name – a personal name in the Portuguese language – is typically composed of one or two personal names, the mother's family surname and the father's family surname (rarely only one surname, sometimes more than two). For practicality, usually only the last surname (excluding prepositions) is used in formal greetings.*
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
    

## Footnotes

```{footnotes}
```
 
## See also

### Unicode 

+ *UTF-8, Explained Simply*, Nic Baker - Youtube Video
  + https://www.youtube.com/watch?v=vpSkBV5vydg
+ *"The History of UTF-8, as told by Rob Pike"* (2003)
  + https://doc.cat-v.org/bell_labs/utf-8_history
+ *"The History of UTF-8, as told by Rob Pike"* (2003)
  + https://www.cl.cam.ac.uk/%7Emgk25/ucs/utf-8-history.txt
+ *Be aware of sorting locales*, Adrian Stoll
  + https://www.adrianstoll.com/post/beware-of-sorting-locales/
+ *locale(7) — Linux manual page*
  + https://man7.org/linux/man-pages/man7/locale.7.html
  + *A locale is a set of language and cultural rules.  These cover aspects such as language for messages, different character sets, lexicographic conventions, and so on. A program needs to be able to determine its locale and act accordingly to be portable to different cultures.*
+ *Iterating strings and manually decoding UTF-8*, Zylinski
  + https://zylinski.se/posts/iterating-strings-and-manually-decoding-utf8/
+ *Python's splitlines does a lot more than just newlines*, yossarian\.net
  + https://yossarian.net/til/post/python-s-splitlines-does-a-lot-more-than-just-newlines/
+ *The Country That Broke Kotlin*, Sam Cooper
  + https://sam-cooper.medium.com/the-country-that-broke-kotlin-84bdd0afb237
  + *Logic vs language: how a Turkish alphabet bug played a years-long game of hide-and-seek inside the Kotlin compiler.*
+ *Does Your Code Pass The Turkey Test?*, Moserware (2008)
  + https://www.moserware.com/2008/02/does-your-code-pass-turkey-test.html
  + *Over the past 6 years or so, I’ve failed each item on “The Turkey Test.” It’s very simple: will your code work properly on a person’s machine in or around the country of Turkey? Take this simple test.*
+ *SMS Turkish Disaster*
  + https://revealingerrors.com/turkish_sms_disaster
+ *Strcasecmp in Turkish*, Daniel Stenberg (2008) - Curl Project
  + https://daniel.haxx.se/blog/2008/10/15/strcasecmp-in-turkish/
  + *A friendly user submitted the (lib)curl bug report [2154627](http://curl.haxx.se/bug/view.cgi?id=2154627) which identified a problem with our URL parser. It doesn’t treat “file://” as a known protocol if the locale in use is Turkish.*
+ *Internationalization for Turkish: Dotted and Dotless Letter "I"*, I18nGuy
  + http://www.i18nguy.com/unicode/turkish-i18n.html
  + *Many software and web applications that are already internationalized and are successfully supporting many languages, often suffer catastrophic failure when they add support for the Turkish language. This page explains the difficulty of supporting the Turkish language and typical solutions. There are 3 sections: A brief overview of Turkish characters and encodings. Turkish language problem and solutions. A brief history of the Turkish language is offered as background material.*
+ *Locale-agnostic case conversions by default*
  + https://github.com/Kotlin/KEEP/blob/main/proposals/stdlib/KEEP-0223-locale-agnostic-case-conversions.md
  
### Internationalization and Localization  Reading

+ *Internationalization and localization*, Wikipedia
  + https://en.wikipedia.org/wiki/Internationalization_and_localization
+ *International Components for Unicode*, Wikipedia
  + https://en.wikipedia.org/wiki/International_Components_for_Unicode
  + *International Components for Unicode (ICU) is an open-source project of mature C/C++ and Java libraries for Unicode support, software internationalization, and software globalization. ICU is widely portable to many operating systems and environments. It gives applications the same results on all platforms and between C, C++, and Java software. The ICU project is a technical committee of the Unicode Consortium and sponsored, supported, and used by IBM and many other companies.[2] ICU has been included as a standard component with Microsoft Windows since Windows 10 version 1703.[3]*
+ *ICU-TC Home Page*
  + https://icu.unicode.org/
+ *Unicode CLDR Project*
  + https://cldr.unicode.org/
  + *The Unicode ==Common Locale Data Repository== (CLDR) provides key building blocks for software to support the world’s languages with the largest and most extensive standard repository of locale data available. This data is supplied by contributors for their languages via the CLDR SurveyTool. CLDR is used by a wide spectrum of companies for their ==software internationalization and localization==, adapting software to the conventions of different languages for such common software tasks. It includes: Locale-specific patterns for formatting and parsing: dates, times, timezones, numbers and currency values, measurement units,… Translations of names: languages, scripts, countries and regions, currencies, eras, months, weekdays, day periods, time zones, cities, and time units, emoji characters and sequences (and search keywords),… Language & script information: characters used; plural cases; gender of lists; capitalization; rules for sorting & searching; writing direction; transliteration rules; rules for spelling out numbers; rules for segmenting text into graphemes, words, and sentences; keyboard layouts… Country information: language usage, currency information, calendar preference, week conventions,… Validity: Definitions, aliases, and validity information for Unicode locales, languages, scripts, regions, and extensions,…*
+ *Language Plural Rules*, ICU Project
  + https://www.unicode.org/cldr/cldr-aux/charts/29/supplemental/language_plural_rules.html
+ *A complete guide to ICU message format & syntax with examples*, Llya Kurowski (2024)
  + https://lokalise.com/blog/complete-guide-to-icu-message-format/
+ *ICU message format: Guide to plurals, dates & localization syntax*, Kinga Pomkala (2023), SimpleLocalize
  + https://simplelocalize.io/blog/posts/what-is-icu/
  + *ICU message format is the standard way developers handle plurals, dates, numbers, and other localized text in software. It's part of the internationalization (i18n) toolkit that ensures your messages are grammatically correct, culturally accurate, and easy to translate, no matter the language or region. By using ICU, you can avoid common localization bugs like “1 rooms” or incorrect date formats, while keeping translations consistent across all platforms. Used by Google, Microsoft, and countless frameworks like React Intl and Angular, ICU allows you to define all variations of a message in one place, making life easier for both developers and translators.*
+ *International Components for Unicode APIs*, IBM (2022)
  + https://www.ibm.com/docs/en/i/7.5.0?topic=category-international-components-unicode-apis
  + *The International Components for Unicode (ICU), IBM® i option 39, is a C and C++ library that provides Unicode services for writing global applications in ILE programming languages. ICU offers flexibility to extend and customize the supplied services, which include: ...*
+ *The Ultimate Guide to ICU Message Format*, Crowdin Blog (2022)
  + https://crowdin.com/blog/2022/04/13/icu-guide
  + *What Does ICU Stand for? As ICU documentation states, ICU means International Components for Unicode – a widely used set of C/C++ and Java libraries providing Unicode and globalization support for software and applications. ICU is released under a nonrestrictive open source license that is suitable for use with both commercial software and open source or free software.*
+ *Finally Doing Pluralization Right How the ICU plural syntax works*, Alan Allegret (2021)
  + https://medium.com/expedia-group-tech/finally-doing-pluralization-right-948e2e9d40bb
+ *A Practical Guide to the ICU Message Format*, Mohamed Ashour (2025), Phrase
  + https://phrase.com/blog/posts/guide-to-the-icu-message-format/
+ *Unicode and internationalization support*, Android API Docs
  + https://developer.android.com/guide/topics/resources/internationalization
  + *Android leverages the ICU library and CLDR project to provide Unicode and other internationalization support. This page's discussion of Unicode and internationalization support is divided into two sections: Android 6.0 (API level 23) and lower, and Android 7.0 (API level 24) and higher.*
+ *Java Localization – Formatting Messages*, Baeldung
  + https://www.baeldung.com/java-localization-messages-formatting
+ *10 UI Localization Best Practices for Developers*, Nimrod Kramer (2024)
  + https://daily.dev/blog/10-ui-localization-best-practices-for-developers
+ *Personal names around the world*, W3C
  + https://www.w3.org/International/questions/qa-personal-names
  + *How do people's names differ around the world, and what are the implications of those differences on the design of forms, databases, ontologies, etc. for the Web?*
+ *Implementing UI translation in SumatraPDF, a C++ Windows application*, Kowalcyzky\.info
  + https://blog.kowalczyk.info/a-vn0v/implementing-ui-translation-in-sumatrapdf-a-c-windows-application.html
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
+ *Integrating Localization Into Design Systems*, Rebecca Hemstand and Mark Malek
  + https://www.smashingmagazine.com/2025/05/integrating-localization-into-design-systems/
  + *Learn how two designers tackled the challenges of building a ==localization-ready design system== for a global audience. This case study dives into how Rebecca and Mark combined Figma Variables and design tokens to address ==multilingual design issues==, such as text overflow, RTL layouts, and font inconsistencies. They share key lessons learned and the hurdles they faced — including Figma’s limitations — along with the solutions they developed to create dynamic, scalable designs that adapt ==seamlessly across languages==, themes, and densities. If you’re navigating the complexities of internationalization in design systems, this article is for you.*
+ *Right-to-Left (RTL) Localization: The Definitive Guide*
  + https://centus.com/blog/right-to-left-languages-translation
+ *k-yak / stati18n Public* (2014)
  + https://github.com/k-yak/stati18n   
 
  
### Numbers and Mesurement

+ *International System of Units*, Wikipedia
  + https://en.wikipedia.org/wiki/International_System_of_Units
+ *SI base unit*, Wikipedia
  + https://en.wikipedia.org/wiki/SI_base_unit
+ *SI derived unit*, Wikipedia
  + https://en.wikipedia.org/wiki/SI_derived_unit
+ *Decimal separator*, Wikipedia
  + https://en.wikipedia.org/wiki/Decimal_separator
 + *Number formatting in Europe vs. the U.S.*
   + https://www.languageediting.com/number-formatting-europe-vs-us/
+ *Hindu–Arabic numeral system*, Wikipedia
  + https://en.wikipedia.org/wiki/Hindu%E2%80%93Arabic_numeral_system
+ *Arabic numerals*, Wikipedia
  + https://en.wikipedia.org/wiki/Arabic_numerals
+ *Eastern Arabic numerals*, Wikipedia
   + https://en.wikipedia.org/wiki/Eastern_Arabic_numerals
+ *Indian numbering system*, Wikipedia
  + https://en.wikipedia.org/wiki/Indian_numbering_system
+ *Chinese numerals*, Wikipedia
  + https://en.wikipedia.org/wiki/Chinese_numerals
+ *Japanese numerals*, Wikipedia
  + https://en.wikipedia.org/wiki/Japanese_numerals