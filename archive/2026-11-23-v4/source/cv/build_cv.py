#!/usr/bin/env python3
"""Build matching Word and LaTeX CVs using only Python's standard library.

Edit source/cv/cv_data.json, then run this script from any directory.
The Word file is written to the repository root; LaTeX source is generated here.
"""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
import json
import re
import zipfile

SOURCE = Path(__file__).resolve().parent
ROOT = SOURCE.parents[1]
DATA = json.loads((SOURCE / 'cv_data.json').read_text())
NAVY = '00205B'

class Inline(HTMLParser):
    def __init__(self, value):
        super().__init__(); self.parts = []; self.bold = False; self.italic = False; self.url = None
        self.feed(value)
    def handle_starttag(self, tag, attrs):
        if tag in ('b', 'strong'): self.bold = True
        if tag in ('i', 'em'): self.italic = True
        if tag == 'a': self.url = dict(attrs)['href']
    def handle_endtag(self, tag):
        if tag in ('b', 'strong'): self.bold = False
        if tag in ('i', 'em'): self.italic = False
        if tag == 'a': self.url = None
    def handle_data(self, value):
        self.parts.append((value, self.bold, self.italic, self.url))

def tex_escape(s):
    return ''.join({'&':r'\&', '%':r'\%', '$':r'\$', '#':r'\#', '_':r'\_', '{':r'\{', '}':r'\}', '~':r'\textasciitilde{}', '^':r'\textasciicircum{}', '\\':r'\textbackslash{}'}.get(c, c) for c in s)

def rich_tex(value):
    out = []
    for text, bold, italic, url in Inline(value).parts:
        text = tex_escape(text)
        if bold: text = r'\textbf{' + text + '}'
        if italic: text = r'\textit{' + text + '}'
        if url: text = r'\href{' + url.replace('&', r'\&') + '}{' + text + '}'
        out.append(text)
    return ''.join(out)

rels = [('rStyles', 'styles', 'styles.xml', False), ('rFooter', 'footer', 'footer1.xml', False)]
def runs(value):
    result = []
    for text, bold, italic, url in Inline(value).parts:
        props = ('<w:b/>' if bold else '') + ('<w:i/>' if italic else '')
        if url: props += '<w:color w:val="305D82"/>'
        r = '<w:r><w:rPr>' + props + '</w:rPr><w:t xml:space="preserve">' + escape(text) + '</w:t></w:r>'
        if url:
            rid = 'rLink' + str(len(rels))
            rels.append((rid, 'hyperlink', url, True))
            r = '<w:hyperlink r:id="' + rid + '">' + r + '</w:hyperlink>'
        result.append(r)
    return ''.join(result)

def para(text, style='Normal', extra='', tail=''):
    return '<w:p><w:pPr><w:pStyle w:val="' + style + '"/>' + extra + '</w:pPr>' + runs(text) + tail + '</w:p>'

tex = [r'''\documentclass[10pt,letterpaper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{newtxtext}
\usepackage[margin=0.55in,top=0.48in,bottom=0.5in,footskip=18pt]{geometry}
\usepackage{xcolor,fancyhdr,hyperref}
\definecolor{navy}{HTML}{00205B}
\hypersetup{colorlinks=true,urlcolor=navy,pdftitle={Qicheng Zeng - Curriculum Vitae},pdfauthor={Qicheng Zeng}}
\pagestyle{fancy}\fancyhf{}\renewcommand{\headrulewidth}{0pt}
\fancyfoot[C]{\fontsize{8}{9}\selectfont\color{gray}Qicheng Zeng · Curriculum Vitae · Updated November 2026\quad\thepage/2}
\setlength{\parindent}{0pt}\setlength{\parskip}{4pt}
\newcommand{\cvsection}[1]{\par\vspace{8pt}{\color{navy}\bfseries\fontsize{11}{12}\selectfont #1}\par\nobreak\vspace{2pt}{\color{navy}\hrule height 0.4pt}\nobreak\vspace{4pt}}
\newcommand{\entry}[2]{\noindent #1\hfill #2\par}
\begin{document}
\fontsize{11}{13}\selectfont
''']
doc = []
for item in DATA:
    kind = item['kind']; value = item.get('text', '')
    if kind == 'name':
        tex.append(r'{\centering\color{navy}\fontsize{19}{21}\selectfont\bfseries ' + rich_tex(value) + r'\par}\vspace{2pt}')
        doc.append(para(value, 'Name'))
    elif kind == 'contact':
        tex.append(r'{\centering\fontsize{9}{10.5}\selectfont ' + rich_tex(value) + r'\par}')
        doc.append(para(value, 'Contact'))
    elif kind == 'section':
        tex.append(r'\cvsection{' + tex_escape(value.upper()) + '}')
        doc.append(para(value.upper(), 'Heading1'))
    elif kind == 'break':
        tex.append(r'\newpage')
        doc.append('<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="20" w:lineRule="exact"/></w:pPr><w:r><w:br w:type="page"/></w:r></w:p>')
    elif kind == 'row':
        tex.append(r'\entry{' + rich_tex(value) + '}{' + tex_escape(item.get('right', '')) + '}')
        doc.append(para(value, 'Row', tail='<w:r><w:tab/></w:r>' + runs(escape(item.get('right', '')))))
    elif kind == 'sub':
        tex.append(r'\vspace{-2pt}{\fontsize{10}{12}\selectfont\entry{' + rich_tex(value) + '}{' + tex_escape(item.get('right', '')) + '}}')
        doc.append(para(value, 'Sub', tail='<w:r><w:tab/></w:r>' + runs(escape(item.get('right', '')))))
    elif kind in ('pub', 'presentation'):
        tex.append(r'{\hangindent=12pt\hangafter=1 ' + rich_tex(value) + r'\par}')
        doc.append(para(value, 'Citation'))
    else:
        tex.append(rich_tex(value) + r'\par')
        doc.append(para(value))
