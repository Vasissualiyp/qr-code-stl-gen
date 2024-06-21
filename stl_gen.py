import numpy as np
from PIL import Image
import trimesh

def extrude_qr_code(image_path, output_path, image_size_mm, extrusion_depth_mm):
    # Load the image
    image = Image.open(image_path).convert('L')  # Convert to grayscale
    image_array = np.array(image)

    # Binarize the image (0 for white, 1 for black)
    threshold = 128
    binary_image = (image_array < threshold).astype(np.uint8)

    # Get the dimensions of the image in pixels
    n, m = binary_image.shape

    # Calculate the pixel size in mm
    pixel_size_mm = image_size_mm / max(n, m)

    # Create the vertices and faces for the extrusion
    vertices = []
    faces = []

    # Iterate over the pixels
    for i in range(n):
        for j in range(m):
            if binary_image[i, j] == 1:
                # Calculate the 3D coordinates for the black pixels
                x1, y1 = j * pixel_size_mm, i * pixel_size_mm
                x2, y2 = (j + 1) * pixel_size_mm, (i + 1) * pixel_size_mm
                z = extrusion_depth_mm

                # Create vertices for the extruded cube
                v0 = (x1, y1, 0)
                v1 = (x2, y1, 0)
                v2 = (x2, y2, 0)
                v3 = (x1, y2, 0)
                v4 = (x1, y1, z)
                v5 = (x2, y1, z)
                v6 = (x2, y2, z)
                v7 = (x1, y2, z)

                # Add vertices to the list
                base_index = len(vertices)
                vertices.extend([v0, v1, v2, v3, v4, v5, v6, v7])

                # Create faces for the cube
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

    # Create the mesh
    vertices = np.array(vertices)
    faces = np.array(faces)
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

    # Export the mesh to STL
    mesh.export(output_path)

# Usage
image_path = 'path/to/your/qr_code.png'
output_path = 'path/to/output/qr_code.stl'
image_size_mm = 50  # Size of the image in mm
extrusion_depth_mm = 10  # Depth of the extrusion in mm

extrude_qr_code(image_path, output_path, image_size_mm, extrusion_depth_mm)
