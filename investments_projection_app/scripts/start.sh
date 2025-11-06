#!/bin/bash
cd ..
source env/Scripts/activate
# uvicorn main:app --reload
python -m streamlit run main_invest.py 