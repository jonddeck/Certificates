import pytesseract
from PIL import Image, ImageDraw, ImageFont

# Path to the image
image_path = 'alison green belt.png'
output_path = 'alison_green_belt_edited.png'

# Load the image
img = Image.open(image_path)
draw = ImageDraw.Draw(img)

# Configuration for Tesseract
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

def get_placeholder_box(words_to_find):
    n_boxes = len(data['text'])
    # Try to find sequences that match words_to_find
    # Since text might be fragmented, we search for indices
    for i in range(n_boxes - len(words_to_find) + 1):
        match = True
        for j in range(len(words_to_find)):
            if words_to_find[j].lower() not in data['text'][i+j].lower():
                match = False
                break
        if match:
            # Found it, return the combined box
            # Get indices that match
            indices = list(range(i, i+len(words_to_find)))
            left = min([data['left'][k] for k in indices])
            top = min([data['top'][k] for k in indices])
            right = max([data['left'][k] + data['width'][k] for k in indices])
            bottom = max([data['top'][k] + data['height'][k] for k in indices])
            return (left, top, right, bottom)
    return None

# Placeholder definitions
replacements = {
    tuple(['YOUR', 'NAME', 'WILL', 'APPEAR', 'HERE']): 'Jonas De Decker',
    tuple(['YOUR', 'COURSE', 'NAME', 'WILL', 'APPEAR', 'HERE']): 'Lean Six Sigma: Green Belt Foundations',
    tuple(['27h', 'April,', '2024']): '14th November, 2026'
}

for words, replacement in replacements.items():
    box = get_placeholder_box(list(words))
    if box:
        print(f"Found placeholder {words} at {box}")
        # Draw white rectangle to cover
        draw.rectangle(box, fill='white', outline='white')
        # Add new text
        # For a better font, you'd load one, but for this exercise let's use a basic one or try to scale it.
        # ImageFont.truetype(font='arial.ttf', size=20)
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        # Centering text inside the box is hard without font measurement, 
        # but let's just place it.
        draw.text((box[0], box[1]), replacement, fill='black', font=font)
    else:
        print(f"Could not find placeholder: {words}")

img.save(output_path)
print(f"Saved to {output_path}")

