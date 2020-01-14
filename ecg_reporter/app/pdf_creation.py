from ecg_reporter.app.configs import get_config
from ecg_reporter.app.logs import add_to_log
from fpdf import FPDF
import os

pdf = FPDF()

def add_to_pdf(startdate, enddate):
    """
    :param startdate: string
    :param enddate: string
    :return: string, pdf path / string, filename
    """
    images_directory = get_config('images_path')
    pdf_directory = get_config('pdf_path')

    # pdf file structure
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Weekly ECG report {} - {}'.format(startdate, enddate))
    pdf.set_font('Arial', '', 12)

    for filename in os.listdir(images_directory):
        print(filename)
        filename = str(filename)
        length = len(filename)
        pdf.ln(10)
        pdf.cell(40, 10, filename[1:length - 4])
        pdf.ln(10)
        pdf.image(images_directory + '/' + filename, None, None, 200, 100)

    filename = 'Weekly_ECG_Report_{}_{}.pdf'.format(startdate, enddate)
    full_path = pdf_directory + '/' + filename
    pdf.output(full_path, 'F')

    return full_path, filename

    add_to_log('PDF file was created')