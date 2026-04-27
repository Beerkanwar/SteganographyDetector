import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.cuda.amp import GradScaler, autocast
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm

from ml.config import Config
from ml.model import get_model
from ml.dataset import DynamicStegoDataset
from ml.evaluate import evaluate

def train():
    Config.setup_dirs()
    writer = SummaryWriter(log_dir=Config.LOG_DIR)
    
    # Dataset & DataLoader
    train_dataset = DynamicStegoDataset(Config.TRAIN_DIR)
    val_dataset = DynamicStegoDataset(Config.VAL_DIR)
    
    # Use drop_last to avoid batch norm issues with size 1
    train_loader = DataLoader(
        train_dataset, 
        batch_size=Config.BATCH_SIZE, 
        shuffle=True, 
        num_workers=Config.NUM_WORKERS,
        drop_last=True
    )
    
    val_loader = DataLoader(
        val_dataset, 
        batch_size=Config.BATCH_SIZE, 
        shuffle=False, 
        num_workers=Config.NUM_WORKERS
    )
    
    # Model, Loss, Optimizer
    model = get_model()
    
    # Class balancing (stego generation is exactly 50/50, so weights are equal here, but configurable)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=Config.LEARNING_RATE, weight_decay=Config.WEIGHT_DECAY)
    
    # Cosine Annealing Scheduler
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=Config.NUM_EPOCHS)
    
    # Mixed precision scaler
    scaler = GradScaler()
    
    best_roc_auc = 0.0
    patience_counter = 0
    
    print(f"Starting training on {Config.DEVICE}...")
    for epoch in range(Config.NUM_EPOCHS):
        model.train()
        running_loss = 0.0
        
        # Training loop
        progress_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{Config.NUM_EPOCHS}")
        
        optimizer.zero_grad()
        for i, (images, labels) in enumerate(progress_bar):
            images, labels = images.to(Config.DEVICE), labels.to(Config.DEVICE)
            
            with autocast():
                outputs = model(images)
                loss = criterion(outputs, labels)
                # Gradient accumulation scaling
                loss = loss / Config.GRADIENT_ACCUMULATION_STEPS
            
            scaler.scale(loss).backward()
            
            if (i + 1) % Config.GRADIENT_ACCUMULATION_STEPS == 0:
                scaler.step(optimizer)
                scaler.update()
                optimizer.zero_grad()
                
            running_loss += loss.item() * Config.GRADIENT_ACCUMULATION_STEPS
            progress_bar.set_postfix({'loss': running_loss / (i + 1)})
            
        train_loss = running_loss / len(train_loader)
        writer.add_scalar('Loss/train', train_loss, epoch)
        
        # Evaluation
        val_loss, metrics = evaluate(model, val_loader, criterion, Config.DEVICE)
        
        writer.add_scalar('Loss/val', val_loss, epoch)
        writer.add_scalar('Metrics/ROC_AUC', metrics['roc_auc'], epoch)
        writer.add_scalar('Metrics/F1', metrics['f1'], epoch)
        
        print(f"Epoch {epoch+1}: Train Loss={train_loss:.4f}, Val Loss={val_loss:.4f}, AUC={metrics['roc_auc']:.4f}")
        
        scheduler.step()
        
        # Early stopping and checkpointing
        if metrics['roc_auc'] > best_roc_auc:
            best_roc_auc = metrics['roc_auc']
            patience_counter = 0
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'roc_auc': best_roc_auc,
            }, os.path.join(Config.CHECKPOINT_DIR, "best_model.pth"))
            print(f"New best model saved! (AUC: {best_roc_auc:.4f})")
        else:
            patience_counter += 1
            if patience_counter >= Config.EARLY_STOPPING_PATIENCE:
                print(f"Early stopping triggered at epoch {epoch+1}")
                break

if __name__ == "__main__":
    # We require creating the dummy data dir to prevent instant failure if users run it locally without setup
    os.makedirs(Config.TRAIN_DIR, exist_ok=True)
    os.makedirs(Config.VAL_DIR, exist_ok=True)
    train()
