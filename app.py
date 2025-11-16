import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Загрузка environment variables
load_dotenv()

# Импорты наших сервисов
from services.stage_aware_metrics import StageAwareMetrics
from services.pre_seed_advisor import PreSeedAdvisor
from services.cohort_analyzer import RealisticCohortAnalyzer
from services.year_1_roadmap import Year1Roadmap
from services.runway_calculator import RunwayCalculator
from gigachat_analyst import SaaSUnitEconomicsAI

# === CALLBACK ФУНКЦИИ ДЛЯ НАВИГАЦИИ ПО МЕСЯЦАМ ===
def next_month():
    """Callback для следующего месяца"""
    st.session_state.current_month += 1

def prev_month():
    """Callback для предыдущего месяца"""
    if st.session_state.current_month > 1:
        st.session_state.current_month -= 1

# Функция для получения credentials
def get_gigachat_credentials():
    """Получение credentials из secrets (продакшен) или .env (разработка)"""
    try:
        # Пробуем получить из Streamlit Secrets (продакшен)
        return {
            'api_key': st.secrets["GIGACHAT_API_KEY"],
            'auth_url': st.secrets.get("GIGACHAT_AUTH_URL", "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"),
            'scope': st.secrets.get("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")
        }
    except Exception as e:
        # Fallback на .env файл (разработка)
        return {
            'api_key': os.getenv('GIGACHAT_API_KEY'),
            'auth_url': os.getenv('GIGACHAT_AUTH_URL', 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'),
            'scope': os.getenv('GIGACHAT_SCOPE', 'GIGACHAT_API_PERS')
        }

# Проверка наличия credentials
def check_credentials():
    credentials = get_gigachat_credentials()
    if not credentials['api_key'] or credentials['api_key'] == 'your_actual_api_key_here':
        st.error("⚠️ GigaChat API ключ не настроен. Пожалуйста, настройте секреты в Streamlit Cloud или .env файл для локальной разработки.")
        return False
    return True

st.set_page_config(
    page_title="SaaS Unit Economics - Pre-Seed Edition", 
    layout="wide", 
    page_icon="🚀"
)

# Инициализация сервисов с проверкой credentials
@st.cache_resource
def init_services():
    if not check_credentials():
        return None
        
    credentials = get_gigachat_credentials()
    return {
        'stage_metrics': StageAwareMetrics(),
        'pre_seed_advisor': PreSeedAdvisor(),
        'cohort_analyzer': RealisticCohortAnalyzer(),
        'roadmap': Year1Roadmap(),
        'runway_calc': RunwayCalculator(),
        'ai_analyst': SaaSUnitEconomicsAI()
    }

services = init_services()

def init_session_state():
    """Инициализация session state с историей данных"""
    if 'analysis_triggered' not in st.session_state:
        st.session_state.analysis_triggered = False
    if 'user_inputs_history' not in st.session_state:
        st.session_state.user_inputs_history = []
    if 'current_month' not in st.session_state:
        st.session_state.current_month = 1
    if 'monthly_results' not in st.session_state:
        st.session_state.monthly_results = {}
    if 'user_inputs' not in st.session_state:
        st.session_state.user_inputs = {}
    if 'last_submitted_month' not in st.session_state:
        st.session_state.last_submitted_month = 0

def main():
    st.title("🚀 SaaS Unit Economics - Pre-Seed Edition")
    st.markdown("### Специально для B2B SaaS стартапов на ранней стадии")
    
    # Инициализация session state
    init_session_state()
    
    # Навигация
    page = st.sidebar.selectbox(
        "Навигация",
        ["📊 Главный дашборд", "👥 Когортный анализ", "🎯 Цели и Roadmap", "💰 Бюджет и Runway"]
    )
    
    # Боковая панель с вводом данных
    user_inputs = render_sidebar()
    
    # КНОПКА ВЫЧИСЛЕНИЙ
    if st.sidebar.button("🚀 Запустить анализ", type="primary", use_container_width=True):
        # Проверяем, что это новый месяц
        if st.session_state.current_month > st.session_state.last_submitted_month:
            st.session_state.analysis_triggered = True
            # Сохраняем историю вводов
            st.session_state.user_inputs_history.append({
                'month': st.session_state.current_month,
                'inputs': user_inputs.copy(),
                'timestamp': datetime.now()
            })
            # Сохраняем текущие inputs
            st.session_state.user_inputs = user_inputs
            st.session_state.last_submitted_month = st.session_state.current_month
            st.rerun()
        else:
            st.sidebar.warning("⚠️ Вы уже ввели данные для этого месяца. Перейдите к следующему месяцу.")
    
    # Отображение выбранной страницы
    if page == "📊 Главный дашборд":
        render_main_dashboard(user_inputs)
    elif page == "👥 Когортный анализ":
        render_cohort_analysis(user_inputs)
    elif page == "🎯 Цели и Roadmap":
        render_goals_roadmap(user_inputs)
    elif page == "💰 Бюджет и Runway":
        render_budget_runway(user_inputs)

def render_sidebar():
    """Боковая панель для ввода данных с учетом истории"""
    with st.sidebar:
        st.header("🎯 Параметры вашего стартапа")
        
        # Показываем текущий месяц и прогресс
        st.subheader(f"📅 Месяц {st.session_state.current_month}")
        
        # Показываем историю месяцев
        if st.session_state.user_inputs_history:
            months_recorded = len(st.session_state.user_inputs_history)
            st.write(f"📊 Записей: {months_recorded} месяцев")
        
        # === ИСПРАВЛЕННАЯ НАВИГАЦИЯ С CALLBACK ===
        col1, col2 = st.columns(2)
        with col1:
            st.button("⬅️ Предыдущий месяц", 
                     on_click=prev_month, 
                     use_container_width=True,
                     key="prev_month")
        
        with col2:
            st.button("➡️ Следующий месяц", 
                     on_click=next_month, 
                     use_container_width=True,
                     key="next_month")
        
        # Основная информация
        st.subheader("📊 Текущее состояние")
        
        # Получаем данные предыдущего месяца для автозаполнения
        previous_month_data = {}
        if st.session_state.user_inputs_history:
            # Ищем данные для предыдущего месяца
            for entry in st.session_state.user_inputs_history:
                if entry['month'] == st.session_state.current_month - 1:
                    previous_month_data = entry['inputs']
                    break
        
        # Если нет данных для текущего месяца, используем предыдущий или значения по умолчанию
        current_month_data = {}
        for entry in st.session_state.user_inputs_history:
            if entry['month'] == st.session_state.current_month:
                current_month_data = entry['inputs']
                break
        
        monthly_budget = st.number_input("Месячный маркетинговый бюджет (руб.)", 
                                       value=current_month_data.get('monthly_budget', 
                                                                   previous_month_data.get('monthly_budget', 100000)), 
                                       step=50000,
                                       key=f"budget_{st.session_state.current_month}")
        
        team_size = st.number_input("Размер команды", 
                                  value=current_month_data.get('team_size', 
                                                             previous_month_data.get('team_size', 3)), 
                                  step=1,
                                  key=f"team_{st.session_state.current_month}")
        
        cash_balance = st.number_input("Текущий кэш (руб.)", 
                                     value=current_month_data.get('cash_balance', 
                                                                previous_month_data.get('cash_balance', 2000000)), 
                                     step=100000,
                                     key=f"cash_{st.session_state.current_month}")
        
        st.subheader("💰 Ценообразование")
        monthly_price = st.number_input("Цена подписки (руб./месяц)", 
                                      value=current_month_data.get('monthly_price', 
                                                                 previous_month_data.get('monthly_price', 5000)), 
                                      step=1000,
                                      key=f"price_{st.session_state.current_month}")
        
        st.subheader("📈 Текущие метрики")
        
        # Рассчитываем предполагаемое количество клиентов на основе роста
        if previous_month_data:
            # Предполагаем консервативный рост 15% если не указано иное
            suggested_customers = int(previous_month_data.get('current_customers', 0) * 1.15)
        else:
            suggested_customers = current_month_data.get('current_customers', 0)
            
        current_customers = st.number_input("Текущие клиенты", 
                                          value=current_month_data.get('current_customers', suggested_customers), 
                                          step=1,
                                          key=f"customers_{st.session_state.current_month}")
        
        # Рассчитываем предполагаемый MRR
        suggested_mrr = current_customers * monthly_price
        current_mrr = st.number_input("Текущий MRR (руб.)", 
                                    value=current_month_data.get('current_mrr', int(suggested_mrr)), 
                                    step=5000,
                                    key=f"mrr_{st.session_state.current_month}")
        
        st.subheader("🎯 Бизнес-параметры")
        target_cac = st.number_input("Целевой CAC (руб.)", 
                                   value=current_month_data.get('target_cac', 
                                                              previous_month_data.get('target_cac', 15000)), 
                                   step=1000,
                                   key=f"cac_{st.session_state.current_month}")
        
        expected_churn = st.slider("Ожидаемый Churn Rate (%)", 5, 40, 
                                 int(current_month_data.get('expected_churn', 
                                                          previous_month_data.get('expected_churn', 0.2)) * 100),
                                 key=f"churn_{st.session_state.current_month}") / 100
        
        # Показываем историю изменений
        if st.session_state.user_inputs_history:
            with st.expander("📈 История месяцев", expanded=False):
                for entry in sorted(st.session_state.user_inputs_history, key=lambda x: x['month']):
                    status = "✅" if entry['month'] == st.session_state.current_month else "📋"
                    st.write(f"{status} Месяц {entry['month']}: {entry['inputs']['current_customers']} клиентов, "
                           f"{entry['inputs']['current_mrr']:,.0f} ₽ MRR")
        
        return {
            'monthly_budget': monthly_budget,
            'team_size': team_size,
            'cash_balance': cash_balance,
            'monthly_price': monthly_price,
            'current_customers': current_customers,
            'current_mrr': current_mrr,
            'target_cac': target_cac,
            'expected_churn': expected_churn,
            'current_month': st.session_state.current_month
        }

def render_main_dashboard(user_inputs):
    """Главный дашборд с учетом истории"""
    
    st.header("📊 Pre-Seed Dashboard")
    
    # Показываем прогресс по месяцам
    if st.session_state.user_inputs_history:
        total_months = len(st.session_state.user_inputs_history)
        st.subheader(f"📈 Прогресс за {total_months} месяцев")
        
        # Создаем график прогресса
        history_data = []
        for entry in sorted(st.session_state.user_inputs_history, key=lambda x: x['month']):
            history_data.append({
                'Month': f"Месяц {entry['month']}",
                'Month_Num': entry['month'],
                'Customers': entry['inputs']['current_customers'],
                'MRR': entry['inputs']['current_mrr'],
                'Cash': entry['inputs']['cash_balance'],
                'Budget': entry['inputs']['monthly_budget']
            })
        
        history_df = pd.DataFrame(history_data)
        
        # Показываем ключевые метрики прогресса
        if len(history_df) > 1:
            first_month = history_df.iloc[0]
            last_month = history_df.iloc[-1]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_growth = last_month['Customers'] - first_month['Customers']
                st.metric("📈 Общий рост клиентов", 
                         f"{last_month['Customers']}",
                         delta=f"+{total_growth}")
            
            with col2:
                mrr_growth = last_month['MRR'] - first_month['MRR']
                st.metric("💰 Общий рост MRR", 
                         f"{last_month['MRR']:,.0f} ₽",
                         delta=f"+{mrr_growth:,.0f} ₽")
            
            with col3:
                avg_mrr_per_customer = last_month['MRR'] / last_month['Customers'] if last_month['Customers'] > 0 else 0
                st.metric("👤 Средний MRR на клиента", 
                         f"{avg_mrr_per_customer:,.0f} ₽")
            
            with col4:
                months_active = len(history_df)
                st.metric("⏱️ Активных месяцев", 
                         f"{months_active}")
        
        # Графики прогресса
        col1, col2 = st.columns(2)
        
        with col1:
            fig_customers = px.line(history_df, x='Month', y='Customers',
                                  title='📊 Рост клиентской базы по месяцам',
                                  markers=True)
            fig_customers.update_layout(xaxis_title='Месяц', yaxis_title='Количество клиентов')
            st.plotly_chart(fig_customers, use_container_width=True)
        
        with col2:
            fig_mrr = px.line(history_df, x='Month', y='MRR',
                            title='💰 Рост MRR по месяцам',
                            markers=True)
            fig_mrr.update_layout(xaxis_title='Месяц', yaxis_title='MRR (руб.)')
            st.plotly_chart(fig_mrr, use_container_width=True)
    
    # Проверяем, была ли нажата кнопка анализа для текущего месяца
    current_month_analyzed = any(
        entry['month'] == st.session_state.current_month 
        for entry in st.session_state.user_inputs_history
    )
    
    if not current_month_analyzed:
        st.info("""
        ## 🎯 Готов к анализу!
        
        **Заполните параметры для месяца {} и нажмите кнопку:**
        ### 🚀 "Запустить анализ"
        
        *Каждый месяц обновляйте данные чтобы видеть прогресс!*
        """.format(st.session_state.current_month))
        return
    
    # Показываем индикатор загрузки для текущего месяца
    with st.spinner("🤖 Проводим анализ метрик и строим прогнозы..."):
        # Расчет ключевых метрик
        metrics = services['stage_metrics'].get_metrics_for_stage('pre_seed', user_inputs)
        forecast = services['pre_seed_advisor'].generate_realistic_forecast(user_inputs)
    
    st.success(f"✅ Анализ для месяца {user_inputs['current_month']} завершен!")
    
    # Визуализация ключевых метрик текущего месяца
    st.subheader(f"📊 Метрики месяца {user_inputs['current_month']}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎯 Potential Customers", 
                 f"{forecast['phase_1_months_1_3']['target_customers']}",
                 "Months 1-3")
    
    with col2:
        cac_estimate = user_inputs['monthly_budget'] / max(forecast['phase_1_months_1_3']['target_customers'], 1)
        st.metric("💰 Estimated CAC", f"{cac_estimate:,.0f} ₽")
    
    with col3:
        burn_rate = user_inputs['monthly_budget'] + (user_inputs['team_size'] * 150000)
        st.metric("🔥 Monthly Burn", f"{burn_rate:,.0f} ₽")
    
    with col4:
        runway = services['runway_calc'].calculate_runway(burn_rate, user_inputs['cash_balance'])
        status_color = "🟢" if runway > 12 else "🟡" if runway > 6 else "🔴"
        st.metric("⏱️ Runway", f"{runway:.1f} месяцев", delta=status_color)
    
    # Рекомендации AI
    st.subheader("🤖 AI Рекомендации")
    
    with st.spinner("Генерируем персонализированные рекомендации..."):
        ai_analysis = services['ai_analyst'].analyze_pre_seed_situation(user_inputs, metrics)
    
    for i, recommendation in enumerate(ai_analysis.get('recommendations', []), 1):
        with st.expander(f"📌 Рекомендация {i}: {recommendation['title']}", expanded=i==1):
            st.write(recommendation['description'])
            if 'priority' in recommendation:
                st.progress(recommendation['priority'])
            
            if 'actions' in recommendation:
                st.write("**Конкретные действия:**")
                for action in recommendation['actions']:
                    st.write(f"• {action}")
    
    # Сравнение с предыдущим месяцем
    if len(st.session_state.user_inputs_history) > 1:
        st.subheader("📊 Сравнение с предыдущим месяцем")
        
        # Находим данные предыдущего месяца
        prev_month_data = None
        for entry in st.session_state.user_inputs_history:
            if entry['month'] == st.session_state.current_month - 1:
                prev_month_data = entry['inputs']
                break
        
        if prev_month_data:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                customer_growth = user_inputs['current_customers'] - prev_month_data['current_customers']
                growth_percent = (customer_growth / prev_month_data['current_customers'] * 100) if prev_month_data['current_customers'] > 0 else 0
                st.metric("👥 Рост клиентов", 
                         user_inputs['current_customers'],
                         delta=f"+{customer_growth} ({growth_percent:.1f}%)")
            
            with col2:
                mrr_growth = user_inputs['current_mrr'] - prev_month_data['current_mrr']
                mrr_growth_percent = (mrr_growth / prev_month_data['current_mrr'] * 100) if prev_month_data['current_mrr'] > 0 else 0
                st.metric("💰 Рост MRR", 
                         f"{user_inputs['current_mrr']:,.0f} ₽",
                         delta=f"+{mrr_growth:,.0f} ₽ ({mrr_growth_percent:.1f}%)")
            
            with col3:
                cash_change = user_inputs['cash_balance'] - prev_month_data['cash_balance']
                st.metric("🏦 Изменение кэша", 
                         f"{user_inputs['cash_balance']:,.0f} ₽",
                         delta=f"{cash_change:,.0f} ₽")

def render_cohort_analysis(user_inputs):
    """Страница когортного анализа с историей"""
    
    st.header("👥 Когортный анализ")
    
    # Показываем историю для когортного анализа
    if st.session_state.user_inputs_history:
        st.subheader("📈 Исторические данные по месяцам")
        history_data = []
        for entry in sorted(st.session_state.user_inputs_history, key=lambda x: x['month']):
            history_data.append({
                'Месяц': entry['month'],
                'Клиенты': entry['inputs']['current_customers'],
                'MRR': f"{entry['inputs']['current_mrr']:,.0f} ₽",
                'Бюджет': f"{entry['inputs']['monthly_budget']:,.0f} ₽",
                'CAC Цель': f"{entry['inputs']['target_cac']:,.0f} ₽"
            })
        
        history_df = pd.DataFrame(history_data)
        st.dataframe(history_df, use_container_width=True)
    
    # Проверяем, есть ли данные для текущего месяца
    current_month_analyzed = any(
        entry['month'] == st.session_state.current_month 
        for entry in st.session_state.user_inputs_history
    )
    
    if not current_month_analyzed:
        st.info("""
        ## 📊 Когортный анализ
        
        **Для доступа к когортному анализу:**
        1. Заполните параметры для текущего месяца
        2. Нажмите кнопку 🚀 **"Запустить анализ"**
        3. Вернитесь на эту вкладку
        
        *Анализ будет учитывать историю всех месяцев!*
        """)
        return
    
    if user_inputs['current_customers'] < 10:
        st.warning("""
        **📊 Когортный анализ будет доступен после 10+ клиентов**
        
        Сейчас мы можем показать только прогнозные данные на основе эталонных метрик B2B SaaS.
        """)
        
    else:
        # Реальный когортный анализ с учетом истории
        with st.spinner("Анализируем когорты с учетом исторических данных..."):
            cohort_data = services['cohort_analyzer'].generate_startup_cohorts(user_inputs)
        
        # Используем правильные ключи из возвращаемых данных
        st.subheader("📊 Кривая удержания")
        if 'retention_curve' in cohort_data:
            retention_curve = cohort_data['retention_curve']
            
            # Проверяем тип данных и преобразуем в DataFrame если нужно
            if isinstance(retention_curve, dict):
                # Если это словарь, создаем DataFrame
                retention_df = pd.DataFrame.from_dict(retention_curve, orient='index')
                retention_df.index.name = 'Cohort'
                st.dataframe(retention_df, use_container_width=True)
            elif hasattr(retention_curve, 'style'):
                # Если это уже DataFrame со стилем
                st.dataframe(retention_curve, use_container_width=True)
            else:
                # Просто отображаем как есть
                st.write(retention_curve)
        else:
            st.warning("Данные о кривой удержания недоступны")
        
        st.subheader("💰 Расчетный LTV")
        if 'estimated_ltv' in cohort_data:
            estimated_ltv = cohort_data['estimated_ltv']
            
            if isinstance(estimated_ltv, dict):
                # Преобразуем словарь в DataFrame для красивого отображения
                ltv_df = pd.DataFrame(list(estimated_ltv.items()), 
                                    columns=['Параметр', 'Значение'])
                st.dataframe(ltv_df, use_container_width=True)
            else:
                st.write(estimated_ltv)
        else:
            st.warning("Данные о LTV недоступны")

def render_goals_roadmap(user_inputs):
    """Страница целей и roadmap с прогрессом"""
    
    st.header("🎯 Цели и Roadmap")
    
    # Проверяем, есть ли данные для анализа
    if not st.session_state.user_inputs_history:
        st.info("""
        ## 🗓️ Планирование целей
        
        **Заполните данные для первого месяца и запустите анализ чтобы увидеть roadmap!**
        """)
        return
    
    # Показываем прогресс по месяцам
    st.subheader("📊 Ваш прогресс по месяцам")
    progress_data = []
    for entry in sorted(st.session_state.user_inputs_history, key=lambda x: x['month']):
        progress_data.append({
            'Месяц': entry['month'],
            'Клиенты': entry['inputs']['current_customers'],
            'MRR_тыс': entry['inputs']['current_mrr'] / 1000  # в тысячах
        })
    
    progress_df = pd.DataFrame(progress_data)
    fig_progress = px.line(progress_df, x='Месяц', y=['Клиенты', 'MRR_тыс'],
                         title='📈 Динамика достижения целей по месяцам',
                         labels={'value': 'Значение', 'variable': 'Метрика', 'MRR_тыс': 'MRR (тыс. ₽)'})
    st.plotly_chart(fig_progress, use_container_width=True)
    
    # Генерация плана на 1 год
    with st.spinner("Создаем дорожную карту..."):
        yearly_plan = services['roadmap'].generate_quarterly_plan(user_inputs)
    
    # Отображение по кварталам
    st.subheader("📅 Годовая дорожная карта")
    
    quarters = list(yearly_plan.keys())
    selected_quarter = st.selectbox("Выберите квартал:", quarters)
    
    if selected_quarter:
        quarter_data = yearly_plan[selected_quarter]
        
        st.subheader(f"📅 {selected_quarter.replace('_', ' ').title()}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🎯 Целевые метрики:**")
            for metric, target in quarter_data['metrics_targets'].items():
                st.write(f"• {metric}: {target}")
        
        with col2:
            st.write("**💰 Распределение бюджета:**")
            for category, percentage in quarter_data['budget_allocation'].items():
                st.write(f"• {category}: {percentage*100}%")
        
        st.write("**📋 Критические активности:**")
        for activity in quarter_data['critical_activities']:
            st.write(f"• {activity}")

def render_budget_runway(user_inputs):
    """Управление бюджетом и runway с историей"""
    
    st.header("💰 Управление бюджетом и Runway")
    
    # Проверяем, есть ли данные для анализа
    if not st.session_state.user_inputs_history:
        st.info("""
        ## 💸 Финансовый анализ
        
        **Заполните данные для первого месяца и запустите анализ!**
        """)
        return
    
    # Расчет текущих метрик
    burn_rate = user_inputs['monthly_budget'] + (user_inputs['team_size'] * 150000)
    runway = services['runway_calc'].calculate_runway(burn_rate, user_inputs['cash_balance'])
    
    st.subheader(f"💳 Финансовые метрики месяца {user_inputs['current_month']}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("💸 Monthly Burn", f"{burn_rate:,.0f} ₽")
    
    with col2:
        st.metric("🏦 Cash Balance", f"{user_inputs['cash_balance']:,.0f} ₽")
    
    with col3:
        status_color = "🟢" if runway > 12 else "🟡" if runway > 6 else "🔴"
        st.metric("⏱️ Runway", f"{runway:.1f} месяцев", delta=status_color)
    
    # Показываем финансовую историю
    st.subheader("📊 Финансовая история по месяцам")
    
    finance_data = []
    for entry in sorted(st.session_state.user_inputs_history, key=lambda x: x['month']):
        monthly_burn = entry['inputs']['monthly_budget'] + (entry['inputs']['team_size'] * 150000)
        monthly_runway = services['runway_calc'].calculate_runway(monthly_burn, entry['inputs']['cash_balance'])
        
        finance_data.append({
            'Месяц': entry['month'],
            'Бюджет': entry['inputs']['monthly_budget'],
            'Кэш': entry['inputs']['cash_balance'],
            'Runway': monthly_runway,
            'Burn Rate': monthly_burn
        })
    
    finance_df = pd.DataFrame(finance_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_budget = px.line(finance_df, x='Месяц', y='Бюджет',
                           title='💰 Динамика бюджета по месяцам',
                           markers=True)
        st.plotly_chart(fig_budget, use_container_width=True)
    
    with col2:
        fig_runway = px.line(finance_df, x='Месяц', y='Runway',
                           title='⏱️ Динамика Runway по месяцам',
                           markers=True)
        st.plotly_chart(fig_runway, use_container_width=True)

# Запуск приложения
if __name__ == "__main__":
    main()