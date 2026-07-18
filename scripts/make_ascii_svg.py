import os
import cv2
import numpy as np

def convert_to_ascii_svg(input_path="source-prepped.png", output_path="avi-ascii.svg"):
    if not os.path.exists(input_path):
        print(f"Error: Prepped image '{input_path}' not found. Run prep_photo.py first.")
        return

    # Load the prepped grayscale image
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    
    # Target grid resolution (~100 columns wide, adjusting height proportionally)
    # Character aspect ratios are typically taller than wide (~1:2), so we adjust the scale
    target_width = 100
    aspect_ratio = img.shape[0] / img.shape[1]
    target_height = int(target_width * aspect_ratio * 0.55)
    
    # Resize to the small character grid
    grid = cv2.resize(img, (target_width, target_height), interpolation=cv2.INTER_AREA)

    # Clean density ramp: bright (spaces) to dark (dense characters)
    # The leading space allows bright areas/background to wash away completely
    RAMP = " .`:-=+*cs#%@"
    ramp_len = len(RAMP)

    # Convert pixel values (0-255) to character indices
    ascii_rows = []
    for y in range(target_height):
        row_chars = ""
        for x in range(target_width):
            pixel_val = grid[y, x]
            # Map 0-255 to 0 -> ramp_len - 1
            idx = int((pixel_val / 255.0) * (ramp_len - 1))
            row_chars += RAMP[idx]
        ascii_rows.append(row_chars)

    # SVG layout metrics
    font_size = 12
    char_width = 7.2    # Horizontal spacing per character
    char_height = 13.0  # Vertical line spacing
    
    svg_width = int(target_width * char_width)
    svg_height = int(target_height * char_height)

    # Build the SVG content with SMIL text-reveal layout
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">',
        '  <defs>',
        '    <style>',
        '      @import url("https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&amp;display=swap");',
        '      .ascii-text { font-family: "Fira Code", monospace; font-size: 12px; fill: #a6acb9; }',
        '    </style>',
        '  </defs>',
        f'  <rect width="100%" height="100%" fill="#0d1117" />' # Dark terminal background
    ]

    # Generate each row with a staggered animation delay to create the typewriter effect
    for idx, row in enumerate(ascii_rows):
        y_pos = int((idx + 1) * char_height)
        # Escape any raw XML entities just in case
        safe_row = row.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        # Stagger delay calculations (top-to-bottom row reveal)
        delay = idx * 0.04
        
        # Pack the line into the SVG with a subtle fade/reveal SMIL block attribute
        svg_lines.append(f'  <text x="10" y="{y_pos}" class="ascii-text" opacity="0">')
        svg_lines.append(f'    {safe_row}')
        svg_lines.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.1s" begin="{delay:.2f}s" fill="freeze" />')
        svg_lines.append('  </text>')

    svg_lines.append('</svg>')

    # Write out the self-contained animated artwork
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
        
    print(f"Success! Animated ASCII portrait compiled to: {output_path}")

if __name__ == "__main__":
    convert_to_ascii_svg()
