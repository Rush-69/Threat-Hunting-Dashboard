# Threat Hunting Dashboard

A real-world SOC analyst project that detects DDoS attack patterns 
in network traffic using behavioral analysis and interactive visualization.

## Project Overview
- Analyzed 221,264 real network connections from the CICIDS 2017 dataset
- Identified 128,014 DDoS attack flows using behavioral pattern analysis
- Built an interactive dashboard to visualize attack vs normal traffic
- Mapped findings to MITRE ATT&CK framework (T1498)
- Produced a professional Threat Hunt Report with detection recommendations

## Tools Used
- Python 3.13
- Pandas (data analysis)
- Plotly Dash (interactive dashboard)
- Jupyter Notebook (exploratory analysis)

## Dataset
Download from: https://www.kaggle.com/datasets/dhoogla/cicids2017
File needed: DDoS-Friday-no-metadata.parquet

## How to Run
1. Install dependencies: pip install pandas dash plotly fastparquet
2. Download the dataset and convert to CSV using the Jupyter notebook
3. Run the dashboard: python dashboard.py
4. Open browser at: http://127.0.0.1:8050
