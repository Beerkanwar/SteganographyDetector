import os
import random
import numpy as np
from PIL import Image
import torch
from torch.utils.data import Dataset
import torchvision.transforms as T

from ml.config import Config

class DynamicStegoDataset(Dataset):
    """
    Loads clean images from a directory and dynamically converts 50% of them
    into steganographic images by embedding random bits in the LSBs.
    This prevents the model from just memorizing pre-generated dataset artifacts.
    """
    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.image_paths = []
        
        # Load all image paths
        if os.path.exists(data_dir):
            for filename in os.listdir(data_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    self.image_paths.append(os.path.join(data_dir, filename))
                    
        self.transform = transform or T.Compose([
            T.Resize((Config.IMAGE_SIZE, Config.IMAGE_SIZE)),
            T.ToTensor(),
            # Standard ImageNet normalization since we use pretrained timm models
            T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def _embed_random_payload(self, img: Image.Image) -> Image.Image:
        """Embeds a random payload of random size into the image LSBs."""
        img_arr = np.array(img)
        flat_arr = img_arr.flatten()
        
        # Determine a random payload size (between 5% and 80% of capacity)
        capacity = len(flat_arr)
        payload_bits_len = random.randint(int(capacity * 0.05), int(capacity * 0.8))
        
        # Generate random bits
        payload_bits = np.random.randint(0, 2, size=payload_bits_len, dtype=np.uint8)
        
        # Embed in LSB
        flat_arr[:payload_bits_len] = (flat_arr[:payload_bits_len] & ~1) | payload_bits
        
        stego_arr = flat_arr.reshape(img_arr.shape)
        return Image.fromarray(stego_arr, mode=img.mode)

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        try:
            img = Image.open(img_path).convert("RGB")
        except Exception:
            # Fallback to creating a random blank image if file is corrupt
            img = Image.new("RGB", (Config.IMAGE_SIZE, Config.IMAGE_SIZE))
            
        # 50% chance to be stego
        is_stego = random.random() > 0.5
        label = 1 if is_stego else 0
        
        if is_stego:
            img = self._embed_random_payload(img)
            
        if self.transform:
            img = self.transform(img)
            
        return img, torch.tensor(label, dtype=torch.long)
