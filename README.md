# Image Processing Application


## A professional desktop application for image processing built with Python and Tkinter, featuring a modern Arabic/English interface.
<p align="center">
  <!-- Technologies -->
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Tkinter-FF6F00?style=for-the-badge&logo=python&logoColor=white" alt="Tkinter" />
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV" />
  <img src="https://img.shields.io/badge/Pillow-5C1E00?style=for-the-badge&logo=pillow&logoColor=white" alt="Pillow" />
  <img src="https://img.shields.io/badge/numpy-013243?style=for-the-badge&logo=python&logoColor=white" alt="NumPy" />
</p>

---

## Screenshot

<p align="center">
<p align="center">
  <img src="https://github.com/user-attachments/assets/e28d9e2e-1a70-4a18-b747-482b4af133b5" alt="Application Screenshot" width="600" />
</p>
</p>

---

## Features

- **Image Loading**: Support for multiple image formats (JPG, PNG, BMP, TIFF)
- **Real-time Processing**: Side-by-side comparison of original and processed images
- **Image Operations**:
  - Histogram Equalization (CLAHE)
  - Edge Detection (Canny)
  - Color Inversion
  - Image Rotation
  - Interactive Cropping
- **Save Options**: 
  - Quick save to default location
  - Save with custom location dialog
- **Navigation**: Browse through multiple images
- **Modern UI**: Dark theme with hover effects and Arabic support

## Project Structure

### Core Files

1. **`gui.py`** - Main application interface
   - Modern GUI with dark theme
   - Bilingual support (Arabic/English)
   - Interactive image display and controls
   - Event handling for user interactions

2. **`image_operations.py`** - Image processing functions
   - Static methods for various image operations
   - OpenCV-based implementations
   - Error handling and validation

3. **`image_processor.py`** - Image management and utilities
   - Display preparation and scaling
   - Save functionality with dialog options
   - File management utilities
  
  

## Requirements

```
opencv-python
Pillow
numpy
tkinter (included with Python)
```

## Installation

1. Clone or download the project files
2. Install required packages:
   ```bash
   pip install opencv-python Pillow numpy
   ```
3. Run the application:
   ```bash
   python gui.py
   ```

## Usage

1. **Open Images**: Click "📂 فتح الصور" to select image files
2. **Apply Operations**: Use the processing buttons to apply effects
3. **Navigate**: Use Previous/Next buttons to browse multiple images
4. **Crop**: Click and drag on the original image to select crop area
5. **Save**: Choose between quick save or save with custom location
6. **Reset**: Return to original image state

## Key Classes and Methods

### ImageProcessingApp (gui.py)
- `_setup_modern_gui()`: Creates the modern interface
- `_display_images()`: Handles image rendering
- `_save_with_dialog()`: Custom save location
- `_apply_*()`: Various image processing operations

### ImageOperations (image_operations.py)
- `load_image()`: Load image from file
- `equalize_histogram()`: CLAHE histogram equalization
- `detect_edges()`: Canny edge detection
- `rotate_image()`: Image rotation
- `crop_image()`: Image cropping
- `invert_colors()`: Color inversion

### ImageProcessor (image_processor.py)
- `prepare_for_display()`: Scale images for GUI display
- `save_image_with_dialog()`: Interactive save with file dialog
- `save_image()`: Quick save to default location

## Interface Language

The application supports both Arabic and English text, with Arabic being the primary language for the interface elements and English for technical terms and file operations.

## Notes

- The application automatically scales images to fit the display canvas
- All processing operations work on the original image data
- Supports batch processing through multiple image navigation
- Modern flat design with hover effects for better user experience

## 📧 Contact

- **Email:** faresalhomazzah@gmail.com
- **LinkedIn:** https://www.linkedin.com/in/fares-abdulghani-alhomazah-6b1802288?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app



