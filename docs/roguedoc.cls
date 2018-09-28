%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% roguedoc.cls
%
% (c) Rogue Robotics 2018
% Styling template for MATE Underwater Robotics Competition Technical
%      Documentation
%
% LaTeX file prepared by Eric Zheng, Mechanical Lead
%
% Notes:
%      Compile with XeLaTeX---there should be a provided build.sh script,
%           But you may find it easier to debug when running manually
%      You may need to compile twice for the footer to look right
%      This does not create a title page; draw that yourself---Adobe
%           Illustrator does the job well
%      Feel free to modify/distribute as you like, as long as you keep this
%           original header and credit Rogue Robotics for the design
%      Graphics are automatically taken from the ./images/ directory and
%           accept PDF and PNG files
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{roguedoc}[2018/05/12 MATE ROV Documentation]

\LoadClass[12pt]{article}  % MATE rubric specifies 12pt font size
\RequirePackage[margin=0.75in]{geometry}
\RequirePackage[T1]{fontenc}
\RequirePackage{threeparttable}
\RequirePackage{float}
\RequirePackage{color}
\RequirePackage{tikz}
\RequirePackage{everypage}
\RequirePackage{fontspec}
\RequirePackage{titling}
\RequirePackage{multicol}
\RequirePackage{siunitx}
\RequirePackage{graphicx}
\RequirePackage{caption}
\RequirePackage{subcaption}
\RequirePackage{colortbl}
\RequirePackage{etoolbox}
\RequirePackage{array}
\RequirePackage[skins]{tcolorbox}
\RequirePackage{hyperref}

\graphicspath{{./img/}}
\usetikzlibrary{calc}

% use Roboto font if installed
\setmainfont{Roboto}
\captionsetup[figure]{labelfont=bf, textfont=it, font=small}
\captionsetup[table]{labelfont=bf, textfont=it, font=small}

% fix vertical alignment in multicol table of contents
\patchcmd{\l@section}
  {\hfil}
  {\leaders\hbox{\normalfont$\m@th\mkern \@dotsep mu\hbox{.}\mkern \@dotsep     mu$}\hfill}
  {}{}
\renewcommand\tableofcontents{%
  \begin{multicols}{2}[\section*{\contentsname
  \@mkboth{%
    \MakeUppercase\contentsname}{\MakeUppercase\contentsname}}]%
    \@starttoc{toc}%
    \end{multicols}%
  }

% nice, matching theme colors for tables: orange for header, alternating grey for rows
\definecolor{light-grey}{gray}{0.9}
\definecolor{light-orange}{rgb}{1, 0.76, 0}

% fancy curvy ribbon, drawn in Adobe Illustrator
\newcommand{\colorhead}{
  \thispagestyle{empty}
  \begin{tikzpicture}[overlay, remember picture]
    \draw let \p1 = (current page.west), \p2 = (current page.east) in
      node[minimum width=\x2-\x1, minimum height=3cm, draw, rectangle, fill overzoom image=wave.pdf, draw=white, anchor=north west, align=left, text width=\x2-\x1] at ($(current page.north west)$) {};
  \end{tikzpicture}
}

% orange footer
\newcommand{\colorfoot}[1]{
  \thispagestyle{empty}
  \begin{tikzpicture}[overlay, remember picture]
    \draw let \p1 = (current page.west), \p2 = (current page.east) in
      node[minimum width=\x2-\x1, minimum height=1cm, draw, rectangle, fill=light-orange, draw=light-orange, anchor=south west, align=left, text width=\x2-\x1] at ($(current page.south west)$) {\quad #1};
  \end{tikzpicture}
}

% set up running header and footer
\AddEverypageHook{\colorhead}
\AddEverypageHook{\colorfoot{\sffamily\theauthor\hspace{4.75in}\thetitle~|~\thepage}}

% start page counter at 2 to accommodate the separate title page
\setcounter{page}{2}

% allow the use of \si{\dollar} for consistent unit formatting
\DeclareSIUnit{\dollar}{\$}

% initial table of contents page, including copyright message at the bottom
% if you want, you can override the regular copyright message with a custom one
% just use \setcopyright{...} before \roguetoc{}
\newcommand{\@copyright}{Content (c) \theauthor{} \the\year{}. Design (c) Rogue Robotics \the\year{}.}
\newcommand{\setcopyright}[1]{\renewcommand{\@copyright}{#1}}
\newcommand{\roguetoc}{
  \thispagestyle{empty}
  {\small
    \tableofcontents
    \vspace*{\fill}
    \textcolor{gray}{\@copyright}
  }
  \pagebreak
}
