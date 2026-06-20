# StickerServer

A Python-based Flask REST server designed to transform text and images into printable labels for ESC/POS thermal printers.

## Overview

StickerServer provides an easy-to-use interface to convert digital content into physical stickers. It handles the complexities of image processing (scaling, rotation, monochrome conversion) and protocol-specific commands required by thermal printers.

## Key Features

* **Text Labels**: Generate framed text labels with customizable styling (bold, italic, font size).
* **Image Printing**: Upload images to be printed, with automatic rotation and edge enhancement for optimal thermal printing.
* **Emoji Stickers**: Specialized support for generating stylized emoji stickers.
* **RESTful API**: Simple endpoints for automated integrations.

## API Endpoints

### **Text Labels**
`GET /label`
- **Purpose**: Generates and prints a text label.
- **Parameters**:
    - `text`: The content to print.
    - `bold`: (Boolean) Apply bold styling.
    - `italic`: (Boolean) Apply italic styling.
    - `font_size`: Size of the font.
    - `emoji_mode`: (Boolean) Enable special emoji styling.

### **Images**
`POST /image`
- **Purpose**: Prints an uploaded image.
- **Options**: Supports auto-rotation and edge enhancement for better clarity on thermal paper.

### **Web Interface**
`GET /`
- **Purpose**: Serves a simple web UI for manual control.

## Technical Implementation

* **Backend**: [Flask](https://flask.palletsprojects.com/)
* **Printer Protocol**: ESC/POS via USB (using `python-escpos`)
* **Image Processing**: [Pillow (PIL)](https://python-pillow.org/) for monochrome conversion and scaling.
* **Hardware Target**: Typically designed for USB-connected thermal printers (e.g., Vendor ID: `0x28e9`, Product ID: `0x0289`).

## Setup & Usage

Requires Python 3.x and the following dependencies:
- `flask`
- `python-escpos`
- `Pillow`

Install dependencies:
```bash
pip install flask python-escpos Pillow
```

Run the server:
```bash
python server.py
```

*Note: Ensure your thermal printer is connected and permissions are correctly configured for USB access.*
