# Qicheng Zeng — Seismology

Academic website and curriculum vitae of **Qicheng Zeng**, Postdoctoral Research Associate in the Department of Earth, Environmental and Planetary Sciences at Rice University.

**Website:** [sites.google.com/view/qichengzeng](https://sites.google.com/view/qichengzeng/)

Research spans environmental seismology, structural imaging of volcanoes and sedimentary basins, seismic observations of geomorphic processes, and temporal changes in seismic velocity associated with thermoelastic and tidal strains and diagenesis.

## Curriculum vitae

- [Download the two-page PDF CV](Qicheng_Zeng_CV.pdf)
- [Download the editable Word CV](Qicheng_Zeng_CV.docx)

The CV and website include publications, research interests, education and appointments, field experience, teaching, professional service, awards, and internships. The waterfall paper, *Seasonal ice breakup increases the seismically measured force of waterfalls*, is in press with **Science Advances**.

## Repository contents

| File | Purpose |
| --- | --- |
| `index.html` | Website source, including embedded images and links to both CV formats |
| `cv_data.json` | Editable content used to generate both CV formats |
| `build_cv.py` | Python script that generates the Word document and LaTeX source |
| `Qicheng_Zeng_CV.tex` | LaTeX source for the PDF |
| `Qicheng_Zeng_CV.pdf` | Print-ready CV, verified as two pages |
| `Qicheng_Zeng_CV.docx` | Editable Word CV, formatted for two US Letter pages |
| `Qicheng_Zeng_CV_2026_Final_v2.pdf` | Updated copy retained for existing download links |

## Updating the CV and website

Edit `cv_data.json`, then regenerate the files with Python 3 and a TeX Live installation containing `newtxtext`, `geometry`, `fancyhdr`, and `hyperref`:

```sh
python3 build_cv.py
pdflatex -interaction=nonstopmode -halt-on-error Qicheng_Zeng_CV.tex
pdflatex -interaction=nonstopmode -halt-on-error Qicheng_Zeng_CV.tex
cp Qicheng_Zeng_CV.pdf Qicheng_Zeng_CV_2026_Final_v2.pdf
```

Update the corresponding text in `index.html` as well. Check that the PDF remains two pages, review the Word pagination in your editor, and verify both download links before publishing. Word pagination may vary if fonts or page settings are changed. Google Sites publishing is managed separately unless that site embeds the GitHub-hosted page.

Contact: [qz58@rice.edu](mailto:qz58@rice.edu) · [Google Scholar](https://scholar.google.com/citations?user=TfB7z8sAAAAJ) · [ORCID](https://orcid.org/0000-0001-6937-7875)
