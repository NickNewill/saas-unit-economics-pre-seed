from typing import Dict, Any

class RunwayCalculator:
    def calculate_runway(self, monthly_burn: float, cash_balance: float) -> float:
        """Расчет runway (времени до окончания денег)"""
        if monthly_burn <= 0:
            return 0
        return cash_balance / monthly_burn
    
    def optimize_marketing_budget(self, inputs: Dict) -> Dict:
        """Оптимизация маркетингового бюджета"""
        monthly_budget = inputs.get('monthly_budget', 100000)
        cash_balance = inputs.get('cash_balance', 2000000)
        team_size = inputs.get('team_size', 3)
        
        burn_rate = monthly_budget + (team_size * 150000)
        runway = self.calculate_runway(burn_rate, cash_balance)
        
        if runway < 6:
            recommendation = "🚨 КРИТИЧЕСКИ: Увеличить runway до 6+ месяцев перед масштабированием"
            suggested_allocation = 0.2
        elif runway < 12:
            recommendation = "⚠️ ОСТОРОЖНО: Можно тестировать каналы, но сохранять осторожность"
            suggested_allocation = 0.3
        else:
            recommendation = "✅ СТАБИЛЬНО: Можно активно инвестировать в рост"
            suggested_allocation = 0.4
        
        return {
            'recommendation': recommendation,
            'suggested_marketing_budget': monthly_budget * suggested_allocation,
            'runway_months': runway,
            'allocation_breakdown': {
                'Content Marketing': 0.3,
                'Paid Acquisition': 0.4,
                'Sales Tools': 0.2,
                'Events & Partnerships': 0.1
            }
        }