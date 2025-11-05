from collections import defaultdict
from datetime import datetime


def calculate_basic_stats(transactions: list) -> dict:
    """
    Calculates basic financial indicators:
      - total income (positive amounts)
      - total expenses (negative amounts)
      - balance
      - number of transactions
    """
    income = 0
    expense = 0
    for t in transactions:
        amount = t.get('amount', 0)
        if amount > 0:
            income += amount
        else:
            expense += abs(amount)
    balance = income - expense
    total_transactions = len(transactions)
    return {
        'total_income': round(income, 2),
        'total_expense': round(expense, 2),
        'balance': round(balance, 2),
        'transactions_count': total_transactions
    }


def calculate_by_category(transactions: list) -> dict:
    """
    Groups transactions by category and calculates:
      - total amount
      - number of transactions
      - percentage of total expenses
    """
    category_stats = defaultdict(lambda: {'total': 0, 'count': 0})
    total_expense = 0
    for t in transactions:
        category = t.get('category', 'other')
        amount = t.get('amount', 0)
        category_stats[category]['total'] += amount
        category_stats[category]['count'] += 1
        if amount < 0:
            total_expense += abs(amount)
    result = {}
    for category, data in category_stats.items():
        total = data['total']
        count = data['count']
        if total < 0 and total_expense > 0:
            percent = abs(total) / total_expense * 100
        else:
            percent = 0
        result[category] = {
            'total_amount': round(total, 2),
            'transactions_count': count,
            'expense_share_%': round(percent, 2)
        }

    def sort_by_amount(item) -> float:
        """Returns the total amount value for sorting categories."""
        return item[1]['total_amount']

    result = dict(sorted(result.items(), key=sort_by_amount))
    return result


def analyze_by_time(transactions: list) -> dict:
    """
    Analyzes transaction dynamics by month:
      - income
      - expenses
      - balance
      - top spending categories
    """
    monthly_stats = defaultdict(lambda: {
        'income': 0,
        'expense': 0,
        'top_categories': defaultdict(int)
    })
    for t in transactions:
        date_str = t.get('date')
        if not date_str:
            continue
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            continue
        month_key = date.strftime("%Y-%m")
        amount = t.get('amount', 0)
        category = t.get('category', 'other')
        if amount > 0:
            monthly_stats[month_key]['income'] += amount
        else:
            monthly_stats[month_key]['expense'] += abs(amount)
        monthly_stats[month_key]['top_categories'][category] += abs(amount)
    result = {}
    for month, data in monthly_stats.items():
        income = data['income']
        expense = data['expense']
        balance = income - expense

        def sort_by_value(item) -> float:
            """Returns the category total amount value for sorting."""
            return item[1]

        sorted_cats = sorted(
            data['top_categories'].items(),
            key=sort_by_value,
            reverse=True
        )
        top_categories = [c[0] for c in sorted_cats[:3]]
        result[month] = {
            'income': round(income, 2),
            'expense': round(expense, 2),
            'balance': round(balance, 2),
            'top_categories': top_categories
        }
    sorted_months = sorted(result.keys())
    final_result = {m: result[m] for m in sorted_months}
    return final_result