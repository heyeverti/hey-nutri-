import streamlit as st
import pandas as pd
import numpy as np
import io
import math
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# CONFIGURAÇÃO DA PÁGINA & ESTILO VISUAL
# ==========================================
st.set_page_config(
    page_title="Hey Nutri | Avaliação Antropométrica e Gestão Nutricional",
    page_icon="🥦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS para estilo profissional
st.markdown("""
<style>
    /* Estilo do container principal */
    .main {
        background-color: #F8FAFC;
    }
    
    /* Header estilizado */
    .app-header {
        background: linear-gradient(135deg, #059669 0%, #10B981 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .app-header h1 {
        color: white !important;
        font-weight: 700;
        margin: 0;
        font-size: 2.2rem;
    }
    .app-header p {
        color: #ECFDF5 !important;
        margin-top: 6px;
        font-size: 1.05rem;
    }
    
    /* Cards de métricas personalizados */
    .metric-card {
        background-color: white;
        border-radius: 10px;
        padding: 18px;
        border-left: 5px solid #10B981;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .metric-card-title {
        font-size: 0.85rem;
        color: #64748B;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .metric-card-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #0F172A;
        margin: 4px 0;
    }
    .metric-card-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
    }
    .badge-normal { background-color: #DEF7EC; color: #03543F; }
    .badge-alert { background-color: #FDE8E8; color: #9B1C1C; }
    .badge-warning { background-color: #FEF08A; color: #854D0E; }
    .badge-info { background-color: #E1EFFE; color: #1E429F; }

    /* Estilo dos cards do autor */
    .author-card {
        background-color: #F1F5F9;
        padding: 14px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Dados Iniciais Demonstrativos para alimentar os relatórios
DADOS_EXEMPLO = [
    {
        "Data": "05/10/2026", "Prontuário": "2026-001", "Nome": "Ana Clara Ramos", "Idade": 28, "Sexo": "Feminino",
        "Faixa Etária": "Adulto (20-59 anos)", "Peso (kg)": 58.0, "Estatura (m)": 1.65, "IMC (kg/m²)": 21.30,
        "Diagnóstico IMC": "Eutrofia", "Critério IMC": "OMS (1995/2004)", "Circ. Abdominal (cm)": 74.0,
        "Risco Cardiovascular (CA)": "Sem risco aumentado", "Risco DCV Status": "Não",
        "RCQ": 0.76, "Diagnóstico RCQ": "Risco Adequado", "Circ. Panturrilha (cm)": "N/A", "Diagnóstico Sarcopenia": "Não se aplica (<60 anos)",
        "PB (cm)": 26.0, "DCT (mm)": 15.0, "CMB (cm)": 21.29, "AMBc (cm²)": 29.53, "Reserva Muscular": "Eutrofia / Reserva Preservada",
        "Observações": "Acompanhamento de rotina", "Avaliador": "Everti Alves Pimentel"
    },
    {
        "Data": "05/10/2026", "Prontuário": "2026-002", "Nome": "Carlos Eduardo Souza", "Idade": 42, "Sexo": "Masculino",
        "Faixa Etária": "Adulto (20-59 anos)", "Peso (kg)": 88.0, "Estatura (m)": 1.75, "IMC (kg/m²)": 28.73,
        "Diagnóstico IMC": "Sobrepeso", "Critério IMC": "OMS (1995/2004)", "Circ. Abdominal (cm)": 98.0,
        "Risco Cardiovascular (CA)": "Risco Aumentado", "Risco DCV Status": "Sim",
        "RCQ": 0.93, "Diagnóstico RCQ": "Risco Elevado", "Circ. Panturrilha (cm)": "N/A", "Diagnóstico Sarcopenia": "Não se aplica (<60 anos)",
        "PB (cm)": 33.0, "DCT (mm)": 18.0, "CMB (cm)": 27.35, "AMBc (cm²)": 49.52, "Reserva Muscular": "Hipertrofia / Boa Reserva Muscular",
        "Observações": "Orientação para reeducação alimentar", "Avaliador": "Everti Alves Pimentel"
    },
    {
        "Data": "06/10/2026", "Prontuário": "2026-003", "Nome": "Mariana Santos", "Idade": 35, "Sexo": "Feminino",
        "Faixa Etária": "Adulto (20-59 anos)", "Peso (kg)": 92.0, "Estatura (m)": 1.60, "IMC (kg/m²)": 35.94,
        "Diagnóstico IMC": "Obesidade", "Critério IMC": "OMS (1995/2004)", "Circ. Abdominal (cm)": 96.0,
        "Risco Cardiovascular (CA)": "Risco Muito Aumentado", "Risco DCV Status": "Sim",
        "RCQ": 0.89, "Diagnóstico RCQ": "Risco Elevado", "Circ. Panturrilha (cm)": "N/A", "Diagnóstico Sarcopenia": "Não se aplica (<60 anos)",
        "PB (cm)": 36.0, "DCT (mm)": 28.0, "CMB (cm)": 27.20, "AMBc (cm²)": 52.33, "Reserva Muscular": "Hipertrofia / Boa Reserva Muscular",
        "Observações": "Atendimento ambulatorial", "Avaliador": "Everti Alves Pimentel"
    },
    {
        "Data": "06/10/2026", "Prontuário": "2026-004", "Nome": "Lucas Ferreira", "Idade": 24, "Sexo": "Masculino",
        "Faixa Etária": "Adulto (20-59 anos)", "Peso (kg)": 52.0, "Estatura (m)": 1.80, "IMC (kg/m²)": 16.05,
        "Diagnóstico IMC": "Baixo Peso", "Critério IMC": "OMS (1995/2004)", "Circ. Abdominal (cm)": 72.0,
        "Risco Cardiovascular (CA)": "Sem risco aumentado", "Risco DCV Status": "Não",
        "RCQ": 0.78, "Diagnóstico RCQ": "Risco Adequado", "Circ. Panturrilha (cm)": "N/A", "Diagnóstico Sarcopenia": "Não se aplica (<60 anos)",
        "PB (cm)": 23.0, "DCT (mm)": 8.0, "CMB (cm)": 20.49, "AMBc (cm²)": 23.41, "Reserva Muscular": "Eutrofia / Reserva Preservada",
        "Observações": "Ganho de peso ponderal", "Avaliador": "Everti Alves Pimentel"
    },
    {
        "Data": "06/10/2026", "Prontuário": "2026-005", "Nome": "Patricia Lima", "Idade": 50, "Sexo": "Feminino",
        "Faixa Etária": "Adulto (20-59 anos)", "Peso (kg)": 64.0, "Estatura (m)": 1.62, "IMC (kg/m²)": 24.38,
        "Diagnóstico IMC": "Eutrofia", "Critério IMC": "OMS (1995/2004)", "Circ. Abdominal (cm)": 82.0,
        "Risco Cardiovascular (CA)": "Risco Aumentado", "Risco DCV Status": "Sim",
        "RCQ": 0.82, "Diagnóstico RCQ": "Risco Adequado", "Circ. Panturrilha (cm)": "N/A", "Diagnóstico Sarcopenia": "Não se aplica (<60 anos)",
        "PB (cm)": 28.0, "DCT (mm)": 16.0, "CMB (cm)": 22.97, "AMBc (cm²)": 35.53, "Reserva Muscular": "Eutrofia / Reserva Preservada",
        "Observações": "Acompanhamento profilático", "Avaliador": "Everti Alves Pimentel"
    },
    {
        "Data": "07/10/2026", "Prontuário": "2026-006", "Nome": "João Batista Oliveira", "Idade": 68, "Sexo": "Masculino",
        "Faixa Etária": "Idoso (≥ 60 anos)", "Peso (kg)": 72.0, "Estatura (m)": 1.70, "IMC (kg/m²)": 24.91,
        "Diagnóstico IMC": "Eutrofia", "Critério IMC": "Lipschitz (1994) / SISVAN (2011)", "Circ. Abdominal (cm)": 90.0,
        "Risco Cardiovascular (CA)": "Sem risco aumentado", "Risco DCV Status": "Não",
        "RCQ": 0.88, "Diagnóstico RCQ": "Risco Adequado", "Circ. Panturrilha (cm)": 34.0, "Diagnóstico Sarcopenia": "Massa Muscular Preservada (≥ 31 cm)",
        "PB (cm)": 29.0, "DCT (mm)": 12.0, "CMB (cm)": 25.23, "AMBc (cm²)": 40.66, "Reserva Muscular": "Hipertrofia / Boa Reserva Muscular",
        "Observações": "Paciente saudável e ativo", "Avaliador": "Everti Alves Pimentel"
    },
    {
        "Data": "07/10/2026", "Prontuário": "2026-007", "Nome": "Maria de Lourdes", "Idade": 72, "Sexo": "Feminino",
        "Faixa Etária": "Idoso (≥ 60 anos)", "Peso (kg)": 50.0, "Estatura (m)": 1.55, "IMC (kg/m²)": 20.81,
        "Diagnóstico IMC": "Baixo Peso", "Critério IMC": "Lipschitz (1994) / SISVAN (2011)", "Circ. Abdominal (cm)": 78.0,
        "Risco Cardiovascular (CA)": "Sem risco aumentado", "Risco DCV Status": "Não",
        "RCQ": 0.80, "Diagnóstico RCQ": "Risco Adequado", "Circ. Panturrilha (cm)": 29.0, "Diagnóstico Sarcopenia": "Risco de Sarcopenia / Depleção Muscular (< 31 cm)",
        "PB (cm)": 23.5, "DCT (mm)": 10.0, "CMB (cm)": 20.36, "AMBc (cm²)": 26.49, "Reserva Muscular": "Eutrofia / Reserva Preservada",
        "Observações": "Suplementação recomendada", "Avaliador": "Everti Alves Pimentel"
    },
    {
        "Data": "07/10/2026", "Prontuário": "2026-008", "Nome": "Antônio Carlos", "Idade": 78, "Sexo": "Masculino",
        "Faixa Etária": "Idoso (≥ 60 anos)", "Peso (kg)": 85.0, "Estatura (m)": 1.68, "IMC (kg/m²)": 30.12,
        "Diagnóstico IMC": "Sobrepeso", "Critério IMC": "Lipschitz (1994) / SISVAN (2011)", "Circ. Abdominal (cm)": 104.0,
        "Risco Cardiovascular (CA)": "Risco Muito Aumentado", "Risco DCV Status": "Sim",
        "RCQ": 0.98, "Diagnóstico RCQ": "Risco Elevado", "Circ. Panturrilha (cm)": 33.0, "Diagnóstico Sarcopenia": "Massa Muscular Preservada (≥ 31 cm)",
        "PB (cm)": 32.0, "DCT (mm)": 16.0, "CMB (cm)": 26.97, "AMBc (cm²)": 47.91, "Reserva Muscular": "Hipertrofia / Boa Reserva Muscular",
        "Observações": "Acompanhamento hipertensão", "Avaliador": "Everti Alves Pimentel"
    },
    {
        "Data": "08/10/2026", "Prontuário": "2026-009", "Nome": "Francisca Alves", "Idade": 65, "Sexo": "Feminino",
        "Faixa Etária": "Idoso (≥ 60 anos)", "Peso (kg)": 62.0, "Estatura (m)": 1.58, "IMC (kg/m²)": 24.84,
        "Diagnóstico IMC": "Eutrofia", "Critério IMC": "Lipschitz (1994) / SISVAN (2011)", "Circ. Abdominal (cm)": 79.0,
        "Risco Cardiovascular (CA)": "Sem risco aumentado", "Risco DCV Status": "Não",
        "RCQ": 0.81, "Diagnóstico RCQ": "Risco Adequado", "Circ. Panturrilha (cm)": 32.5, "Diagnóstico Sarcopenia": "Massa Muscular Preservada (≥ 31 cm)",
        "PB (cm)": 27.0, "DCT (mm)": 14.0, "CMB (cm)": 22.60, "AMBc (cm²)": 34.15, "Reserva Muscular": "Eutrofia / Reserva Preservada",
        "Observações": "Consulta de seguimento", "Avaliador": "Everti Alves Pimentel"
    },
    {
        "Data": "08/10/2026", "Prontuário": "2026-010", "Nome": "José Benedito", "Idade": 81, "Sexo": "Masculino",
        "Faixa Etária": "Idoso (≥ 60 anos)", "Peso (kg)": 61.0, "Estatura (m)": 1.65, "IMC (kg/m²)": 22.41,
        "Diagnóstico IMC": "Eutrofia", "Critério IMC": "Lipschitz (1994) / SISVAN (2011)", "Circ. Abdominal (cm)": 88.0,
        "Risco Cardiovascular (CA)": "Sem risco aumentado", "Risco DCV Status": "Não",
        "RCQ": 0.86, "Diagnóstico RCQ": "Risco Adequado", "Circ. Panturrilha (cm)": 31.5, "Diagnóstico Sarcopenia": "Massa Muscular Preservada (≥ 31 cm)",
        "PB (cm)": 25.5, "DCT (mm)": 11.0, "CMB (cm)": 22.04, "AMBc (cm²)": 28.69, "Reserva Muscular": "Eutrofia / Reserva Preservada",
        "Observações": "Avaliação geriátrica preventiva", "Avaliador": "Everti Alves Pimentel"
    }
]

# Inicialização do banco de dados na sessão (Session State)
if "historico_pacientes" not in st.session_state or len(st.session_state["historico_pacientes"]) == 0:
    st.session_state["historico_pacientes"] = DADOS_EXEMPLO.copy()

# ==========================================
# BARRA LATERAL (SIDEBAR) - AUTOR E NAVEGAÇÃO
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/isometric-folders/100/hospital.png", width=70)
    st.title("Hey Nutri")
    st.caption("Sistema de Gestão & Avaliação Antropométrica")
    st.markdown("---")
    
    st.subheader("👨‍⚕️ Responsável Técnico")
    st.markdown("""
    **Autor:** Everti Alves Pimentel  
    *Estudante de Nutrição*  
    """)
    
    st.markdown("---")
    st.info("💡 **Diretrizes Clínicas:** Diagnósticos parametrizados conforme OMS (1995/2004), Lipschitz (1994) e SISVAN (2011).")

# ==========================================
# HEADER PRINCIPAL
# ==========================================
st.markdown("""
<div class="app-header">
    <h1>🥦 Hey Nutri — Avaliação & Gestão Nutricional</h1>
    <p>Plataforma Inteligente de Antropometria, Diagnóstico Clínico e Análise de Dados</p>
</div>
""", unsafe_allow_html=True)

# Abas do aplicativo
tab_cadastro, tab_graficos, tab_historico, tab_sobre = st.tabs([
    "📝 Nova Avaliação / Paciente", 
    "📊 Relatório Gráfico & Dashboards",
    "🗂️ Banco de Dados & Exportação Excel", 
    "ℹ️ Sobre & Referências Teóricas"
])

# ==========================================
# ABA 1: FORMULÁRIO DE AVALIAÇÃO E CÁLCULOS
# ==========================================
with tab_cadastro:
    st.subheader("📋 Preenchimento dos Dados Antropométricos do Paciente")
    
    with st.form("form_paciente", clear_on_submit=False):
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            nome = st.text_input("Nome Completo do Paciente*", value="Gabriela Mendes")
            idade = st.number_input("Idade (anos)*", min_value=18, max_value=115, value=32, step=1)
        with col_p2:
            sexo = st.selectbox("Sexo Biológico*", ["Feminino", "Masculino"])
            data_aval = st.date_input("Data da Avaliação", datetime.now())
        with col_p3:
            prontuario = st.text_input("Nº Prontuário / ID", value="2026-011")
            leito_obs = st.text_input("Observação / Atendimento", value="Consulta Inicial")

        st.markdown("#### 📏 Medidas Corporais Diretas")
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            peso = st.number_input("Peso Total (kg)*", min_value=20.0, max_value=250.0, value=61.2, step=0.1)
            estatura = st.number_input("Estatura (m)*", min_value=1.00, max_value=2.20, value=1.66, step=0.01)
        with col_m2:
            ca = st.number_input("Circ. Abdominal (cm)*", min_value=30.0, max_value=200.0, value=76.5, step=0.1)
            quadril = st.number_input("Circ. Quadril (cm)", min_value=0.0, max_value=200.0, value=94.0, step=0.1)
        with col_m3:
            pb = st.number_input("Perímetro Braquial - PB (cm)", min_value=10.0, max_value=60.0, value=27.0, step=0.1)
            dct = st.number_input("Dobra Tricipital - DCT (mm)", min_value=1.0, max_value=60.0, value=13.5, step=0.1)
        with col_m4:
            cp = st.number_input("Circ. Panturrilha - CP (cm)", min_value=0.0, max_value=60.0, value=33.0, step=0.1, help="Obrigatório para Idosos ≥ 60 anos")
            
        submitted = st.form_submit_button("⚡ Processar Avaliação e Salvar Prontuário", use_container_width=True)

    # PROCESSAMENTO E DIAGNÓSTICO
    if submitted or "ultimo_calculo" in st.session_state:
        if submitted:
            # Faixa Etária
            faixa_etaria = "Idoso (≥ 60 anos)" if idade >= 60 else "Adulto (20-59 anos)"
            
            # 1. Cálculo do IMC com Alternância Etária
            imc = peso / (estatura ** 2)
            if idade >= 60:
                criterio_imc = "Lipschitz (1994) / SISVAN (2011)"
                if imc < 22.0:
                    diag_imc = "Baixo Peso"
                    cls_imc_badge = "badge-alert"
                elif 22.0 <= imc <= 27.0:
                    diag_imc = "Eutrofia"
                    cls_imc_badge = "badge-normal"
                else:
                    diag_imc = "Sobrepeso"
                    cls_imc_badge = "badge-warning"
            else:
                criterio_imc = "OMS (1995/2004)"
                if imc < 18.5:
                    diag_imc = "Baixo Peso"
                    cls_imc_badge = "badge-alert"
                elif 18.5 <= imc <= 24.99:
                    diag_imc = "Eutrofia"
                    cls_imc_badge = "badge-normal"
                elif 25.0 <= imc <= 29.99:
                    diag_imc = "Sobrepeso"
                    cls_imc_badge = "badge-warning"
                else:
                    diag_imc = "Obesidade"
                    cls_imc_badge = "badge-alert"

            # 2. Circunferência Abdominal (Risco Cardiovascular - OMS 1998)
            if sexo == "Feminino":
                if ca < 80.0:
                    diag_ca = "Sem risco aumentado"
                    risco_dcv_status = "Não"
                    cls_ca_badge = "badge-normal"
                elif 80.0 <= ca < 88.0:
                    diag_ca = "Risco Aumentado"
                    risco_dcv_status = "Sim"
                    cls_ca_badge = "badge-warning"
                else:
                    diag_ca = "Risco Muito Aumentado"
                    risco_dcv_status = "Sim"
                    cls_ca_badge = "badge-alert"
            else:
                if ca < 94.0:
                    diag_ca = "Sem risco aumentado"
                    risco_dcv_status = "Não"
                    cls_ca_badge = "badge-normal"
                elif 94.0 <= ca < 102.0:
                    diag_ca = "Risco Aumentado"
                    risco_dcv_status = "Sim"
                    cls_ca_badge = "badge-warning"
                else:
                    diag_ca = "Risco Muito Aumentado"
                    risco_dcv_status = "Sim"
                    cls_ca_badge = "badge-alert"

            # 3. Razão Cintura-Quadril (RCQ)
            rcq_val = 0.0
            diag_rcq = "Não calculado"
            if quadril > 0:
                rcq_val = ca / quadril
                if sexo == "Feminino":
                    diag_rcq = "Risco Elevado" if rcq_val >= 0.85 else "Risco Adequado"
                else:
                    diag_rcq = "Risco Elevado" if rcq_val >= 0.90 else "Risco Adequado"

            # 4. Circunferência da Panturrilha (CP) - Sarcopenia
            diag_cp = "Não se aplica (<60 anos)"
            cls_cp_badge = "badge-info"
            if idade >= 60:
                if cp > 0 and cp < 31.0:
                    diag_cp = "Risco de Sarcopenia / Depleção Muscular (< 31 cm)"
                    cls_cp_badge = "badge-alert"
                elif cp >= 31.0:
                    diag_cp = "Massa Muscular Preservada (≥ 31 cm)"
                    cls_cp_badge = "badge-normal"
                else:
                    diag_cp = "Medida não informada"

            # 5. Reserva Proteica e Muscular (CMB e AMBc)
            cmb_val = 0.0
            ambc_val = 0.0
            diag_muscular = "Medidas incompletas"
            if pb > 0 and dct > 0:
                dct_cm = dct / 10.0
                cmb_val = pb - (math.pi * dct_cm)
                amb_raw = (cmb_val ** 2) / (4 * math.pi)
                const_sexo = 10.0 if sexo == "Masculino" else 6.5
                ambc_val = max(0.0, amb_raw - const_sexo)
                
                if ambc_val < 15.0:
                    diag_muscular = "Depleção Muscular Proteica"
                elif 15.0 <= ambc_val <= 40.0:
                    diag_muscular = "Eutrofia / Reserva Preservada"
                else:
                    diag_muscular = "Hipertrofia / Boa Reserva Muscular"

            # Objeto de Paciente
            paciente_data = {
                "Data": data_aval.strftime("%d/%m/%Y"),
                "Prontuário": prontuario,
                "Nome": nome,
                "Idade": idade,
                "Sexo": sexo,
                "Faixa Etária": faixa_etaria,
                "Peso (kg)": peso,
                "Estatura (m)": estatura,
                "IMC (kg/m²)": round(imc, 2),
                "Diagnóstico IMC": diag_imc,
                "Critério IMC": criterio_imc,
                "Circ. Abdominal (cm)": ca,
                "Risco Cardiovascular (CA)": diag_ca,
                "Risco DCV Status": risco_dcv_status,
                "RCQ": round(rcq_val, 2) if quadril > 0 else "N/A",
                "Diagnóstico RCQ": diag_rcq,
                "Circ. Panturrilha (cm)": cp if idade >= 60 else "N/A",
                "Diagnóstico Sarcopenia": diag_cp,
                "PB (cm)": pb if pb > 0 else "N/A",
                "DCT (mm)": dct if dct > 0 else "N/A",
                "CMB (cm)": round(cmb_val, 2) if cmb_val > 0 else "N/A",
                "AMBc (cm²)": round(ambc_val, 2) if ambc_val > 0 else "N/A",
                "Reserva Muscular": diag_muscular,
                "Observações": leito_obs,
                "Avaliador": "Everti Alves Pimentel"
            }
            
            st.session_state["historico_pacientes"].append(paciente_data)
            st.session_state["ultimo_calculo"] = paciente_data
            st.success(f"✅ Avaliação de **{nome}** salva com sucesso no Hey Nutri!")

        p = st.session_state.get("ultimo_calculo", st.session_state["historico_pacientes"][-1])

        # EXIBIÇÃO DOS RESULTADOS EM CARDS DE ALTA DEFINIÇÃO
        st.markdown("---")
        st.subheader(f"📊 Diagnóstico Antropométrico — {p['Nome']}")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-title">Índice de Massa Corporal (IMC)</div>
                <div class="metric-card-value">{p['IMC (kg/m²)']} <span style="font-size:1rem;">kg/m²</span></div>
                <span class="metric-card-badge badge-info">{p['Diagnóstico IMC']}</span>
                <p style="font-size:0.75rem; color:#64748B; margin-top:8px;">{p['Critério IMC']}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-title">Risco Cardiovascular (CA)</div>
                <div class="metric-card-value">{p['Circ. Abdominal (cm)']} <span style="font-size:1rem;">cm</span></div>
                <span class="metric-card-badge badge-warning">{p['Risco Cardiovascular (CA)']}</span>
                <p style="font-size:0.75rem; color:#64748B; margin-top:8px;">OMS (1998)</p>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-title">Triagem de Sarcopenia (CP)</div>
                <div class="metric-card-value">{p['Circ. Panturrilha (cm)']} <span style="font-size:1rem;">cm</span></div>
                <span class="metric-card-badge badge-info">{p['Diagnóstico Sarcopenia']}</span>
                <p style="font-size:0.75rem; color:#64748B; margin-top:8px;">WHO (1995) / SISVAN (2018)</p>
            </div>
            """, unsafe_allow_html=True)

        with c4:
            ambc_str = f"{p['AMBc (cm²)']} cm²" if isinstance(p['AMBc (cm²)'], (int, float)) else "N/A"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-title">Reserva Muscular (AMBc)</div>
                <div class="metric-card-value">{ambc_str}</div>
                <span class="metric-card-badge badge-normal">{p['Reserva Muscular']}</span>
                <p style="font-size:0.75rem; color:#64748B; margin-top:8px;">Heymsfield et al. (1982)</p>
            </div>
            """, unsafe_allow_html=True)

        # LAUDO TEXTUAL PRONTO PARA PRONTUÁRIO
        st.markdown("#### 📄 Laudo Síntese (Pronto para Copiar para o Prontuário)")
        texto_laudo = f"""====================================================================
LAUDO DE AVALIAÇÃO NUTRICIONAL ANTROPOMÉTRICA - HEY NUTRI
====================================================================
Paciente: {p['Nome']} | Idade: {p['Idade']} anos | Sexo: {p['Sexo']} | Prontuário: {p['Prontuário']}
Data da Avaliação: {p['Data']} | Avaliador: {p['Avaliador']} (Estudante de Nutrição)
--------------------------------------------------------------------
1. DIAGNÓSTICO PONDEROPONDERAL:
   - Peso: {p['Peso (kg)']} kg | Estatura: {p['Estatura (m)']} m
   - IMC: {p['IMC (kg/m²)']} kg/m² -> Classificação: {p['Diagnóstico IMC']} [{p['Critério IMC']}]

2. RISCO CARDIOMETABÓLICO & GORDURA VISCERAL:
   - Circunferência Abdominal: {p['Circ. Abdominal (cm)']} cm -> {p['Risco Cardiovascular (CA)']} (Risco DCV: {p['Risco DCV Status']})
   - Razão Cintura-Quadril (RCQ): {p['RCQ']} -> {p['Diagnóstico RCQ']}

3. COMPOSIÇÃO CORPORAL & MASSA MAGRA:
   - Circunferência da Panturrilha (CP): {p['Circ. Panturrilha (cm)']} cm -> {p['Diagnóstico Sarcopenia']}
   - Perímetro Braquial (PB): {p['PB (cm)']} cm | Dobra Tricipital (DCT): {p['DCT (mm)']} mm
   - Circunferência Muscular do Braço (CMB): {p['CMB (cm)']} cm
   - Área Muscular do Braço Corrigida (AMBc): {p['AMBc (cm²)']} cm² -> {p['Reserva Muscular']}

Observações do Atendimento: {p['Observações']}
===================================================================="""
        st.text_area("Laudo do Prontuário", value=texto_laudo, height=220)

# ==========================================
# ABA 2: RELATÓRIO GRÁFICO & DASHBOARDS
# ==========================================
with tab_graficos:
    st.subheader("📈 Relatório Gráfico Epidemiológico & Perfil de Atendimento")
    st.caption("Visão estatística unificada e gráficos interativos da população de pacientes cadastrados no Hey Nutri.")
    
    if len(st.session_state["historico_pacientes"]) == 0:
        st.warning("Nenhum dado cadastrado para gerar os gráficos. Cadastre pacientes na primeira aba.")
    else:
        df_g = pd.DataFrame(st.session_state["historico_pacientes"])
        
        # MÉTIRCAS GERAIS DE TOPO
        m1, m2, m3, m4 = st.columns(4)
        total_pacientes = len(df_g)
        total_adultos = len(df_g[df_g["Faixa Etária"] == "Adulto (20-59 anos)"])
        total_idosos = len(df_g[df_g["Faixa Etária"] == "Idoso (≥ 60 anos)"])
        total_risco_dcv = len(df_g[df_g["Risco DCV Status"] == "Sim"])
        
        m1.metric("Total de Atendimentos", f"{total_pacientes} pacientes")
        m2.metric("Adultos (20-59 anos)", f"{total_adultos} ({total_adultos/total_pacientes*100:.0f}%)")
        m3.metric("Idosos (≥ 60 anos)", f"{total_idosos} ({total_idosos/total_pacientes*100:.0f}%)")
        m4.metric("Com Risco DCV (CA)", f"{total_risco_dcv} ({total_risco_dcv/total_pacientes*100:.0f}%)")
        
        st.markdown("---")
        
        # LINHA 1 DE GRÁFICOS: SEXO E FAIXA ETÁRIA
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            st.markdown("#### 1️⃣ Perfil de Atendimento por Sexo")
            df_sexo = df_g["Sexo"].value_counts().reset_index()
            df_sexo.columns = ["Sexo", "Quantidade"]
            
            fig_sexo = px.pie(
                df_sexo, values="Quantidade", names="Sexo",
                color="Sexo",
                color_discrete_map={"Feminino": "#EC4899", "Masculino": "#3B82F6"},
                hole=0.4,
                title="Distribuição Populacional por Sexo"
            )
            fig_sexo.update_traces(textposition='inside', textinfo='percent+label+value')
            fig_sexo.update_layout(margin=dict(t=40, b=10, l=10, r=10), showlegend=True)
            st.plotly_chart(fig_sexo, use_container_width=True)

        with col_g2:
            st.markdown("#### 2️⃣ Perfil por Idade (Adultos vs Idosos)")
            df_faixa = df_g["Faixa Etária"].value_counts().reset_index()
            df_faixa.columns = ["Faixa Etária", "Quantidade"]
            
            fig_faixa = px.bar(
                df_faixa, x="Faixa Etária", y="Quantidade",
                color="Faixa Etária",
                color_discrete_map={"Adulto (20-59 anos)": "#10B981", "Idoso (≥ 60 anos)": "#F59E0B"},
                text="Quantidade",
                title="Atendimentos por Faixa Etária"
            )
            fig_faixa.update_traces(textposition='outside')
            fig_faixa.update_layout(margin=dict(t=40, b=10, l=10, r=10), showlegend=False, yaxis_title="Nº de Pacientes")
            st.plotly_chart(fig_faixa, use_container_width=True)

        st.markdown("---")
        
        # LINHA 2 DE GRÁFICOS: DIAGNÓSTICO NUTRICIONAL IMC & RISCO DCV POR FAIXA ETÁRIA
        col_g3, col_g4 = st.columns(2)
        
        with col_g3:
            st.markdown("#### 3️⃣ Diagnóstico Nutricional (IMC)")
            df_imc_cat = df_g["Diagnóstico IMC"].value_counts().reset_index()
            df_imc_cat.columns = ["Diagnóstico IMC", "Quantidade"]
            
            # Ordem clínica
            ordem_imc = ["Baixo Peso", "Eutrofia", "Sobrepeso", "Obesidade"]
            df_imc_cat["Diagnóstico IMC"] = pd.Categorical(df_imc_cat["Diagnóstico IMC"], categories=ordem_imc, ordered=True)
            df_imc_cat = df_imc_cat.sort_values("Diagnóstico IMC")
            
            fig_imc = px.bar(
                df_imc_cat, x="Diagnóstico IMC", y="Quantidade",
                color="Diagnóstico IMC",
                color_discrete_map={
                    "Baixo Peso": "#EF4444",
                    "Eutrofia": "#10B981",
                    "Sobrepeso": "#F59E0B",
                    "Obesidade": "#DC2626"
                },
                text="Quantidade",
                title="Classificação de Estado Nutricional"
            )
            fig_imc.update_traces(textposition='outside')
            fig_imc.update_layout(margin=dict(t=40, b=10, l=10, r=10), showlegend=False, yaxis_title="Nº de Pacientes")
            st.plotly_chart(fig_imc, use_container_width=True)

        with col_g4:
            st.markdown("#### 4️⃣ Risco de Doenças Cardiovasculares (DCV) por Faixa Etária")
            
            # Agrupamento Faixa Etária x Risco DCV Status
            df_dcv_group = df_g.groupby(["Faixa Etária", "Risco DCV Status"]).size().reset_index(name="Quantidade")
            
            fig_dcv = px.bar(
                df_dcv_group, x="Faixa Etária", y="Quantidade", color="Risco DCV Status",
                barmode="group",
                color_discrete_map={"Sim": "#EF4444", "Não": "#10B981"},
                text="Quantidade",
                title="Risco Cardiometabólico (Circ. Abdominal - OMS)"
            )
            fig_dcv.update_traces(textposition='outside')
            fig_dcv.update_layout(
                margin=dict(t=40, b=10, l=10, r=10),
                legend_title_text="Risco DCV",
                yaxis_title="Nº de Pacientes"
            )
            st.plotly_chart(fig_dcv, use_container_width=True)

# ==========================================
# ABA 3: BANCO DE DADOS & EXPORTAÇÃO EXCEL
# ==========================================
with tab_historico:
    st.subheader("🗂️ Registro Histórico de Pacientes Avaliados")
    
    if len(st.session_state["historico_pacientes"]) == 0:
        st.info("Nenhum paciente cadastrado até o momento. Preencha o formulário na aba 'Nova Avaliação'.")
    else:
        df_historico = pd.DataFrame(st.session_state["historico_pacientes"])
        
        st.write(f"Total de atendimentos registrados: **{len(df_historico)}**")
        st.dataframe(df_historico, use_container_width=True)
        
        # GERADOR DE PLANILHA EXCEL (.XLSX) PROFISSIONAL
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_historico.to_excel(writer, index=False, sheet_name='Avaliacoes_HeyNutri')
            
            worksheet = writer.sheets['Avaliacoes_HeyNutri']
            for col in worksheet.columns:
                max_len = max(len(str(cell.value or '')) for cell in col)
                col_letter = col[0].column_letter
                worksheet.column_dimensions[col_letter].width = max(max_len + 3, 12)

        buffer.seek(0)
        
        col_btn1, col_btn2 = st.columns([2, 1])
        with col_btn1:
            st.download_button(
                label="📥 Baixar Relatório Completo em Excel (.xlsx)",
                data=buffer,
                file_name=f"Relatorio_HeyNutri_Atendimentos_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        with col_btn2:
            if st.button("🗑️ Limpar Banco de Dados", use_container_width=True):
                st.session_state["historico_pacientes"] = []
                if "ultimo_calculo" in st.session_state:
                    del st.session_state["ultimo_calculo"]
                st.rerun()

# ==========================================
# ABA 4: REFERÊNCIAS TEÓRICAS E CRÉDITOS
# ==========================================
with tab_sobre:
    st.markdown("""
    ### 📚 Fundamentação Teórica & Metodológica
    
    O **Hey Nutri** foi desenvolvido e parametrizado com base em protocolos e consensos científicos consagrados da literatura nutricional e de saúde pública:
    
    1. **Adultos (20 a 59 anos):**
       * **IMC:** Classificação do Índice de Massa Corporal segundo a Organização Mundial da Saúde (OMS, 1995/2004).
       * **Risco Cardiovascular:** Pontos de corte de Circunferência Abdominal (CA) da OMS (1998) por sexo biológico.
       * **Reserva Proteica Somática:** Fórmulas de Área Muscular do Braço Corrigida (AMBc) de Heymsfield et al. (1982).
       
    2. **Idosos (≥ 60 anos):**
       * **IMC:** Pontos de corte específicos de Lipschitz (1994), chancelados pelo Ministério da Saúde (SISVAN, 2011).
       * **Sarcopenia & Triagem Muscular:** Circunferência da Panturrilha (CP < 31 cm) conforme recomendações da WHO (1995) e Manual de Atenção à Saúde da Pessoa Idosa (Brasil, 2018).
       
    ---
    ### 👨‍💻 Créditos de Desenvolvimento
    * **Aplicativo:** Hey Nutri — Sistema de Gestão & Avaliação Antropométrica
    * **Autor & Desenvolvedor:** Everti Alves Pimentel
    * **Titulação:** Estudante de Nutrição
    * **Ano de Atualização:** 2026
    """)
