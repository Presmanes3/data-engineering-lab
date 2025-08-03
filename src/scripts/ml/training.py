from dotenv import load_dotenv
import os
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import product

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

from mlflow import (
    log_metric,
    log_params,
    set_tracking_uri,
    start_run,
    set_experiment,
    log_artifact,
    set_tag
)
from mlflow.sklearn import log_model
from mlflow.models.signature import infer_signature
from mlflow.tracking import MlflowClient

# 🔒 Load environment variables
load_dotenv()

# 🔗 MLflow and MinIO configuration
set_tracking_uri("http://localhost:5000")
os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY")
os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://host.docker.internal:9000"

# 🎯 Experiment
EXPERIMENT_NAME = "random-forest-experiment"
client = MlflowClient()
experiment = client.get_experiment_by_name(EXPERIMENT_NAME)
if experiment is None:
    experiment_id = client.create_experiment(EXPERIMENT_NAME)
else:
    experiment_id = experiment.experiment_id
set_experiment(EXPERIMENT_NAME)

# 📊 Dataset
data = pd.read_csv("src/scripts/fake_data/synthetic_data.csv")
X = data.drop("label", axis=1)
y = data["label"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# 🔧 Hyperparameter grid to test
param_grid = {
    "n_estimators": [50, 100],
    "max_depth": [5, 10, None],
    "random_state": [42]  # for reproducibility
}

# 🧪 Try all combinations
for values in product(*param_grid.values()):
    params = dict(zip(param_grid.keys(), values))

    run_name = f"rf_ne{params['n_estimators']}_md{params['max_depth']}"
    with start_run(run_name=run_name):
        # 🕒 Training
        start_time = time.time()
        clf = RandomForestClassifier(**params)
        clf.fit(X_train, y_train)
        duration = time.time() - start_time

        # 📈 Metrics
        y_pred = clf.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        # 🔐 Logging
        log_metric("accuracy", acc)
        log_metric("precision", precision)
        log_metric("recall", recall)
        log_metric("f1_score", f1)
        log_metric("training_time_sec", duration)
        log_params(params)

        set_tag("model_type", "RandomForest")
        set_tag("data_version", "v1.0")
        set_tag("author", "presmanes")

        # 📦 Model
        signature = infer_signature(X_test, y_pred)
        log_model(clf, "model", signature=signature, input_example=X_test.iloc[:5])

        # 📊 Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(6, 4))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title("Confusion Matrix")
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.tight_layout()
        img_name = f"conf_matrix_{run_name}.png"
        plt.savefig(img_name)
        log_artifact(img_name)

        print(f"✅ Run complete: {run_name}")
