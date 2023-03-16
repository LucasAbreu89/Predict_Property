import pandas as pd
import unidecode
import streamlit as st
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
import warnings
import json
from PIL import Image
import time
import base64
import os
warnings.filterwarnings("ignore", category=FutureWarning)

# loading and cleaning data
df = pd.read_csv("real.csv")
df.drop_duplicates(inplace=True)
df2 = df.drop(["url(image)", "url(apt)", "address"], axis=1)
df3 = df2[(df2['area(m²)'] > 15) & (df2['area(m²)'] < 1500)]
df3 = df3[(df3['condo(R$)'] < 10000) & (df3['condo(R$)'] >= 30)]
df3 = df3[(df3['price(R$)'] > 100000)]
df4 = df3.dropna(subset=['condo(R$)'])
df4.loc[:, 'district'] = df4['district'].apply(
    lambda x: unidecode.unidecode(x))
df4.reset_index(drop=True, inplace=True)
df4.fillna(0, inplace=True)
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
rfc = RandomForestClassifier(n_estimators=200,
                             random_state=42,
                             max_depth=30,
                             max_features="auto",
                             max_samples=0.5)
rfc.fit(X_train, y_train)

# acuracy
# st.subheader("Acuracy:")
# st.write(accuracy_score(y_test, rfc.predict(X_test)))

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
