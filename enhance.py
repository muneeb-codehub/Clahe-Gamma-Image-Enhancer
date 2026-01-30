import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# ---------- Setup ----------
save_path = "results-final"
os.makedirs(save_path, exist_ok=True)

# ---------- Function: Showing + Saving image and histogram ----------
def show_and_save(title, original, processed, filename, suffix):
    out_path = os.path.join(save_path, f"{filename}_{suffix}.jpg")
    cv2.imwrite(out_path, processed)

    fig, axs = plt.subplots(2, 2, figsize=(12, 7))
    fig.suptitle(title, fontsize=14)

    # Original
    axs[0, 0].imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    axs[0, 0].set_title("Original")
    axs[0, 0].axis("off")

    # Processed
    axs[0, 1].imshow(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB))
    axs[0, 1].set_title("Enhanced")
    axs[0, 1].axis("off")

    # Histogram (Original RGB)
    colors = ('b', 'g', 'r')
    for i, col in enumerate(colors):
        axs[1, 0].hist(original[:, :, i].ravel(), bins=256, color=col, alpha=0.5, label=f"{col.upper()}")
    axs[1, 0].set_title("Original Histogram")
    axs[1, 0].legend()

    # Histogram (Processed RGB)
    for i, col in enumerate(colors):
        axs[1, 1].hist(processed[:, :, i].ravel(), bins=256, color=col, alpha=0.5, label=f"{col.upper()}")
    axs[1, 1].set_title("Enhanced Histogram")
    axs[1, 1].legend()

    plt.show()

# ---------- Histogram Equalization (CLAHE on Color Image) ----------
def histogram_equalization(img, filename):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)

    limg = cv2.merge((cl, a, b))
    equ_bgr = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    show_and_save("Histogram Equalization (Color)", img, equ_bgr, filename, "histeq")
    return equ_bgr

# ---------- Gamma Correction ----------
def gamma_correction(img, gamma, filename):
    if gamma <= 0:
        gamma = 1.0

    table = np.array([((i / 255.0) ** gamma) * 255
                      for i in np.arange(256)]).astype("uint8")

    gamma_img = cv2.LUT(img, table)
    show_and_save(f"Gamma Correction (γ={gamma})", img, gamma_img, filename, f"gamma{gamma}")
    return gamma_img

# ---------- Combined Enhancement (CLAHE + Gamma) ----------
def combined_enhancement(img, gamma, filename):
    # Step 1: Apply CLAHE
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)

    limg = cv2.merge((cl, a, b))
    clahe_bgr = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    # Step 2: Apply Gamma Correction
    if gamma <= 0:
        gamma = 1.0
    table = np.array([((i / 255.0) ** gamma) * 255
                      for i in np.arange(256)]).astype("uint8")
    combined_img = cv2.LUT(clahe_bgr, table)

    show_and_save(f"Combined Enhancement (CLAHE + γ={gamma})", img, combined_img, filename, f"combined_gamma{gamma}")
    return combined_img

# ---------- Main ----------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python enhance.py <image_path>")
        sys.exit(1)

    img_path = sys.argv[1]
    if not os.path.exists(img_path):
        print(f"[ERROR] File not found: {img_path}")
        sys.exit(1)

    # Loading image
    img = cv2.imread(img_path)
    if img is None:
        print(f"[ERROR] Could not read image: {img_path}")
        sys.exit(1)

    filename = os.path.splitext(os.path.basename(img_path))[0]
    print(f"[INFO] Processing: {filename}")

    # Applying techniques
    histogram_equalization(img, filename)
    gamma_correction(img, gamma=0.5, filename=filename)

    # Combined Enhancement (dark images use γ=0.5, light images use γ=1.5 or 2.0)
    combined_enhancement(img, gamma=0.5, filename=filename)   # for dark image
    combined_enhancement(img, gamma=1.5, filename=filename)   # for bright image

    print(f"[INFO] Done! Enhanced images saved in: {save_path}")
