import numpy as np
from PIL import Image
import trimesh
import qrcodegen as qrcg

def load_image(image_path):
    """Load and binarize the image."""
    image = Image.open(image_path).convert('L')
    image_array = np.array(image)
    threshold = 128
    binary_image = (image_array < threshold).astype(np.uint8)
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

def load_qr_matrix(qr):
    """Get the binary matrix from the QRCode object."""
    qr_matrix = qr.get_matrix()
    binary_matrix = np.array(qr_matrix).astype(np.uint8)
    return binary_matrix

def find_black_squares_from_qrmatrix(binary_matrix):
    """Identify the positions of black squares."""
    n, m = binary_matrix.shape
    black_squares = []
    for i in range(n):
        for j in range(m):
            if binary_matrix[i, j] == 1:
                black_squares.append((i, j))
    return black_squares

def create_vertices_and_faces(black_squares, pixel_size_mm, extrusion_depth_mm):
    """Generate vertices and faces for the 3D extrusion."""
    vertices = []
    faces = []
    for (i, j) in black_squares:
        x1, y1 = j * pixel_size_mm, i * pixel_size_mm
        x2, y2 = (j + 1) * pixel_size_mm, (i + 1) * pixel_size_mm
        z = extrusion_depth_mm

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

def extrude_qr_code_from_image(image_path, output_path, image_size_mm, extrusion_depth_mm):
    binary_image = load_image(image_path)
    black_squares = find_black_squares_from_image(binary_image)
    pixel_size_mm = image_size_mm / max(binary_image.shape)
    vertices, faces = create_vertices_and_faces(black_squares, pixel_size_mm, extrusion_depth_mm)
    mesh = create_mesh(vertices, faces)
    save_mesh(mesh, output_path)

def extrude_qr_code_from_url(url, output_path, image_size_mm, extrusion_depth_mm):
    QRcode = qrcg.generate_qr_code(url)
    QRmatrix = load_qr_matrix(QRcode)
    black_squares = find_black_squares_from_qrmatrix(QRmatrix)
    pixel_size_mm = image_size_mm / len(QRmatrix)
    vertices, faces = create_vertices_and_faces(black_squares, pixel_size_mm, extrusion_depth_mm)
    mesh = create_mesh(vertices, faces)
    save_mesh(mesh, output_path)

def main():
    # Usage
    image_path = 'qrout.png'
    url = 'https://www.zou-mse-utoronto-ca.net/'

    output_path = 'out.stl'
    image_size_mm = 50  # Size of the image in mm
    extrusion_depth_mm = 10  # Depth of the extrusion in mm
    
    extrude_qr_code_from_url(url, output_path, image_size_mm, extrusion_depth_mm)
    #extrude_qr_code_from_image(image_path, output_path, image_size_mm, extrusion_depth_mm)

if __name__ == '__main__':
    main()
