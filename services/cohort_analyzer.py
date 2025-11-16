import pandas as pd
from typing import Dict, Any, List

class RealisticCohortAnalyzer:
    """Реалистичный когортный анализ для ранних стадий"""
    
    def generate_startup_cohorts(self, saas_data: Dict, real_data: pd.DataFrame = None) -> Dict:
        """Генерация реалистичных когорт с учетом stage"""
        
        if real_data is not None:
            return self._analyze_real_cohorts(real_data)
        else:
            return self._generate_realistic_projection(saas_data)
    
    def _generate_realistic_projection(self, saas_data: Dict) -> Dict:
        """Генерация реалистичной проекции для стартапа без данных"""
        
        # Основано на эталонных данных для SaaS стартапов
        base_retention = {
            'month_1': 0.75,  # 25% отток в первый месяц - норма для стартапа
            'month_3': 0.50,  # 50% удержание к 3 месяцу
            'month_6': 0.35,  # 35% к 6 месяцу
            'month_12': 0.25  # 25% долгосрочное удержание
        }
        
        # Адаптация под бизнес-модель
        if saas_data.get('business_model') == 'b2b_enterprise':
            base_retention = {k: v * 1.3 for k, v in base_retention.items()}
        elif saas_data.get('business_model') == 'b2c':
            base_retention = {k: v * 0.7 for k, v in base_retention.items()}
        
        return {
            'retention_curve': base_retention,
            'estimated_ltv': self._calculate_realistic_ltv(saas_data, base_retention),
            'growth_scenarios': self._generate_growth_scenarios(saas_data),
            'critical_insights': self._get_critical_insights(saas_data, base_retention)
        }
    
    def _calculate_realistic_ltv(self, saas_data: Dict, retention: Dict) -> float:
        """Реалистичный расчет LTV для стартапа"""
        arpu = saas_data.get('monthly_price', 5000)
        
        # Консервативный подход - учитываем только 12 месяцев
        total_months = 0
        for month, retention_rate in retention.items():
            month_num = int(month.split('_')[1])
            total_months += arpu * retention_rate
        
        return total_months * 0.7  # Дисконт 30% для рисков стартапа
    
    def _generate_growth_scenarios(self, saas_data: Dict) -> Dict:
        return {
            'optimistic': {
                'customers_6m': 50,
                'customers_12m': 150,
                'assumptions': 'Быстрое достижение PMF, низкий CAC'
            },
            'base': {
                'customers_6m': 25,
                'customers_12m': 75,
                'assumptions': 'Средние темпы роста, стабильный CAC'
            },
            'conservative': {
                'customers_6m': 10,
                'customers_12m': 30,
                'assumptions': 'Медленное достижение PMF, высокий CAC'
            }
        }
    
    def _get_critical_insights(self, saas_data: Dict, retention: Dict) -> List[str]:
        insights = [
            "Удержание в первый месяц критически важно для LTV",
            "Фокус на улучшении onboarding может значительно повысить удержание",
            "Ранние когорты могут показать заниженный LTV из-за итераций продукта"
        ]
        
        if retention['month_1'] < 0.7:
            insights.append("Низкое удержание в первый месяц - стоит пересмотреть onboarding")
        
        return insights