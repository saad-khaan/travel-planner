from fpdf import FPDF
import os

def export_itinerary_pdf(city, start_date, end_date):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Trip to {city}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Dates: {start_date} to {end_date}", ln=True, align='L')
    pdf.output("itinerary.pdf")
    return os.path.abspath("itinerary.pdf")