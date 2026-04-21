from fpdf import FPDF

def create_pdf(text):
    if not text:
        return None

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in text.split("\n"):
        safe = line.encode("latin-1","replace").decode("latin-1")
        pdf.cell(200,10,txt=safe,ln=True)

    file = "notes.pdf"
    pdf.output(file)
    return file