---
title:       Internationalization i18n and Localization i10n concepts
label:       
description: Study about how to build an internationalization infrastructure for adding localization to a software without changing the source code allowing the contribution of non programmers.
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

```{figure} ![[pasted-image-1757439080745.jpg]]
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
  + Lazy loading locatization strings
  + Load only what is needed
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

+ Country Flag does not represent a language. For instance do not use the Brazilian flag for representing the Portuguese language.
+ There are more than one dialect and spelling of the same language. For instance, some words in American English and British English have different spellings, i.e *internationalization* (American English) and *internationalisation* (British English). That is the reason why country flags should not be used for representing a language.
+ Do not use IP address or user geographic location for selecting the language or locale used by a website. The language should be selected based on the user preference indicated by the http header [Accept-Language](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Accept-Language) and the graphicsuser interface should always have a button or selection box allowing the user to switch the language.
  
## Software Libraries

JavaScript
 + i18Next

Python
+ Gettext
    

## See also

+ *Internationalization and localization*, Wikipedia
  + https://en.wikipedia.org/wiki/Internationalization_and_localization
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
 