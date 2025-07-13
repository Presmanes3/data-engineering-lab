# Data Engineering & Forecasting Project: Real-Time Power Consumption Prediction

## Objective

This project simulates an industrial environment with multiple sensors generating real-time data, processes the data through a modern streaming architecture, and trains machine learning models to predict future power consumption of machines. It also visualizes the data and predictions in real time, enabling human interaction for a complete human-in-the-loop feedback system.


## High-Level Architecture
- **Sensor Simulation:** Simulated IoT sensors using Python

- **Streaming:** Real-time message flow via Kafka

- **Storage:** Data persistence in PostgreSQL

- **Visualization:** Live dashboards using Streamlit and Grafana

- **ML Forecasting:** Model training to predict future power usage

- **Deployment:** Serving models via MLflow or FastAPI

- **Human-in-the-loop:** Feedback from operators to refine model performance

## Simulated Sensors
- Temperature (°C)

- Vibration (m/s²)

- Pressure (bar)

- Power Consumption (Watts)

Each sensor sends readings every 10 seconds via Kafka (in JSON format).

## Data Flow

1. **Simulation:** Sensor values generated with Python (faker, random, numpy)

2. **Streaming:** Events sent to Kafka topics

3. **Ingestion:** Kafka consumer writes to PostgreSQL

4. **Processing:** Aggregation and feature extraction for ML

5. **Visualization:**

    - Grafana for metrics and alerts

    - Streamlit for interactivity and ML control

## Forecasting User Case: Power Consumption
### Goal
Predict a machine’s power consumption for the next 15 minutes using historical sensor data.

### Features
- Time series of:
    - `power_consumption`, `temperature`, `vibration`, `pressure`
- Derived features:
    - Moving averages, deltas, time-based features (hour of day, etc.)

### ML Models
- XBoost
- LSTM or Darts
- MLflow

## ML Pipeline
1. Time-series preprocessing
2. Sliding window creation for features/targets
3. Model training with cross-validation
4. MLflow logging and model registration
5. Model deployment via MLflow

### Human-in-the-loop system
- A Streamlit dashboard displays predictions
- Users can validate predictions as correct or incorrect
- Feedback is logged in PostgreSQL for future training

## Visualization

### Grafana
- Real-time sensor dashboards
- Alerts for anomalous values

### Streamlit
- Trigger model training and inference
- Show and validate model predictions

# Roadmap
- [X] Sensor simulation and Kafka streaming
- [X] Data ingestion and storage in PostgreSQL
- [ ] Grafana dashboards
- [ ] Power consumption forecasting (MVP with XGBoost)
- [ ] MLflow integration and model deployment
- [ ] Human-in-the-loop Streamlit validation
- [ ] Pipeline orchestration with Airflow or Prefect

# Key Learning Goals
- Real-time data streaming and processing
- Time series feature engineering
- ML training and prediction pipelines
- Visualization and human interaction
- MLOps with tracing, deployment and feedback loops







