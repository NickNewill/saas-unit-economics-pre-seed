from typing import Dict, Any

class StageAwareMetrics:
    """Метрики, адаптированные под стадию стартапа"""
    
    def get_metrics_for_stage(self, stage: str, saas_data: Dict) -> Dict:
        stages = {
            'pre_seed': self._pre_seed_metrics(saas_data),
            'seed': self._seed_metrics(saas_data), 
            'scale': self._scale_metrics(saas_data)
        }
        return stages.get(stage, self._pre_seed_metrics(saas_data))
    
    def _pre_seed_metrics(self, saas_data: Dict) -> Dict:
        """Метрики для стадии pre-seed (0-6 месяцев)"""
        return {
            'critical': [
                {'name': 'Product-Market Fit Score', 'target': '> 40%'},
                {'name': 'Weekly Active Users', 'target': '> 100'},
                {'name': 'Activation Rate', 'target': '> 30%'},
                {'name': 'User Retention W1', 'target': '> 25%'},
                {'name': 'Paying Conversion Rate', 'target': '> 3%'}
            ],
            'important': [
                {'name': 'CAC', 'target': '< 15,000 ₽'},
                {'name': 'MRR', 'target': '> 50,000 ₽'},
                {'name': 'Burn Rate', 'target': '< 500,000 ₽/мес'},
                {'name': 'Runway', 'target': '> 12 месяцев'}
            ]
        }
    
    def _seed_metrics(self, saas_data: Dict) -> Dict:
        """Метрики для стадии seed (6-24 месяца)"""
        return {
            'critical': [
                {'name': 'MRR Growth Rate', 'target': '> 15% в месяц'},
                {'name': 'Net Revenue Retention', 'target': '> 110%'},
                {'name': 'LTV/CAC Ratio', 'target': '> 3.0'},
                {'name': 'CAC Payback Period', 'target': '< 12 месяцев'},
                {'name': 'Churn Rate', 'target': '< 8%'}
            ]
        }
    
    def _scale_metrics(self, saas_data: Dict) -> Dict:
        """Метрики для стадии масштабирования (24+ месяцев)"""
        return {
            'critical': [
                {'name': 'Gross Margin', 'target': '> 80%'},
                {'name': 'Net Profit', 'target': '> 20%'},
                {'name': 'Enterprise Value/Revenue', 'target': '> 8x'},
                {'name': 'Rule of 40 Score', 'target': '> 40%'}
            ]
        }