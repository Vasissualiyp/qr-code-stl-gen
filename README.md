# QR Code to STL Extruder

This project provides a script to generate a 3D extruded model (STL file) from a QR code. The QR code can be created either from a URL or an existing image file. 

It is highly recommended to use the built-in QR code generation feature rather than generating a QR code from an image. QR codes generated directly from the URL are significantly smaller in size (approximately 0.5 MB) compared to those generated from images (which can be as large as 1.6 GB).

## Features

- Generate a QR code from a URL and extrude it to a 3D model.
- Use an existing image to create a QR code and extrude it to a 3D model.
- Configuration through a JSON file for flexibility and ease of use.

## Requirements

- Python 3.x
- Required libraries: `argparse`, `qrcode`, `numpy`, `Pillow`, `trimesh`

You can install the required libraries using pip:

```sh
pip install argparse qrcode numpy pillow trimesh
```

## Configuration

The script uses a JSON configuration file to specify the parameters. Create a `config.json` file with the following structure:

```json
{
    "qrcode_type": "url",
    "image_path": "path/to/your/image.png",
    "url": "https://example.com",
    "output_path": "output.stl",
    "qr_size_mm": 50,
    "qr_depth_mm": 10,
    "invert": false
}
```

- `qrcode_type`: Specifies the type of QR code source. Possible values are `url` `roundimg` or `image`.
- `image_path`: Path to the input image file (used if `qrcode_type` is `image` or `roundimg`).
- `url`: URL to encode in the QR code (used if `qrcode_type` is `url` or `roundimg`).
- `output_path`: Path to save the output STL file.
- `qr_size_mm`: Size of the QR code image in millimeters (when look from the top)
- `qr_depth_mm`: Depth of the extrusion in millimeters (height when look from the side)
- `invert`: Whether to invert the QR code (pass boolean `true` or `false`)

So the final stl of the qr code will have the dimensions of:
```
qr_size_mm x qr_size_mm x qr_depth_mm
```

You can also use the example config file, provided in the codebase, as a template.

### QR Code types

Currently, the following values of `qrcode_type` are supported:
- `url`: creates square QR code in stl format, taken from the url. 
**This QR code type would be the most space-efficient compared to the options below**
- `image`: creates square QR code in stl format, taken from the image.
- `roundimg`: creates round QR code in stl format, taken from the url.
- `lineimg`: creates bar-type QR code in stl format, taken from the url.


## Usage

Run the script with the configuration file as an argument:

```sh
python stl_gen.py --config config.json
```

If you run the code from inside of the IDE or don't pass the config flag, it would just take in
`config.json` file by default.

## Script Overview

The main script performs the following steps:

1. **Setup Argument Parser**: Parses the command-line argument for the config file path.
2. **Load Configuration**: Reads the configuration file and retrieves values.
3. **Process QR Code**:
   - If `qrcode_type` is `url`, generate a QR code from the URL and extrude it.
   - If `qrcode_type` is `image`, use the existing image to generate the QR code and extrude it.
4. **Generate 3D Model**: Creates the 3D vertices and faces from the QR code and saves it as an STL file.

The functions used in the script include:
- `load_config(config_path)`: Loads the configuration file.
- `extrude_qr_code_from_url(url, output_path, image_size_mm, extrusion_depth_mm)`: Generates and extrudes a QR code from a URL.
- `extrude_qr_code_from_image(image_path, output_path, image_size_mm, extrusion_depth_mm)`: Generates and extrudes a QR code from an image file.

Ensure that the configuration file is correctly specified and all required libraries are installed before running the script.

### Contributions

If you need additional features beyond URL-based QR code generation, feel free to request them or contribute by adding them yourself. Pull requests are welcome!


