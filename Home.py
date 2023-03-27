import pandas as pd
import streamlit as st
import warnings
from datetime import date, datetime
import os
from dotenv import load_dotenv
from supabase import create_client
from sklearn.metrics import r2_score
import plotly.express as px
warnings.filterwarnings("ignore", category=FutureWarning)

st.set_page_config(page_title="Predicting App",
                   layout="centered", initial_sidebar_state="expanded")

# title
st.header("""Predicting price of properties""")
st.text("The graphs below show the number of properties that we have cataloged\nin our database and the average price per neighborhood in Belo Horizonte.")

st.sidebar.subheader(
    "Select above the type of prediction you would like to make")

st.subheader("Property for sale chart")
load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY2")
supabase = create_client(url, key)

scrap_day = supabase.table("data_scrap").select("*").execute()
my_dict = {'Alta Tensao': 'Barreiro', 'Aarao Reis': 'Norte', 'Acaba Mundo': 'Centro-sul', 'Acaiaca': 'Nordeste', 'Ademar Maldonado': 'Barreiro', 'Aeroporto': 'Pampulha', 'Aguas Claras': 'Barreiro', 'Alipio De Melo': 'Pampulha', 'Alpes': 'Oeste', 'Alto Barroca': 'Oeste', 'Alto Caicaras': 'Noroeste', 'Alto Das Antenas': 'Barreiro', 'Alto Dos Pinheiros': 'Noroeste', 'Alto Vera Cruz': 'Leste', 'Alvaro Camargos': 'Noroeste', 'Ambrosina': 'Oeste', 'Anchieta': 'Centro-sul', 'Andiroba': 'Nordeste', 'Antonio Ribeiro De Abreu': 'Nordeste', 'Aparecida': 'Noroeste', 'Aparecida Setima Secao': 'Noroeste', 'Apia': 'Centro-sul', 'Apolonia': 'Venda nova', 'Araguaia': 'Barreiro', 'Atila De Paiva': 'Barreiro', 'Bacurau': 'Norte', 'Bairro Das Industrias I': 'Barreiro', 'Bairro Das Industrias II': 'Oeste', 'Bairro Novo Das Industrias': 'Barreiro', 'Baleia': 'Leste', 'Bandeirantes': 'Pampulha', 'Barao Homem De Melo': 'Oeste', 'Barreiro': 'Barreiro', 'Barro Preto': 'Centro-sul', 'Barroca': 'Oeste', 'Beija Flor': 'Nordeste', 'Beira-Linha': 'Nordeste', 'Bela Vitoria': 'Nordeste', 'Belem': 'Leste', 'Belmonte': 'Nordeste', 'Belvedere': 'Centro-sul', 'Bernadete': 'Barreiro', 'Betania': 'Oeste', 'Biquinhas': 'Norte', 'Bispo De Maura': 'Pampulha', 'Boa Esperanca': 'Nordeste', 'Boa Uniao': 'Norte', 'Boa Viagem': 'Centro-sul', 'Boa Vista': 'Leste', 'Bom Jesus': 'Noroeste', 'Bonfim': 'Noroeste', 'Bonsucesso': 'Barreiro', 'Brasil Industrial': 'Barreiro', 'Braunas': 'Pampulha', 'Buritis': 'Oeste', 'Cabana Do Pai Tomas': 'Oeste', 'Cachoeirinha': 'Nordeste', 'Caetano Furquim': 'Leste', 'Caicara-Adelaide': 'Noroeste', 'Caicaras': 'Noroeste', 'Caicara': 'Noroeste', 'Calafate': 'Oeste', 'California': 'Noroeste', 'Camargos': 'Oeste', 'Campo Alegre': 'Norte', 'Camponesa': 'Leste', 'Campus Ufmg': 'Pampulha', 'Canaa': 'Venda nova', 'Canada': 'Nordeste', 'Candelaria': 'Venda nova', 'Capitao Eduardo': 'Nordeste', 'Cardoso': 'Barreiro', 'Carlos Prates': 'Noroeste', 'Carmo': 'Centro-sul', 'Casa Branca': 'Leste', 'Castanheira': 'Barreiro', 'Castelo': 'Pampulha', 'Cdi Jatoba': 'Barreiro', 'Cenaculo': 'Venda nova', 'Centro': 'Centro-sul', 'Ceu Azul': 'Pampulha', 'Chacara Leonina': 'Oeste', 'Cidade Jardim': 'Centro-sul', 'Cidade Jardim Taquaril': 'Leste', 'Cidade Nova': 'Nordeste', 'Cinquentenario': 'Oeste', 'Colegio Batista': 'Nordeste', 'Comiteco': 'Centro-sul', 'Concordia': 'Nordeste', 'Conego Pinheiro': 'Leste', 'Conego Pinheiro A': 'Leste', 'Confisco': 'Pampulha', 'Conjunto Bonsucesso': 'Barreiro', 'Conjunto California': 'Noroeste', 'Conjunto Capitao Eduardo': 'Nordeste', 'Conjunto Celso Machado': 'Pampulha', 'Conjunto Floramar': 'Norte', 'Conjunto Jardim Filadelfia': 'Noroeste', 'Conjunto Jatoba': 'Barreiro', 'Conjunto Lagoa': 'Pampulha', 'Conjunto Minascaixa': 'Venda nova', 'Conjunto Novo Dom Bosco': 'Noroeste', 'Conjunto Paulo': 'Nordeste', 'Conjunto Providencia': 'Norte', 'Conjunto Santa Maria': 'Centro-sul', 'Conjunto Sao Francisco De Assis': 'Pampulha', 'Conjunto Serra Verde': 'Venda nova', 'Conjunto Taquaril': 'Leste', 'Copacabana': 'Pampulha', 'Coqueiros': 'Noroeste', 'Coracao De Jesus': 'Centro-sul', 'Coracao Eucaristico': 'Noroeste', 'Corumbiara': 'Barreiro', 'Cruzeiro': 'Centro-sul', 'Custodinha': 'Oeste', 'Delta': 'Noroeste', 'Diamante': 'Barreiro', 'Distrito Industrial Do Jatoba': 'Barreiro', 'Dom Bosco': 'Noroeste', 'Dom Cabral': 'Noroeste', 'Dom Joaquim': 'Nordeste', 'Dom Silverio': 'Nordeste', 'Dona Clara': 'Pampulha', 'Engenho Nogueira': 'Pampulha', 'Ermelinda': 'Noroeste', 'Ernesto Do Nascimento': 'Barreiro', 'Esperanca': 'Barreiro', 'Esplanada': 'Leste', 'Estoril': 'Oeste', 'Estrela': 'Centro-sul', 'Estrela Do Oriente': 'Oeste', 'Etelvina Carneiro': 'Norte', 'Europa': 'Venda nova', 'Eymard': 'Nordeste', 'Fazendinha': 'Centro-sul', 'Fernao Dias': 'Nordeste', 'Flamengo': 'Venda nova', 'Flavio De Oliveira': 'Barreiro', 'Flavio Marques Lisboa': 'Barreiro', 'Floramar': 'Norte', 'Floresta': 'Centro-sul', 'Frei Leopoldo': 'Norte', 'Funcionarios': 'Centro-sul', 'Gameleira': 'Oeste', 'Garcas': 'Pampulha', 'Gloria': 'Noroeste', 'Goiania': 'Nordeste', 'Graca': 'Nordeste', 'Grajau': 'Oeste', 'Granja De Freitas': 'Leste', 'Granja Werneck': 'Norte', 'Grota': 'Leste', 'Grotinha': 'Nordeste', 'Guanabara': 'Nordeste', 'Guarani': 'Norte', 'Guarata': 'Oeste', 'Gutierrez': 'Oeste', 'Havai': 'Oeste', 'Heliopolis': 'Norte', 'Horto': 'Leste', 'Horto Florestal': 'Leste', 'Imbaubas': 'Oeste', 'Inconfidencia': 'Pampulha', 'Indaia': 'Pampulha', 'Independencia': 'Barreiro', 'Ipe': 'Nordeste', 'Ipiranga': 'Nordeste', 'Itaipu': 'Barreiro', 'Itapoa': 'Pampulha', 'Itatiaia': 'Pampulha', 'Jaqueline': 'Norte', 'Jaragua': 'Pampulha', 'Jardim Alvorada': 'Pampulha', 'Jardim America': 'Oeste', 'Jardim Atlantico': 'Pampulha', 'Jardim Do Vale': 'Barreiro', 'Jardim Dos Comerciarios': 'Venda nova', 'Jardim Felicidade': 'Norte', 'Jardim Guanabara': 'Norte', 'Jardim Leblon': 'Venda nova', 'Jardim Montanhes': 'Noroeste', 'Jardim Sao Jose': 'Pampulha', 'Jardim Vitoria': 'Nordeste', 'Jardinopolis': 'Oeste', 'Jatoba': 'Barreiro', 'Joao Alfredo': 'Leste', 'Joao Paulo Ii': 'Barreiro', 'Joao Pinheiro': 'Noroeste', 'Jonas Veiga': 'Leste', 'Juliana': 'Norte', 'Lagoa': 'Venda nova', 'Lagoa Da Pampulha': 'Pampulha', 'Lagoinha': 'Noroeste', 'Lagoinha Leblon': 'Venda nova', 'Lajedo': 'Norte', 'Laranjeiras': 'Venda nova', 'Leonina': 'Oeste', 'Leticia': 'Venda nova', 'Liberdade': 'Pampulha', 'Lindeia': 'Barreiro', 'Lorena': 'Noroeste', 'Lourdes': 'Centro-sul', 'Luxemburgo': 'Centro-sul', 'Madre Gertrudes': 'Oeste', 'Madri': 'Norte', 'Mala E Cuia': 'Centro-sul', 'Manacas': 'Pampulha', 'Mangabeiras': 'Centro-sul', 'Mangueiras': 'Barreiro', 'Mantiqueira': 'Venda nova', 'Marajo': 'Oeste', 'Maravilha': 'Oeste', 'Marcola': 'Centro-sul', 'Maria Goretti': 'Nordeste', 'Maria Helena': 'Venda nova', 'Maria Teresa': 'Norte', 'Maria Virginia': 'Nordeste', 'Mariano De Abreu': 'Leste', 'Marieta': 'Barreiro', 'Marilandia': 'Barreiro', 'Mariquinhas': 'Norte', 'Marmiteiros': 'Noroeste', 'Milionarios': 'Barreiro', 'Minas Brasil': 'Noroeste', 'Minascaixa': 'Venda nova', 'Minaslandia': 'Norte', 'Mineirao': 'Barreiro', 'Miramar': 'Barreiro', 'Mirante': 'Norte', 'Mirtes': 'Nordeste', 'Monsenhor Messias': 'Noroeste', 'Monte Azul': 'Norte', 'Monte Sao Jose': 'Centro-sul', 'Morro Dos Macacos': 'Nordeste', 'Nazare': 'Nordeste', 'Nossa Senhora Da Aparecida': 'Centro-sul', 'Nossa Senhora Da Conceicao': 'Centro-sul', 'Nossa Senhora De Fatima': 'Centro-sul',
           'Nossa Senhora Do Rosario': 'Centro-sul', 'Nova America': 'Venda nova', 'Nova Cachoeirinha': 'Noroeste', 'Nova Cintra': 'Oeste', 'Nova Esperanca': 'Noroeste', 'Nova Floresta': 'Nordeste', 'Nova Gameleira': 'Oeste', 'Nova Granada': 'Oeste', 'Nova Pampulha': 'Pampulha', 'Nova Suissa': 'Oeste', 'Nova Vista': 'Leste', 'Novo Aarao Reis': 'Norte', 'Novo Gloria': 'Noroeste', 'Novo Ouro Preto': 'Pampulha', 'Novo Santa Cecilia': 'Barreiro', 'Novo Sao Lucas': 'Centro-sul', 'Novo Tupi': 'Norte', 'Oeste': 'Oeste', 'Olaria': 'Barreiro', "Olhos D'Agua": 'Barreiro', 'Ouro Minas': 'Nordeste', 'Ouro Preto': 'Pampulha', 'Padre Eustaquio': 'Noroeste', 'Palmares': 'Nordeste', 'Palmeiras': 'Oeste', 'Pantanal': 'Oeste', 'Paqueta': 'Pampulha', 'Paraiso': 'Leste', 'Parque Sao Jose': 'Oeste', 'Parque Sao Pedro': 'Venda nova', 'Paulo Vi': 'Nordeste', 'Pedreira Prado Lopes': 'Noroeste', 'Penha': 'Nordeste', 'Petropolis': 'Barreiro', 'Pilar': 'Barreiro', 'Pindorama': 'Noroeste', 'Pindura Saia': 'Centro-sul', 'Piraja': 'Nordeste', 'Piratininga': 'Venda nova', 'Pirineus': 'Leste', 'Planalto': 'Norte', 'Pompeia': 'Leste', 'Pongelupe': 'Barreiro', 'Pousada Santo Antonio': 'Nordeste', 'Prado': 'Oeste', 'Primeiro De Maio': 'Norte', 'Providencia': 'Norte', 'Renascenca': 'Nordeste', 'Ribeiro De Abreu': 'Nordeste', 'Rio Branco': 'Venda nova', 'Sagrada Familia': 'Leste', 'Salgado Filho': 'Oeste', 'Santa Amelia': 'Pampulha', 'Santa Branca': 'Pampulha', 'Santa Cecilia': 'Barreiro', 'Santa Cruz': 'Nordeste', 'Santa Efigenia': 'Leste', 'Santa Helena': 'Barreiro', 'Santa Ines': 'Leste', 'Santa Isabel': 'Centro-sul', 'Santa Lucia': 'Oeste', 'Santa Margarida': 'Barreiro', 'Santa Maria': 'Oeste', 'Santa Monica': 'Pampulha', 'Santa Rita': 'Barreiro', 'Santa Rita De Cassia': 'Centro-sul', 'Santa Rosa': 'Pampulha', 'Santa Sofia': 'Oeste', 'Santa Tereza': 'Leste', 'Santa Terezinha': 'Pampulha', 'Santana Do Cafezal': 'Centro-sul', 'Santo Agostinho': 'Centro-sul', 'Santo Andre': 'Noroeste', 'Santo Antonio': 'Centro-sul', 'Sao Benedito': 'Nordeste', 'Sao Bento': 'Centro-sul', 'Sao Bernardo': 'Norte', 'Sao Cristovao': 'Noroeste', 'Sao Damiao': 'Venda nova', 'Sao Francisco': 'Pampulha', 'Sao Francisco Das Chagas': 'Noroeste', 'Sao Gabriel': 'Nordeste', 'Sao Geraldo': 'Leste', 'Sao Goncalo': 'Norte', 'Sao Joao': 'Barreiro', 'Sao Joao Batista': 'Venda nova', 'Sao Jorge': 'Oeste', 'Sao Jose': 'Pampulha', 'Sao Lucas': 'Centro-sul', 'Sao Luiz': 'Pampulha', 'Sao Marcos': 'Nordeste', 'Sao Paulo': 'Nordeste', 'Sao Pedro': 'Centro-sul', 'Sao Salvador': 'Noroeste', 'Sao Sebastiao': 'Nordeste', 'Sao Tomaz': 'Norte', 'Sao Vicente': 'Leste', 'Satelite': 'Norte', 'Saudade': 'Leste', 'Savassi': 'Centro-sul', 'Senhor Dos Passos': 'Noroeste', 'Serra': 'Centro-sul', 'Serra Do Curral': 'Barreiro', 'Serra Verde': 'Venda nova', 'Serrano': 'Pampulha', 'Silveira': 'Nordeste', 'Sion': 'Centro-sul', 'Solar Do Barreiro': 'Barreiro', 'Solimoes': 'Norte', 'Sport Club': 'Oeste', 'Sumare': 'Noroeste', 'Suzana': 'Pampulha', 'Taquaril': 'Leste', 'Teixeira Dias': 'Barreiro', 'Tiradentes': 'Nordeste', 'Tirol': 'Barreiro', 'Tres Marias': 'Nordeste', 'Trevo': 'Pampulha', 'Tunel De Ibirite': 'Barreiro', 'Tupi A': 'Norte', 'Tupi B': 'Norte', 'Uniao': 'Nordeste', 'Unidas': 'Venda nova', 'Universitario': 'Pampulha', 'Universo': 'Venda nova', 'Urca': 'Pampulha', 'Vale Do Jatoba': 'Barreiro', 'Varzea Da Palma': 'Venda nova', 'Venda Nova': 'Venda nova', 'Ventosa': 'Oeste', 'Vera Cruz': 'Leste', 'Vila Aeroporto': 'Norte', 'Vila Aeroporto Jaragua': 'Pampulha', 'Vila Antena': 'Oeste', 'Vila Antena Montanhes': 'Pampulha', 'Vila Atila De Paiva': 'Barreiro', 'Vila Bandeirantes': 'Centro-sul', 'Vila Barragem Santa Lucia': 'Centro-sul', 'Vila Batik': 'Barreiro', 'Vila Betania': 'Oeste', 'Vila Boa Vista': 'Leste', 'Vila Calafate': 'Oeste', 'Vila California': 'Noroeste', 'Vila Canto Do Sabia': 'Venda nova', 'Vila Cemig': 'Barreiro', 'Vila Cloris': 'Norte', 'Vila Copacabana': 'Venda nova', 'Vila Copasa': 'Barreiro', 'Vila Coqueiral': 'Noroeste', 'Vila Da Amizade': 'Oeste', 'Vila Da Area': 'Leste', 'Vila Da Luz': 'Nordeste', 'Vila Da Paz': 'Nordeste', 'Vila Das Oliveiras': 'Noroeste', 'Vila De Sa': 'Nordeste', 'Vila Dias': 'Leste', 'Vila Do Pombal': 'Nordeste', 'Vila Dos Anjos': 'Venda nova', 'Vila Ecologica': 'Barreiro', 'Vila Engenho Nogueira': 'Pampulha', 'Vila Esplanada': 'Nordeste', 'Vila Formosa': 'Barreiro', 'Vila Fumec': 'Centro-sul', 'Vila Havai': 'Oeste', 'Vila Independencia': 'Barreiro', 'Vila Inestan': 'Nordeste', 'Vila Ipiranga': 'Nordeste', 'Vila Jardim Alvorada': 'Pampulha', 'Vila Jardim Leblon': 'Venda nova', 'Vila Jardim Montanhes': 'Pampulha', 'Vila Jardim Sao Jose': 'Pampulha', 'Vila Madre Gertrudes': 'Oeste', 'Vila Maloca': 'Noroeste', 'Vila Mangueiras': 'Barreiro', 'Vila Mantiqueira': 'Venda nova', 'Vila Maria': 'Nordeste', 'Vila Minaslandia': 'Norte', 'Vila Nossa Senhora Aparecida': 'Venda nova', 'Vila Nossa Senhora Do Rosario': 'Leste', 'Vila Nova': 'Norte', 'Vila Nova Cachoeirinha': 'Noroeste', 'Vila Nova Dos Milionarios': 'Barreiro', 'Vila Nova Gameleira': 'Oeste', 'Vila Nova Paraiso': 'Oeste', 'Vila Novo Sao Lucas': 'Centro-sul', 'Vila Oeste': 'Oeste', "Vila Olhos D'Agua": 'Barreiro', 'Vila Ouro Minas': 'Nordeste', 'Vila Paqueta': 'Pampulha', 'Vila Paraiso': 'Leste', 'Vila Paris': 'Centro-sul', 'Vila Petropolis': 'Barreiro', 'Vila Pilar': 'Barreiro', 'Vila Pinho': 'Barreiro', 'Vila Piratininga': 'Barreiro', 'Vila Piratininga Venda Nova': 'Venda nova', 'Vila Primeiro De Maio': 'Norte', 'Vila Puc': 'Noroeste', 'Vila Real': 'Pampulha', 'Vila Rica': 'Pampulha', 'Vila Santa Monica': 'Venda nova', 'Vila Santa Rosa': 'Pampulha', 'Vila Santo Antonio': 'Pampulha', 'Vila Santo Antonio Barroquinha': 'Pampulha', 'Vila Sao Dimas': 'Nordeste', 'Vila Sao Francisco': 'Pampulha', 'Vila Sao Gabriel': 'Nordeste', 'Vila Sao Gabriel Jacui': 'Nordeste', 'Vila Sao Geraldo': 'Leste', 'Vila Sao Joao Batista': 'Venda nova', 'Vila Sao Paulo': 'Nordeste', 'Vila Sao Rafael': 'Leste', 'Vila Satelite': 'Venda nova', 'Vila Sesc': 'Venda nova', 'Vila Sumare': 'Noroeste', 'Vila Suzana': 'Pampulha', 'Vila Tirol': 'Barreiro', 'Vila Trinta E Um De Marco': 'Noroeste', 'Vila Uniao': 'Leste', 'Vila Vera Cruz': 'Leste', 'Vila Vista Alegre': 'Oeste', 'Virginia': 'Oeste', 'Vista Alegre': 'Oeste', 'Vista Do Sol': 'Nordeste', 'Vitoria': 'Nordeste', 'Vitoria Da Conquista': 'Barreiro', 'Xangri-La': 'Pampulha', 'Xodo-Marize': 'Norte', 'Zilah Sposito': 'Norte'}

