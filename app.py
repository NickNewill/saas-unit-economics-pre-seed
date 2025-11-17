import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="SaaS Unit Economics - Pre-Seed Edition", 
    layout="wide"
)

def main():
    st.title("🚀 SaaS Unit Economics - Pre-Seed Edition")
    st.markdown("### Специально для B2B SaaS стартапов на ранней стадии")
    
    st.success("✅ Приложение успешно загружено в Streamlit Cloud!")
    
    # Простая демонстрация
    st.subheader("📊 Демо-дашборд")
    
    # Пример данных
    data = {
        'Месяц': [1, 2, 3, 4, 5, 6],
        'MRR': [10000, 25000, 45000, 70000, 100000, 140000],
        'Клиенты': [2, 6, 12, 20, 30, 45],
        'CAC': [15000, 12000, 9000, 7500, 6000, 5000]
    }
    df = pd.DataFrame(data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("💰 Текущий MRR", "140,000 ₽", "40%")
        st.metric("👥 Клиенты", "45", "15")
        
    with col2:
        st.metric("🎯 CAC", "5,000 ₽", "-16%")
        st.metric("📈 LTV", "75,000 ₽", "25%")
    
    # Графики
    fig_mrr = px.line(df, x='Месяц', y='MRR', title='Рост MRR')
    st.plotly_chart(fig_mrr, use_container_width=True)
    
    st.dataframe(df)
    
    st.info("""
    **🚀 Полная версия с AI-аналитикой будет доступна после настройки сервисов**
    - GigaChat интеграция
    - Когортный анализ  
    - Прогнозы и рекомендации
    - Budget planning
    """)

if __name__ == "__main__":
    main()