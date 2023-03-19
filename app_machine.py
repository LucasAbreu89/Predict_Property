import pandas as pd
import unidecode
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_classification
import warnings
import time
import os
from dotenv import load_dotenv
from supabase import create_client
from sklearn.metrics import r2_score
import plotly.express as px
from unidecode import unidecode
import re
from rapidfuzz import fuzz
warnings.filterwarnings("ignore", category=FutureWarning)

# loading data
load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

scrap_day = supabase.table("data_scrap").select("*").execute()
bairro_categorizado = pd.read_excel("Categoria_bairros.xlsx", index_col=0)
my_dict = bairro_categorizado.to_dict()['regional']
df4 = pd.DataFrame(scrap_day.data)

# cleaning data
df4 = df4.reset_index()
df4 = df4.drop(["id", "created_at", "index"], axis=1)
df4.drop_duplicates(inplace=True)
df4.drop(["url(image)", "url(apt)", "address"], axis=1, inplace=True)
df4 = df4[(df4['area(m²)'] > 15) & (df4['area(m²)'] < 1500)]
df4 = df4[(df4['condo(R$)'] < 10000) & (df4['condo(R$)'] >= 30)]
df4 = df4[(df4['price(R$)'] > 100000)]
df4.dropna(subset=['condo(R$)'], inplace=True)
print(df4.shape)
df4['district'] = df4['district'].apply(lambda x: unidecode(x))
df4['district'] = df4['district'].str.title()
df4['district'] = df4['district'].apply(
    lambda x: re.sub(r'\([^)]*\)', '', x).strip())
df4['district'] = df4['district'].str.replace("ç", "c")
df4 = df4.reset_index(drop=True)
df4['regional'] = None
for key, value in my_dict.items():
    mask = df4['district'] == key
    if mask.any():
        df4.loc[mask, 'regional'] = value
    else:
        # find the closest match to the key
        ratios = [(fuzz.ratio(key, district), district)
                  for district in df4['district']]
        closest_match = max(ratios, key=lambda x: x[0])[1]
        # set the value in the 'regional' column for the closest match
        mask = df4['district'] == closest_match
        df4.loc[mask, 'regional'] = value

counts_by_regional = df4.groupby('regional')['price(R$)'].count().reset_index()
counts_by_regional = counts_by_regional.rename(columns={'price(R$)': 'count'})
df_mean_price = df4.groupby('regional', as_index=False).mean()

df4.drop(["regional"], axis=1, inplace=True)
df4[['bedroom', 'bathrooms', 'parkings', "condo(R$)"]] = df4[[
    'bedroom', 'bathrooms', 'parkings', "condo(R$)"]].fillna(0)

district_options = df4["district"].unique()

# training test
X = df4.drop(["price(R$)"], axis=1)
y = df4["price(R$)"]
onehot = OneHotEncoder(sparse=False)
normalizador = MinMaxScaler()
X_cat = X.select_dtypes(include=['object'])
X_bin = onehot.fit_transform(X_cat)
X_num = X.select_dtypes(exclude=['object'])
X_num = normalizador.fit_transform(X_num)
X_all = np.append(X_num, X_bin, axis=1)
X_train, X_test, y_train, y_test = train_test_split(
    X_all, y, test_size=1/3, random_state=42)

# set page config to center the app content
st.set_page_config(page_title="Predicting App",
                   layout="centered", initial_sidebar_state="expanded")


with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# title
st.header("""Predicting price of properties""")

# subheader
st.subheader("Property Information")
st.sidebar.subheader("Propertie Features")

# input data
user_input = st.sidebar.text_input("Owner name")
st.write("Owner name: ", user_input)


# get user data
def get_user_data(user_input):
    district = st.sidebar.selectbox(
        "District", district_options)
    condo = st.sidebar.text_input("Condo (R$)", "0")
    area = st.sidebar.text_input("Area (m²)", "0")
    bedrooms = st.sidebar.slider("Bedrooms", 0, 10, 0)
    bathrooms = st.sidebar.slider("Bathrooms", 0, 10, 0)
    parkings = st.sidebar.slider("Parkings", 0, 10, 0)

    if st.sidebar.button("Apply"):
        user_data = {"condo(R$)": int(condo),
                     "area(m²)": int(area),
                     "bedroom": bedrooms,
                     "bathrooms": bathrooms,
                     "parkings": parkings,
                     "district": district}
        features = pd.DataFrame(user_data, index=[user_input])

        return features
    else:
        return None


user_input_variables = get_user_data(user_input)
if user_input_variables is not None:
    st.write("User Input Variables:")
    st.dataframe(user_input_variables, width=800)

# modelo
rfc = RandomForestRegressor(n_estimators=200,
                            random_state=42,
                            max_depth=30,
                            max_features="auto",
                            max_samples=0.5)
rfc.fit(X_train, y_train)

# acuracy

y_pred = rfc.predict(X_test)
r2 = r2_score(y_test, y_pred)
st.subheader("R-squared (R2) value: " + str(r2))

# normalize data
try:
    X_new_cat = user_input_variables.select_dtypes(include=['object'])
    X_new_bin = onehot.transform(X_new_cat)
    X_new_num = user_input_variables.select_dtypes(exclude=['object'])
    X_new_num = normalizador.transform(X_new_num)
    X_new_all = np.append(X_new_num, X_new_bin, axis=1)

    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.04)
        my_bar.progress(percent_complete + 1, text=progress_text)
    # predict
    if percent_complete == 99:
        pred = rfc.predict(X_new_all)[0]
        # st.subheader("forecast:")
        st.header(f"Estimated price: R${pred:.2f}")
except:
    st.write("Please fill in all the required fields.")

# plots


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
