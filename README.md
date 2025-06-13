# Template 🚗

## Description

Insert description

## Web pages

[Web dashboard](https://qxzjy-get-around-streamlit.hf.space/) (Streamlit)\
[Pricing API](https://qxzjy-get-around-fastapi.hf.space/docs) (FastAPI) \
[ML Server](https://qxzjy-get-around-mlflow.hf.space/#/experiments/1) (MLFlow)


## Getting Started

### Project structure

```
.
├── data/
├── fastapi/
│   ├── src/
│   ├── Dockerfile
│   ├── README.md
│   └── requirements.txt
├── mlflow/
│   ├── ml/
│   ├── Dockerfile
│   ├── README.md
│   └── requirements.txt
├── notebooks/
├── fastapi/
│   ├── src/
│   ├── Dockerfile
│   ├── README.md
│   └── requirements.txt
├── README.md
└── requirements.txt
```

### Dependencies

In order to run it locally, a few things are required.

Librairie : `pandas`, `mlflow`, `scikit-learn`, `xgboost`, `plotly`, `streamlit`, `fastapi`, `numpy`, `pydantic`

Software : `docker`

Environment variables

### Installing

1. Clone the repo
```shell
git clone https://github.com/qxzjy/dsfs-ft-34-certification.git
cd dsfs-ft-34-certification/BLOCK_5/01_GETAROUND
```

2. Create an environment
```shel
# Using conda
conda create getaround-env
conda activate getaround-env

# Using venv
python -m venv getaround-env
source getaround-env/bin/activate
```

3. Install dependencies
```shel
pip install -r requirements.txt
```

### Executing program

To run FastAPI locally :\
`fastapi run ./src/app.py --port $PORT`


* Step-by-step bullets
```
code blocks for commands
```

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

[Maxime RENAULT](https://github.com/qxzjy)