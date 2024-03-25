import fitz  # PyMuPDF
import re

# Open the PDF file
pdf_document = fitz.open("dataset/64_channel_sharbrough.pdf")

# Iterate through each page (there should be only one in this case)
for page_num in range(len(pdf_document)):
    # Get the page
    page = pdf_document[page_num]
    
    # Extract text from the page along with bbox positions
    text_instances = page.search_for(r"\b(\w+\d+)\b")  # Regex to find words followed by numbers

# Will hold our label and bbox center positions
eeg_coords = {}

# Process text instances and save the center positions
for inst in text_instances:
    # Extracting label from the bbox block (assuming the label is within the bbox)
    # Get the actual text that corresponds to this bbox
    words = page.get_textbox(inst)
    print(words)
    # Find labels like Fp1, F7, Oz, etc., but ignore single characters as they are not EEG labels
    label_search = re.search(r'\b(\w\d+)\b', words)
    if label_search:
        label = label_search.group(1)
        # Calculate the center of the bbox (which is a rectangle given by top-left and bottom-right points)
        center_x = inst[0] + (inst[2] - inst[0]) / 2
        center_y = inst[1] + (inst[3] - inst[1]) / 2
        eeg_coords[label] = (center_x, center_y)

pdf_document.close()

print(eeg_coords)