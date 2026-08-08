from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO

def replace_pdf_title(input_pdf, output_pdf, new_title, font_path,
                      font_name="CustomFont", 
                      x=100, y=500, 
                      font_size=36,
                      box_width=600, box_height=80):
    """
    Replaces the title on the first page of a PDF by covering the old text 
    with a white rectangle and writing a new title using a custom font.
    """

    # Register custom font
    pdfmetrics.registerFont(TTFont(font_name, font_path))

    # Create overlay with white box + new title
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    # Draw white rectangle to "erase" old title
    can.setFillColor(white)
    can.rect(x-10, y-10, box_width, box_height, stroke=0, fill=1)

    # Draw new title text
    can.setFillColorRGB(0, 0, 0)  # black text (change if needed)
    can.setFont(font_name, font_size)
    can.drawString(x, y, new_title)
    can.save()

    # Move buffer to start
    packet.seek(0)

    # Read overlay + original PDF
    overlay_pdf = PdfReader(packet)
    original_pdf = PdfReader(open(input_pdf, "rb"))
    writer = PdfWriter()

    # Merge overlay onto first page
    first_page = original_pdf.pages[0]
    first_page.merge_page(overlay_pdf.pages[0])
    writer.add_page(first_page)

    # Keep the rest of the pages unchanged
    for page in original_pdf.pages[1:]:
        writer.add_page(page)

    # Save new PDF
    with open(output_pdf, "wb") as f:
        writer.write(f)


# Example usage:
replace_pdf_title(
    input_pdf="slide.pdf",
    output_pdf="slide_custom.pdf",
    new_title="My Custom Title",
    font_path="MyFont.ttf",   # custom font file
    font_name="MyFont",
    x=150, y=400,             # position of new title
    font_size=48,
    box_width=700, box_height=100  # adjust to fully cover old title
)
