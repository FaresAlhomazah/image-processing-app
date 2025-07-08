
import os
import cv2
from PIL import Image
from tkinter import filedialog

class ImageProcessor:
    def __init__(self):
        self.display_width = 600
        self.display_height = 600
        self.image_counter = 1 
        
    def prepare_for_display(self, image):
        if image is None:
            return Image.new('RGB', (self.display_width, self.display_height), (0, 0, 0))
        
        try:
            img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            h, w = img_rgb.shape[:2]
            scale = min(self.display_width/w, self.display_height/h)
            new_size = (int(w*scale), int(h*scale))
            return Image.fromarray(img_rgb).resize(new_size, Image.Resampling.LANCZOS)
        except Exception as e:
            print(f"Display preparation error: {e}")
            return Image.new('RGB', (self.display_width, self.display_height), (0, 0, 0))
    
    def save_image_with_dialog(self, image, original_path, prefix="processed"):
        """حفظ الصورة مع إمكانية اختيار المكان"""
        # اقتراح اسم الملف
        suggested_name = f"{prefix}_{self.image_counter}_{os.path.basename(original_path)}"
        
        # فتح نافذة اختيار مكان الحفظ
        save_path = filedialog.asksaveasfilename(
            title="حفظ الصورة المعالجة",
            defaultextension=".jpg",
            initialfilename=suggested_name,
            filetypes=[
                ("JPEG files", "*.jpg"),
                ("PNG files", "*.png"),
                ("BMP files", "*.bmp"),
                ("All files", "*.*")
            ]
        )
        
        if save_path:
            success = cv2.imwrite(save_path, image)
            if not success:
                raise RuntimeError(f"Failed to save image to {save_path}")
            self.image_counter += 1
            return save_path
        return None
    
    def save_image(self, image, original_path, prefix="processed"):
        """الطريقة القديمة للحفظ التلقائي"""
        save_dir = r"C:\Users\engfa\Desktop\Processed Images"
        os.makedirs(save_dir, exist_ok=True)
        filename = f"{prefix}_{self.image_counter}_{os.path.basename(original_path)}"
        save_path = os.path.join(save_dir, filename)
        success = cv2.imwrite(save_path, image)
        if not success:
            raise RuntimeError(f"Failed to save image to {save_path}")
        self.image_counter += 1
        return save_path