df4 = pd.DataFrame(scrap_day.data)

# cleaning data
df4 = df4.reset_index()
df4 = df4.drop(["id", "created_at", "index", "lat", "lng"], axis=1)
df4.drop_duplicates(inplace=True)
df4.drop(["url(image)", "url(apt)", "address"], axis=1, inplace=True)
df4 = df4[(df4['area(m²)'] > 15) & (df4['area(m²)'] < 1500)]
df4 = df4[(df4['condo(R$)'] < 10000) & (df4['condo(R$)'] >= 30)]
df4 = df4[(df4['price(R$)'] > 100000)]
df4.dropna(subset=['condo(R$)'], inplace=True)


counts_by_regional1 = df4.groupby(
    'regional')['price(R$)'].count().reset_index()
counts_by_regional1 = counts_by_regional1.rename(
    columns={'price(R$)': 'count'})
df_mean_price1 = df4.groupby('regional', as_index=False).mean()

df4.drop(["regional"], axis=1, inplace=True)
df4[['bedroom', 'bathrooms', 'parkings', "condo(R$)"]] = df4[[
    'bedroom', 'bathrooms', 'parkings', "condo(R$)"]].fillna(0)

district_options = df4["district"].unique()

fig1 = px.bar(counts_by_regional1, x='regional', y='count', color="regional",
              title='Counts of properties by regional',
              hover_data=['count'])

