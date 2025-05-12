# IoT Sensor Anomaly Detection Architecture

## Technologies Used

- **Apache Kafka**: Streaming pipeline for real-time sensor data
- **MinIO**: Object storage for `.pickle` files
- **PostgreSQL**: Structured storage of sensor readings
- **MLflow**: Model training, tracking, and versioning



## Architecture Overview
### Sensor Simulation
    ├── Sends sensor data to Kafka topic "sensor-data"
    ├── Saves raw `.pickle` files to MinIO
         ↓
### Kafka Consumer (ETL)
    ├── Reads from "sensor-data"
    ├── Inserts readings into PostgreSQL table `sensor_readings`
         ↓
### ML Training Pipeline
    ├── Loads data from PostgreSQL
    ├── Trains LSTM Autoencoder for anomaly detection
    ├── Logs model + metrics to MLflow
         ↓
### Anomaly Detection Service (optional)
    ├── Loads model from MLflow
    ├── Applies model to new data
    ├── Publishes alerts to Kafka topic "anomaly-alerts"
         ↓
### Dashboard (optional)
    ├── Visualizes anomalies (Streamlit / Grafana)

| Sensor      | Typical Range | Anomaly Examples                      |
| ----------- | ------------- | ------------------------------------- |
| Temperature | 15°C - 40°C   | Spikes (>50°C), drops (<0°C)          |
| Vibration   | 0 - 100 (RMS) | Sustained spikes, strong random noise |
| Pressure    | 1 - 5 bar     | Sudden drops, constant flat values    |
| Humidity    | 30% - 80%     | Sudden >95% or drops below 10%        |

## Project Roadmap
### Phase 1: Infrastructure Setup

- [X] Docker Compose with Kafka, PostgreSQL, MinIO, MLflow

- [X] Create Kafka topics (e.g., sensor-data)

- [X] Create PostgreSQL schema (sensor_readings table)

- [ ] Setup MinIO bucket for .pickle files

### Phase 2: Simulation and ETL
- [ ] Simulate multiple sensors with different signal types

- [ ] Send sensor data to Kafka

- [ ] Save .pickle files to MinIO

- [ ] Kafka Consumer inserts structured data into PostgreSQL

### Phase 3: Machine Learning Pipeline
- [ ] Extract historical data from PostgreSQL

- [ ] Train LSTM Autoencoder for anomaly detection

- [ ] Log model artifacts and metrics to MLflow

### Phase 4: Inference & Visualization (Optional)
- [ ] Load model and run prediction on live or batch data

- [ ] Stream detected anomalies into a new Kafka topic

- [ ] Visualize anomaly scores using Streamlit or Grafana