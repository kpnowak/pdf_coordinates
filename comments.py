import fitz  # PyMuPDF

def parse_annotation_data(file_path):
    annotations = []
    
    with open(file_path, 'r') as file:
        for line in file:
            # Extract the sentence (text to highlight), coordinates, and comment content
            sentence = line.split('"')[1]
            coordinates_part = line.split('(')[1].split(')')[0]
            coordinates = tuple(map(int, coordinates_part.split(',')))
            comment = line.split("Comment_content: ")[1].strip()
            
            annotations.append((sentence, coordinates, comment))
    
    return annotations

def highlight_text_and_add_annotations(pdf_path, output_path, annotations):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    
    # Iterate through the pages
    for page_number in range(doc.page_count):
        page = doc.load_page(page_number)
        
        for annotation in annotations:
            text_to_highlight, (x, y), comment = annotation

            # Calculate the rectangle for the annotation based on the specified coordinates
            rect = fitz.Rect(x, y, x + 200, y + 100)  # Adjust box width and height as needed

            # Search for the text and highlight it
            text_instances = page.search_for(text_to_highlight)

            for inst in text_instances:
                highlight = page.add_highlight_annot(inst)
                highlight.update()

            # Add a sticky note annotation (text annotation) at the specified coordinates
            text_annot = page.add_text_annot(rect.tl, comment)  # Place the annotation at the top-left corner of the rectangle
            text_annot.update()

    # Save the modified PDF
    doc.save(output_path)

# Example usage
pdf_path = "Find mistakes 1.pdf"
output_path = "output_highlighted.pdf"
annotations_file = "separate_output.txt"

annotations = parse_annotation_data(annotations_file)
highlight_text_and_add_annotations(pdf_path, output_path, annotations)