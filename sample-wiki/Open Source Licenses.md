---
title:       Open Source Licenses
label:       oss-license       
description: Summary of open source licenses.

---

% Note that this is a definition list.
%

## Open Source Licences Overview

IP
  : Intelectual Property 

OSI 
  : Open Source Iniciative 
  
OSS
  : Open Source Software 
  : Software (Programa de Computador) de Codigo Aberto
  
FOSS 
  : Free and Open Source Sofware 
  : Software Livre e de Codigo Aberto
  
DRM 
  : Digital Rights Managment
  
APS 
  : Application Service Provider
  
SaaS 
  : Software-as-a-Service
  
SBIL
  : Software Bill of Materials 
  : List de Materiais de Software 
  
EULA (used by Closed Source Software)
  : End User License Agreement 
  : Contrato de Licensa de Usuario Final (PT)
  
Open Source Licenses
  : Permissive Licenses and Copyleft Licenses 

Permissive Licenses 
  : Allows modification and distribution of software with few restrictions. This kind of license is more popular among companies that wishes to use the software commercially or to keep their software modifications *closed source*. Example: BSD and MIT licenses.
  
Source Avaiable Licenses (Not Open Source)
  : Despite that this type of license may look like an open source license as the the source code is available. Licenses of this kind may have many commercial use restrictions of the software, what makes this license not open source. Example: MongoDB no-SQL document database switched from AGPL to SSPL (Server Side Public License), which was introduced by MongoDB itself. 
  
Dual License Model
  : Software released, often under a copyleft license and a commerical license, which removes the restriction of the copyleft license. Example: Qt5.0 library by Qt Company, which is available under LGPL and commercial license allowing static linking by closed source software.
  
Open Core Model 
  : Software under open source license with other features closed source or paywalled.
  
Copyleft Linceses
  : Any version of modification of the software must be distributed under the same copyleft license. This license style is not favored by companies that need to keep their software modification proprietary.
  
MIT License (Permissive)
  : Introduced by MIT - Massachussets Institute of Technology in the 1980s. Used by React JS front-end framework and Ruby programming language. The only requirement of this license is to include the **copyright notice** in derivative works. Drawback: the license grants any patent rights, what creates legal uncertainty for software that depends on **patented technologies**.
  
Apache 2.0 License (Permissive)
  : Similar to MIT license, but it grants patent rights to any user of a sofware released under MIT license.
  
BSD-2 Clause License (Permissive)
  : Similar to MIT's license, but requires that a copy of the BSD-2 license copyright notice to be included in the source code of derivativ works and compiled binaries.
  
BSD-3 Clause License (Permissive)
  : Introduces an additional no-endorsement clause to BSD-2 license, which restricts the use of the **copyright holders** names and contributors for promotional use in derivative works.
  
GPL v2.0 (Copyleft)
   : GPL v.20 and the GPL license family were introduced by FSF (Free Software Foundation) in 1989. GPL v2.0 and other licneses of the same family require all derivative work to released under the same license. Example: **Wordpress** PHP blogging platform and **Linux Kernel**, created by Linus Torvalds is released under GPL 2.0 license.

GPL v3.0 (Copyleft)
  : License similar to GPL v2.0 introduced in 2007. This license forbids "Tivoization", where hardware manufactures blocks user attempt to install modified versions of an open source software under GPLv3.0 license using **DRM (Digital Rights Management)**. The purpose of GPL v3.0 license is to guarantee that works of contributors will not be used in **proprietary software**. However, this license does not require disclosing the source code or releasing the software under the same license if the software is run on the server-side on the cloud.
  
LGPL - GNU Lesser General Public License (Weak Copyleft) 
  : This license is mostly used by compilers and native code software libraries. Derivative works can be released and distributed as closed source and are allowed to dynamic link against the libraries, unless the library code is modified or the software static link against the library. 

AGPL - GNU Afero Public License (Copyleft)
  : Requires source code disclosure of any software modification even if it is never distributed and run on the server side. The AGPL license was introduced for addressing the cloud loophole in the GPL 3.0 license, which does not mandate release of source code if it the sofware is run on the server side or on the cloud. Big tech companies have been exploiting the cloud loophole of GPL3.0 to take way open source software to provide SaaS software as service and keep their modifications closed source. The AGPL license is mostly used by server software and databases. 
  
  
Unlicense 
  : Public Domain License. Used by SQLite embedded database engine.
  
CC0-1.0 
  : Creative Commons 1.0 - public domain dedication tool used mostly by **creative works**.

