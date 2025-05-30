% This template aims to simplify and improve the (Xe)LaTeX template
% provided by the EPFL. Original template by EPFL. Rewritten
% template by Daan Zwaneveld (https://dzwaneveld.github.io). EPFL
% adapted template by Batuhan Faik Derinbay.
% (https://github.com/batuhanfaik/EPFL-Report-Template)
%
% This template is available under CC BY-NC 4.0. For more information,
% see https://creativecommons.org/licenses/by-nc/4.0/. No attribution
% is required in reports/theses created using this template.
%
%% ----------------------------------------------------------------------
%%    Setting up the class, main packages and basic definitions
%% ----------------------------------------------------------------------

%% Class is based on the default book class and options will be passed
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{epflreport}[17-12-2022 v1.1 EPFL Report Class]

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{book}}
\ProcessOptions\relax
\LoadClass[10pt,oneside]{book}

%% Main packages in the document --- Some are imported later in the class file
\RequirePackage{mathtools}  % Mathematical tools to use with amsmath
\RequirePackage{amssymb}    % Extended symbol collection
\RequirePackage{siunitx}    % Comprehensive (SI) units package

\RequirePackage{tabularx}   % Tabulars with adjustable-width columns
\RequirePackage{booktabs}   % Publication quality tables
\RequirePackage{longtable}  % Allow tables to flow over page boundaries
\RequirePackage{multirow}   % Create tabular cells spanning multiple rows

\RequirePackage{graphicx}   % Enhanced support for images
\RequirePackage{float}      % Improved interface for floating objects
\RequirePackage[labelfont=bf,justification=centering,footnotesize]{caption} % Captions
\RequirePackage{subcaption} % Support for sub-captions
\RequirePackage{pdfpages}   % Include PDF documents

\RequirePackage[pdfusetitle,hidelinks]{hyperref} % Extensive support for hypertext
\RequirePackage[noabbrev]{cleveref} % Intelligent cross-referencing
\RequirePackage{xcolor}     % Driver-independent color extensions
\RequirePackage{tikz}       % Create PostScript and PDF graphics
\RequirePackage{xspace}     % Define commands that appear not to eat spaces
\RequirePackage{microtype}  % Refinements towards typographical perfection

\RequirePackage{geometry}   % Customize document dimensions
\RequirePackage{titlesec}   % Select alternative section titles
\RequirePackage{titletoc}   % Alternative headings for toc
\RequirePackage{fancyhdr}   % Control of page headers and footers
\RequirePackage{enumitem}   % Control layout of itemize, enumerate, description
\RequirePackage{etoolbox}   % Toolbox of programming facilities
\RequirePackage{iftex}      % Adds if-else statements to support multiple compilers
\RequirePackage{datetime}   % Change format of \today

%% Establish commands for the subtitle, subject, affiliation, cover image and table of authors
\newcommand*{\subtitle}[1]{\def\@subtitle{#1}}
\newcommand*{\subject}[1]{\def\@subject{#1}}
\newcommand*{\affiliation}[1]{\def\@affiliation{#1}}
\newcommand*{\coverimage}[1]{\def\@coverimage{#1}}
\newcommand*{\covertable}[1]{\def\@covertable{#1}}

%% Scale the margins to be slightly smaller than default (.7)
\geometry{a4paper,hscale=0.75,vscale=0.8}

%% ----------------------------------------------------------------------
%%    Setting up the fonts
%% ----------------------------------------------------------------------

\ifPDFTeX
%% With pdfLaTeX, use Paletino as the main font and Roboto Slab as title fonts
\RequirePackage[T1]{fontenc}  % Select T1 font encoding
\RequirePackage{newpxtext}    % Palatino-like font...
\RequirePackage{newpxmath}    % ...with support for mathematics

\newcommand{\titlestyle}{\fontfamily{RobotoSlab-TLF}\fontseries{light}\selectfont}
\newcommand{\largetitlestyle}{\fontfamily{RobotoSlab-TLF}\fontseries{thin}\selectfont}
\else
%% If XeLaTeX or LuaLaTeX is set as the compiler, the EPFL house style fonts are used
\RequirePackage{fontspec} % Advanced font selection

%% Use SuisseIntl as the main font
\newfontfamily\suisseintl{SuisseIntl}
[Path=layout/epfl/fonts/suisse-intl/,
    Extension=.ttf,
    UprightFont=*-Regular,
    BoldFont=*-Bold,
    ItalicFont=*-RegularItalic,
    BoldItalicFont=*-BoldItalic,
    Ligatures=TeX]

%% Adding SuisseIntl as the main font and supplementary fonts
\setmainfont{SuisseIntl}
[Path=layout/epfl/fonts/suisse-intl/,
    Extension=.ttf,
    UprightFont=*-Regular,
    BoldFont=*-Bold,
    ItalicFont=*-RegularItalic,
    BoldItalicFont=*-BoldItalic]
\setmathsf{SuisseIntl}
[Path=layout/epfl/fonts/suisse-intl/,
    Extension=.ttf,
    UprightFont=*-Regular,
    BoldFont=*-Bold,
    ItalicFont=*-RegularItalic,
    BoldItalicFont=*-BoldItalic]
\setmathtt{SuisseIntl}
[Path=layout/epfl/fonts/suisse-intl/,
    Extension=.ttf,
    UprightFont=*-Regular,
    BoldFont=*-Bold,
    ItalicFont=*-RegularItalic,
    BoldItalicFont=*-BoldItalic]
\setsansfont{SuisseIntl}
[Path=layout/epfl/fonts/suisse-intl/,
    Extension=.ttf,
    UprightFont=*-Regular,
    BoldFont=*-Bold,
    ItalicFont=*-RegularItalic,
    BoldItalicFont=*-BoldItalic]
\setmonofont{SuisseIntlMono}
[Path=layout/epfl/fonts/suisse-intl-mono/,
    Scale=0.9,
    LetterSpace=-6,
    Extension=.ttf,
    UprightFont=*-Regular,
    BoldFont=*-Bold]

\newfontfamily\titlestyle[Path=layout/epfl/fonts/suisse-intl/,Ligatures=TeX]{SuisseIntl-Bold.ttf}
\newfontfamily\largetitlestyle[Path=layout/epfl/fonts/suisse-intl/,Ligatures=TeX]{SuisseIntl-SemiBold.ttf}
\newfontfamily\subtitlestyle[Path=layout/epfl/fonts/suisse-intl/,Ligatures=TeX]{SuisseIntl-Thin.ttf}
\newfontfamily\subjectstyle[Path=layout/epfl/fonts/suisse-intl/,Ligatures=TeX]{SuisseIntl-Regular.ttf}
\newfontfamily\quotefont[Path=layout/epfl/fonts/suisse-intl-mono/,Ligatures=TeX]{SuisseIntlMono-Regular.ttf}

%% Changing the quote environment to use SuissIntlMono
\AtBeginEnvironment{quote}{\quotefont}
\fi

%% ----------------------------------------------------------------------
%%    Formatting the titles and table of contents
%% ----------------------------------------------------------------------

%% Format the chapter titles and spacing
\titleformat{\chapter}[display]
{\flushright}
{\fontsize{96}{96}\selectfont\largetitlestyle\thechapter}
{0pt}
{\Huge\titlestyle}
\titlespacing*{\chapter}{0pt}{0pt}{2\baselineskip}

%% Format the section titles and spacing
\titleformat{\section}
{\Large\titlestyle\bfseries}
{\thesection.}
{5pt}
{}
\titlespacing*{\section}{0pt}{\baselineskip}{0pt}

%% Format the subsections titles and spacing
\titleformat{\subsection}
{\large\titlestyle\bfseries}
{\thesubsection.}
{5pt}
{}
\titlespacing*{\subsection}{0pt}{\baselineskip}{0pt}

%% Format the subsubsections titles and spacing
\titleformat{\subsubsection}
{\titlestyle\bfseries}
{}
{0pt}
{}
\titlespacing*{\subsubsection}{0pt}{\bigskipamount}{0pt}

%% Reduce the vertical white space between chapters in the table of contents
\dottedcontents{chapter}[1.5em]{\vspace{0.5\baselineskip}\bfseries}{1.5em}{0pt}

%% ----------------------------------------------------------------------
%%    Formatting the header and footer
%% ----------------------------------------------------------------------

%% Format the header and footer of 'plain' pages
\fancypagestyle{plain}{%
    \fancyhf{}
    \renewcommand{\headrulewidth}{0pt}
    \fancyfoot[C]{\titlestyle\thepage}}

%% Format the header and footer of 'fancy' pages (based on twoside option)
\if@twoside
\fancyhf{}
\fancyhead[LE,RO]{\titlestyle\thepage}
\fancyhead[RE]{\titlestyle\nouppercase{\leftmark}}
\fancyhead[LO]{\titlestyle\nouppercase{\rightmark}}
\RequirePackage{emptypage} % Remove header and footer on empty pages
\else
\fancyhf{}
\fancyhead[R]{\titlestyle\thepage}
\fancyhead[L]{\titlestyle\nouppercase{\rightmark}}
\fi

\pagestyle{fancy} % Set the package defaults and the additional changes as the style

%% ----------------------------------------------------------------------
%%    Setting up the \makecover command for the cover page
%% ----------------------------------------------------------------------

\newcommand*{\makecover}{
%% Use the Tikz library positioning and clear the page header and footer
    \usetikzlibrary{positioning}
    \thispagestyle{empty}

%% Construct the cover page with Tikz
    \begin{tikzpicture}[overlay,remember picture]

        %% Add the cover image
        \node[above=0,inner sep=0] at (current page.south) {%
            \includegraphics[width=\paperwidth]{\@coverimage}};

        %% Add the affiliation on the left
        \node[rotate=0,above right=1.8mm and 7mm] at (current page.south west) {%
            \ifdefvoid{\@affiliation}{}{\fontsize{8}{9.8}\selectfont\color{white}\@affiliation}};

        %% Add the logo in the bottom left
        \node[above right=10mm] at (current page.south west) {%
            \includegraphics[width=0.35\linewidth]{layout/tristan-logo.jpg}};

        %% Add the banner with the title, subtitle, subject and author(s)
        \node[below=2cm,fill=black!80,minimum width={\paperwidth},inner ysep=25pt,opacity=0.4,text opacity=1] at (current page.north) {%
            \begin{minipage}{0.9\paperwidth}
                %% Format and add the title
                \color{title}\raggedright\largetitlestyle\fontsize{50}{50}\selectfont%
                \@title \\[0.5ex]
                %% Format and add (optional) subtitle and subject
                \color{white}\titlestyle\fontsize{22}{22}\selectfont%
                \ifdefvoid{\@subtitle}{}{\@subtitle \\[2.5ex]}%
                \ifdefvoid{\@subject}{}{\@subject \\[0.5ex]}
                %% Format and add author or table of authors
                \largetitlestyle\fontsize{20}{24}\selectfont%
                \ifdefvoid{\@covertable}{\@author}{\@covertable}
            \end{minipage}};

    \end{tikzpicture}
    \newpage
}

%% ----------------------------------------------------------------------
%%    Setting up listings
%% ----------------------------------------------------------------------

\RequirePackage{listings} % Typeset source code listings

\lstset{
    basicstyle=\ttfamily\footnotesize,  % Style of the font that is used for the code
    backgroundcolor=\color{gray!10},    % Background color
    keywordstyle=\color{red!75!black},  % Keyword style
    stringstyle=\color{green!40!black}, % String style
    commentstyle=\color{blue!30!black}, % Comment style
    numbers=left,                       % Add line numbers on the left side
    numbersep=5pt,                      % Decrease distance between line numbers and code
    numberstyle=\tiny,                  % Line number style
    breaklines=true,                    % Line break automatically
}
