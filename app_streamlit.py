import streamlit as st
import pandas as pd
import numpy as np
import joblib

def prepare_data(data):
    """
    Підготовка даних для прогнозування.
    Приймає на вхід словник або DataFrame.
    Повертає словник з підготовленими даними.
    """
    if isinstance(data, dict):
        return data
    elif isinstance(data, pd.DataFrame):
        return data.iloc[0].to_dict()
    else:
        raise ValueError("Не підтримуваний тип даних")

def predict(single_input):
    model = joblib.load('models/streamlit_pipeline.joblib')
    data = pd.DataFrame([single_input])
    predictions = model.predict(data)
    return predictions[0]

st.title('Прогнозування дощу в Австралії на завтра')
st.markdown('На основі сьогоднішніх метеорологічних даних прогнозуємо ймовірність дощу на завтра')

# Створення контейнера для зображення
with st.container():
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.image('images/rain_map.jpg')

st.title("Введіть дані про погоду сьогодні:")

data_input_method = st.radio("Оберіть метод введення даних:", ("Вручну", "Завантажити файл"))

if data_input_method == "Вручну":
    with st.form("my_form"):
            date = st.date_input("Дата")
            location = st.text_input("Місцевість")
            Rainfall = st.text_input("Кількість опадів, що випала за добу в мм")
            Evaporation = st.text_input("Випаровування")
            Sunshine = st.text_input("Кількість годин яскравого сонячного світла в день")
            WindGustDir = st.text_input("Напрямок найсильнішого пориву вітру за 24 години до півночі")
            WindGustSpeed = st.text_input("Швидкість (км/год) найсильнішого пориву вітру за 24 години до півночі")
            WindDir9am = st.text_input("Напрямок вітру о 9 ранку")
            WindDir3pm = st.text_input("Напрямок вітру о 15:00")
            Humidity9am = st.text_input("Вологість (у відсотках) о 9 ранку")
            Humidity3pm = st.text_input("Вологість (у відсотках) о 15:00")
            Pressure9am = st.text_input("Атмосферний тиск (гПа) знизився до середнього рівня моря о 9 ранку")
            Pressure3pm = st.text_input("Атмосферний тиск (гПа) знизився до середнього рівня моря о 15:00")
            Cloud9am = st.text_input("Частина неба, закрита хмарами о 9 ранку. Це вимірюється в октах, які є одиницею восьмих. Він записує, скільки восьмих неба")
            Cloud3pm = st.text_input("Частина неба, закрита хмарами (в октах: восьмі) о 15:00")
            RainToday = st.text_input("Чи був сьогодні дощ?")
            submitted = st.form_submit_button("Підтвердити")
            if submitted:
                new_input = {
                    'Date': date,
                    'Location': location,
                    'Rainfall': Rainfall,
                    'Evaporation': Evaporation,
                    'Sunshine': Sunshine,
                    'WindGustDir': WindGustDir,
                    'WindGustSpeed': WindGustSpeed,
                    'WindDir9am': WindDir9am,
                    'WindDir3pm': WindDir3pm,
                    'Humidity9am': Humidity9am,
                    'Humidity3pm': Humidity3pm,
                    'Pressure9am': Pressure9am,
                    'Pressure3pm': Pressure3pm,
                    'Cloud9am': Cloud9am,
                    'Cloud3pm': Cloud3pm,
                    'RainToday': RainToday
                }
                # Виклик функції для прогнозування
                prediction = predict(new_input)
                st.write("Прогноз:", prediction)


elif data_input_method == "Завантажити файл":
    uploaded_file = st.file_uploader("Завантажте файл Excel")
    df = None  # Ініціалізуємо df як None

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.success("Файл успішно завантажено!")

    if st.button("Зробити прогноз"):
        if df is not None:
            new_input = prepare_data(df)
            prediction = predict(new_input)
        else:
            st.warning("Спочатку завантажте файл")


if 'prediction' in locals():
    if prediction == "Yes":
        st.markdown("<h2 style='text-align: center;'><b>Очікується дощ. Візьміть парасольку!</b></h2>", unsafe_allow_html=True)
        st.image('images/Rain.png')
    else:
        st.markdown("<h2 style='text-align: center;'><b>Очікується сонячна погода!</b></h2>", unsafe_allow_html=True)
        st.image('images/Sun.png')
