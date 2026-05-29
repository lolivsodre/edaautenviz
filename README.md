# Executive Summary
Jane Austen remains one of the most adapted authors in history. This project investigates how her works have been reinterpreted across media, decades, and adaptation formats using web scraping, data cleaning, exploratory analysis, and data visualization.

# Business Question
How have Jane Austen's works been adapted over time, and what does the evolution of adaptation formats reveal about her cultural relevance?

# Metodology
1. Web Scraping
2. Data Cleaning
3. Feature Engineering
4. Exploratory Data Analysis
5. Data Visualization
6. Insight Generation

# Dataset Construction
The dataset was built through five main steps. First, adaptation records were extracted from online sources using web scraping. Each entry was collected with key information such as title, year, source work, medium, and adaptation type.
Next, titles were standardized to avoid duplicates caused by spelling variations, translations, or formatting differences. The adaptations were then classified by medium, such as film, TV miniseries, theatre, web series, or streaming.
Each record was also classified as either a direct adaptation, when it closely followed Austen’s original work, or a loose adaptation, when it reinterpreted the story through new settings, characters, or contexts.
Finally, a new variable, decade, was created from the release year to support historical analysis and visualize adaptation trends over time.

jane-austen-adaptations-analysis/

│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_webscraping.ipynb
│   ├── 02_cleaning.ipynb
│   ├── 03_analysis.ipynb
│
├── visualizations/
│   ├── 01_obras.png
│   ├── 02_decadas.png
│   ├── ...
│
├── src/
│   ├── scraping.py
│   ├── cleaning.py
│   └── analysis.py
│
├── README.md
└── requirements.txt
