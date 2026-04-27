import os
import torch

class Config:
    # Reproducibility
    SEED = 42
    
    # Dataset
    # Expects COCO structure:
    # ml/data/coco2017/train2017/
    # ml/data/coco2017/val2017/
    DATA_DIR = os.getenv("DATASET_PATH", "./data/coco2017")
    TRAIN_DIR = os.path.join(DATA_DIR, "train2017")
    VAL_DIR = os.path.join(DATA_DIR, "val2017")
    
    # Model
    MODEL_NAME = "tf_efficientnetv2_s.in21k_ft_in1k" # Good balance of speed and subtle feature extraction
    NUM_CLASSES = 2 # 0: Clean, 1: Stego
    IMAGE_SIZE = 256 # Standardized input size
    
    # Training
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", "32"))
    NUM_EPOCHS = int(os.getenv("NUM_EPOCHS", "50"))
    LEARNING_RATE = float(os.getenv("LEARNING_RATE", "1e-4"))
    WEIGHT_DECAY = 1e-5
    
    # Advanced Training Features
    MIXED_PRECISION = True
    GRADIENT_ACCUMULATION_STEPS = 2
    EARLY_STOPPING_PATIENCE = 7
    NUM_WORKERS = min(8, os.cpu_count() or 4)
    
    # Paths
    CHECKPOINT_DIR = "./checkpoints"
    LOG_DIR = "./logs"
    
    # Device
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    
    @classmethod
    def setup_dirs(cls):
        os.makedirs(cls.CHECKPOINT_DIR, exist_ok=True)
        os.makedirs(cls.LOG_DIR, exist_ok=True)
