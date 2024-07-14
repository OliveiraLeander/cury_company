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

st.set_page_config(page_title = 'Visão Entregadores', layout = 'wide')

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

def top_delivers(df1, top_asc): #Função que nas colunas solicitadas, realizará os cálculos, agrupará por tipo de cidade, concatena as tabelas e retorna a tabela montada.
    df2 = df1.loc[:, ['Time_taken(min)', 'City', 'Delivery_person_ID']].groupby(['City', 'Delivery_person_ID']).min().sort_values(['City', 'Time_taken(min)'], ascending=top_asc).reset_index() #Nessa linha que retorna quando será os entregadores mais rápidos e mais lentos.
    df_aux1 = df2.loc[ df2['City'] == 'Metropolitian', :].head(10)
    df_aux2 = df2.loc[ df2['City'] == 'Urban', :].head(10)
    df_aux3 = df2.loc[ df2['City'] == 'Semi-Urban', :].head(10)
    df3 = pd.concat([df_aux1, df_aux2,df_aux3]).reset_index(drop=True)
    return df3

# Limpando os dados
df1 = cleaning_code(df)


#===============================
### Barra lateral  ###
#===============================
# para executar com o stremlit usar o comando -> streamlit run <arquivo>

st.header('Marketplace - Visão Entregadores')

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
# criando as abas (tabs)
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])

# primeira aba
with tab1:
    # linha 1
    with st.container():
        st.title('Overall Metrics')
        # criando colunas na linha 1
        col1, col2, col3, col4 = st.columns(4, gap='large')

        # linha 1, coluna 1
        # A maior idade dos entregadores
        with col1:
            #st.subheader('Maior idade')
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric('Maior idade', maior_idade)

        #linha 1 , coluna 2
        # A menor idade dos entregadores
        with col2:
            #st.subheader('Menor idade')
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Menor idade', menor_idade)

        # linha 1, coluna 3
        # A melhor condição dos veículos
        with col3:
            #st.subheader('Melhor condição de veículos')
            melhor_consicao = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric('Melhor condição', melhor_consicao)

        # linha 1, coluna 4
        # A pior condição dos veículos
        with col4:
            #st.subheader('Pior condição de veículos')
            pior_condicao = df1.loc[:, 'Vehicle_condition'].min()
            col4.metric('Pior condição', pior_condicao)

    # linha 2
    with st.container():
        st.markdown('''___''')
        st.title('Avaliações')

        # criando colunas na linha 2
        col1, col2 = st.columns(2)

        # linha 2, coluna 1
        with col1:
            st.markdown('##### Avaliação média por entregador')
            df_aux = df1.loc[:, ['Delivery_person_Ratings', 'Delivery_person_ID']].groupby(['Delivery_person_ID']).mean().reset_index()
            # exibindo o dataframe
            st.dataframe(df_aux)

        # linha 2, coluna 2
        with col2:
            st.markdown('##### Avaliação média por trânsito')
            df_alt = df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']].groupby(['Road_traffic_density']).agg({'Delivery_person_Ratings': ['mean', 'std']})
            # renomeando as colunas
            df_alt.columns = ['delivery_mean', 'delivery_std']
            # reset do index
            df_alt = df_alt.reset_index()
            # exibindo o dataframe
            st.dataframe(df_alt)


            st.markdown('##### Avaliação média por clima')
            df_aux = df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']].groupby(['Weatherconditions']).agg({'Delivery_person_Ratings': ['mean', 'std']})
            # renomeando as colunas
            df_aux.columns = ['delivery_mean', 'delivery_std']
            # reset do index
            df_aux = df_aux.reset_index()
            # exibindo o dataframe
            st.dataframe(df_aux)

    # linha 3
    with st.container():
        st.markdown('''___''')
        st.title('Velocidade de entrega')
        
        # criando colunas da linha 3
        col1, col2 = st.columns(2)

        # linha 3, colun 1
        with col1:
            st.markdown('##### Entregadores mais rápidos')
            df3 = top_delivers(df1, top_asc = True) #Chama a função, passando a ordem para mostrar os mais rápidos
            st.dataframe(df3)

        # linha 3, coluna 2
        with col2:
            st.markdown('##### Entregadores mais lentos')
            df3 = top_delivers(df1, top_asc = False) #Chama a função, passando a ordem para mostrar os mais lentos
            st.dataframe(df3) #Após o retorno da função, exibe o dataframe
                       