fig2 = px.bar(df_mean_price1, x='regional', y='price(R$)', color='regional',
              labels={'regional': 'Regional', 'price(R$)': 'Average Price (R$)'})

fig2.update_layout(title='Average Property Price by Region',
                   xaxis_title='Region',
                   yaxis_title='Average Price (R$)')

tab1, tab2 = st.tabs(['Counts of properties by regional',
                     'Average Property Price by Region'])

with tab1:
    # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
    st.plotly_chart(fig1, use_container_width=True)
with tab2:
    # Use the native Plotly theme.
    st.plotly_chart(fig2, use_container_width=True)


st.subheader("Property for rent chart")

scrap_rent = supabase.table("rent_scrap").select("*").execute()
my_dict = {'Alta Tensao': 'Barreiro', 'Aarao Reis': 'Norte', 'Acaba Mundo': 'Centro-sul', 'Acaiaca': 'Nordeste', 'Ademar Maldonado': 'Barreiro', 'Aeroporto': 'Pampulha', 'Aguas Claras': 'Barreiro', 'Alipio De Melo': 'Pampulha', 'Alpes': 'Oeste', 'Alto Barroca': 'Oeste', 'Alto Caicaras': 'Noroeste', 'Alto Das Antenas': 'Barreiro', 'Alto Dos Pinheiros': 'Noroeste', 'Alto Vera Cruz': 'Leste', 'Alvaro Camargos': 'Noroeste', 'Ambrosina': 'Oeste', 'Anchieta': 'Centro-sul', 'Andiroba': 'Nordeste', 'Antonio Ribeiro De Abreu': 'Nordeste', 'Aparecida': 'Noroeste', 'Aparecida Setima Secao': 'Noroeste', 'Apia': 'Centro-sul', 'Apolonia': 'Venda nova', 'Araguaia': 'Barreiro', 'Atila De Paiva': 'Barreiro', 'Bacurau': 'Norte', 'Bairro Das Industrias I': 'Barreiro', 'Bairro Das Industrias II': 'Oeste', 'Bairro Novo Das Industrias': 'Barreiro', 'Baleia': 'Leste', 'Bandeirantes': 'Pampulha', 'Barao Homem De Melo': 'Oeste', 'Barreiro': 'Barreiro', 'Barro Preto': 'Centro-sul', 'Barroca': 'Oeste', 'Beija Flor': 'Nordeste', 'Beira-Linha': 'Nordeste', 'Bela Vitoria': 'Nordeste', 'Belem': 'Leste', 'Belmonte': 'Nordeste', 'Belvedere': 'Centro-sul', 'Bernadete': 'Barreiro', 'Betania': 'Oeste', 'Biquinhas': 'Norte', 'Bispo De Maura': 'Pampulha', 'Boa Esperanca': 'Nordeste', 'Boa Uniao': 'Norte', 'Boa Viagem': 'Centro-sul', 'Boa Vista': 'Leste', 'Bom Jesus': 'Noroeste', 'Bonfim': 'Noroeste', 'Bonsucesso': 'Barreiro', 'Brasil Industrial': 'Barreiro', 'Braunas': 'Pampulha', 'Buritis': 'Oeste', 'Cabana Do Pai Tomas': 'Oeste', 'Cachoeirinha': 'Nordeste', 'Caetano Furquim': 'Leste', 'Caicara-Adelaide': 'Noroeste', 'Caicaras': 'Noroeste', 'Caicara': 'Noroeste', 'Calafate': 'Oeste', 'California': 'Noroeste', 'Camargos': 'Oeste', 'Campo Alegre': 'Norte', 'Camponesa': 'Leste', 'Campus Ufmg': 'Pampulha', 'Canaa': 'Venda nova', 'Canada': 'Nordeste', 'Candelaria': 'Venda nova', 'Capitao Eduardo': 'Nordeste', 'Cardoso': 'Barreiro', 'Carlos Prates': 'Noroeste', 'Carmo': 'Centro-sul', 'Casa Branca': 'Leste', 'Castanheira': 'Barreiro', 'Castelo': 'Pampulha', 'Cdi Jatoba': 'Barreiro', 'Cenaculo': 'Venda nova', 'Centro': 'Centro-sul', 'Ceu Azul': 'Pampulha', 'Chacara Leonina': 'Oeste', 'Cidade Jardim': 'Centro-sul', 'Cidade Jardim Taquaril': 'Leste', 'Cidade Nova': 'Nordeste', 'Cinquentenario': 'Oeste', 'Colegio Batista': 'Nordeste', 'Comiteco': 'Centro-sul', 'Concordia': 'Nordeste', 'Conego Pinheiro': 'Leste', 'Conego Pinheiro A': 'Leste', 'Confisco': 'Pampulha', 'Conjunto Bonsucesso': 'Barreiro', 'Conjunto California': 'Noroeste', 'Conjunto Capitao Eduardo': 'Nordeste', 'Conjunto Celso Machado': 'Pampulha', 'Conjunto Floramar': 'Norte', 'Conjunto Jardim Filadelfia': 'Noroeste', 'Conjunto Jatoba': 'Barreiro', 'Conjunto Lagoa': 'Pampulha', 'Conjunto Minascaixa': 'Venda nova', 'Conjunto Novo Dom Bosco': 'Noroeste', 'Conjunto Paulo': 'Nordeste', 'Conjunto Providencia': 'Norte', 'Conjunto Santa Maria': 'Centro-sul', 'Conjunto Sao Francisco De Assis': 'Pampulha', 'Conjunto Serra Verde': 'Venda nova', 'Conjunto Taquaril': 'Leste', 'Copacabana': 'Pampulha', 'Coqueiros': 'Noroeste', 'Coracao De Jesus': 'Centro-sul', 'Coracao Eucaristico': 'Noroeste', 'Corumbiara': 'Barreiro', 'Cruzeiro': 'Centro-sul', 'Custodinha': 'Oeste', 'Delta': 'Noroeste', 'Diamante': 'Barreiro', 'Distrito Industrial Do Jatoba': 'Barreiro', 'Dom Bosco': 'Noroeste', 'Dom Cabral': 'Noroeste', 'Dom Joaquim': 'Nordeste', 'Dom Silverio': 'Nordeste', 'Dona Clara': 'Pampulha', 'Engenho Nogueira': 'Pampulha', 'Ermelinda': 'Noroeste', 'Ernesto Do Nascimento': 'Barreiro', 'Esperanca': 'Barreiro', 'Esplanada': 'Leste', 'Estoril': 'Oeste', 'Estrela': 'Centro-sul', 'Estrela Do Oriente': 'Oeste', 'Etelvina Carneiro': 'Norte', 'Europa': 'Venda nova', 'Eymard': 'Nordeste', 'Fazendinha': 'Centro-sul', 'Fernao Dias': 'Nordeste', 'Flamengo': 'Venda nova', 'Flavio De Oliveira': 'Barreiro', 'Flavio Marques Lisboa': 'Barreiro', 'Floramar': 'Norte', 'Floresta': 'Centro-sul', 'Frei Leopoldo': 'Norte', 'Funcionarios': 'Centro-sul', 'Gameleira': 'Oeste', 'Garcas': 'Pampulha', 'Gloria': 'Noroeste', 'Goiania': 'Nordeste', 'Graca': 'Nordeste', 'Grajau': 'Oeste', 'Granja De Freitas': 'Leste', 'Granja Werneck': 'Norte', 'Grota': 'Leste', 'Grotinha': 'Nordeste', 'Guanabara': 'Nordeste', 'Guarani': 'Norte', 'Guarata': 'Oeste', 'Gutierrez': 'Oeste', 'Havai': 'Oeste', 'Heliopolis': 'Norte', 'Horto': 'Leste', 'Horto Florestal': 'Leste', 'Imbaubas': 'Oeste', 'Inconfidencia': 'Pampulha', 'Indaia': 'Pampulha', 'Independencia': 'Barreiro', 'Ipe': 'Nordeste', 'Ipiranga': 'Nordeste', 'Itaipu': 'Barreiro', 'Itapoa': 'Pampulha', 'Itatiaia': 'Pampulha', 'Jaqueline': 'Norte', 'Jaragua': 'Pampulha', 'Jardim Alvorada': 'Pampulha', 'Jardim America': 'Oeste', 'Jardim Atlantico': 'Pampulha', 'Jardim Do Vale': 'Barreiro', 'Jardim Dos Comerciarios': 'Venda nova', 'Jardim Felicidade': 'Norte', 'Jardim Guanabara': 'Norte', 'Jardim Leblon': 'Venda nova', 'Jardim Montanhes': 'Noroeste', 'Jardim Sao Jose': 'Pampulha', 'Jardim Vitoria': 'Nordeste', 'Jardinopolis': 'Oeste', 'Jatoba': 'Barreiro', 'Joao Alfredo': 'Leste', 'Joao Paulo Ii': 'Barreiro', 'Joao Pinheiro': 'Noroeste', 'Jonas Veiga': 'Leste', 'Juliana': 'Norte', 'Lagoa': 'Venda nova', 'Lagoa Da Pampulha': 'Pampulha', 'Lagoinha': 'Noroeste', 'Lagoinha Leblon': 'Venda nova', 'Lajedo': 'Norte', 'Laranjeiras': 'Venda nova', 'Leonina': 'Oeste', 'Leticia': 'Venda nova', 'Liberdade': 'Pampulha', 'Lindeia': 'Barreiro', 'Lorena': 'Noroeste', 'Lourdes': 'Centro-sul', 'Luxemburgo': 'Centro-sul', 'Madre Gertrudes': 'Oeste', 'Madri': 'Norte', 'Mala E Cuia': 'Centro-sul', 'Manacas': 'Pampulha', 'Mangabeiras': 'Centro-sul', 'Mangueiras': 'Barreiro', 'Mantiqueira': 'Venda nova', 'Marajo': 'Oeste', 'Maravilha': 'Oeste', 'Marcola': 'Centro-sul', 'Maria Goretti': 'Nordeste', 'Maria Helena': 'Venda nova', 'Maria Teresa': 'Norte', 'Maria Virginia': 'Nordeste', 'Mariano De Abreu': 'Leste', 'Marieta': 'Barreiro', 'Marilandia': 'Barreiro', 'Mariquinhas': 'Norte', 'Marmiteiros': 'Noroeste', 'Milionarios': 'Barreiro', 'Minas Brasil': 'Noroeste', 'Minascaixa': 'Venda nova', 'Minaslandia': 'Norte', 'Mineirao': 'Barreiro', 'Miramar': 'Barreiro', 'Mirante': 'Norte', 'Mirtes': 'Nordeste', 'Monsenhor Messias': 'Noroeste', 'Monte Azul': 'Norte', 'Monte Sao Jose': 'Centro-sul', 'Morro Dos Macacos': 'Nordeste', 'Nazare': 'Nordeste', 'Nossa Senhora Da Aparecida': 'Centro-sul', 'Nossa Senhora Da Conceicao': 'Centro-sul', 'Nossa Senhora De Fatima': 'Centro-sul',
           'Nossa Senhora Do Rosario': 'Centro-sul', 'Nova America': 'Venda nova', 'Nova Cachoeirinha': 'Noroeste', 'Nova Cintra': 'Oeste', 'Nova Esperanca': 'Noroeste', 'Nova Floresta': 'Nordeste', 'Nova Gameleira': 'Oeste', 'Nova Granada': 'Oeste', 'Nova Pampulha': 'Pampulha', 'Nova Suissa': 'Oeste', 'Nova Vista': 'Leste', 'Novo Aarao Reis': 'Norte', 'Novo Gloria': 'Noroeste', 'Novo Ouro Preto': 'Pampulha', 'Novo Santa Cecilia': 'Barreiro', 'Novo Sao Lucas': 'Centro-sul', 'Novo Tupi': 'Norte', 'Oeste': 'Oeste', 'Olaria': 'Barreiro', "Olhos D'Agua": 'Barreiro', 'Ouro Minas': 'Nordeste', 'Ouro Preto': 'Pampulha', 'Padre Eustaquio': 'Noroeste', 'Palmares': 'Nordeste', 'Palmeiras': 'Oeste', 'Pantanal': 'Oeste', 'Paqueta': 'Pampulha', 'Paraiso': 'Leste', 'Parque Sao Jose': 'Oeste', 'Parque Sao Pedro': 'Venda nova', 'Paulo Vi': 'Nordeste', 'Pedreira Prado Lopes': 'Noroeste', 'Penha': 'Nordeste', 'Petropolis': 'Barreiro', 'Pilar': 'Barreiro', 'Pindorama': 'Noroeste', 'Pindura Saia': 'Centro-sul', 'Piraja': 'Nordeste', 'Piratininga': 'Venda nova', 'Pirineus': 'Leste', 'Planalto': 'Norte', 'Pompeia': 'Leste', 'Pongelupe': 'Barreiro', 'Pousada Santo Antonio': 'Nordeste', 'Prado': 'Oeste', 'Primeiro De Maio': 'Norte', 'Providencia': 'Norte', 'Renascenca': 'Nordeste', 'Ribeiro De Abreu': 'Nordeste', 'Rio Branco': 'Venda nova', 'Sagrada Familia': 'Leste', 'Salgado Filho': 'Oeste', 'Santa Amelia': 'Pampulha', 'Santa Branca': 'Pampulha', 'Santa Cecilia': 'Barreiro', 'Santa Cruz': 'Nordeste', 'Santa Efigenia': 'Leste', 'Santa Helena': 'Barreiro', 'Santa Ines': 'Leste', 'Santa Isabel': 'Centro-sul', 'Santa Lucia': 'Oeste', 'Santa Margarida': 'Barreiro', 'Santa Maria': 'Oeste', 'Santa Monica': 'Pampulha', 'Santa Rita': 'Barreiro', 'Santa Rita De Cassia': 'Centro-sul', 'Santa Rosa': 'Pampulha', 'Santa Sofia': 'Oeste', 'Santa Tereza': 'Leste', 'Santa Terezinha': 'Pampulha', 'Santana Do Cafezal': 'Centro-sul', 'Santo Agostinho': 'Centro-sul', 'Santo Andre': 'Noroeste', 'Santo Antonio': 'Centro-sul', 'Sao Benedito': 'Nordeste', 'Sao Bento': 'Centro-sul', 'Sao Bernardo': 'Norte', 'Sao Cristovao': 'Noroeste', 'Sao Damiao': 'Venda nova', 'Sao Francisco': 'Pampulha', 'Sao Francisco Das Chagas': 'Noroeste', 'Sao Gabriel': 'Nordeste', 'Sao Geraldo': 'Leste', 'Sao Goncalo': 'Norte', 'Sao Joao': 'Barreiro', 'Sao Joao Batista': 'Venda nova', 'Sao Jorge': 'Oeste', 'Sao Jose': 'Pampulha', 'Sao Lucas': 'Centro-sul', 'Sao Luiz': 'Pampulha', 'Sao Marcos': 'Nordeste', 'Sao Paulo': 'Nordeste', 'Sao Pedro': 'Centro-sul', 'Sao Salvador': 'Noroeste', 'Sao Sebastiao': 'Nordeste', 'Sao Tomaz': 'Norte', 'Sao Vicente': 'Leste', 'Satelite': 'Norte', 'Saudade': 'Leste', 'Savassi': 'Centro-sul', 'Senhor Dos Passos': 'Noroeste', 'Serra': 'Centro-sul', 'Serra Do Curral': 'Barreiro', 'Serra Verde': 'Venda nova', 'Serrano': 'Pampulha', 'Silveira': 'Nordeste', 'Sion': 'Centro-sul', 'Solar Do Barreiro': 'Barreiro', 'Solimoes': 'Norte', 'Sport Club': 'Oeste', 'Sumare': 'Noroeste', 'Suzana': 'Pampulha', 'Taquaril': 'Leste', 'Teixeira Dias': 'Barreiro', 'Tiradentes': 'Nordeste', 'Tirol': 'Barreiro', 'Tres Marias': 'Nordeste', 'Trevo': 'Pampulha', 'Tunel De Ibirite': 'Barreiro', 'Tupi A': 'Norte', 'Tupi B': 'Norte', 'Uniao': 'Nordeste', 'Unidas': 'Venda nova', 'Universitario': 'Pampulha', 'Universo': 'Venda nova', 'Urca': 'Pampulha', 'Vale Do Jatoba': 'Barreiro', 'Varzea Da Palma': 'Venda nova', 'Venda Nova': 'Venda nova', 'Ventosa': 'Oeste', 'Vera Cruz': 'Leste', 'Vila Aeroporto': 'Norte', 'Vila Aeroporto Jaragua': 'Pampulha', 'Vila Antena': 'Oeste', 'Vila Antena Montanhes': 'Pampulha', 'Vila Atila De Paiva': 'Barreiro', 'Vila Bandeirantes': 'Centro-sul', 'Vila Barragem Santa Lucia': 'Centro-sul', 'Vila Batik': 'Barreiro', 'Vila Betania': 'Oeste', 'Vila Boa Vista': 'Leste', 'Vila Calafate': 'Oeste', 'Vila California': 'Noroeste', 'Vila Canto Do Sabia': 'Venda nova', 'Vila Cemig': 'Barreiro', 'Vila Cloris': 'Norte', 'Vila Copacabana': 'Venda nova', 'Vila Copasa': 'Barreiro', 'Vila Coqueiral': 'Noroeste', 'Vila Da Amizade': 'Oeste', 'Vila Da Area': 'Leste', 'Vila Da Luz': 'Nordeste', 'Vila Da Paz': 'Nordeste', 'Vila Das Oliveiras': 'Noroeste', 'Vila De Sa': 'Nordeste', 'Vila Dias': 'Leste', 'Vila Do Pombal': 'Nordeste', 'Vila Dos Anjos': 'Venda nova', 'Vila Ecologica': 'Barreiro', 'Vila Engenho Nogueira': 'Pampulha', 'Vila Esplanada': 'Nordeste', 'Vila Formosa': 'Barreiro', 'Vila Fumec': 'Centro-sul', 'Vila Havai': 'Oeste', 'Vila Independencia': 'Barreiro', 'Vila Inestan': 'Nordeste', 'Vila Ipiranga': 'Nordeste', 'Vila Jardim Alvorada': 'Pampulha', 'Vila Jardim Leblon': 'Venda nova', 'Vila Jardim Montanhes': 'Pampulha', 'Vila Jardim Sao Jose': 'Pampulha', 'Vila Madre Gertrudes': 'Oeste', 'Vila Maloca': 'Noroeste', 'Vila Mangueiras': 'Barreiro', 'Vila Mantiqueira': 'Venda nova', 'Vila Maria': 'Nordeste', 'Vila Minaslandia': 'Norte', 'Vila Nossa Senhora Aparecida': 'Venda nova', 'Vila Nossa Senhora Do Rosario': 'Leste', 'Vila Nova': 'Norte', 'Vila Nova Cachoeirinha': 'Noroeste', 'Vila Nova Dos Milionarios': 'Barreiro', 'Vila Nova Gameleira': 'Oeste', 'Vila Nova Paraiso': 'Oeste', 'Vila Novo Sao Lucas': 'Centro-sul', 'Vila Oeste': 'Oeste', "Vila Olhos D'Agua": 'Barreiro', 'Vila Ouro Minas': 'Nordeste', 'Vila Paqueta': 'Pampulha', 'Vila Paraiso': 'Leste', 'Vila Paris': 'Centro-sul', 'Vila Petropolis': 'Barreiro', 'Vila Pilar': 'Barreiro', 'Vila Pinho': 'Barreiro', 'Vila Piratininga': 'Barreiro', 'Vila Piratininga Venda Nova': 'Venda nova', 'Vila Primeiro De Maio': 'Norte', 'Vila Puc': 'Noroeste', 'Vila Real': 'Pampulha', 'Vila Rica': 'Pampulha', 'Vila Santa Monica': 'Venda nova', 'Vila Santa Rosa': 'Pampulha', 'Vila Santo Antonio': 'Pampulha', 'Vila Santo Antonio Barroquinha': 'Pampulha', 'Vila Sao Dimas': 'Nordeste', 'Vila Sao Francisco': 'Pampulha', 'Vila Sao Gabriel': 'Nordeste', 'Vila Sao Gabriel Jacui': 'Nordeste', 'Vila Sao Geraldo': 'Leste', 'Vila Sao Joao Batista': 'Venda nova', 'Vila Sao Paulo': 'Nordeste', 'Vila Sao Rafael': 'Leste', 'Vila Satelite': 'Venda nova', 'Vila Sesc': 'Venda nova', 'Vila Sumare': 'Noroeste', 'Vila Suzana': 'Pampulha', 'Vila Tirol': 'Barreiro', 'Vila Trinta E Um De Marco': 'Noroeste', 'Vila Uniao': 'Leste', 'Vila Vera Cruz': 'Leste', 'Vila Vista Alegre': 'Oeste', 'Virginia': 'Oeste', 'Vista Alegre': 'Oeste', 'Vista Do Sol': 'Nordeste', 'Vitoria': 'Nordeste', 'Vitoria Da Conquista': 'Barreiro', 'Xangri-La': 'Pampulha', 'Xodo-Marize': 'Norte', 'Zilah Sposito': 'Norte'}

