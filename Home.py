import streamlit as st
from PIL import Image

st.set_page_config(
    page_title = "Home")

#image_path = '/DSA/Comunidade_DS/Analisando_Dados_Python/Ciclo05/repos/' #Usando o comando pwd no terminal aparece o path
image = Image.open('logo.png')
st.sidebar.image(image, width = 120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown('''___''')

st.write("# Cury Company Growth Dashboard")

st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos entregadores e restaurantes.
    ### Como utilizar esse dashboard?
    
    - Visão Empresa:
        * Visão gerencial: métricas gerais de comportamento;
        * Visão tática: indicadores semanais de crescimento;
        * Visão geográfica: insights de geolocalização.
    - Visão Entregador:
        * Acompanhamento dos indicadores semanais de crescimento.
    - Visão Restaurante:
        * Indicadores semanis de crescimento dos restaurantes

    #### Para maiores esclarecimentos:
        - Time de Cientistas de Dados.
        - @leandro
    """
)