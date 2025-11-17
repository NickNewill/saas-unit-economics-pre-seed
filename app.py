import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="SaaS Unit Economics - Pre-Seed Edition", 
    layout="wide"
)

st.title("🚀 SaaS Unit Economics - Pre-Seed Edition")
st.markdown("### Специально для B2B SaaS стартапов на ранней стадии")

st.success("✅ Приложение успешно загружено!")
st.info("Функциональность постепенно добавляется...")

# Простой пример работы
st.subheader("📊 Тестовая визуализация")
df = pd.DataFrame({
    'Месяц': [1, 2, 3, 4, 5],
    'MRR': [10000, 15000, 22000, 30000, 40000],
    'Клиенты': [2, 5, 8, 12, 18]
})

fig = px.line(df, x='Месяц', y='MRR', title='Рост MRR')
st.plotly_chart(fig)

st.dataframe(df)