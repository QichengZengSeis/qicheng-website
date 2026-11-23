# CV source

Edit `cv_data.json` to update the CV content. The builder uses Python 3's standard library; PDF generation requires TeX Live with `newtxtext`, `geometry`, `fancyhdr`, and `hyperref`.

From the repository root:

```sh
python3 source/cv/build_cv.py
pdflatex -interaction=nonstopmode -halt-on-error -output-directory . source/cv/Qicheng_Zeng_CV.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory . source/cv/Qicheng_Zeng_CV.tex
```

Current PDF and Word downloads are written to the repository root. The intermediate LaTeX file is generated beside the builder and is not tracked. Check the two-page PDF and Word layout after edits, and update the corresponding text in `index.html`.

Before revising a CV, preserve the current PDF, Word document, data, and builder in a new dated `archive/` folder and update its version history.
