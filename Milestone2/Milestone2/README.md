# Milestone 2 — AI-Powered Skill Gap Analyzer

Summary
-------
This milestone implements a Streamlit app that extracts skills from a Resume and a Job Description using a multi-method NLP pipeline, computes semantic similarity using Sentence-BERT, and provides a set of visualizations and data-export options to analyze skill gaps and overlaps.

Key Features (Milestone 2)
--------------------------
- Multi-method skill extraction pipeline (invoked via `extract_skills_multi_method`) to collect candidate skills and classify them as `Technical` or `Soft`.
- BERT-based semantic similarity matrix (via `calculate_similarity_matrix`) to compare resume skills against JD skills.
- Visualizations (Plotly + Plotly Graph Objects):
  - Radar chart comparing per-document skill-type distribution (each dataset normalized to percentages so each sums to 100%).
  - Skill type distribution bar charts (counts + percent labels).
  - Overall skill gap bar chart (Matched / Needed / Extra counts).
  - Top-N skills horizontal bar charts (frequency counts, colored by skill type).
- Styled skill tag display with hover tooltips and metrics (counts of matched, needed, extra skills).
- Export options to download extracted data as CSV.
- Placeholder and notes in the sidebar for future custom NER/annotation training (Prodigy/doccano, spaCy/BERT fine-tuning).

Files of interest
-----------------
- `app.py` — Main Streamlit application. Contains UI, file upload, extraction orchestration, and charting functions.
- `skill_analyzer_core.py` — Core logic (skill extraction functions and similarity matrix calculation). (Not modified by this README.)

Dependencies
------------
Recommended Python packages (example):

- streamlit
- pandas
- plotly
- plotly-express
- pdfminer.six
- python-docx
- sentence-transformers
- scikit-learn
- numpy

You can install them (example):

```powershell
python -m pip install streamlit pandas plotly pdfminer.six python-docx sentence-transformers scikit-learn numpy
```

Running the app
---------------
From the project root (where `app.py` is located):

```powershell
streamlit run app.py
```

Usage
-----
1. Upload a Resume and a Job Description (supported formats: `.txt`, `.pdf`, `.docx`).
2. Click "Analyze Skills".
3. Inspect the visualizations and metrics:
   - Radar chart: shows the proportion of skill types in each document (percentages per document).
   - Skill Type Distribution: bar charts with counts and percent labels per document.
   - Overall Skill Gap: counts of matched, needed, and extra skills.
   - Top Skills Comparison: top N skill frequency lists for each document.
4. Download the extracted skills report as CSV if needed.

What the charts represent (short)
--------------------------------
- Radar chart: for each document (Resume / JD) the chart shows the percentage of skills that fall into each skill type category (Technical / Soft / any other categories found). Each dataset is normalized so their values sum to 100% separately.
- Top skills bar charts: the length of a bar is the number of times the skill appears in the document (frequency). Bars are colored by skill type.
- Skill type distribution: raw counts of skills by type, with percent-of-document annotated.

Known limitations & notes
-------------------------
- Skill extraction quality depends on `skill_analyzer_core.py` methods and quality of input text.
- Small documents with only one or two skills will produce charts with low granularity; radar and percent charts are still normalized per-document.
- The app currently treats the first matching type for a skill when assigning type in Top-N charts.

Next steps / Improvements
------------------------
- Add a requirements.txt and automated environment setup.
- Improve aggregation: unify synonyms and aliases before counting (e.g., 'SQL' vs 'Sql').
- Add interactive pairing/mapping UI for semantic matches and manual corrections.
- Implement a full annotation interface and model fine-tuning pipeline for custom NER.

License
-------
MIT License — adapt and reuse as needed.

Contact
-------
This repository is part of a Milestone project. For questions about the implementation details, check `app.py` and `skill_analyzer_core.py`.