df5 = pd.DataFrame(scrap_rent.data)

# cleaning data
df5 = df5.reset_index()
df5 = df5.drop(["id", "created_at", "index", "lat", "lng"], axis=1)
df5.drop_duplicates(inplace=True)
df5.drop(["url(image)", "url(apt)", "address"], axis=1, inplace=True)
df5 = df5[(df5['area(m²)'] > 15) & (df5['area(m²)'] < 1500)]
df5 = df5[(df5['condo(R$)'] < 10000) & (df5['condo(R$)'] >= 30)]
df5 = df5[(df5['price(R$)'] > 100)]
df5.dropna(subset=['condo(R$)'], inplace=True)


counts_by_regional = df5.groupby('regional')['price(R$)'].count().reset_index()
counts_by_regional = counts_by_regional.rename(columns={'price(R$)': 'count'})
df_mean_price = df5.groupby('regional', as_index=False).mean()

df5.drop(["regional"], axis=1, inplace=True)
df5[['bedroom', 'bathrooms', 'parkings', "condo(R$)"]] = df5[[
    'bedroom', 'bathrooms', 'parkings', "condo(R$)"]].fillna(0)

district_options = df5["district"].unique()

fig1 = px.bar(counts_by_regional, x='regional', y='count', color="regional",
              title='Counts of properties by regional',
              hover_data=['count'])

