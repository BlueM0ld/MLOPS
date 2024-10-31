import os
import torch
import subprocess
from datetime import datetime


def save_checkpoint(model, epoch, model_name):
    """Save a checkpoint of the model, 
    Args:
        model: The model to save.
        epoch: The current epoch number.
        model_name: The name of the model.
    Returns:
        None
    Outputs:
        A checkpoint file in ./checkpoints/
        Filename format: {model_name}_{timestamp}_epoch_{epoch+1}_{git_commit}.pth
    """
    os.makedirs("./checkpoints", exist_ok=True)
    commit = subprocess.check_output(
        ['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = f"./checkpoints/{model_name}_{timestamp}_epoch_{epoch+1}_{commit}.pth"
    torch.save(model.state_dict(), model_path)
