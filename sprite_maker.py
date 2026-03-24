#!/usr/bin/env python3

import sys
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans


def expand_matrix_to_square(arr, fill_value=0):
    arr = np.asarray(arr)
    rows, cols = arr.shape

    if rows == cols:
        return arr

    if rows < cols:
        diff = cols - rows
        pad_top = diff // 2
        pad_bottom = diff - pad_top
        padding = ((pad_top, pad_bottom), (0, 0))
    else:
        diff = rows - cols
        pad_left = diff // 2
        pad_right = diff - pad_left
        padding = ((0, 0), (pad_left, pad_right))
    return np.pad(arr, padding, mode='constant', constant_values=fill_value)

def resize_image(img, max_size):
    w, h = img.size

    if w <= max_size and h <= max_size:
        return img

    scale = min(max_size / w, max_size / h)
    new_w = int(w * scale)
    new_h = int(h * scale)

    return img.resize((new_w, new_h), Image.LANCZOS)


def quantize_to_indices(img, k):
    data = np.array(img)
    h, w, _ = data.shape

    pixels = data.reshape((-1, 3))

    kmeans = KMeans(n_clusters=k, n_init=10)
    labels = kmeans.fit_predict(pixels)

    palette = kmeans.cluster_centers_.astype(np.uint8)

    index_matrix = labels.reshape((h, w))

    return index_matrix, palette

def show_indexed_image(index_matrix, palette):
    import matplotlib.pyplot as plt

    # Convert indices → RGB image
    rgb_image = palette[index_matrix]

    plt.imshow(rgb_image)
    plt.axis('off')
    plt.title("Quantized Image")
    plt.show()


def matrix_to_2bpp(matrix):
    bin = 2 ** np.arange(matrix.shape[1] - 1, -1, -1)
    msb = (matrix >> 1) @ bin
    lsb = (matrix & 1) @ bin

    return np.column_stack((msb, lsb)).ravel()

def burn_matrix(fd, matrix, label, size="byte", label_end_suff="End"):
    res = "\n".join([f".{size} " + ", ".join([f"${v:02X}" for v in row]) for row in matrix])
    fd.write(f"{label}:\n{res}\n{label}{label_end_suff}:\n")

def color24bit_to_rgb555(v):
    v = v.astype(np.int32)  # avoid overflow if input is uint8

    return (
        ((v[:, 2] & (~7)) >> 3) +
        ((v[:, 1] & (~7)) << 2) +
        ((v[:, 0] & (~7)) << 7)
    )
def main():
    if len(sys.argv) != 4:
        print("Usage: script.py <image_path> <num_colors> <max_size>")
        sys.exit(1)

    image_path = sys.argv[1]
    k = int(sys.argv[2])
    max_size = int(sys.argv[3])

    img = Image.open(image_path).convert("RGB")
    img = resize_image(img, max_size)

    index_matrix, palette = quantize_to_indices(img, k)

    expand_matrix_to_square(index_matrix)

    # Print results (or you can process further)
    palette_rgb555 = color24bit_to_rgb555(palette)
    index_mat_2bpp = matrix_to_2bpp(index_matrix)
    with open("sprite.asm", "w") as f:
        burn_matrix(f, index_mat_2bpp.reshape(-1, 4), "Sprite")
        f.write("\n")
        burn_matrix(f, palette_rgb555.reshape(1, -1), "Palette", size="word")

if __name__ == "__main__":
    main()
