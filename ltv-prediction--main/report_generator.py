from reportlab.platypus import (

    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer

)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

import pandas as pd

# -----------------------------------
# GENERATE PDF REPORT
# -----------------------------------
def generate_pdf_report(df):

    pdf_file = "customer_ltv_report.pdf"

    doc = SimpleDocTemplate(

        pdf_file,

        pagesize=letter

    )

    elements = []

    styles = getSampleStyleSheet()

    # -----------------------------------
    # TITLE
    # -----------------------------------
    title = Paragraph(

        "Customer Lifetime Value Analytics Report",

        styles['Title']

    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    # -----------------------------------
    # SUMMARY
    # -----------------------------------
    total_customers = len(df)

    total_revenue = df['predicted_ltv'].sum()

    summary = Paragraph(

        f"""
        <b>Total Customers:</b> {total_customers}
        <br/>
        <b>Total Predicted Revenue:</b> ₹{total_revenue:,.2f}
        """,

        styles['BodyText']

    )

    elements.append(summary)

    elements.append(Spacer(1, 20))

    # -----------------------------------
    # TABLE DATA
    # -----------------------------------
    table_data = [list(df.columns)]

    for row in df.values.tolist():

        table_data.append(row)

    # -----------------------------------
    # CREATE TABLE
    # -----------------------------------
    table = Table(table_data)

    table.setStyle(

        TableStyle([

            ('BACKGROUND', (0,0), (-1,0), colors.grey),

            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),

            ('ALIGN', (0,0), (-1,-1), 'CENTER'),

            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),

            ('BOTTOMPADDING', (0,0), (-1,0), 12),

            ('BACKGROUND', (0,1), (-1,-1), colors.beige),

            ('GRID', (0,0), (-1,-1), 1, colors.black)

        ])

    )

    elements.append(table)

    # -----------------------------------
    # BUILD PDF
    # -----------------------------------
    doc.build(elements)

    return pdf_file