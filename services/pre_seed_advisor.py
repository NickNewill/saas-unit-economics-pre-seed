from typing import Dict, Any
import pandas as pd

class PreSeedAdvisor:
    def generate_realistic_forecast(self, user_inputs: Dict) -> Dict:
        """Генерация реалистичного прогноза на основе введенных данных"""
        
        monthly_budget = user_inputs.get('monthly_budget', 100000)
        monthly_price = user_inputs.get('monthly_price', 5000)
        target_cac = user_inputs.get('target_cac', 15000)
        
        # Более сложные расчеты
        potential_customers = int(monthly_budget / target_cac)
        
        return {
            'phase_1_months_1_3': {
                'target_customers': max(3, int(potential_customers * 0.3)),
                'target_mrr': 15000,
                'key_activities': [
                    "🎯 Найти 3-5 'идеальных' первых клиентов",
                    "💬 Провести 30+ customer interviews",
                    "🔧 Выпускать продукт каждую неделю",
                    "📊 Измерять активацию и удержание"
                ]
            },
            'phase_2_months_4_6': {
                'target_customers': int(potential_customers * 0.7),
                'target_mrr': monthly_price * int(potential_customers * 0.7),
                'key_activities': [
                    "🔧 Оптимизировать onboarding процесс",
                    "📈 Начать системный outbound",
                    "💰 Измерить LTV первых клиентов"
                ]
            }
        }