# StickerServer Project Documentation for AI Agents

## Project Overview
StickerServer is a Flask-based REST server designed to interface with an ESC/POS thermal printer via USB. It converts text and images into formats suitable for sticker/label printing.

## Core Components
- **`server.py`**: The main Flask application.
    - **`/label` (GET)**: Generates and prints text labels. Supports parameters: `text`, `bold`, `italic`, `font_size`, and `emoji_mode`.
    - **`/image` (POST)**: Accepts image files and prints them with options for auto-rotation and edge enhancement.
    - **`/`**: Serves the web interface.
- **`print_image.py`**: Handles physical interaction with the USB printer (Vendor ID: `0x28e9`, Product ID: `0x0289`). Manages image scaling, rotation, and monochrome conversion (`bitImageColumn`).
- **`label_maker.py`**: Utility for creating framed text images, handles line splitting and monochrome conversion.
- **`emoji_sticker_maker.py`**: Generates specific sticker-style emoji images.

## Technical Details
- **Framework**: Flask (Python)
- **Printer Protocol**: ESC/POS via USB (using `python-escpos`)
- **Image Processing**: `Pillow` (PIL) for scaling, rotation, and monochrome conversion.
- **Font Support**: Uses Noto Sans fonts (typically located in `/home/pi/StickerServer/static/fonts/` on target devices).
