import cv2
import numpy as np
from PIL import Image
from typing import Tuple

# TODO: Check if the image preprocessor is aligned properly with how the AI works

class ImagePreprocessor:
    """
    Handles image transformations for MobileNetV3 (Freshness) and YOLOv8n (Defect Detection).
    """

    @staticmethod
    def preprocess_for_freshness(pil_image: Image.Image) -> np.ndarray:
        """
        Prepares input tensor for MobileNetV3-Small (Input name: 'x', Shape: [1, 3, 224, 224]).
        Applies standard ImageNet normalization: (x - mean) / std.
        """
        img = pil_image.resize((224, 224), Image.Resampling.BILINEAR)
        img_np = np.array(img, dtype=np.float32) / 255.0

        # Standard ImageNet distribution parameters
        mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
        std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
        img_np = (img_np - mean) / std

        # Transpose HWC -> CHW -> NCHW
        tensor = np.transpose(img_np, (2, 0, 1))
        tensor = np.expand_dims(tensor, axis=0)
        return tensor.astype(np.float32)

    @staticmethod
    def letterbox(
        img: np.ndarray, 
        new_shape: Tuple[int, int] = (640, 640), 
        color: Tuple[int, int, int] = (114, 114, 114)
    ) -> Tuple[np.ndarray, float, Tuple[float, float]]:
        """
        Resizes and pads image to 640x640 preserving aspect ratio for YOLOv8.
        """
        shape = img.shape[:2]  # [height, width]
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        
        dw = (new_shape[1] - new_unpad[0]) / 2  # width padding
        dh = (new_shape[0] - new_unpad[1]) / 2  # height padding

        if shape[::-1] != new_unpad:
            img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)

        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        padded_img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
        
        return padded_img, r, (dw, dh)

    @staticmethod
    def preprocess_for_defects(pil_image: Image.Image) -> Tuple[np.ndarray, float, Tuple[float, float], Tuple[int, int]]:
        """
        Prepares input tensor for YOLOv8n (Input name: 'images', Shape: [1, 3, 640, 640]).
        """
        rgb_img = np.array(pil_image)
        bgr_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2BGR)
        orig_shape = bgr_img.shape[:2]  # (height, width)

        letterboxed, ratio, (dw, dh) = ImagePreprocessor.letterbox(bgr_img, (640, 640))
        
        # Convert BGR -> RGB & normalize to [0.0, 1.0]
        rgb_letterboxed = cv2.cvtColor(letterboxed, cv2.COLOR_BGR2RGB)
        tensor = rgb_letterboxed.astype(np.float32) / 255.0
        
        # (H, W, C) -> (1, C, H, W)
        tensor = np.transpose(tensor, (2, 0, 1))
        tensor = np.expand_dims(tensor, axis=0)
        
        return tensor.astype(np.float32), ratio, (dw, dh), orig_shape