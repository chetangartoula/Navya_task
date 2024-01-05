import os

from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer
from reportlab.lib import colors


def generate_transaction_pdf(filename, table_list: list,header=None):
    logo_path = os.path.join(settings.BASE_DIR, "static/") + "Djago HUB.png"
    logo = Image(logo_path, width=100, height=50)
    path = os.path.join(settings.BASE_DIR, "transaction_files")
    file_path = f"{path}/{filename}"
    doc = SimpleDocTemplate(file_path, pagesize=letter)

    table_data = []
    if header:
        table_data = [header]
    for data in table_list:
        table_data.append([str(val) for val in data.values()])
    table = Table(table_data)

    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]
    )

    table.setStyle(style)
    content = [Spacer(1, 5), logo, Spacer(1, 20), table]
    doc.build(content)
