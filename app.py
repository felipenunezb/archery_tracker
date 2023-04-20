from collections import defaultdict
import streamlit as st
import pandas as pd
import json

from data import read_data
from plots import get_overall_plot, get_round_scores, get_x_m_counts

st.set_page_config(page_icon="🎯", page_title="Archery Progress", layout="wide")

OPTION_EXAMPLE = "Ver ejemplo"
OPTION_UPLOAD = "Subir planilla"
SIDEBAR_OPTIONS = [OPTION_EXAMPLE, OPTION_UPLOAD]

ANALYSIS_SINGLE = 'Analizar curso'
ANALYSIS_COMPARISON = 'Comparar cursos'
ANALYSIS_EVOLUTION = 'Comparar progresion'
ANALYSIS_OVERALL = 'Reporte Cambios Significativos'
ANALYSIS_OPTIONS = [ANALYSIS_SINGLE, ANALYSIS_EVOLUTION, ANALYSIS_OVERALL]

def main():
    
    st.sidebar.title("Seleccione archivo:")
    app_mode = st.sidebar.selectbox("Fuente", SIDEBAR_OPTIONS)
    
    #set child multi-element container, for easy cleaning
    c = st.empty()
    sc = c.container()
    
    if app_mode == OPTION_UPLOAD:
        
        f = st.sidebar.file_uploader("Seleccione planilla", type=['xls'], accept_multiple_files=True)
        
        if f:
            
            sc.write("WIP")

    elif app_mode == OPTION_EXAMPLE:
        
        eg_filepath = './sample_data/sample_data.xlsx'
        data = read_data(eg_filepath)
            
        main_plot = get_overall_plot(data["scores_agg"])
        sc.write("##### Progreso puntaje")
        sc.bokeh_chart(main_plot, use_container_width=True)
        
        col1, col2 = sc.columns(2)
        with col1:
            round_plot = get_round_scores(data["round_scores_df"])
            st.write("##### Puntaje promedio por ronda")
            st.bokeh_chart(round_plot, use_container_width=True)
            
        with col2:
            count_plot = get_x_m_counts(data["x_m_df"])
            st.write("##### Progreso X/M")
            st.bokeh_chart(count_plot, use_container_width=True)
        
main()