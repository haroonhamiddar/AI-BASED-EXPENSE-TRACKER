import json
import os
from datetime import datetime

FILE_NAME = "expenses.json"


class ExpenseTracker:
    def __init__(self):
        self.expenses = self.load_expenses()

    def load_expenses(self):
        if os.path.exists(FILE_NAME):
            try:
                with open(FILE_NAME, "r") as file:
                    return json.load(file)
            except (json.JSONDecodeError, OSError):
                return []
        return []

    def save_expenses(self):
        with open(FILE_NAME, "w") as file:
            json.dump(self.expenses, file, indent=4)

    def add_expense(self):
        print("\n--- Add New Expense ---")

        title = input("Enter expense name: ").strip()
        if not title:
            print("Expense name cannot be empty!")
            return

        category = input(
            "Enter category (Food/Travel/Shopping/Bills/Other): "
        ).strip()

        if not category:
            category = "Other"

        try:
            amount = float(input("Enter amount (Rs): "))

            if amount <= 0:
                print("Amount must be greater than zero!")
                return

        except ValueError:
            print("Please enter a valid amount!")
            return

        date = input(
            "Enter date (YYYY-MM-DD) or press Enter for today: "
        ).strip()

        if date:
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                print("Invalid date! Please use YYYY-MM-DD.")
                return
        else:
            date = datetime.now().strftime("%Y-%m-%d")

        expense = {
            "title": title,
            "category": category,
            "amount": amount,
            "date": date
        }

        self.expenses.append(expense)
        self.save_expenses()

        print("Expense added successfully!")

    def view_expenses(self):
        print("\n--- All Expenses ---")

        if not self.expenses:
            print("No expenses recorded yet.")
            return

        print("-" * 75)
        print(f"{'No.':<5}{'Date':<15}{'Name':<20}"
              f"{'Category':<15}{'Amount (Rs)':>15}")
        print("-" * 75)

        for i, expense in enumerate(self.expenses, start=1):
            print(
                f"{i:<5}"
                f"{expense['date']:<15}"
                f"{expense['title'][:19]:<20}"
                f"{expense['category'][:14]:<15}"
                f"{expense['amount']:>15.2f}"
            )

        print("-" * 75)
        total = sum(e["amount"] for e in self.expenses)
        print(f"Total Expenses: Rs {total:.2f}")

    def total_expenses(self):
        total = sum(e["amount"] for e in self.expenses)
        print(f"\nTotal Expenses: Rs {total:.2f}")

    def monthly_expenses(self):
        month = input("Enter month (YYYY-MM): ").strip()

        try:
            datetime.strptime(month, "%Y-%m")
        except ValueError:
            print("Invalid month! Use YYYY-MM.")
            return

        monthly = [
            e for e in self.expenses
            if e["date"].startswith(month)
        ]

        if not monthly:
            print("No expenses found for this month.")
            return

        print(f"\n--- Expenses for {month} ---")

        for expense in monthly:
            print(
                f"{expense['date']} | "
                f"{expense['title']} | "
                f"{expense['category']} | "
                f"Rs {expense['amount']:.2f}"
            )

        total = sum(e["amount"] for e in monthly)
        print(f"\nMonthly Total: Rs {total:.2f}")

    def category_summary(self):
        print("\n--- Category-wise Summary ---")

        if not self.expenses:
            print("No expenses recorded yet.")
            return

        summary = {}

        for expense in self.expenses:
            category = expense["category"]
            summary[category] = (
                summary.get(category, 0) + expense["amount"]
            )

        for category, amount in sorted(summary.items()):
            print(f"{category}: Rs {amount:.2f}")

    def delete_expense(self):
        self.view_expenses()

        if not self.expenses:
            return

        try:
            number = int(input("\nEnter expense number to delete: "))

            if 1 <= number <= len(self.expenses):
                removed = self.expenses.pop(number - 1)
                self.save_expenses()
                print(f"Deleted expense: {removed['title']}")
            else:
                print("Invalid expense number!")

        except ValueError:
            print("Please enter a valid number!")

    def run(self):
        while True:
            print("\n" + "=" * 35)
            print("     PERSONAL EXPENSE TRACKER")
            print("=" * 35)
            print("1. Add Expense")
            print("2. View All Expenses")
            print("3. Calculate Total Expenses")
            print("4. View Monthly Expenses")
            print("5. Category-wise Summary")
            print("6. Delete Expense")
            print("7. Exit")

            choice = input("\nEnter your choice (1-7): ").strip()

            if choice == "1":
                self.add_expense()
            elif choice == "2":
                self.view_expenses()
            elif choice == "3":
                self.total_expenses()
            elif choice == "4":
                self.monthly_expenses()
            elif choice == "5":
                self.category_summary()
            elif choice == "6":
                self.delete_expense()
            elif choice == "7":
                print("Thank you for using Personal Expense Tracker!")
                break
            else:
                print("Invalid choice! Please select 1-7.")


if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.run()