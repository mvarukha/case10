from role1 import import_financial_data
from role2 import categorize_all_transactions, get_classification_stats
from role3 import calculate_basic_stats, calculate_by_category, analyze_by_time
from role4 import analyze_historical_spending, create_budget_template, compare_budget_vs_actual
from collections import defaultdict
from datetime import datetime, timedelta
import json


def main():
    """
    main function
    """
    print("FINANCIAL ANALYSIS AND BUDGET PLANNING\n")

    print("Import Financial Data\n")
    filename = input("Enter the name of the data file (CSV or JSON): ").strip()

    try:
        transactions = import_financial_data(filename)
        print(f"\nData successfully loaded")
    except Exception as e:
        print(f"Data upload error {e}")
        return

    if not transactions:
        print("No data available for analysis")
        return

    categorized_transactions = categorize_all_transactions(transactions)

    print("\nFinancial analysis")
    basic_stats = calculate_basic_stats(categorized_transactions)

    print(f"\nKey indicators:\n")
    print(f"   Income: {basic_stats['total_income']:,.2f} rub.")
    print(f"   Expenses: {basic_stats['total_expense']:,.2f} rub.")
    print(f"   Balance: {basic_stats['balance']:,.2f} rub.")
    print(f"   Total transactions: {basic_stats['transactions_count']}")

    print("\nCategorization of transactions\n")

    category_expenses = defaultdict(lambda: {'total': 0, 'count': 0})
    for transaction in categorized_transactions:
        if transaction.get('amount', 0) < 0:
            category = transaction.get('category', 'other')
            amount = abs(transaction['amount'])
            category_expenses[category]['total'] += amount
            category_expenses[category]['count'] += 1

    total_expenses = sum(data['total'] for data in category_expenses.values())

    income_by_category = defaultdict(float)
    expenses_by_category = defaultdict(float)

    for transaction in categorized_transactions:
        category = transaction.get('category', 'other')
        amount = transaction.get('amount', 0)

        if amount > 0:
            income_by_category[category] += amount
        else:
            expenses_by_category[category] += abs(amount)

    total_income = sum(income_by_category.values())
    total_expenses = sum(expenses_by_category.values())

    all_categories = set(income_by_category.keys()) | set(expenses_by_category.keys())

    print(f"{'Category':<25} {'Income':<15} {'Expenses':<15} {'Balance':<15}")
    print("-" * 70)

    for category in sorted(all_categories):
        income = income_by_category.get(category, 0)
        expenses = expenses_by_category.get(category, 0)
        balance = income - expenses

        print(f"{category:<15} {income:>12,.0f} rub. {expenses:>12,.0f} rub. "
              f"{balance:>12,.0f} rub.")

    print("-" * 70)
    print(
        f"{'Total':<15} {total_income:>12,.0f} rub. {total_expenses:>12,.0f}"
        f" rub. {total_income - total_expenses:>12,.0f} rub.")

    print(f"\nTotal expenses: {total_expenses:,.2f} rub.")
    print(f"Total expense categories: {len(category_expenses)}")

    print("\nBudget planning")
    spending_analysis = analyze_historical_spending(categorized_transactions)
    budget_template = create_budget_template(spending_analysis)
    budget_comparison = compare_budget_vs_actual(budget_template, categorized_transactions)
    performance = budget_comparison['performance_summary']
    savings = budget_comparison['savings_comparison']

    print(f"\nBudget execution results")
    print(f"   Success rate: {performance['performance_rate']}%")
    print(f"   Categories in the budget: {performance['total_categories_analyzed']}")
    print(f"   Did you meet the budget: {performance['categories_within_budget']}")
    print(f"   Exceeded the budget: {performance['categories_over_budget']}")

    print(f"\nSavings:")
    print(f"   Actual: {savings['actual_savings']:,.2f} rub.")
    print(f"   Planned: {savings['planned_savings']:,.2f} rub.")
    print(f"   Task: Try to reduce consumption of all categories by 10% -  "
          f"{'Achieved!' if savings['savings_goal_met'] else 'Not Achieved :('}")
    print(f"   Goal: {'Achieved!' if savings['savings_goal_met'] else 'Not Achieved :('}")

    # Рекомендации
    print(f"\nRecommendations:")
    for i, recommendation in enumerate(spending_analysis['recommendations'][:3], 1):
        print(f"   {i}. {recommendation}")


if __name__ == "__main__":
    main()