import torch
import numpy as np
import cv2
from torch.utils.data import Dataset
from pathlib import Path

data_path = Path('data')


class AngyodysplasiaDataset(Dataset):
    def __init__(self, img_paths: list, to_augment=False, transform=None, mode='train', limit=None):
        self.img_paths = img_paths
        self.to_augment = to_augment
        self.transform = transform
        self.mode = mode
        self.limit = limit

    def __len__(self):
        if self.limit is None:
            return len(self.img_paths)
        else:
            return self.limit

    def __getitem__(self, idx):
        if self.limit is None:
            img_file_name = self.img_paths[idx]
        else:
            img_file_name = np.random.choice(self.img_paths)

        img = load_image(img_file_name)

        if self.mode == 'train':
            mask = load_mask(img_file_name)

            img, mask = self.transform(img, mask)
            img = to_float_tensor(img)
            mask = torch.from_numpy(np.expand_dims(mask, 0)).float()
            img_real = torch.zeros((img.shape[0], 576, 576))
            mask_real = torch.zeros((mask.shape[0], 576, 576))
            img_real[:, 38:-38, 1:-1] = img
            mask_real[:, 38:-38, 1:-1] = mask
            return img_real, mask_real
            #return to_float_tensor(img), torch.from_numpy(np.expand_dims(mask, 0)).float()
        else:
            mask = np.zeros(img.shape[:2])
            img, mask = self.transform(img, mask)
            img = to_float_tensor(img)
            img_real = torch.zeros((img.shape[0], 576, 576))
            img_real[:, 144:-144, 96:-96]
            return img_real, str(img_file_name)


def to_float_tensor(img):
    return torch.from_numpy(np.moveaxis(img, -1, 0)).float()


def load_image(path):
    img = cv2.imread(str(path))
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def load_mask(path):
    mask = cv2.imread(str(path).replace('images', 'masks').replace(r'.jpg', r'_a.jpg'), 0)
    return (mask > 0).astype(np.uint8)
