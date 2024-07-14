# Imports
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from haversine import haversine
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
from datetime import datetime

st.set_page_config(page_title = 'Visão Empresa', layout = 'wide')

# Carregando o dataset
df = pd.read_csv('train.csv')
print("\n")
print('Dados Carregados com Sucesso!')
print("\n")
print('Shape:', df.shape)


#Funções
def cleaning_code(df1):    
    """ Função responsável para limpeza do dataframe:
        1. Remoção dos NaN;
        2. Mudança do tipo da coluna de dados;
        3. Remoção dos espaços das variáveis de texto;
        4. Formatação coluna de datas;
        5. Limpeza coluna de tempo (remoção do texto da variável numérica)

        Input e Output : Dataframe
    """
    # Excluir as linhas com a idade dos entregadores vazia
    linhas_vazias = df1['Delivery_person_Age'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]#.copy()
    # Conversao de texto/categoria/string para numeros inteiros
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )
    
    # Excluir NaN do road_trafic
    linhas_vazias = df1['Road_traffic_density'] != 'NaN'
    df1 = df1.loc[linhas_vazias, :]
    
    # Excluir NaN de Cidade
    linhas_vazias = df1['City'] != 'NaN'
    df1 = df1.loc[linhas_vazias, :]
    
    # Excluir NaN de Festival
    linhas_vazias = df1['Festival'] != 'NaN'
    df1 = df1.loc[linhas_vazias, :]
    
    # Excluir NaN da colunaTime_taken(min)
    linhas_vazias = df1['Time_taken(min)'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]
    
    # Conversao de texto/categoria/strings para numeros decimais
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)
    
    # Conversao de texto para data
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')
    
    # Exclui linhas vazias e converte para tipo inteiro
    linhas_vazias = df['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )# Removendo os espaços dentro de strings/ texto/ object
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip() #Executa o comando e após a execução, guarda dentro da mesma coluna em que foi realizado o processo.
    df1.loc[:, 'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    
    # Limpando a coluna de time taken
    #df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1]) #.apply comando que aplica outra função, no caso, o lambda onde x é cada linha. O split vai ir em cada linha(x) retirar o '(min) ' e deixar o número de cada linha representado pelo [1] (2 elemento).
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.replace('(min) ', ''))
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int) #Transforma todos os resultados retornados acima da coluna, em int
    
    print("\n")
    print('Limpeza dos dados realizadas com Sucesso!')
    print("\n")

    return df1

def order_metric(df1): #Recebe e executa o df, retornando a figura
    # seleção de linhas
    # Criando as colunas
    cols = ['ID', 'Order_Date']
    # Agrupando os dados
    df_graf = df1.loc[:, cols].groupby('Order_Date').count().reset_index()
    # Desenhando o gráfico
    fig = px.bar(df_graf, x='Order_Date', y='ID', title='Quantidade de pedidos por dia')
    return fig

def traffic_order_share(df1):
    # Agrupando os dados
    df_perc = df1.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
    #Criando coluna e calculando as porcentagens
    df_perc['Percent_delivery'] = df_perc['ID']/ df_perc['ID'].sum()
    # Desenhando o gráfico de pizza
    piz = px.pie(df_perc, values = 'Percent_delivery', names = 'Road_traffic_density', 
                 title='% da distribuição pedidos por tipo de tráfego')
    return piz

def traffic_order_city(df1):
    # Agrupando os dados
    df_vol = df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
    # Desenhando o gráfico de bolhas
    bub = px.scatter(df_vol, x = 'City', y = 'Road_traffic_density', size = 'ID', color = 'City', 
                     title='Comparação do volume de pedidos por cidade e tipo de tráfego.')
    return bub


# Limpando os dados
df1 = cleaning_code(df)

#Visão empresa
# Criando as colunas
cols = ['ID', 'Order_Date']

# Agrupando os dados
df_graf = df1.loc[:, cols].groupby('Order_Date').count().reset_index() #Resetando o índex cria uma nova coluna numerando as linhas, sem isso, a coluna Order_Date vira uma coluna de index e fica de fora do gráfico.

# Desenhando gráfico de linhas
# Plotly
px.bar(df_graf, x = 'Order_Date', y = 'ID')


