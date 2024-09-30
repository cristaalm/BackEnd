# donations/utils/pdf/donations/pdf_formats.py

from reportlab.lib import colors 
from reportlab.platypus import TableStyle

def create_table_style(data):
    estilo_tabla = TableStyle([
        # Encabezado
        ('SPAN', (0,0), (4,0)), 
        ('BACKGROUND', (0,0), (4,0), colors.HexColor('#3fb5d1')),
        ('TEXTCOLOR', (0,0), (4,0), colors.white),

        # Encabezado secundatio
        ('BACKGROUND', (0,1), (4,1), colors.HexColor('#86e6fe')),
        ('TEXTCOLOR', (0,1), (4,1), colors.black),
        
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,0), (-1,1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ])
    # Estilos para alternar colores en las filas de datos
    for i in range(2, len(data) - 1):  # Excluyendo las filas de encabezado y de totales
        if i % 2 == 0:
            # Color para filas pares
            program_color = colors.HexColor('#d5f6ff')
        else:
            # Color para filas impares
            program_color = colors.HexColor('#fcffff')

        # Aplicar color a cada sección de las filas
        estilo_tabla.add('BACKGROUND', (0, i), (4, i), program_color)

    return estilo_tabla