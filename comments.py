import fitz  # PyMuPDF

def parse_annotation_data(file_path):
    annotations = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith('"') and 'Comment_content' in line:
                # Case where the sentence and comment are on the same line
                sentence = line.split('"')[1]
                coordinates_part = line.split('(')[1].split(')')[0]
                coordinates = tuple(map(int, coordinates_part.split(',')))
                comment = line.split("Comment_content: ")[1].strip()
                annotations.append((sentence, coordinates, comment))
                i += 1
            elif line.startswith('"') and i + 1 < len(lines) and lines[i + 1].startswith("Comment_content"):
                # Case where the comment is on the next line
                sentence = line.split('"')[1]
                coordinates_part = line.split('(')[1].split(')')[0]
                coordinates = tuple(map(int, coordinates_part.split(',')))
                comment = lines[i + 1].split("Comment_content: ")[1].strip()
                annotations.append((sentence, coordinates, comment))
                i += 2
            else:
                i += 1
    
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