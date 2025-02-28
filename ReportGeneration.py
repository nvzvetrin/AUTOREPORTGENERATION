import csv
import os
#from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def analyze_data(file_path):
    data = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)

        if not data:
            raise ValueError("CSV file is empty.")

        summary = {}
        for key in data[0]: 
            try:
                values = [float(row[key]) for row in data if row[key].replace('.', '', 1).isdigit()]
                summary[key] = {
                    "Count": len(values),
                    "Sum": round(sum(values), 2),
                    "Average": round(sum(values) / len(values), 2) if values else 0,
                    "Max": max(values) if values else None,
                    "Min": min(values) if values else None
                }
            except ValueError:
                pass  # Ignore non-numeric data

        return summary

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error processing file: {e}")
        return None

# Function to create a PDF report with a table
def generate_pdf_report(summary, output_path):
    if not summary:
        print("No valid data to generate report.")
        return

    pdf = SimpleDocTemplate(output_path, pagesize=letter)
    elements = []

    # Header
    title = [["CODSOFT PVT LTD"]]
    title_table = Table(title, colWidths=[500])
    title_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.blue),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12)
    ]))
    elements.append(title_table)

    # Table Data
    table_data = [["Column", "Count", "Sum", "Average", "Max", "Min"]]  # Header row

    for column, stats in summary.items():
        row = [column, stats["Count"], stats["Sum"], stats["Average"], stats["Max"], stats["Min"]]
        table_data.append(row)

    # Table Styling
    table = Table(table_data, colWidths=[120, 80, 80, 80, 80, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)

    # Generate PDF
    pdf.build(elements)
    print(f"Report successfully saved as '{output_path}'")

# Main function
def main():
    input_file = "demo1.csv"  # Replace with your actual data file
    output_file = "result.pdf"

    if not os.path.exists(input_file):
        print(f"Error: The file '{input_file}' does not exist.")
        return

    summary = analyze_data(input_file)
    generate_pdf_report(summary, output_file)

if __name__ == "__main__":
    main()
