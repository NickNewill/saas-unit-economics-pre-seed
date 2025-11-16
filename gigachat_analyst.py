import requests
import os
from typing import Dict, Any

class SaaSUnitEconomicsAI:
    def __init__(self):
        self.api_key = os.getenv('GIGACHAT_API_KEY', '')
        self.base_url = "https://gigachat.devices.sberbank.ru/api/v1"
        self.access_token = None
    
    def analyze_pre_seed_situation(self, user_inputs: Dict, metrics: Dict) -> Dict:
        """Анализ ситуации pre-seed стартапа"""
        # Если API ключ не установлен, возвращаем демо-рекомендации
        if not self.api_key:
            return self._get_demo_recommendations(user_inputs, metrics)
        
        # Здесь будет реальная интеграция с GigaChat API
        # Пока возвращаем демо-данные
        return self._get_demo_recommendations(user_inputs, metrics)
    
    def _get_demo_recommendations(self, user_inputs: Dict, metrics: Dict) -> Dict:
        """Демо-рекомендации если GigaChat недоступен"""
        return {
            'recommendations': [
                {
                    'title': 'Фокус на первых клиентах',
                    'description': 'Сфокусируйтесь на привлечении 3-5 идеальных клиентов для валидации продукта',
                    'priority': 0.9,
                    'actions': [
                        'Проведите 30+ интервью с потенциальными клиентами',
                        'Определите четкий ICP (Ideal Customer Profile)',
                        'Предложите бесплатный trial для получения обратной связи'
                    ]
                },
                {
                    'title': 'Оптимизация бюджета',
                    'description': f'При текущем runway {user_inputs.get("runway", 0):.1f} месяцев важно оптимизировать расходы',
                    'priority': 0.7,
                    'actions': [
                        'Сфокусируйте маркетинговый бюджет на 1-2 каналах',
                        'Автоматизируйте процессы для экономии времени',
                        'Рассмотрите удаленный формат для сокращения расходов'
                    ]
                }
            ]
        }