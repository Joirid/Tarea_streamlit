import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl as opxl

st.title("Testeando Streamlit")
# Subir el archivo de vendedores
uploaded_file = st.file_uploader("Sube el archivo vendedores.xlsx", type="xlsx")

if uploaded_file is not None and uploaded_file.name == 'vendedores.xlsx':
    # Cargar información
    df = pd.read_excel(uploaded_file)
    
    # Filtrar tabla por región
    st.header("Datos filtrados por región")
    unique_regions = df['REGION'].unique()
    selected_region = st.selectbox("Selecciona la región", unique_regions)
    filtered_df = df[df['REGION'] == selected_region]
    st.write(filtered_df)
    
    # Gráficas por Unidades Vendidas, Ventas Totales y Porcentajes de Ventas
    st.header("Gráficas")
    # Lista de columnas que se podrían seleccionar
    columns_graphics = ['UNIDADES VENDIDAS', 'VENTAS TOTALES', 'PORCENTAJE DE VENTAS']
    # Selección de columna a visualizar
    visualization_column = columns_graphics [0]
    select_column = st.segmented_control("Selecciona la columna para la gráfica", columns_graphics)
    visualization_column = select_column if select_column else columns_graphics[0] 
    # Dataframe para visualización
    df_graphic = df[visualization_column]
    
    if select_column:
        st.subheader(select_column)
        
        # Personalización de histograma
        col1, col2 = st.columns([3, 1])
        with col1:
            bins = st.slider('Número de bins', 5, 100, 50) # Selección bins
        with col2:
            color = st.color_picker('Color del histograma', '#5046CE') # Selección color
        
        # Configuración para visualizar el histograma
        fig, ax = plt.subplots(figsize=(10, 6), dpi=600)
        ax.hist(df_graphic, bins=bins, alpha=0.7, color=color, edgecolor='black')
        ax.set_title(f'Histograma de {select_column.lower()} ({bins} bins)')
        ax.set_xlabel('Valores')
        ax.set_ylabel('Frecuencia')
        ax.grid(alpha=0.3)

        st.pyplot(fig) # Mostrar el histograma
    
    # Información de vendedor específico
    st.header("Información por vendedor")
    # Selección de ID de vendedor para visualización de información
    unique_id = df['ID'].unique()
    selected_id = st.selectbox("Selecciona el ID del vendedor", unique_id)
    vendor_df = df[df['ID'] == selected_id]
    
    # Despliegue de información con formato personalizado
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    with col1:
        st.write("**ID**")
        st.write(f"{selected_id}")
        st.metric("**Salario**", f"${vendor_df['SALARIO'].values[0]:,}")
    with col2:
        st.write("**Nombre**")
        st.write(f"{vendor_df['NOMBRE'].values[0]}")
        st.metric("**Unidades Vendidas**", f"{vendor_df[columns_graphics[0]].values[0]:,}")
    with col3:
        st.write("**Apellidos**")
        st.write(f"{vendor_df['APELLIDO'].values[0]}")
        st.metric("**Ventas totales**", f"{vendor_df[columns_graphics[1]].values[0]:,}")
    with col4:
        st.write("**Región**")
        st.write(f"{vendor_df['REGION'].values[0]}")
        st.metric("**Porcentaje de ventas**", f"{vendor_df[columns_graphics[2]].values[0]:.2%}")
elif uploaded_file is not None:
    st.warning("Por favor, sube el archivo 'vendedores.xlsx' para continuar.")
    