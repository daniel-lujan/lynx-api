# Lynx

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) ![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white) ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)

## Application Description

Stores user form responses about tastes and personality, and computes a "matching" user and nearest establishment from a previously-stored list of motels.

> [!NOTE]
> This is the REST API backend server for the application. Check [frontend repo]() for web application.

## Computation

Implements KD Tree data structures (as proposed in [Multidimensional binary search trees used for associative searching](https://dl.acm.org/doi/10.1145/361002.361007)) and performs Nearest Neighbor Search algorithm to find a "match" for each user.


### Flow

![Image](https://github.com/daniel-lujan/lynx-api/blob/main/docs/computing_flow.png)

## Quick start
> [!WARNING]
> Built with Python 3.11.4, using lower version than 3.11 might lead to incompatibility issues.

Clone repository:

```bash
git clone https://github.com/daniel-lujan/lynx-api.git

cd lynx-api
```

> [!NOTE]
> It is recommended to set up a virtual environment before installing dependencies.
> ```bash
> python -m venv venv
> 
> source /venv/bin/activate
> # or, for Windows command line
> ./venv/Scripts/activate.bat
> ```

Install dependencies:
```bash
pip install -r requirements.txt
```

Start development server:
```bash
python app.py
```

The API should be now available at `http://localhost:5000`.

## Environment

To change development configuration (like port, or MongoDB address), check the [`.env.development`](https://github.com/daniel-lujan/lynx-api/blob/main/.env.development) file.



