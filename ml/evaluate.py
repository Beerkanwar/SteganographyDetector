import torch
import numpy as np
from sklearn.metrics import confusion_matrix, roc_auc_score, precision_recall_fscore_support
import torch.nn.functional as F

def evaluate(model, dataloader, criterion, device):
    model.eval()
    val_loss = 0.0
    all_preds = []
    all_labels = []
    all_probs = []
    
    with torch.no_grad():
        for images, labels in dataloader:
            images, labels = images.to(device), labels.to(device)
            
            outputs = model(images)
            loss = criterion(outputs, labels)
            val_loss += loss.item()
            
            probs = F.softmax(outputs, dim=1)[:, 1].cpu().numpy()
            preds = torch.argmax(outputs, dim=1).cpu().numpy()
            
            all_probs.extend(probs)
            all_preds.extend(preds)
            all_labels.extend(labels.cpu().numpy())
            
    val_loss /= len(dataloader)
    
    # Avoid errors if dataloader is empty
    if len(all_labels) == 0:
        return val_loss, {'roc_auc': 0, 'f1': 0, 'precision': 0, 'recall': 0}
        
    try:
        roc_auc = roc_auc_score(all_labels, all_probs)
    except ValueError:
        roc_auc = 0.0 # Handle case where only 1 class is present in a tiny validation set
        
    precision, recall, f1, _ = precision_recall_fscore_support(all_labels, all_preds, average='binary', zero_division=0)
    
    # cm = confusion_matrix(all_labels, all_preds)
    # Could log or print confusion matrix here
    
    metrics = {
        'roc_auc': roc_auc,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }
    
    return val_loss, metrics
