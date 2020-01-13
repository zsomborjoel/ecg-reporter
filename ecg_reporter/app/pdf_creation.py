from fpdf import FPDF

pdf = FPDF()

def add_to_pdf(startdate, enddate, filename):

    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Heti ECG kimutatás {} - {}')
    pdf.ln(10)
    pdf.image('test.png', None, None, 200, 100)
    pdf.ln(10)
    pdf.image('new.png', None, None, 200, 100)
    pdf.ln(5)
    pdf.image('fullecg.png', None, None, 200, 100)


    pdf.output("yourfile6.pdf", "F")