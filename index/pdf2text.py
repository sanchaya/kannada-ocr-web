
import sys
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import os
import io

language = "kan+eng"

class Pdf2Text:
    
    def __init__(self, pdf, output):
        """
        pdf selected
        """
        self.pdf = pdf
        self.output = output
    
    def convert2text(self):
        pages = convert_from_path(self.pdf, 500)
        text = ""
        page_count = 1
        for page in pages:
            temp = io.BytesIO()
            page.save(temp, 'JPEG')
            text += str(((pytesseract.image_to_string(Image.open(temp), lang=language))))
            print("%s -> page %d completed."%(self.pdf, page_count))
            page_count += 1
    

        with open(self.output, "w") as f:
            f.write(text)
            
        print("file saved!")
        
    def convert(self):
        if os.path.isfile(self.pdf):
            self.convert2text()
        else:
            print("pdf file does not exist")