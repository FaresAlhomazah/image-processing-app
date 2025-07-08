
from image_processor import ImageProcessor
from image_operations import ImageOperations
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.processor = ImageProcessor()
        self.current_image = None
        self.original_image = None
        self.processed_image = None
        self.image_paths = []
        self.current_index = 0
        self.cumulative_angle = 0
        self.crop_coords = {'start': None, 'end': None}
        self.crop_rect = None
        self.display_scale = 1.0
        self.dragging = False
        
        self._setup_modern_gui()
        self._bind_events()
    
    def _setup_modern_gui(self):
        self.root.title("🎨 Professional Image Processor - معالج الصور الاحترافي")
        self.root.geometry("1600x1000")
        self.root.configure(bg="#1a1a1a")
        self.root.state('zoomed')  # ملء الشاشة
        
        # تحسين الستايل
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # ألوان عصرية
        self.colors = {
            'primary': '#2563eb',
            'secondary': '#7c3aed', 
            'success': '#059669',
            'danger': '#dc2626',
            'warning': '#d97706',
            'dark': '#1f2937',
            'light': '#f8fafc',
            'accent': '#06b6d4'
        }
        
        self._create_modern_header()
        self._create_main_content()
        self._create_modern_controls()
        self._create_modern_status_bar()
    
    def _create_modern_header(self):
        """إنشاء هيدر عصري"""
        header_frame = tk.Frame(self.root, bg=self.colors['dark'], height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        # عنوان التطبيق
        title_label = tk.Label(
            header_frame,
            text="🎨 معالج الصور الاحترافي",
            font=('Segoe UI', 24, 'bold'),
            bg=self.colors['dark'],
            fg=self.colors['light']
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        # أزرار التحكم الرئيسية
        controls_frame = tk.Frame(header_frame, bg=self.colors['dark'])
        controls_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        modern_buttons = [
            ("📂 فتح الصور", self._open_images, self.colors['primary']),
            ("💾 حفظ باختيار المكان", self._save_with_dialog, self.colors['success']),
            ("💾 حفظ سريع", self._save_current, self.colors['accent']),
            ("🔄 إعادة تعيين", self._reset_image, self.colors['danger'])
        ]
        
        for i, (text, cmd, color) in enumerate(modern_buttons):
            btn = tk.Button(
                controls_frame,
                text=text,
                command=cmd,
                bg=color,
                fg='white',
                font=('Segoe UI', 11, 'bold'),
                relief='flat',
                padx=20,
                pady=8,
                cursor='hand2'
            )
            btn.grid(row=0, column=i, padx=5)
            
            # تأثير hover
            self._add_hover_effect(btn, color)
    
    def _add_hover_effect(self, button, original_color):
        """إضافة تأثير hover للأزرار"""
        def on_enter(e):
            button.configure(bg=self._darken_color(original_color))
        
        def on_leave(e):
            button.configure(bg=original_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def _darken_color(self, color):
        """تغميق اللون للتأثير"""
        color_map = {
            self.colors['primary']: '#1d4ed8',
            self.colors['success']: '#047857',
            self.colors['danger']: '#b91c1c',
            self.colors['accent']: '#0891b2'
        }
        return color_map.get(color, color)
    
    def _create_main_content(self):
        """المحتوى الرئيسي مع الصور"""
        main_frame = tk.Frame(self.root, bg="#1a1a1a")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # إطار الصور مع تسميات
        images_container = tk.Frame(main_frame, bg="#1a1a1a")
        images_container.pack(expand=True, fill=tk.BOTH)
        
        # الصورة الأصلية
        original_section = tk.Frame(images_container, bg="#1a1a1a")
        original_section.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(0, 5))
        
        tk.Label(
            original_section,
            text="📷 الصورة الأصلية",
            font=('Segoe UI', 14, 'bold'),
            bg="#1a1a1a",
            fg=self.colors['light']
        ).pack(pady=(0, 10))
        
        self.original_canvas = tk.Canvas(
            original_section,
            bg="white",
            relief='solid',
            borderwidth=2,
            highlightthickness=0
        )
        self.original_canvas.pack(expand=True, fill=tk.BOTH)
        
        # الصورة المعالجة
        processed_section = tk.Frame(images_container, bg="#1a1a1a")
        processed_section.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=(5, 0))
        
        tk.Label(
            processed_section,
            text="✨ الصورة المعالجة",
            font=('Segoe UI', 14, 'bold'),
            bg="#1a1a1a",
            fg=self.colors['light']
        ).pack(pady=(0, 10))
        
        self.processed_canvas = tk.Canvas(
            processed_section,
            bg="white",
            relief='solid',
            borderwidth=2,
            highlightthickness=0
        )
        self.processed_canvas.pack(expand=True, fill=tk.BOTH)
    
    def _create_modern_controls(self):
        """لوحة التحكم العصرية"""
        controls_main = tk.Frame(self.root, bg=self.colors['dark'])
        controls_main.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # عمليات معالجة الصور
        operations_frame = tk.LabelFrame(
            controls_main,
            text="🛠️ عمليات المعالجة",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['dark'],
            fg=self.colors['light'],
            relief='flat'
        )
        operations_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 5), pady=10)
        
        operations = [
            ("📊 توزيع الألوان", self._apply_histogram, self.colors['primary']),
            ("🔍 كشف الحواف", self._apply_edge_detection, self.colors['secondary']),
            ("🎨 عكس الألوان", self._apply_invert, self.colors['warning']),
            ("🔄 دوران", self._apply_rotation, self.colors['accent'])
        ]
        
        for i, (text, cmd, color) in enumerate(operations):
            btn = tk.Button(
                operations_frame,
                text=text,
                command=cmd,
                bg=color,
                fg='white',
                font=('Segoe UI', 10, 'bold'),
                relief='flat',
                padx=15,
                pady=8,
                cursor='hand2'
            )
            btn.grid(row=0, column=i, padx=8, pady=10)
            self._add_hover_effect(btn, color)
        
        # إعدادات الدوران
        rotation_frame = tk.LabelFrame(
            controls_main,
            text="⚙️ إعدادات الدوران",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['dark'],
            fg=self.colors['light'],
            relief='flat'
        )
        rotation_frame.pack(side=tk.RIGHT, padx=(5, 10), pady=10)
        
        tk.Label(
            rotation_frame,
            text="الزاوية:",
            font=('Segoe UI', 10),
            bg=self.colors['dark'],
            fg=self.colors['light']
        ).grid(row=0, column=0, padx=5, pady=10)
        
        self.angle_var = tk.IntVar(value=90)
        angle_entry = tk.Entry(
            rotation_frame,
            textvariable=self.angle_var,
            width=8,
            font=('Segoe UI', 10),
            justify='center'
        )
        angle_entry.grid(row=0, column=1, padx=5, pady=10)
        
        # أزرار التنقل
        navigation_frame = tk.Frame(controls_main, bg=self.colors['dark'])
        navigation_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        
        nav_buttons = [
            ("⏪ السابق", self._previous_image, self.colors['secondary']),
            ("⏩ التالي", self._next_image, self.colors['secondary'])
        ]
        
        for i, (text, cmd, color) in enumerate(nav_buttons):
            btn = tk.Button(
                navigation_frame,
                text=text,
                command=cmd,
                bg=color,
                fg='white',
                font=('Segoe UI', 10, 'bold'),
                relief='flat',
                padx=15,
                pady=8,
                cursor='hand2'
            )
            btn.grid(row=0, column=i, padx=5)
            self._add_hover_effect(btn, color)
    
    def _create_modern_status_bar(self):
        """شريط الحالة العصري"""
        status_frame = tk.Frame(self.root, bg=self.colors['dark'], height=40)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_var = tk.StringVar(value="جاهز للاستخدام")
        self.status_bar = tk.Label(
            status_frame,
            textvariable=self.status_var,
            font=('Segoe UI', 10),
            bg=self.colors['dark'],
            fg=self.colors['light'],
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.LEFT, padx=15, pady=10)
        
        # معلومات الصورة
        self.image_info_var = tk.StringVar()
        self.image_info_label = tk.Label(
            status_frame,
            textvariable=self.image_info_var,
            font=('Segoe UI', 10),
            bg=self.colors['dark'],
            fg=self.colors['accent'],
            anchor=tk.E
        )
        self.image_info_label.pack(side=tk.RIGHT, padx=15, pady=10)
    
    def _bind_events(self):
        self.original_canvas.bind("<ButtonPress-1>", self._crop_start)
        self.original_canvas.bind("<B1-Motion>", self._crop_drag)
        self.original_canvas.bind("<ButtonRelease-1>", self._crop_end)
    
    def _update_status(self, message):
        self.status_var.set(f"الحالة: {message}")
    
    def _update_image_info(self):
        if self.original_image is not None:
            h, w = self.original_image.shape[:2]
            info = f"الأبعاد: {w}x{h} | الصورة: {self.current_index + 1}/{len(self.image_paths)}"
            self.image_info_var.set(info)
    
    def _open_images(self):
        paths = filedialog.askopenfilenames(
            title="اختر الصور",
            filetypes=[
                ("جميع الصور", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff"),
                ("JPEG", "*.jpg;*.jpeg"),
                ("PNG", "*.png"),
                ("BMP", "*.bmp"),
                ("جميع الملفات", "*.*")
            ]
        )
        if paths:
            self.image_paths = paths
            self.current_index = 0
            self.cumulative_angle = 0
            self._load_image()
    
    def _load_image(self):
        try:
            path = self.image_paths[self.current_index]
            self.original_image = ImageOperations.load_image(path)
            self.processed_image = self.original_image.copy()
            self._display_images()
            self._update_status(f"تم تحميل: {os.path.basename(path)}")
            self._update_image_info()
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تحميل الصورة: {str(e)}")
    
    def _display_images(self):
        self.original_canvas.delete("all")
        self.processed_canvas.delete("all")
        
        if self.original_image is not None:
            # عرض الصورة الأصلية
            original_display = self.processor.prepare_for_display(self.original_image)
            self.display_scale = original_display.width / self.original_image.shape[1]
            self.original_imgtk = ImageTk.PhotoImage(original_display)
            
            canvas_width = self.original_canvas.winfo_width()
            canvas_height = self.original_canvas.winfo_height()
            x = (canvas_width - original_display.width) // 2
            y = (canvas_height - original_display.height) // 2
            
            self.original_canvas.create_image(x, y, anchor=tk.NW, image=self.original_imgtk)
            
            # عرض الصورة المعالجة
            processed_display = self.processor.prepare_for_display(self.processed_image)
            self.processed_imgtk = ImageTk.PhotoImage(processed_display)
            
            canvas_width = self.processed_canvas.winfo_width()
            canvas_height = self.processed_canvas.winfo_height()
            x = (canvas_width - processed_display.width) // 2
            y = (canvas_height - processed_display.height) // 2
            
            self.processed_canvas.create_image(x, y, anchor=tk.NW, image=self.processed_imgtk)
    
    def _save_with_dialog(self):
        """حفظ مع اختيار المكان"""
        try:
            if not self.image_paths:
                raise ValueError("لا توجد صورة للحفظ")
            
            path = self.image_paths[self.current_index]
            save_path = self.processor.save_image_with_dialog(self.processed_image, path)
            
            if save_path:
                messagebox.showinfo("تم الحفظ", f"تم حفظ الصورة في:\n{save_path}")
                self._update_status(f"تم الحفظ: {os.path.basename(save_path)}")
            else:
                self._update_status("تم إلغاء الحفظ")
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في حفظ الصورة: {str(e)}")
    
    # ... existing code ...
    def _save_current(self):
        try:
            if not self.image_paths:
                raise ValueError("لا توجد صورة للحفظ")
            path = self.image_paths[self.current_index]
            save_path = self.processor.save_image(self.processed_image, path)
            messagebox.showinfo("تم الحفظ", f"تم حفظ الصورة في:\n{save_path}")
            self._update_status(f"تم الحفظ: {os.path.basename(save_path)}")
        except Exception as e:
            messagebox.showerror("خطأ", str(e))
    
    def _apply_histogram(self):
        try:
            self.processed_image = ImageOperations.equalize_histogram(self.original_image)
            self._display_images()
            self._update_status("تم تطبيق توزيع الألوان")
        except Exception as e:
            messagebox.showerror("خطأ", str(e))
    
    def _apply_edge_detection(self):
        try:
            self.processed_image = ImageOperations.detect_edges(self.original_image)
            self._display_images()
            self._update_status("تم تطبيق كشف الحواف")
        except Exception as e:
            messagebox.showerror("خطأ", str(e))
            
    def _apply_invert(self):
        try:
            self.processed_image = ImageOperations.invert_colors(self.original_image)
            self._display_images()
            self._update_status("تم عكس الألوان")
        except Exception as e:
            messagebox.showerror("خطأ", str(e))
 
    def _apply_rotation(self):
        try:
            angle = self.angle_var.get()
            self.cumulative_angle += angle
            pil_image = Image.fromarray(cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB))
            rotated_image = ImageOperations.rotate_image(pil_image, self.cumulative_angle)
            self.processed_image = cv2.cvtColor(np.array(rotated_image), cv2.COLOR_RGB2BGR)
            
            self._display_images()
            self._update_status(f"تم الدوران بزاوية {self.cumulative_angle}°")
        except Exception as e:
            messagebox.showerror("خطأ", str(e))

    def _crop_start(self, event):
        self.dragging = True
        self.crop_coords['start'] = (event.x, event.y)
        self.crop_rect = self.original_canvas.create_rectangle(
            event.x, event.y, event.x, event.y, outline="red", width=2)
    
    def _crop_drag(self, event):
        if self.dragging and self.crop_coords['start']:
            x1, y1 = self.crop_coords['start']
            self.original_canvas.coords(self.crop_rect, x1, y1, event.x, event.y)
    
    def _crop_end(self, event):
        self.dragging = False
        self.crop_coords['end'] = (event.x, event.y)
        self._apply_crop()
    
    def _apply_crop(self):
        try:
            x1 = int(self.crop_coords['start'][0] / self.display_scale)
            y1 = int(self.crop_coords['start'][1] / self.display_scale)
            x2 = int(self.crop_coords['end'][0] / self.display_scale)
            y2 = int(self.crop_coords['end'][1] / self.display_scale)
            
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            x = min(x1, x2)
            y = min(y1, y2)
            
            self.processed_image = ImageOperations.crop_image(
                self.original_image, x, y, width, height
            )
            self._display_images()
            self._update_status("تم تطبيق القص")
            self.original_canvas.delete(self.crop_rect)
        except Exception as e:
            messagebox.showerror("خطأ في القص", str(e))
    
    def _reset_image(self):
        if self.original_image is not None:
            self.processed_image = self.original_image.copy()
            self.cumulative_angle = 0
            self._display_images()
            self._update_status("تم إعادة تعيين الصورة")
    
    def _previous_image(self):
        if len(self.image_paths) == 0:
            return
        self.current_index = max(0, self.current_index - 1)
        self._load_image()
    
    def _next_image(self):
        if len(self.image_paths) == 0:
            return
        self.current_index = min(len(self.image_paths) - 1, self.current_index + 1)
        self._load_image()

if __name__ == "__main__":  
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()