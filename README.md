# xnb-extractor

A fast, lightweight standalone Python tool and library to extract Microsoft XNA and MonoGame `Texture2D` `.xnb` asset files into standard `.png` images.

---

## Features

- **Direct Texture Extraction**: Parses XNA 4.0 binary `Texture2D` chunks into standard PNGs.
- **Single File & Batch Mode**: Unpack a single asset or recursively convert entire game asset directories.
- **Python Library & CLI**: Use as a command-line utility or import directly into your own data pipeline scripts.
- **Zero Heavy Dependencies**: Built purely on Python and [Pillow](https://python-pillow.org/).

---

## Installation

### From Source
```bash
git clone https://github.com/<YOUR_USERNAME>/xnb-extractor.git
cd xnb-extractor
pip install -e .
```

Or install the single required dependency directly:
```bash
pip install Pillow
```

---

## CLI Usage

### 1. Extract a single `.xnb` file:
```bash
python xnb_extractor.py path/to/texture.xnb
# Creates path/to/texture.png
```

Specifying a custom output path:
```bash
python xnb_extractor.py path/to/texture.xnb -o output/sprite.png
```

### 2. Batch extract a directory:
```bash
python xnb_extractor.py path/to/Content/ -o extracted_pngs/
```

### 3. Recursive directory extraction:
```bash
python xnb_extractor.py path/to/Content/ -o extracted_pngs/ --recursive
```

---

## Python API Usage

You can also import `xnb-extractor` in your own scripts:

```python
from xnb_extractor import unpack_xnb_texture

# Unpacks and saves to PNG, returning a PIL Image object
image = unpack_xnb_texture("sprites.xnb", "sprites.png")
print(f"Dimensions: {image.width}x{image.height}")
```

---

## Supported Formats

- **Format**: Microsoft XNA Game Studio 4.0 / MonoGame `Texture2D`
- **Surface Format**: Color (32-bit RGBA)
- **Compression**: Uncompressed XNB streams

---

## License

MIT License. See [LICENSE](LICENSE) for details.
