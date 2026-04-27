import torch
import torch.nn as nn
import timm
from ml.config import Config

class SteganalysisModel(nn.Module):
    def __init__(self, model_name=Config.MODEL_NAME, num_classes=Config.NUM_CLASSES, pretrained=True):
        super(SteganalysisModel, self).__init__()
        # We use timm to fetch the EfficientNetV2 architecture.
        # Steganalysis often benefits from high-frequency subtle texture detection.
        # EfficientNetV2 is excellent for this without being prohibitively slow like ViTs.
        self.backbone = timm.create_model(
            model_name, 
            pretrained=pretrained, 
            num_classes=0 # Remove the classification head
        )
        
        # Get the number of features output by the backbone
        num_features = self.backbone.num_features
        
        # Custom classification head
        self.head = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(num_features, num_classes)
        )

    def forward(self, x):
        # x is (B, 3, H, W)
        features = self.backbone(x) # (B, num_features)
        output = self.head(features) # (B, num_classes)
        return output

def get_model(device=Config.DEVICE, pretrained=True):
    model = SteganalysisModel(pretrained=pretrained)
    model.to(device)
    return model
