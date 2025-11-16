from typing import Dict, Any, List

class StartupMetricsTracker:
    """Трекер метрик для стартапов без автоматической аналитики"""
    
    def __init__(self):
        self.required_metrics = [
            'weekly_active_users',
            'new_signups', 
            'activated_users',
            'paying_conversions',
            'revenue',
            'customer_feedback'
        ]
    
    def get_weekly_input_template(self) -> Dict:
        """Шаблон для еженедельного ввода данных"""
        return {
            'week_start_date': 'YYYY-MM-DD',
            'user_metrics': {
                'new_signups': 0,
                'activated_users': 0,  # выполнили ключевое действие
                'active_users': 0,
                'churned_users': 0
            },
            'revenue_metrics': {
                'new_customers': 0,
                'mrr': 0,
                'arr': 0
            },
            'feedback_metrics': {
                'customer_interviews': 0,
                'nps_score': None,
                'feature_requests': []
            }
        }
    
    def calculate_pmf_score(self, weekly_data: List[Dict]) -> Dict:
        """Расчет Product-Market Fit score"""
        if len(weekly_data) < 4:
            return {"status": "need_more_data", "message": "Нужно 4+ недели данных"}
        
        # Упрощенный расчет PMF (в реальности используется опросник Sean Ellis)
        total_activated = sum(week['user_metrics']['activated_users'] for week in weekly_data)
        total_signups = sum(week['user_metrics']['new_signups'] for week in weekly_data)
        
        if total_signups == 0:
            return {"status": "no_data", "score": 0}
        
        activation_rate = total_activated / total_signups
        
        # Эмпирические пороги для PMF
        if activation_rate > 0.3:
            status = "strong_pmf"
            score = 80
        elif activation_rate > 0.2:
            status = "moderate_pmf" 
            score = 60
        else:
            status = "weak_pmf"
            score = 40
        
        return {
            "status": status,
            "score": score,
            "message": self._get_pmf_message(status)
        }
    
    def _get_pmf_message(self, status: str) -> str:
        messages = {
            "strong_pmf": "Отличные показатели! Продукт решает реальную проблему.",
            "moderate_pmf": "Есть прогресс, но нужно продолжать улучшать продукт.",
            "weak_pmf": "Требуются значительные улучшения продукта и понимания клиентов.",
            "need_more_data": "Соберите больше данных за 4+ недели.",
            "no_data": "Недостаточно данных для расчета."
        }
        return messages.get(status, "Неизвестный статус")