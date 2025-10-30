# Infosys-Skill-Gap-AI-Analyzing-Resume-and-Job-Post-for-Skill-Gap

SkillGapAI: Automated Skill Gap Analysis Using NLP and BERT
Project Overview
SkillGapAI is an intelligent web application that automates the extraction of skills from resumes and job descriptions and performs semantic skill gap analysis. Leveraging spaCy for Named Entity Recognition (NER), Sentence-BERT (SBERT) for skill embedding, and Streamlit for interactive visualization, the platform simplifies recruitment analytics and candidate assessment.

Features
Upload resumes and job descriptions in PDF, DOCX, or TXT formats

Automatic parsing, cleaning, and text extraction

Extraction of technical and soft skills using customized NLP models

Semantic similarity matching of skills using SBERT embeddings

Identification and ranking of skill gaps

Interactive dashboard with charts and heatmaps

Export analysis reports as CSV and PDF files


**********************************************************
# 🎯 AI Skills Compass — Semantic Skill Gap Analyzer

## Overview

The **AI Skills Compass** is a Streamlit application designed to perform a comprehensive skill gap analysis between an individual's resume (or provided skill list) and a target job description (JD). It leverages **Sentence-BERT** embeddings to calculate **semantic similarity**, allowing it to identify matches, partial overlaps, and critical skill gaps based on the *meaning* of the skills, not just exact keyword matches.

The application generates interactive visualizations, detailed reports, and personalized growth roadmaps to guide users in bridging their identified skill gaps.

## ✨ Key Features

* **Semantic Similarity Matching:** Uses the `all-MiniLM-L6-v2` Sentence-BERT model for accurate, contextual skill comparison.
* **Flexible Input:** Supports **Manual Entry**, **JSON upload** (for structured skill lists), and **PDF upload** (for basic text and keyword extraction).
* **Multi-Level Analysis:** Classifies matches into **Strong**, **Partial**, and **Missing** based on configurable similarity thresholds.
* **Interactive Visualizations:** Generates heatmaps, distribution charts, and radar plots using Plotly for deep insights.
* **Growth Roadmap:** Provides **prioritized learning paths** and resource recommendations for missing skills.
* **Data Export:** Allows export of results in **TXT**, **CSV**, and **JSON** formats.
* **Customizable Settings:** Users can adjust the core similarity thresholds in the `Preferences` tab.

---

## 🚀 Getting Started

### Prerequisites

You need Python 3.8+ installed on your system.

### Installation

Clone the repository (if applicable) and install the necessary Python libraries.

```bash
# 1. Clone the repository (Optional, if hosted)
# git clone <repository_url>
# cd ai-skills-compass

# 2. Install core dependencies
pip install streamlit numpy pandas scikit-learn plotly sentence-transformers

# 3. Install pypdf for PDF processing
pip install pypdf

# 4. Save the provided code as app.py

TO run :streamlit run app.py
use complete folder for final code to run.
