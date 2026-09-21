from fastapi import APIRouter

router = APIRouter(
    prefix="/dashboard/ml",
    tags=["ML Training"]
)

@router.get("/train/v2")
def get_training_v2():
    return {
        "model_name": "Analyzer V2",
        "dataset_size": "Small Dataset (12,000 samples)",
        "status": "Training Completed",
        "accuracy": 88.5,
        "loss": 0.31,
        "last_trained": "2026-06-30",
        "epochs": 30,
        "training_time_minutes": 9,
        "logs": [
            "Epoch 1/30 - loss: 1.12 - acc: 52%",
            "Epoch 10/30 - loss: 0.61 - acc: 71%",
            "Epoch 20/30 - loss: 0.41 - acc: 81%",
            "Epoch 30/30 - loss: 0.31 - acc: 88.5%"
        ]
    }

@router.get("/train/v6")
def get_training_v6():
    return {
        "model_name": "Analyzer V6",
        "dataset_size": "Large Dataset (120,000 samples)",
        "status": "Training Completed",
        "accuracy": 94.2,
        "loss": 0.12,
        "last_trained": "2026-06-30",
        "epochs": 50,
        "training_time_minutes": 18,
        "logs": [
            "Epoch 1/50 - loss: 0.89 - acc: 62%",
            "Epoch 10/50 - loss: 0.45 - acc: 78%",
            "Epoch 25/50 - loss: 0.22 - acc: 88%",
            "Epoch 50/50 - loss: 0.12 - acc: 94.2%"
        ]
    }
