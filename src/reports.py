"""
Módulo de generación de reportes
Maneja la creación de reportes en múltiples formatos
"""

import os
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

class ReportGenerator:
    """Generador de reportes en múltiples formatos"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        self.ensure_output_directory()
    
    def ensure_output_directory(self):
        """Asegura que el directorio de salida existe"""
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
    
    def generate_client_report_pdf(self, client_data: Dict, report_data: List[Dict] = None) -> str:
        """Genera un reporte PDF para un cliente"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cliente_{client_data['id']}_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER
        )
        story.append(Paragraph("Reporte de Cliente", title_style))
        story.append(Spacer(1, 12))
        
        # Información del cliente
        client_info = [
            ['Campo', 'Valor'],
            ['ID', str(client_data['id'])],
            ['Nombre', client_data['name']],
            ['Email', client_data['email'] or 'N/A'],
            ['Teléfono', client_data['phone'] or 'N/A'],
            ['Empresa', client_data['company'] or 'N/A'],
            ['Dirección', client_data['address'] or 'N/A'],
            ['Ciudad', client_data['city'] or 'N/A'],
            ['País', client_data['country'] or 'N/A'],
            ['Fecha de registro', client_data['created_at']]
        ]
        
        client_table = Table(client_info)
        client_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(client_table)
        story.append(Spacer(1, 20))
        
        # Datos adicionales del reporte si existen
        if report_data:
            story.append(Paragraph("Datos del Reporte", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            report_table_data = [['Campo', 'Valor']]
            for data in report_data:
                report_table_data.append([data['field_name'], data['field_value'] or 'N/A'])
            
            report_table = Table(report_table_data)
            report_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(report_table)
        
        # Pie de página
        story.append(Spacer(1, 20))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER
        )
        story.append(Paragraph(f"Generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}", footer_style))
        
        doc.build(story)
        return filepath
    
    def generate_clients_list_pdf(self, clients: List[Dict]) -> str:
        """Genera un reporte PDF con la lista de todos los clientes"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"lista_clientes_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER
        )
        story.append(Paragraph("Lista de Clientes", title_style))
        story.append(Spacer(1, 12))
        
        # Tabla de clientes
        table_data = [['ID', 'Nombre', 'Email', 'Teléfono', 'Empresa', 'Ciudad']]
        for client in clients:
            table_data.append([
                str(client['id']),
                client['name'],
                client['email'] or 'N/A',
                client['phone'] or 'N/A',
                client['company'] or 'N/A',
                client['city'] or 'N/A'
            ])
        
        clients_table = Table(table_data)
        clients_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10)
        ]))
        
        story.append(clients_table)
        
        # Pie de página
        story.append(Spacer(1, 20))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER
        )
        story.append(Paragraph(f"Total de clientes: {len(clients)}", footer_style))
        story.append(Paragraph(f"Generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}", footer_style))
        
        doc.build(story)
        return filepath
    
    def generate_clients_list_excel(self, clients: List[Dict]) -> str:
        """Genera un archivo Excel con la lista de clientes"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"lista_clientes_{timestamp}.xlsx"
        filepath = os.path.join(self.output_dir, filename)
        
        # Crear DataFrame
        df = pd.DataFrame(clients)
        
        # Reordenar columnas
        columns_order = ['id', 'name', 'email', 'phone', 'company', 'address', 'city', 'country', 'created_at']
        df = df.reindex(columns=columns_order)
        
        # Renombrar columnas
        df.columns = ['ID', 'Nombre', 'Email', 'Teléfono', 'Empresa', 'Dirección', 'Ciudad', 'País', 'Fecha de Registro']
        
        # Guardar en Excel
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Clientes', index=False)
            
            # Ajustar ancho de columnas
            worksheet = writer.sheets['Clientes']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        return filepath
    
    def generate_clients_list_csv(self, clients: List[Dict]) -> str:
        """Genera un archivo CSV con la lista de clientes"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"lista_clientes_{timestamp}.csv"
        filepath = os.path.join(self.output_dir, filename)
        
        # Crear DataFrame
        df = pd.DataFrame(clients)
        
        # Reordenar columnas
        columns_order = ['id', 'name', 'email', 'phone', 'company', 'address', 'city', 'country', 'created_at']
        df = df.reindex(columns=columns_order)
        
        # Renombrar columnas
        df.columns = ['ID', 'Nombre', 'Email', 'Teléfono', 'Empresa', 'Dirección', 'Ciudad', 'País', 'Fecha de Registro']
        
        # Guardar en CSV
        df.to_csv(filepath, index=False, encoding='utf-8')
        
        return filepath
    
    def generate_statistics_report(self, client_stats: Dict, report_stats: Dict) -> str:
        """Genera un reporte de estadísticas"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"estadisticas_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER
        )
        story.append(Paragraph("Reporte de Estadísticas", title_style))
        story.append(Spacer(1, 12))
        
        # Estadísticas de clientes
        story.append(Paragraph("Estadísticas de Clientes", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        client_stats_data = [
            ['Métrica', 'Valor'],
            ['Total de Clientes', str(client_stats['total_clients'])]
        ]
        
        if client_stats['clients_by_country']:
            for country, count in client_stats['clients_by_country'].items():
                client_stats_data.append([f"Clientes en {country}", str(count)])
        
        client_stats_table = Table(client_stats_data)
        client_stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(client_stats_table)
        story.append(Spacer(1, 20))
        
        # Estadísticas de reportes
        story.append(Paragraph("Estadísticas de Reportes", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        report_stats_data = [
            ['Métrica', 'Valor'],
            ['Total de Reportes', str(report_stats['total_reports'])]
        ]
        
        if report_stats['reports_by_status']:
            for status, count in report_stats['reports_by_status'].items():
                report_stats_data.append([f"Reportes {status}", str(count)])
        
        if report_stats['reports_by_type']:
            for report_type, count in report_stats['reports_by_type'].items():
                report_stats_data.append([f"Reportes tipo {report_type}", str(count)])
        
        report_stats_table = Table(report_stats_data)
        report_stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(report_stats_table)
        
        # Pie de página
        story.append(Spacer(1, 20))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER
        )
        story.append(Paragraph(f"Generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}", footer_style))
        
        doc.build(story)
        return filepath