# Layout streamlit
st.header('Marketplace - Visão Cliente')

# Logo
#image_path = 'logo.png'
image = Image.open('logo.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown('''___''')
st.sidebar.markdown('# Selecione uma data limite')

date_slider = st.sidebar.slider ('Até qual valor?', 
                                value = datetime(2022, 4, 13),
                                min_value = datetime(2022, 2, 11),
                                max_value = datetime(2022, 4, 6),
                                format = 'DD-MM-YYYY')

st.header(date_slider)
st.sidebar.markdown('''___''')

# Seleção do tráfego
traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'])

st.sidebar.markdown('''___''')
# Rodapé
st.sidebar.markdown('Powered by Comunidade DS')
st.sidebar.markdown('By MMB')
#=================================================================================

#========================
### Colocando os filtros para funcionar ###
#========================

# slider de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# filtro de trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]
#st.dataframe(df1)


#=================================================================================

#========================
### Layout Streamlit ###
#========================

# criação das abas (tabs)
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

# criando conteúdo da tab1
with tab1:
    with st.container():
      # Order Metrics
      fig = order_metric(df1) #Chama a função, passando df1 como argumento
      st.markdown('# Orders by Day') #Mostra o título      
      st.plotly_chart(fig, use_container_width=True) # Mostra o gráfico
      # Essa parte foi transformada em função nesse arquivo, consultar arquivo original para algum esclarecimento.

    
    # Criando conteiner para a acomodação das colunas e gráfico
    with st.container():
      # Criando 2 colunas para colocar 2 figuras
      col1, col2 = st.columns(2)

      # Conteúdo coluna 1
      with col1:
        piz = traffic_order_share(df1)  
        st.header('Traffic Order Share')
        st.plotly_chart(piz, use_container_width=True) # Mostrando o gráfico
        

      # conteúdo coluna 1
      with col2:
        st.header('Traffic Order City')
        bub = traffic_order_city(df1)
        st.plotly_chart(bub, use_container_width=True) # Mostrando o gráfico    

# criando conteúdo da tab2, seguir os passos acima para a modulação
with tab2:
    with st.container():
      st.markdown('# Order by Week')
      # criando coluna das semanas
      df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
      df_aux = df1.loc[:, ['ID', 'week_of_year']].groupby(['week_of_year']).count().reset_index()
      # renomeando as colunas
      df_aux.columns = ['week_of_year', 'qnt_entregas_semana']
      # criando o gráfico de barras
      fig = px.line(df_aux, x='week_of_year', y='qnt_entregas_semana')
      # mostrando o grafico
      st.plotly_chart(fig, use_container_width=True)

    with st.container():
      st.markdown('# Order Share by Week')
      # será preciso fazer em dois passos
      # 1 - calcular a quantidade de pedidos por seman
      df_aux1 = df1.loc[:, ['ID', 'week_of_year']].groupby(['week_of_year']).count().reset_index()
      # 2 - calcular a quantidade de entregadores únicos por semana
      df_aux2 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby(['week_of_year']).nunique().reset_index()
      # 3 - juntando od DataFrames criados
      df_aux = pd.merge(df_aux1, df_aux2, how='inner')
      df_aux.columns = ['semana', 'qnt_entregas', 'entregadores']
      # calculo da quantidade de pedidos por entregador a cada semana
      # qnt_entregas / entregadores
      df_aux['entrega_por_entregador'] = df_aux['qnt_entregas'] / df_aux['entregadores']
      # fazendo o gráfico de linha
      fig = px.line(df_aux, x='semana', y='entrega_por_entregador')
      # mostrando o grafico
      st.plotly_chart(fig, use_container_width=True)


# Criando conteúdo da tab3
with tab3:
    st.markdown('Country Maps')
    df_aux = df1.loc[:, ['Delivery_location_latitude', 'Delivery_location_longitude', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).median().reset_index()
    # desenhando o mapa
    map = folium.Map(zoom_start=11)

    for index, location_info in df_aux.iterrows():
      folium.Marker([location_info['Delivery_location_latitude'],
                      location_info['Delivery_location_longitude']],
                      popup=location_info[['City', 'Road_traffic_density']]).add_to(map)

    folium_static(map, width=1024, height=600)