## Summary 



- MIT, BSD and ISC => "Permissive"
   - Basic Meaning: Do whatever you want, just do not sue me.
   - Give us credit by copying the license: YES
   - One of the most used licenses.
   - Known softwares with those licenses: Free BSD operating system.
- Apache
   - Basic Meaning:"Do whatever you want with the software, just do not sue me."
   - Give us credit by copying the license: YES
- GPL licenses (GPLv3, GPLv2, LGPL, Affero GPL)
   - You must provide the source code alongisde a copy of the license giving credit to the authors if you make any derived work of the code.
   - You can distribute your program with GPL compiled libraries without the source code if you don't change the library code and not static link with your application.
   - Many companies have policies against using GPL libraries due to the legal complexity which comes with their use.
   - Some GPL Libraries have dual license, GPL and commercial which allows static linking native libraies.
   - Known softwares: Linux, GLIBC - Linux's libraries, GNU project's softwares, MediaWiki (Wikipedia's engine).
- Unlicense - Public Doman
   - You have no obligations, just don't sue the author. All risks and liabilities are yours.
   - It is not required to give credit, but it costs nothing and it is always nice.
   - Known Product with Unlicense: SQLite 

## See Also
     

+ *Free Software Licensing Resources*
  + https://www.fsf.org/licensing/education
+ *Right to root access*
  + https://medhir.com/blog/right-to-root-access
+ *Right to root access*
  + https://news.ycombinator.com/item?id=42677835
+ *Open source licenses: Everything you need to know*, Techchrunch
  + https://techcrunch.com/2025/01/12/open-source-licenses-everything-you-need-to-know/
+ *A compendium of "open-source" licenses*
  +  https://github.com/ErikMcClure/bad-licenses
+ *Affirmation of the Open Source Definition* (2019)
  + <https://opensource.org/blog/OSD_Affirmation>
+ *Open source licensing and why we're changing Plausible to the AGPL license*
  + <https://plausible.io/blog/open-source-licenses>
+ *Open Source Software Licenses 101: The AGPL License*
  + <https://fossa.com/blog/open-source-software-licenses-101-agpl-license/>
+ *Understanding the SaaS Loophole in GPL*
  + <https://www.revenera.com/blog/software-composition-analysis/understanding-the-saas-loophole-in-gpl/>
+ *The copyleft effect in cloud computing*
  + <https://www.lexology.com/library/detail.aspx?g=68b1ae41-73a6-4b1f-8ae0-23d68e61fdeb>
+ *The essential guide to AGPL compliance for tech companies* (2024)
  + <https://vaultinum.com/blog/essential-guide-to-agpl-compliance-for-tech-companies>
+ *Closing AGPL cloud services loop-hole: a MongoDB approach*
  + <https://ipkitten.blogspot.com/2019/02/closing-agpl-cloud-services-loop-hole.html>
- *Software patents are evil, but BSD+Patents is probably not the solution - Wes McKinney*
  + http://wesmckinney.com/blog/react-bsd-patents/
- *If you’re a startup, you should not use React (reflecting on the BSD + patents license)*
  + https://medium.com/@raulk/if-youre-a-startup-you-should-not-use-react-reflecting-on-the-bsd-patents-license-b049d4a67dd2
- *BSD licenses - Wikipedia*
  + https://en.wikipedia.org/wiki/BSD_licenses)
- *Business Source License*, Wikipedia
  + https://en.m.wikipedia.org/wiki/Business_Source_License + *The Business Source License (SPDX id BUSL[1]) is a software license which publishes source code but limits the right to use the software to certain classes of users. The BUSL is not an open-source license,[1] but it is source-available license that also mandates an eventual transition to an open-source license. This characteristic has been described as a compromise between traditional proprietary licenses and open source.[2] The originator of the BUSL is MariaDB Corporation AB, where it is used for the MaxScale product, not for the flagship MariaDB.[3]*
+ *Server Side Public License (SSPL) vs. Open Source: A Guide for Investors*
  + https://www.alphanome.ai/post/server-side-public-license-sspl-vs-open-source-a-guide-for-investors
+ *Unveiling Server Side Public License 1.0: Beyond the Code – A Holistic Exploration*
  + https://dev.to/laetitiaperraut/unveiling-server-side-public-license-10-beyond-the-code-a-holistic-exploration-54i5
+ *The Business Source License*, Matt Rickard
  + https://blog.matt-rickard.com/p/the-business-source-license