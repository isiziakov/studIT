import streamlit as st
import pandas as pd
import numpy as np
import requests
import webbrowser as wb
import json
import matplotlib.pyplot as plt

url = "http://127.0.0.1:8000/"

st.title('M5')

st.title('Загрузка набора данных')
tab1, tab2, tab3 = st.tabs(["Один файл", "Несколько файлов", "Папка с файлами"])

with tab1:
    uploaded_file = st.file_uploader("Загрузите файл формата csv", type="csv")
    if uploaded_file is not None:
        if st.button("Отправить без обработки"):
            files = {"file" : uploaded_file}
            x = requests.post(f"{url}/upload", files=files)
            st.write(x.text)
        if st.button("Отправить с обработкой"):
            files = {"file" : uploaded_file}
            x = requests.post(f"{url}/uploadP", files=files)
            st.write(x.text)
with tab2:
    uploaded_file2 = st.file_uploader("Загрузите файлы формата csv", type="csv", accept_multiple_files=True)
    if len(uploaded_file2) > 0:
        if st.button("Отправить без обработки"):
            for f in uploaded_file2:
                files = {"file": f}
                x = requests.post(f"{url}/upload", files=files)
                st.write(x.text)
        if st.button("Отправить c обработкой"):
            for f in uploaded_file2:
                files = {"file": f}
                x = requests.post(f"{url}/uploadP", files=files)
                st.write(x.text)
with tab3:
    uploaded_file2 = st.file_uploader("Перетащите на этот элемент папку с файлами csv, которую нужно загрузить", type="csv", accept_multiple_files=True)
    if len(uploaded_file2) > 0:
        if st.button("Отправить без обработки"):
            for f in uploaded_file2:
                files = {"file": f}
                x = requests.post(f"{url}/upload", files=files)
                st.write(x.text)
        if st.button("Отправить c обработкой"):
            for f in uploaded_file2:
                files = {"file": f}
                x = requests.post(f"{url}/uploadP", files=files)
                st.write(x.text)


st.title("Выбор текущих данных")
if st.button("Получить список наборов данных на сервере"):
    x = requests.get(f"{url}/allFiles")
    st.write(x.text)

name = st.text_input("Введите название файла для выбора")
if name != "":
    if st.button("Выбрать файл"):
        params = {"filename": name}
        x = requests.get(f"{url}/setFile", params=params)
        st.write(x.text)

st.title("Выбор текущей модели")
if st.button("Получить список моделей на сервере"):
    x = requests.get(f"{url}/allModels")
    st.write(x.text)

model = st.text_input("Введите название модели для выбора")
if model != "":
    if st.button("Выбрать модель"):
        params = {"filename": model}
        x = requests.get(f"{url}/setModel", params=params)
        st.write(f"Выбрана модель {x.text}")

st.title("Предсказание")
if st.button("Сделать предсказание по текущим данным и модели"):
    x = requests.get(f"{url}/predict")
    if x.text.find("выбран") != -1:
        st.write(x.text)
    else:
        dat = x.text.replace("[", "").replace("]", "").replace('"', '')
        dat = dat.split(", ")
        st.write(pd.DataFrame(dat))

st.title("Построить график")
feature = st.text_input("Введите название параметра")
if feature != "":
    X = []
    y = []
    params = {"name":feature}
    x = requests.get(f"{url}/feature", params=params)
    if x.text.find("не") != -1:
        st.write(x.text)
    else:
        dat = x.text.replace("[", "").replace("]", "").replace('"', '')
        dat = dat.split(", ")
        X = pd.DataFrame(dat)
    x = requests.get(f"{url}/predict")
    if x.text.find("выбран") != -1:
        st.write(x.text)
    else:
        dat = x.text.replace("[", "").replace("]", "").replace('"', '')
        dat = dat.split(", ")
        y = pd.DataFrame(dat)
    if len(X) > 0 and len(y) > 0:

        genre = st.radio(
            "Выберите тип диаграммы",
            ["Точечная", "Неточечная"],
            index=None,
        )

        if genre == "Точечная":
            fig, ax = plt.subplots()
            plt.scatter(X[0], y[0])
            plt.xlabel(f'{feature}')
            plt.xticks(rotation=90)
            plt.ylabel("Прогноз")
            plt.title(f'Зависимость прогноза от {feature}')
            ax.set_xticklabels(X[0].sort_values())
            st.pyplot(fig)
        if genre == "Неточечная":
            fig, ax = plt.subplots()
            plt.plot(X[0], y[0])
            plt.xlabel(f'{feature}')
            plt.xticks(rotation=90)
            plt.ylabel("Прогноз")
            plt.title(f'Зависимость прогноза от {feature}')
            ax.set_xticklabels(X[0].sort_values())
            st.pyplot(fig)


st.title("Получить информацию об авторе")


@st.dialog("О программе")
def info(text):
    st.write(f"{text}")


if st.button("Получить информацию"):
    x = requests.get(f"{url}/info")
    info(x.text)

st.title("Инструкция пользователя")
if st.button("Открыть инструкцию"):
    wb.open_new_tab(f"instruction.html")
