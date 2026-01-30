# CLAHE-Gamma Image Enhancer

Image enhancement tool utilizing CLAHE (Contrast Limited Adaptive Histogram Equalization) and Gamma Correction to improve low-light and poor-contrast images. Supports multiple enhancement modes with histogram visualization.

## Features

- **Histogram Equalization (CLAHE)**: Applies CLAHE on the luminance channel in LAB color space for adaptive contrast enhancement
- **Gamma Correction**: Adjusts image brightness using gamma transformation
- **Combined Enhancement**: Combines CLAHE and Gamma Correction for optimal results
- **Histogram Visualization**: Displays before/after comparisons with RGB histograms
- **Automatic Saving**: Saves all enhanced images with descriptive filenames

## Requirements

```bash
pip install opencv-python numpy matplotlib
```

## Usage

Run the script with an image path as argument:

```bash
python enhance.py
```

## Enhancement Techniques

1. **Histogram Equalization (CLAHE)**: 
   - Clip Limit: 4.0
   - Tile Grid Size: 8x8
   - Applied on LAB color space

2. **Gamma Correction**: 
   - γ = 0.5 (for dark images)
   
3. **Combined Enhancement**:
   - CLAHE + γ = 0.5 (for dark images)
   - CLAHE + γ = 1.5 (for bright images)

## Output

All enhanced images are saved in the `results-final/` directory with the following naming convention:
- `{filename}_histeq.jpg` - Histogram equalization result
- `{filename}_gamma{value}.jpg` - Gamma correction result
- `{filename}_combined_gamma{value}.jpg` - Combined enhancement result

## Project Structure

```
.
├── enhance.py          # Main enhancement script
├── enhance.ipynb       # Jupyter notebook version
├── *.png              # Sample images
└── results/     # Output directory
```

## Author

**Muneeb Arif**  
Email: muneebarif226@gmail.com

## License

This project is open source and available for educational purposes.