tex.append(r'\end{document}')
(SOURCE / 'Qicheng_Zeng_CV.tex').write_text('\n'.join(tex))

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
declaration = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
styles = f'''<w:styles xmlns:w="{W}">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="22"/><w:color w:val="18212B"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="80" w:line="260" w:lineRule="exact"/><w:widowControl/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Name"><w:name w:val="Name"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:jc w:val="center"/><w:spacing w:after="60" w:line="440" w:lineRule="exact"/></w:pPr><w:rPr><w:b/><w:color w:val="{NAVY}"/><w:sz w:val="38"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Contact"><w:name w:val="Contact"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:jc w:val="center"/><w:spacing w:after="0" w:line="210" w:lineRule="exact"/></w:pPr><w:rPr><w:sz w:val="18"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="160" w:after="80" w:line="240" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="3" w:space="2" w:color="{NAVY}"/></w:pBdr><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:color w:val="{NAVY}"/><w:sz w:val="22"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Row"><w:name w:val="Row"/><w:basedOn w:val="Normal"/><w:pPr><w:keepLines/><w:tabs><w:tab w:val="right" w:pos="10656"/></w:tabs><w:spacing w:after="60"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Sub"><w:name w:val="Sub"/><w:basedOn w:val="Row"/><w:pPr><w:spacing w:after="60" w:line="240" w:lineRule="exact"/></w:pPr><w:rPr><w:sz w:val="20"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Citation"><w:name w:val="Citation"/><w:basedOn w:val="Normal"/><w:pPr><w:keepLines/><w:ind w:left="240" w:hanging="240"/></w:pPr></w:style>
</w:styles>'''
section = '<w:sectPr><w:footerReference w:type="default" r:id="rFooter"/><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="691" w:right="792" w:bottom="720" w:left="792" w:header="288" w:footer="360"/></w:sectPr>'
footer = f'<w:ftr xmlns:w="{W}"><w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:sz w:val="16"/><w:color w:val="666666"/></w:rPr><w:t>Qicheng Zeng · Curriculum Vitae · Updated November 2026     </w:t></w:r><w:fldSimple w:instr="PAGE"><w:r><w:t>1</w:t></w:r></w:fldSimple><w:r><w:t>/2</w:t></w:r></w:p></w:ftr>'
files = {
    'word/document.xml': f'<w:document xmlns:w="{W}" xmlns:r="{R}"><w:body>' + ''.join(doc) + section + '</w:body></w:document>',
    'word/styles.xml': styles,
    'word/footer1.xml': footer,
    'word/_rels/document.xml.rels': '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + ''.join('<Relationship Id="' + rid + '" Type="' + R + '/' + typ + '" Target="' + escape(target, quote=True) + '"' + (' TargetMode="External"' if external else '') + '/>' for rid, typ, target, external in rels) + '</Relationships>',
    '_rels/.rels': '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rDocument" Type="' + R + '/officeDocument" Target="word/document.xml"/></Relationships>',
    '[Content_Types].xml': '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>' + ''.join('<Override PartName="/word/' + f + '.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.' + t + '+xml"/>' for f, t in [('document', 'document.main'), ('styles', 'styles'), ('footer1', 'footer')]) + '</Types>',
}
with zipfile.ZipFile(ROOT / 'Qicheng_Zeng_CV.docx', 'w', zipfile.ZIP_DEFLATED) as z:
    for name, content in files.items(): z.writestr(name, declaration + content)
print('Built Qicheng_Zeng_CV.docx and Qicheng_Zeng_CV.tex')
