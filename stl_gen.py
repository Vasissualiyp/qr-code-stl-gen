import qrcodegen as qrcg

import numpy as np
from PIL import Image
import trimesh
import argparse
import json

######################################################
############### CONFIGURATION SETUP ##################
######################################################

class Config:
    def __init__(self, config_path):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        
        self.qrcode_type = config.get('qrcode_type')
        self.image_path = config.get('image_path')
        self.url = config.get('url')
        self.output_path = config.get('output_path')
        self.qr_size_mm = config.get('qr_size_mm')
        self.qr_depth_mm = config.get('qr_depth_mm')
        self.invert = config.get('invert', False)

def load_config(config_path):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config

######################################################
############ IMAGE/MATRIX MANIPULATION ###############
######################################################

def load_qr_matrix(qr):
    """Get the binary matrix from the QRCode object."""
    qr_matrix = qr.get_matrix()
    binary_matrix = np.array(qr_matrix).astype(np.uint8)
    return binary_matrix

def load_image(image_path):
    """Load and binarize the image."""
    image = Image.open(image_path).convert('L')
    image_array = np.array(image)
    threshold = 128
    binary_image = (image_array < threshold).astype(np.uint8)
    return binary_image

def invert_binary_image(binary_image, config):
    if config.invert:
        #print(binary_image)
        np.set_printoptions(threshold=np.inf)
        print(binary_image)
        flipped_binary_image = 1 - binary_image
        print(flipped_binary_image)
        #print(flipped_binary_image)
        return flipped_binary_image
    else:
        return binary_image

def find_black_squares_from_image(binary_image):
    """Identify the positions of black squares."""
    n, m = binary_image.shape
    black_squares = []
    for i in range(n):
        for j in range(m):
            if binary_image[i, j] == 1:
                black_squares.append((i, j))
    return black_squares

######################################################
################ MESH MANIPULATION ###################
######################################################

def create_vertices_and_faces(black_squares, pixel_size_mm, qr_depth_mm):
    """Generate vertices and faces for the 3D extrusion."""
    vertices = []
    faces = []
    for (i, j) in black_squares:
        x1, y1 = j * pixel_size_mm, i * pixel_size_mm
        x2, y2 = (j + 1) * pixel_size_mm, (i + 1) * pixel_size_mm
        z = qr_depth_mm

        v0 = (x1, y1, 0)
        v1 = (x2, y1, 0)
        v2 = (x2, y2, 0)
        v3 = (x1, y2, 0)
        v4 = (x1, y1, z)
        v5 = (x2, y1, z)
        v6 = (x2, y2, z)
        v7 = (x1, y2, z)

        base_index = len(vertices)
        vertices.extend([v0, v1, v2, v3, v4, v5, v6, v7])

        faces.extend([
            (base_index, base_index + 1, base_index + 2),
            (base_index, base_index + 2, base_index + 3),
            (base_index + 4, base_index + 5, base_index + 6),
            (base_index + 4, base_index + 6, base_index + 7),
            (base_index, base_index + 1, base_index + 5),
            (base_index, base_index + 5, base_index + 4),
            (base_index + 1, base_index + 2, base_index + 6),
            (base_index + 1, base_index + 6, base_index + 5),
            (base_index + 2, base_index + 3, base_index + 7),
            (base_index + 2, base_index + 7, base_index + 6),
            (base_index + 3, base_index, base_index + 4),
            (base_index + 3, base_index + 4, base_index + 7),
        ])
    return vertices, faces

def create_mesh(vertices, faces):
    """Create and return the mesh."""
    vertices = np.array(vertices)
    faces = np.array(faces)
    return trimesh.Trimesh(vertices=vertices, faces=faces)

def save_mesh(mesh, output_path):
    """Save the mesh to an STL file."""
    mesh.export(output_path)

def create_mesh_from_black_squares(black_squares, config, qrcode_array_size):
    pixel_size_mm = config.qr_size_mm / qrcode_array_size
    vertices, faces = create_vertices_and_faces(black_squares, pixel_size_mm, config.qr_depth_mm)
    mesh = create_mesh(vertices, faces)
    save_mesh(mesh, config.output_path)

######################################################
####### EXTRUSION RULES FOR DIFFERENT CASES ##########
######################################################

def extrude_qr_code_from_image(config):
    binary_image = load_image(config.image_path)

    binary_image = invert_binary_image(binary_image, config)
    black_squares = find_black_squares_from_image(binary_image)

    create_mesh_from_black_squares(black_squares, config, max(binary_image.shape))

def extrude_qr_code_from_round(config):
    QRcode = qrcg.generate_qr_code(config.url, vistype = 'round', image_path = config.image_path)
    binary_image = load_image(config.image_path)

    binary_image = invert_binary_image(binary_image, config)
    black_squares = find_black_squares_from_image(binary_image)

    create_mesh_from_black_squares(black_squares, config, max(binary_image.shape))

def extrude_qr_code_from_line(config):
    QRcode = qrcg.generate_qr_code(config.url, vistype = 'line', image_path = config.image_path)
    binary_image = load_image(config.image_path)

    binary_image = invert_binary_image(binary_image, config)
    black_squares = find_black_squares_from_image(binary_image)

    create_mesh_from_black_squares(black_squares, config, max(binary_image.shape))

def extrude_qr_code_from_url(config):
    QRcode = qrcg.generate_qr_code(config.url)
    QRmatrix = load_qr_matrix(QRcode)

    binary_image = invert_binary_image(QRmatrix, config)
    black_squares = find_black_squares_from_image(binary_image)
    
    create_mesh_from_black_squares(black_squares, config, len(binary_image))

def choose_extrusion_model_and_generate_qrcode(config):
    if config.qrcode_type == 'url':
        extrude_qr_code_from_url(config)
    elif config.qrcode_type == 'image':
        extrude_qr_code_from_image(config)
    elif config.qrcode_type == 'roundimg':
        extrude_qr_code_from_round(config)
    elif config.qrcode_type == 'lineimg':
        extrude_qr_code_from_line(config)
    else:
        print("Invalid type of qrcode. So far, the only available 'qrcode_type' values are:")
        print("url, image, roundimg")

######################################################
######################## MAIN ########################
######################################################

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Extrude QR code to STL')
    parser.add_argument('--config', default='config.json', help='Path to the config file (default: default_config.json)')
    # Parse arguments
    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)
    
    # Retrieve values from config
    config = Config(args.config)

    choose_extrusion_model_and_generate_qrcode(config)
    
if __name__ == '__main__':
    main()
