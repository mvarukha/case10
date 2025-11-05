from collections import defaultdict
from datetime import datetime, timedelta


def analyze_historical_spending(transactions: list) -> dict:
    """
    Analyze historical spending patterns.
    Args:
        transactions: List of transaction dictionaries
    Returns:
        Dictionary with spending analysis and recommendations
    """
    monthly_totals = defaultdict(list)
    for t in transactions:
        if t.get('amount', 0) >= 0: continue
        try:
            month = datetime.strptime(t['date'], "%Y-%m-%d").strftime("%Y-%m")
            monthly_totals[t.get('category', 'other')].append(abs(t['amount']))
        except:
            continue

    averages = {cat: round(sum(amounts) / len(amounts), 2)
                for cat, amounts in monthly_totals.items()}
    averages = dict(sorted(averages.items(), key=lambda x: x[1], reverse=True))

    total = sum(averages.values())
    top_categories = [
        {'category': cat, 'average_monthly': amt,
         'percentage_of_total': round(amt / total * 100, 2)}
        for cat, amt in list(averages.items())[:3]
    ]

    recommendations = [
        f"Lower expanses in {cat['category']} ({cat['percentage_of_total']}%)"
        for cat in top_categories if cat['percentage_of_total'] > 20
    ]

    return {
        'monthly_averages': averages,
        'top_spending_categories': top_categories,
        'recommendations': recommendations or ["Your expanses are balanced"]
    }


def create_budget_template(analysis: dict) -> dict:
    """
    Create budget template from spending analysis.
    Args:
        analysis: Historical spending analysis
    Returns:
        Budget template with category limits and savings goal
    """
    averages = analysis['monthly_averages']

    category_limits = {cat: round(amt * 0.9, 2) for cat, amt in averages.items()}
    total_expenses = sum(averages.values())
    estimated_income = round(total_expenses * 1.2, 2)
    planned_savings = round(estimated_income - sum(category_limits.values()), 2)

    return {
        'period': (datetime.now().replace(day=28) +
                   timedelta(days=4)).replace(day=1).strftime("%Y-%m"),
        'estimated_income': estimated_income,
        'category_limits': category_limits,
        'planned_savings': planned_savings
    }


def compare_budget_vs_actual(budget: dict, transactions: list) -> dict:
    """
    Compare budget with actual spending.
    Args:
        budget: Budget template
        transactions: Actual transactions
    Returns:
        Performance comparison results
    """
    # Calculate actual spending
    actual_spending = defaultdict(float)
    total_income = 0

    for t in transactions:
        amount = t.get('amount', 0)
        if amount > 0:
            total_income += amount
        else:
            category = t.get('category', 'other')
            actual_spending[category] += abs(amount)

    # Compare with budget
    total_cats = len(budget['category_limits'])
    within_budget = 0

    for category, budget_limit in budget['category_limits'].items():
        actual = actual_spending.get(category, 0)
        if actual > budget_limit:
            within_budget += 1

    performance_rate = round(within_budget / total_cats * 100, 2) if total_cats > 0 else 0
    actual_savings = total_income - sum(actual_spending.values())

    return {
        'performance_summary': {
            'performance_rate': performance_rate,
            'categories_within_budget': within_budget,
            'categories_over_budget': total_cats - within_budget,
            'total_categories_analyzed': total_cats
        },
        'savings_comparison': {
            'actual_savings': round(actual_savings, 2),
            'planned_savings': budget['planned_savings'],
            'savings_goal_met': actual_savings >= budget['planned_savings']
        }
    }