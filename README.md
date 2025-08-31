# Machine Learning Engineer certification

This repository contains all projects completed as part of the RNCP35288 certification - Level 6 - Machine Learning Engineer

## List of projects

Block 1: Building and feeding a data management infrastructure
- Kayak Project (Data Collection & Management Project)

Block 2: Exploratory, descriptive, and inferential data analysis
- Speed Dating Project (Exploratory Data Analysis Project)
- Steam Project (Big Data Project)

Block 3: Predictive analysis of structured data using artificial intelligence
- Walmart Sales Project (Supervised Machine Learning)
- Conversion Rate Challenge Project (Supervised Machine Learning)
- The North Face Ecommerce Project (Unsupervised Machine Learning)

Block 4: Predictive analysis of unstructured data using artificial intelligence
- AT&T Project (Deep Learning Project)

Block 5: Industrialization of a machine learning algorithm and automation of decision-making processes
- Getaround Project (Deployment Project)

Block 6: Data management project management
- Anime Recommendation Engine Project (Final Project - NLP and recommendation systems)

## Getting Started

1. Clone the repository

```bash
https://github.com/qxzjy/dsfs-ft-34-certification.git
cd dsfs-ft-34-certification
```

2. Create a Python environment

```bash
python -m venv dsfs_env
source dsfs_env/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Details

Block 2 Steam: Project carried out on Databricks with PySpark. See the project README to access Databricks notebooks.

## Repository Structure

```
.
├── BLOCK_1/
|   └── 01_KAYAK_BOOKING/
│       ├── data/
│       ├── notebooks/
│       ├── src/
│       └── README.md
├── BLOCK_2/
│   ├── 01_TINDER_SPEED_DATING/
│   |   ├── data/
│   |   ├── notebooks/
│   |   └── README.md
|   └──  02_STEAM/
│       ├── data/
│       └── README.md
├── BLOCK_3/
│   ├── 01_SUPERVISED_ML/
│   |   ├── 01_WALLMART_SALES/
│   |   |   ├── data/
│   |   |   ├── notebooks/
│   |   |   └── README.md
│   |   └──  02_CONVERSION_RATE_CHALLENGE/
│   |       ├── data/
│   |       ├── notebooks/
│   |       └── README.md
|   └── 02_UNSPERVISED_ML/
|       └── 01_NORTH_FACE_ECOMMERCE/
│           ├── data/
│           ├── notebooks/
│           └── README.md
├── BLOCK_4/
|   └── 01_AT&T_SPAM_DETECTOR/
│       ├── data/
│       ├── notebooks/
│       └── README.md
├── BLOCK_5/
|   └── 01_GETAROUND/
│       ├── data/
│       ├── fastapi/
│       ├── mlflow/
│       ├── notebooks/
│       ├── streamlit/
│       └── README.md
├── BLOCK_6/
|   └── anime-recommendation-engine/
│       ├── notebooks/
│       ├── streamlit/
│       └── README.md
├── README.md
└── requirements.txt
```

## Authors

[Maxime RENAULT](https://github.com/qxzjy)