#!/usr/bin/env python3
"""
xnb-extractor
A standalone Python tool and library for decoding Microsoft XNA / MonoGame
Texture2D .xnb asset files into PNG images.
"""

import os
import sys
import struct
import argparse
from PIL import Image

__version__ = "1.0.0"

def read_7bit_encoded_int(f):
    """Reads a .NET BinaryWriter 7-bit encoded integer."""
    res = 0
    shift = 0
    while True:
        byte = f.read(1)
        if not byte:
            raise EOFError("Unexpected end of file while reading 7-bit encoded int.")
        b = byte[0]
        res |= (b & 0x7F) << shift
        if (b & 0x80) == 0:
            break
        shift += 7
    return res

def unpack_xnb_texture(xnb_path, out_png_path=None):
    """
    Decodes an uncompressed XNA Texture2D .xnb file into a PNG image.

    :param xnb_path: Path to the input .xnb file.
    :param out_png_path: Destination path for the output .png file.
                         If None, replaces .xnb extension with .png.
    :return: PIL.Image instance of the unpacked texture.
    """
    if not os.path.isfile(xnb_path):
        raise FileNotFoundError(f"File not found: {xnb_path}")

    with open(xnb_path, 'rb') as f:
        magic = f.read(3)
        if magic != b'XNB':
            raise ValueError(f"Invalid magic identifier '{magic.decode('latin1', errors='replace')}'; expected 'XNB'.")

        platform = f.read(1).decode('ascii', errors='replace')
        version = f.read(1)[0]
        flags = f.read(1)[0]
        file_size = struct.unpack('<I', f.read(4))[0]

        is_compressed = bool(flags & 0x80)
        if is_compressed:
            raise NotImplementedError(
                f"LZX/Deflate compression is enabled in '{os.path.basename(xnb_path)}'. "
                "Compressed XNB archives are not yet supported."
            )

        # Type Manifest
        reader_count = read_7bit_encoded_int(f)
        readers = []
        for _ in range(reader_count):
            name_len = read_7bit_encoded_int(f)
            reader_name = f.read(name_len).decode('ascii', errors='ignore')
            reader_version = struct.unpack('<I', f.read(4))[0]
            readers.append((reader_name, reader_version))

        shared_resources = read_7bit_encoded_int(f)
        primary_type_index = read_7bit_encoded_int(f)

        # Texture2D Payload
        surface_format = struct.unpack('<I', f.read(4))[0] # 0 = SurfaceFormat.Color (RGBA)
        width = struct.unpack('<I', f.read(4))[0]
        height = struct.unpack('<I', f.read(4))[0]
        mip_count = struct.unpack('<I', f.read(4))[0]
        data_size = struct.unpack('<I', f.read(4))[0]

        raw_bytes = f.read(data_size)

    # Convert to image
    # Format 0 = 32-bit RGBA (XNA Color)
    if surface_format == 0:
        img = Image.frombytes('RGBA', (width, height), raw_bytes)
    else:
        # Fallback raw buffer
        img = Image.frombytes('RGBA', (width, height), raw_bytes[:width * height * 4])

    if out_png_path is None:
        out_png_path = os.path.splitext(xnb_path)[0] + ".png"

    os.makedirs(os.path.dirname(os.path.abspath(out_png_path)), exist_ok=True)
    img.save(out_png_path)
    return img

def batch_extract(input_dir, output_dir=None, recursive=False):
    """
    Finds and extracts all .xnb texture files in a directory.

    :param input_dir: Folder containing .xnb files.
    :param output_dir: Destination folder. Defaults to input_dir if None.
    :param recursive: Whether to search subdirectories recursively.
    """
    if output_dir is None:
        output_dir = input_dir

    count = 0
    for root, _, files in os.walk(input_dir):
        if not recursive and root != input_dir:
            continue

        for fname in files:
            if fname.lower().endswith(".xnb"):
                src_path = os.path.join(root, fname)
                rel_path = os.path.relpath(src_path, input_dir)
                dst_png = os.path.join(output_dir, os.path.splitext(rel_path)[0] + ".png")

                try:
                    img = unpack_xnb_texture(src_path, dst_png)
                    print(f"Extracted: {rel_path} -> {dst_png} ({img.width}x{img.height})")
                    count += 1
                except Exception as e:
                    print(f"Failed to extract '{rel_path}': {e}", file=sys.stderr)

    print(f"\nDone. Successfully extracted {count} textures.")

def main():
    parser = argparse.ArgumentParser(
        prog="xnb-extractor",
        description="Extract Microsoft XNA and MonoGame Texture2D .xnb assets to PNG format."
    )
    parser.add_argument("input", help="Path to an .xnb file or a folder containing .xnb files.")
    parser.add_argument("-o", "--output", help="Output path (PNG file path if single file, or target directory).")
    parser.add_argument("-r", "--recursive", action="store_true", help="Recursively search folders for .xnb files.")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")

    args = parser.parse_args()

    if os.path.isfile(args.input):
        out = args.output or (os.path.splitext(args.input)[0] + ".png")
        img = unpack_xnb_texture(args.input, out)
        print(f"Saved: {out} ({img.width}x{img.height})")
    elif os.path.isdir(args.input):
        batch_extract(args.input, args.output, recursive=args.recursive)
    else:
        print(f"Error: Path does not exist: {args.input}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
