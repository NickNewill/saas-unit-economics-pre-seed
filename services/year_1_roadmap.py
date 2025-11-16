from typing import Dict, Any

class Year1Roadmap:
    """Дорожная карта первого года для pre-seed B2B SaaS"""
    
    def generate_quarterly_plan(self, current_state: Dict) -> Dict:
        return {
            'q1_foundation': {
                'theme': 'Problem-Solution Fit & First Revenue',
                'metrics_targets': {
                    'customer_interviews': 50,
                    'product_iterations': 12,
                    'paying_customers': 3,
                    'activation_rate': 0.3,
                    'mrr': 15000
                },
                'budget_allocation': {
                    'product_development': 0.6,
                    'customer_acquisition': 0.3,
                    'operations': 0.1
                },
                'critical_activities': [
                    "✅ Определить ICP (Ideal Customer Profile)",
                    "✅ Создать MVP с 1-2 killer features", 
                    "✅ Найти 3 early adopters",
                    "✅ Установить базовые метрики",
                    "✅ Провести 50+ customer interviews"
                ]
            },
            'q2_validation': {
                'theme': 'Product-Market Fit & Process Building',
                'metrics_targets': {
                    'paying_customers': 10,
                    'mrr': 50000,
                    'net_revenue_retention': 1.0,
                    'cac': 20000,
                    'sales_cycle': 60  # дней
                },
                'budget_allocation': {
                    'product_development': 0.4,
                    'customer_acquisition': 0.5, 
                    'operations': 0.1
                },
                'critical_activities': [
                    "🔧 Оптимизировать onboarding процесс",
                    "🔧 Начать системный outbound",
                    "🔧 Измерить LTV первых клиентов",
                    "🔧 Построить sales funnel",
                    "🔧 Начать собирать NPS"
                ]
            },
            'q3_growth': {
                'theme': 'Repeatable Growth & Team Scaling', 
                'metrics_targets': {
                    'paying_customers': 25,
                    'mrr': 150000,
                    'ltv_cac_ratio': 2.0,
                    'gross_margin': 0.7,
                    'team_size': 5
                },
                'budget_allocation': {
                    'product_development': 0.3,
                    'customer_acquisition': 0.6,
                    'operations': 0.1
                },
                'critical_activities': [
                    "🚀 Масштабировать успешные каналы",
                    "🚀 Нанять первого sales менеджера", 
                    "🚀 Автоматизировать процессы",
                    "🚀 Запустить referral программу",
                    "🚀 Подготовить pitch deck"
                ]
            },
            'q4_preparation': {
                'theme': 'Scale Preparation & Fundraising',
                'metrics_targets': {
                    'paying_customers': 50,
                    'mrr': 300000,
                    'ltv_cac_ratio': 2.5,
                    'runway': 6,  # месяцев
                    'nps': 30
                },
                'budget_allocation': {
                    'product_development': 0.25,
                    'customer_acquisition': 0.65,
                    'operations': 0.1
                },
                'critical_activities': [
                    "📈 Подготовить финансовую модель",
                    "📈 Провести due diligence",
                    "📈 Увеличить runway до 12+ месяцев",
                    "📈 Начать общение с инвесторами",
                    "📈 Подготовить масштабирование команды"
                ]
            }
        }
    
    def generate_3_year_vision(self, year_1_results: Dict) -> Dict:
        """Видение на 3 года для B2B SaaS в России"""
        
        return {
            'year_2_scale': {
                'theme': 'Market Leadership & Team Building',
                'financial_targets': {
                    'arr': '5-10M ₽',
                    'customers': '100-200',
                    'team_size': '10-15',
                    'valuation': '50-100M ₽'
                },
                'operational_targets': {
                    'cac': '< 15,000 ₽',
                    'ltv_cac_ratio': '> 3.0', 
                    'net_revenue_retention': '> 110%',
                    'gross_margin': '> 75%'
                },
                'strategic_initiatives': [
                    "🏗️ Построить полноценную sales команду",
                    "🏗️ Развить partner ecosystem",
                    "🏗️ Войти в 1-2 новые вертикали",
                    "🏗️ Запустить enterprise offering"
                ]
            },
            'year_3_dominance': {
                'theme': 'Market Dominance & Internationalization', 
                'financial_targets': {
                    'arr': '15-25M ₽',
                    'customers': '300-500',
                    'team_size': '25-40', 
                    'valuation': '150-300M ₽'
                },
                'operational_targets': {
                    'cac': '< 12,000 ₽',
                    'ltv_cac_ratio': '> 3.5',
                    'net_revenue_retention': '> 120%',
                    'gross_margin': '> 80%'
                },
                'strategic_initiatives': [
                    "🌍 Начать экспансию в СНГ",
                    "🌍 Привлечь strategic investor",
                    "🌍 Запустить 2-3 смежных продукта",
                    "🌍 Построение brand authority"
                ]
            }
        }