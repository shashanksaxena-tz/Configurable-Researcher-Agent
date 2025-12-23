"""Report generator for research results."""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from typing import List
from datetime import datetime
import os
import uuid
from backend.models import ResearchResult, EntityType


class ReportGenerator:
    """Generate beautiful reports from research results."""
    
    def __init__(self, reports_dir: str = "./reports"):
        self.reports_dir = reports_dir
        os.makedirs(reports_dir, exist_ok=True)
    
    def generate_pdf_report(
        self,
        entity_name: str,
        entity_type: EntityType,
        results: List[ResearchResult]
    ) -> str:
        """Generate a PDF report."""
        report_id = str(uuid.uuid4())[:8]
        filename = f"{report_id}_{entity_name.replace(' ', '_')}_report.pdf"
        filepath = os.path.join(self.reports_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2563eb'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title
        title = Paragraph(f"Research Report: {entity_name}", title_style)
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # Metadata
        metadata_text = f"""
        <b>Entity Type:</b> {entity_type.value.title()}<br/>
        <b>Report Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>
        <b>Report ID:</b> {report_id}<br/>
        <b>Number of Analyses:</b> {len(results)}
        """
        story.append(Paragraph(metadata_text, styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Results
        for result in results:
            # Section heading
            heading = Paragraph(f"{result.title}", heading_style)
            story.append(heading)
            
            # Summary
            summary = Paragraph(f"<b>Summary:</b> {result.summary}", styles['Normal'])
            story.append(summary)
            story.append(Spacer(1, 0.1*inch))
            
            # Confidence
            confidence_text = f"<b>Confidence Score:</b> {result.confidence * 100:.0f}%"
            story.append(Paragraph(confidence_text, styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
            
            # Data table
            if result.data:
                data_items = []
                for key, value in result.data.items():
                    if isinstance(value, (list, dict)):
                        value = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                    data_items.append([key.replace('_', ' ').title(), str(value)])
                
                if data_items:
                    table = Table(data_items, colWidths=[2*inch, 4.5*inch])
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e0e7ff')),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                        ('TOPPADDING', (0, 0), (-1, -1), 8),
                        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ]))
                    story.append(table)
            
            story.append(Spacer(1, 0.3*inch))
        
        # Build PDF
        doc.build(story)
        return report_id
    
    def generate_html_report(
        self,
        entity_name: str,
        entity_type: EntityType,
        results: List[ResearchResult]
    ) -> str:
        """Generate an HTML report."""
        report_id = str(uuid.uuid4())[:8]
        filename = f"{report_id}_{entity_name.replace(' ', '_')}_report.html"
        filepath = os.path.join(self.reports_dir, filename)
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Research Report - {entity_name}</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }}
                .report-container {{
                    background: white;
                    border-radius: 10px;
                    padding: 40px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                }}
                h1 {{
                    color: #1e40af;
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .metadata {{
                    background: #f0f4f8;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 30px;
                }}
                .result-section {{
                    margin-bottom: 40px;
                    border-left: 4px solid #3b82f6;
                    padding-left: 20px;
                }}
                h2 {{
                    color: #2563eb;
                    margin-bottom: 15px;
                }}
                .summary {{
                    background: #eff6ff;
                    padding: 15px;
                    border-radius: 6px;
                    margin: 10px 0;
                }}
                .confidence {{
                    display: inline-block;
                    background: #10b981;
                    color: white;
                    padding: 5px 15px;
                    border-radius: 20px;
                    font-weight: bold;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background: #e0e7ff;
                    font-weight: bold;
                }}
                tr:hover {{
                    background: #f8fafc;
                }}
            </style>
        </head>
        <body>
            <div class="report-container">
                <h1>Research Report: {entity_name}</h1>
                <div class="metadata">
                    <p><strong>Entity Type:</strong> {entity_type.value.title()}</p>
                    <p><strong>Report Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p><strong>Report ID:</strong> {report_id}</p>
                    <p><strong>Number of Analyses:</strong> {len(results)}</p>
                </div>
        """
        
        for result in results:
            html_content += f"""
                <div class="result-section">
                    <h2>{result.title}</h2>
                    <div class="summary">
                        <strong>Summary:</strong> {result.summary}
                    </div>
                    <p><span class="confidence">Confidence: {result.confidence * 100:.0f}%</span></p>
                    <table>
                        <thead>
                            <tr>
                                <th>Property</th>
                                <th>Value</th>
                            </tr>
                        </thead>
                        <tbody>
            """
            
            for key, value in result.data.items():
                if isinstance(value, (list, dict)):
                    value = str(value)
                html_content += f"""
                            <tr>
                                <td><strong>{key.replace('_', ' ').title()}</strong></td>
                                <td>{value}</td>
                            </tr>
                """
            
            html_content += """
                        </tbody>
                    </table>
                </div>
            """
        
        html_content += """
            </div>
        </body>
        </html>
        """
        
        with open(filepath, 'w') as f:
            f.write(html_content)
        
        return report_id
