from setuptools import setup

setup(
    name="xnb-extractor",
    version="1.0.0",
    description="Standalone CLI and library to decode XNA/MonoGame Texture2D .xnb files into PNG images",
    author="Karl Lopez",
    py_modules=["xnb_extractor"],
    install_requires=[
        "Pillow>=8.0.0"
    ],
    entry_points={
        "console_scripts": [
            "xnb-extractor=xnb_extractor:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics",
    ],
    python_requires=">=3.8",
)
