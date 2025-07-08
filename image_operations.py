
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

class ImageOperations:
    @staticmethod
    def load_image(path):
        image = cv2.imread(path)
        if image is None:
            raise ValueError(f"Failed to load image from {path}")
        return image
    
    @staticmethod
    def equalize_histogram(image):
        """تحسين توزيع الألوان باستخدام CLAHE"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(16,16))
        equalized = clahe.apply(gray)
        return cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)

    @staticmethod
    def detect_edges(image, blur_kernel=5, threshold1=50, threshold2=150):
        """كشف الحواف مع إمكانية التحكم في المعاملات"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (blur_kernel, blur_kernel), 0)
        edges = cv2.Canny(blurred, threshold1, threshold2)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    
    @staticmethod
    def rotate_image(image, angle):
        """دوران الصورة مع الحفاظ على الجودة"""
        rotated_image = image.rotate(angle, expand=True, fillcolor='white')
        return rotated_image
    
    @staticmethod
    def crop_image(image, x, y, width, height):
        """قص الصورة مع التحقق من الحدود"""
        h, w = image.shape[:2]
        x = max(0, min(x, w))
        y = max(0, min(y, h))
        width = min(width, w - x)
        height = min(height, h - y)
        return image[y:y+height, x:x+width]
    
    @staticmethod
    def invert_colors(image):
        """عكس الألوان"""
        return cv2.bitwise_not(image)
    
    @staticmethod
    def adjust_brightness_contrast(image, brightness=0, contrast=0):
        """تعديل السطوع والتباين"""
        if brightness != 0:
            if brightness > 0:
                shadow = brightness
                highlight = 255
            else:
                shadow = 0
                highlight = 255 + brightness
            alpha_b = (highlight - shadow) / 255
            gamma_b = shadow
            image = cv2.addWeighted(image, alpha_b, image, 0, gamma_b)
        
        if contrast != 0:
            f = 131 * (contrast + 127) / (127 * (131 - contrast))
            alpha_c = f
            gamma_c = 127 * (1 - f)
            image = cv2.addWeighted(image, alpha_c, image, 0, gamma_c)
        
        return image
    
    @staticmethod
    def apply_blur(image, blur_type='gaussian', kernel_size=15):
        """تطبيق تأثيرات الضبابية"""
        if blur_type == 'gaussian':
            return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        elif blur_type == 'median':
            return cv2.medianBlur(image, kernel_size)
        elif blur_type == 'bilateral':
            return cv2.bilateralFilter(image, kernel_size, 80, 80)
        return image