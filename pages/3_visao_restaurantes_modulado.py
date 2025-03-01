#===============================
### importando bibliotecas  ###
#===============================
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from haversine import haversine
import streamlit as st
from datetime import datetime
from PIL import Image
import folium
from streamlit_folium import folium_static
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title = 'Visão Restaurante', layout = 'wide')

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

def distance(df1):                        
    colunas = ['Restaurant_latitude', 'Restaurant_longitude', 
               'Delivery_location_latitude', 'Delivery_location_longitude']
    df1['distance'] = df1.loc[:, colunas].apply( lambda x: 
                                haversine((x['Restaurant_latitude'], 
                                           x['Restaurant_longitude']), 
                                          (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
    avg_distance = np.round(df1['distance'].mean(), 2) 
    return avg_distance

def avg_std_time_delivery(df1, festival, op):
    """
    Esta função calcula o tempo médio e o desvio padrão do tempo de entrega em época de festival ou não
    Parâmetros:
        Input:
            * df: Dataframe com os dados necessários para o cálculo;
            * op: Tipo de operação que precisa ser calculada:
                'avg_time': Calcula o tempo médio;
                'std_time': Calcula o desvio padrão do tempo.
            * fe: Determina se as entregas são em tempo de festivais ou não. 
        Output:
            * df: Dataframe com 2 colunas e 1 linha.
    """
    df_aux = df1.loc[:, ['Time_taken(min)','Festival']].groupby(['Festival']).agg({'Time_taken(min)': ['mean', 'std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    df_aux = np.round(df_aux.loc[df_aux['Festival'] == festival, op],2)
    return df_aux

# Limpando os dados
df1 = cleaning_code(df)


#===============================
### Barra lateral  ###
#===============================
# para executar com o stremlit usar o comando -> streamlit run <arquivo>

st.header('Marketplace - Visão Restaurantes')

# logo
#image_path = 'logo.png'
image = Image.open('logo.png')
st.sidebar.image(image, width=120)

# cabeçalho
st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown('''___''')

# slide de seleção de datas
st.sidebar.markdown('Selecione uma data limite')

date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=datetime(2022, 4, 13),
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 4, 6),
    format='DD-MM-YYYY')

#st.header(date_slider)
st.sidebar.markdown('''___''')

# seleção do tráfego
traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'])
st.sidebar.markdown('''___''')


# rodapé
st.sidebar.markdown('Powered by Comunidade DS')
st.sidebar.markdown('By Matheus Maranho Baumguertner')
#=================================================================================

#===============================
### Colocando os filtros para funcionar ###
#===============================

# slider de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# filtro de trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

#=================================================================================

#===============================
### Layout Streamlit ###
#===============================

# criando as abas
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])

# aba 1
with tab1:
    # linha 1
    with st.container():
        st.title('Overall Metrics')
        # criando as colunas da linha 1
        col1, col2, col3, col4, col5, col6 = st.columns(6)

        # linha 1, coluna 1
        with col1:
            #st.markdown('##### coluna 1')
            delivery_unique = len(df1.loc[:, 'Delivery_person_ID'].unique())
            col1.metric('Entregadores únicos', delivery_unique)
        
        # linha 1, coluna 2
        with col2:
            avg_distance = distance(df1)
            col2.metric('A distancia média das entregas', avg_distance)

        # linha 1, coluna 3
        with col3:
            df_aux = avg_std_time_delivery(df1, 'Yes', 'avg_time') #Chama a função 'avg_std_time_delivery' e nela, passa como parâmetro o avg_time para o cálculo do tempo médio durante o festival.
            col3.metric('Tempo médio de entrega com Festival', df_aux)
            
        # linha 1, coluna 4
        with col4:
            df_aux = avg_std_time_delivery(df1, 'Yes', 'std_time') #Chama a função 'avg_std_time_delivery' e nela, passa como parâmetro o std_time para o cálculo do desvio padrão durante o festival.
            col4.metric('STD tempo de entrega com Festival', df_aux)

        # linha 2, coluna 5
        with col5:
            df_aux = avg_std_time_delivery(df1, 'No', 'avg_time') #Chama a função 'avg_std_time_delivery' e nela, passa como parâmetro o avg_time para o cálculo do tempo médio quando não é festival.
            col5.metric('Tempo médio de entrega sem Festival', df_aux)

        # linha 1, coluna 6
        with col6:
           df_aux = avg_std_time_delivery(df1, 'No', 'std_time') #Chama a função 'avg_std_time_delivery' e nela, passa como parâmetro o std_time para o cálculo do desvio padrão quando não é festival.
           col6.metric('STD tempo de entrega sem Festival', df_aux)
            
    # linha 2
    with st.container():
        st.markdown('''___''')

        col1, col2 = st.columns(2)

        # linha 2, coluna 1
        with col1:
            # gráfico de barras com desvios padrão
            st.title('Tempo médio de entrega por cidade')
            df_aux = df1.loc[:, ['Time_taken(min)', 'City']].groupby(['City']).agg({'Time_taken(min)': ['mean', 'std']})
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()

            fig = go.Figure()
            fig.add_trace(go.Bar(name='Control', x=df_aux['City'], y=df_aux['avg_time'], error_y=dict(type='data', array=df_aux['std_time'])))
            fig.update_layout(barmode='group')
            st.plotly_chart(fig)

        # linha 2, coluna 2
        with col2:
            st.title('Distribuição da distância')

            df_aux = df1.loc[:, ['Time_taken(min)', 'City', 'Type_of_order']].groupby(['City', 'Type_of_order']).agg({'Time_taken(min)': ['mean', 'std']})
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            st.dataframe(df_aux)

        

    # linha 3
    with st.container():
        st.markdown('''___''')
        st.title('Distribuição do tempo')

        col1, col2 = st.columns(2)
        
        # linha 3, coluna 1
        with col1:
            #st.markdown('##### coluna 1')
            # pizza tempos
            
            colunas = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
            df1['distance'] = df1.loc[:, colunas].apply( lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
        
            avg_distance = df1.loc[:, ['City', 'distance']].groupby('City').mean().reset_index()
        
            fig = go.Figure(data=[go.Pie(labels=avg_distance['City'], values=avg_distance['distance'], pull=[0, 0.1, 0])])
            # usa o pull pra 'puxar'um pedaço da pizza, mudando os valores muda o pedaço puxado e a distacia que fica da pizza
            st.plotly_chart(fig)
            

        # linha 3, coluna 2
        with col2:
            #st.markdown('##### coluna 2')
            df_aux = df1.loc[:, ['Time_taken(min)', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)': ['mean', 'std']})
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()

            fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time', color='std_time', color_continuous_scale='RdBu', color_continuous_midpoint= np.average(df_aux['std_time']))
            st.plotly_chart(fig)
        


        