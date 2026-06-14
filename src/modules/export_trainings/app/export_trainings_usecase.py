from io import BytesIO
import base64
from datetime import datetime, timezone, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from typing import List

from src.shared.domain.repositories.training_repository_interface import ITrainingRepository
from src.shared.domain.repositories.group_repository_interface import IGroupRepository
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound

class ExportTrainingsUseCase:
    def __init__(self, training_repo: ITrainingRepository, group_repo: IGroupRepository, user_repo: IUserRepository):
        self.training_repo = training_repo
        self.group_repo = group_repo
        self.user_repo = user_repo

    def __call__(self, athlete_id: str, training_id_list: List[str], requester_user_id: str, requester_name: str) -> str:
        # Validate if requester is linked to athlete
        groups = self.group_repo.get_all_groups_by_supporter_id(requester_user_id)
        
        is_linked = False
        
        for group in groups:
            if any(str(aid) == athlete_id for aid in group.athlete_list_id):
                is_linked = True
                break
        
        if not is_linked:
            raise ForbiddenAction("Athlete is not linked to this supporter")

        # Fetch the athlete
        athlete = self.user_repo.get_user(athlete_id)
        athlete_name = athlete.name if athlete else athlete_id

        # Fetch all trainings for the athlete
        all_trainings = self.training_repo.get_all_trainings_by_user(user_id=athlete_id)
        
        # Filter by training_id_list
        selected_trainings = [t for t in all_trainings if t.training_id in training_id_list]
        
        if not selected_trainings:
            raise NoItemsFound("Trainings")
            
        # Calculate Averages
        total_sessions = len(selected_trainings)
        
        # Averages calculation
        total_pre_hydration = sum(t.pre_training_hydration for t in selected_trainings if t.pre_training_hydration is not None)
        total_during_hydration = sum(t.during_training_hydration for t in selected_trainings if t.during_training_hydration is not None)
        total_weight_diff = sum(t.weight_difference for t in selected_trainings if t.weight_difference is not None)
        total_weight_var_perc = sum(t.weight_variation_percentage for t in selected_trainings if t.weight_variation_percentage is not None)
        total_sudorese = sum(t.sudorese for t in selected_trainings if t.sudorese is not None)
        total_urine_elimination = sum(t.during_training_urine_elimination for t in selected_trainings if t.during_training_urine_elimination is not None)
        
        valid_temp_trainings = [t for t in selected_trainings if t.environment_temperature is not None]
        total_temperature = sum(t.environment_temperature for t in valid_temp_trainings)
        avg_temperature = total_temperature / len(valid_temp_trainings) if valid_temp_trainings else 0
        
        valid_humidity_trainings = [t for t in selected_trainings if t.environment_humidity is not None]
        total_humidity = sum(t.environment_humidity for t in valid_humidity_trainings)
        avg_humidity = total_humidity / len(valid_humidity_trainings) if valid_humidity_trainings else 0
        
        total_duration = sum(t.duration for t in selected_trainings if t.duration is not None)
        total_intensity = sum(t.training_intensity for t in selected_trainings if t.training_intensity is not None)
        
        avg_duration = total_duration / total_sessions if total_sessions > 0 else 0
        avg_duration_min = avg_duration / 60
        avg_intensity = total_intensity / total_sessions if total_sessions > 0 else 0
        
        avg_pre_hydration = total_pre_hydration / total_sessions if total_sessions > 0 else 0
        avg_during_hydration = total_during_hydration / total_sessions if total_sessions > 0 else 0
        avg_weight_diff = total_weight_diff / total_sessions if total_sessions > 0 else 0
        avg_weight_var_perc = total_weight_var_perc / total_sessions if total_sessions > 0 else 0
        avg_sudorese = total_sudorese / total_sessions if total_sessions > 0 else 0
        avg_urine_elimination = total_urine_elimination / total_sessions if total_sessions > 0 else 0

        # Build PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
        styles = getSampleStyleSheet()
        elements = []
        
        # Styles
        title_style = ParagraphStyle('TitleCustom', parent=styles['Heading1'], alignment=0, fontSize=22, textColor=colors.HexColor('#1a1a1a'), spaceAfter=5, fontName='Helvetica-Bold')
        subtitle_style = ParagraphStyle('SubtitleCustom', parent=styles['Normal'], alignment=0, fontSize=10, textColor=colors.HexColor('#808080'), spaceAfter=15, fontName='Helvetica-Bold')
        h2_style = ParagraphStyle('H2Custom', parent=styles['Heading2'], fontSize=16, textColor=colors.HexColor('#1a1a1a'), spaceBefore=25, spaceAfter=15, fontName='Helvetica-Bold')
        normal_style = ParagraphStyle('NormalCustom', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#4d4d4d'), leading=16)
        label_style = ParagraphStyle('LabelCustom', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#666666'), leading=14)
        value_style = ParagraphStyle('ValueCustom', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#1a1a1a'), alignment=2, leading=14) # Right aligned
        meta_value_style = ParagraphStyle('MetaValueCustom', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#1a1a1a'), alignment=0, leading=14) # Left aligned
        section_title_style = ParagraphStyle('SectionTitle', parent=styles['Normal'], fontSize=12, textColor=colors.HexColor('#1a1a1a'), fontName='Helvetica-Bold', spaceAfter=10)

        # Header
        elements.append(Paragraph("SISTEMA SÃO CAMILO", subtitle_style))
        elements.append(Paragraph("Relatório de Treinos", title_style))
        
        # Subtle separator
        elements.append(Table([['']], colWidths=[535], style=[('LINEBELOW', (0,0), (-1,-1), 1, colors.HexColor('#e5e7eb'))]))
        elements.append(Spacer(1, 15))
        
        # Meta info
        meta_data = [
            [Paragraph("<b>Atleta:</b>", label_style), Paragraph(athlete_name, meta_value_style), Paragraph("<b>Data de Exportação:</b>", label_style), Paragraph(datetime.now(timezone(timedelta(hours=-3))).strftime('%d/%m/%Y %H:%M'), meta_value_style)],
            [Paragraph("<b>Treinador:</b>", label_style), Paragraph(requester_name, meta_value_style), "", ""]
        ]
        
        meta_table = Table(meta_data, colWidths=[65, 145, 160, 165])
        meta_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (1,0), (1,-1), 'LEFT'),
            ('ALIGN', (3,0), (3,-1), 'LEFT'),
            ('LEFTPADDING', (2, 0), (2, -1), 40), # Push the right block further right
        ]))
        elements.append(meta_table)
        elements.append(Spacer(1, 15))
        
        elements.append(Table([['']], colWidths=[535], style=[('LINEBELOW', (0,0), (-1,-1), 1, colors.HexColor('#e5e7eb'))]))
        elements.append(Spacer(1, 10))

        # Executive Summary (Minimalist)
        elements.append(Paragraph("Dados Médios", h2_style))
        
        summary_data = [
            [Paragraph("Resultados Médios", section_title_style), "", Paragraph("Ingestão Média de Fluidos", section_title_style), ""],
            [Paragraph("Sessões Analisadas:", label_style), Paragraph(f"{total_sessions}", value_style), Paragraph("Pré exercício:", label_style), Paragraph(f"{avg_pre_hydration:.0f} ml".replace('.', ','), value_style)],
            [Paragraph("Duração Média:", label_style), Paragraph(f"{avg_duration_min:.0f} min".replace('.', ','), value_style), Paragraph("Durante exercício:", label_style), Paragraph(f"{avg_during_hydration:.0f} ml".replace('.', ','), value_style)],
            [Paragraph("Intensidade Média:", label_style), Paragraph(f"{avg_intensity:.1f}".replace('.', ','), value_style), Paragraph("Volume Urinário (Durante):", label_style), Paragraph(f"{avg_urine_elimination:.0f} ml".replace('.', ','), value_style)],
            [Paragraph("Variação de Massa (kg):", label_style), Paragraph(f"{avg_weight_diff:.2f} kg".replace('.', ','), value_style), Paragraph("Taxa de Sudorese Estimada:", label_style), Paragraph(f"{avg_sudorese:.2f} L/h".replace('.', ','), value_style)],
            [Paragraph("Variação de Massa (%):", label_style), Paragraph(f"{avg_weight_var_perc:.2f}%".replace('.', ','), value_style), "", ""],
            [Paragraph("Temperatura Média:", label_style), Paragraph(f"{avg_temperature:.1f} °C".replace('.', ','), value_style), "", ""],
            [Paragraph("Umidade Média:", label_style), Paragraph(f"{avg_humidity:.1f}%".replace('.', ','), value_style), "", ""]
        ]
        
        summary_table = Table(summary_data, colWidths=[160, 50, 220, 105])
        summary_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),   # Label 1
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),  # Value 1
            ('ALIGN', (2, 0), (2, -1), 'LEFT'),   # Label 2
            ('ALIGN', (3, 0), (3, -1), 'RIGHT'),  # Value 2
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (2, 0), (2, -1), 40), # Push the right block further right
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 25))
        
        # Session Log Table
        elements.append(Paragraph("Registro de Sessões", h2_style))
        
        table_headers = ["Data", "Modalidade", "Duração\n(min)", "Intens.\n(0-10)", "Temp.\n(°C)", "Umid.\n(%)", "Água\nIngerida\nPré (ml)", "Água\nIngerida\nDur. (ml)", "Var.\nMassa\n(kg)", "Var.\nMassa\n(%)", "Sudorese\n(L/h)", "Urina\nEliminada\n(ml)", "Cor da\nUrina"]
        table_data = [table_headers]
        
        for t in selected_trainings:
            date_str = datetime.fromtimestamp(t.start_date / 1000.0).strftime('%d/%m/%y')
            duration_min = f"{t.duration / 60:.0f}"
            weight_diff = f"{t.weight_difference:.2f}".replace('.', ',') if t.weight_difference is not None else "-"
            loss_perc = f"{t.weight_variation_percentage:.1f}%".replace('.', ',')
            sud_lh = f"{t.sudorese:.2f}".replace('.', ',')
            urine = t.urine_color.value.replace('_', '\n') if t.urine_color else "-"
            modality = t.modality.value[:8] if t.modality else "-" # Abbreviate safely
            pre_h = f"{t.pre_training_hydration:.0f}".replace('.', ',')
            dur_h = f"{t.during_training_hydration:.0f}".replace('.', ',') if t.during_training_hydration is not None else "-"
            urine_elim = f"{t.during_training_urine_elimination:.0f}".replace('.', ',') if t.during_training_urine_elimination is not None else "-"
            temp = f"{t.environment_temperature:.1f}".replace('.', ',') if t.environment_temperature is not None else "-"
            umid = f"{t.environment_humidity:.1f}".replace('.', ',') if t.environment_humidity is not None else "-"
            
            table_data.append([date_str, modality, duration_min, str(t.training_intensity), temp, umid, pre_h, dur_h, weight_diff, loss_perc, sud_lh, urine_elim, urine])
            
        t_style = TableStyle([
            # Table Header & Body common grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
            
            # Table Header
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1a1a1a')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 7.0), # Slightly smaller to fit 12 columns
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('LINEBELOW', (0, 0), (-1, 0), 1.5, colors.HexColor('#1a1a1a')), # Strong line under header
            
            # Table Body
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#4d4d4d')),
            ('FONTSIZE', (0, 1), (-1, -1), 7.0),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ])
        
        table = Table(table_data, colWidths=[40, 40, 35, 35, 35, 35, 40, 40, 40, 40, 40, 40, 70])
        table.setStyle(t_style)
        
        elements.append(table)
        
        # Build PDF
        doc.build(elements)
        
        # Get base64 string
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        base64_encoded = base64.b64encode(pdf_bytes).decode('utf-8')
        
        return base64_encoded