fig2 = px.bar(df_mean_price, x='regional', y='price(R$)', color='regional',
              labels={'regional': 'Regional', 'price(R$)': 'Average Price (R$)'})

fig2.update_layout(title='Average Property Price by Region',
                   xaxis_title='Region',
                   yaxis_title='Average Price (R$)')

tab1, tab2 = st.tabs(['Counts of properties by regional',
                     'Average Property Price by Region'])

with tab1:
    # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
    st.plotly_chart(fig1, use_container_width=True)
with tab2:
    # Use the native Plotly theme.
    st.plotly_chart(fig2, use_container_width=True)

# Get the last ID from the table
res = supabase.table("subscribers").select("id").execute()
last_id = pd.DataFrame(res.data)
next_id = int(last_id.id.max() or 0) + 1

# Get today's date
today = date.today().strftime("%Y-%m-%d")

if "subscribed" not in st.session_state:
    st.session_state.subscribed = False

st.text("If you would like to receive our daily news about real estate in Belo Horizonte,\nsign up below:")

name = ""
email = ""
# Get name and email input from user
name_input = st.text_input("Type your name here", value=name)
email_input = st.text_input("Type your email here", value=email)

# Add Subscribe button
subscribe_button = st.button("Subscribe")

if subscribe_button:
    # Update name, email, date, and ID variables
    name = name_input
    email = email_input
    id = next_id
    date = today

    # Insert name, email, date, and ID into Supabase table
    values = {"name": name, "email": email, "created_at": date, "id": id}
    res = supabase.table("subscribers").insert(values).execute()

    # Display success message and reset button
    st.success(f"You are now subscribed with name: {name}, email: {email}")
    reset_button = st.button("Reset")
    if reset_button:
        name_input = ""
        email_input = ""
        st.session_state.subscribed = False
else:
    # Reset name and email variables
    name = ""
    email = ""
