# Personal Expense Tracker

## Overview

The Personal Expense Tracker is a Python-based application designed to help users manage and analyze their daily expenses. It provides a simple, command-line-style interface within a Jupyter Notebook to add new expenses, view a summary of all transactions, and visualize spending habits with a pie chart.

All expense data is saved to a `expenses.csv` file, ensuring that your financial records are persistent across sessions.

## Key Features

- **Add Expenses:** Easily add new expenses with details such as amount, category, and date.
- **View Summaries:** Get a clear, tabulated summary of all recorded expenses.
- **Data Persistence:** Automatically saves all transactions to a `expenses.csv` file and loads them on startup.
- **Spending Visualization:** Generates a pie chart to visually break down spending by category, helping you understand where your money is going.
- **Object-Oriented Design:** Built with a clean, object-oriented structure that separates the core logic from the user interface.

## Technologies Used

- **Python**
- **Pandas:** For data manipulation and creating dataframes.
- **Matplotlib:** For data visualization and generating the spending chart.
- **Jupyter Notebook:** As the primary user interface for the application.

## Setup and Installation

To run this project, you need to have Python and the required libraries installed.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/expense-tracker.git](https://github.com/your-username/expense-tracker.git)
    cd expense-tracker
    ```

2.  **Install the required libraries:**
    ```bash
    pip install pandas matplotlib notebook
    ```

## How to Run the Project

1.  **Navigate to the project directory** in your terminal.
2.  **Start Jupyter Notebook:**
    ```bash
    jupyter notebook
    ```
3.  From the Jupyter interface in your browser, open the `EXPENSE TRACKER PROJECT.ipynb` file.
4.  Run the cells in the notebook to start the expense tracker application.

## Usage

Once the notebook is running, you will be presented with a menu of options:

1.  **Add a new expense:** Enter the amount, category (e.g., "Food", "Transport", "Entertainment"), and date for your expense.
2.  **View all expenses:** Displays a detailed list of all your past transactions in a clean table.
3.  **Show spending by category:** Generates and displays a pie chart illustrating the proportion of your spending for each category.
4.  **Exit:** Closes the application.

## Code Structure

-   **`EXPENSE TRACKER PROJECT.ipynb`**: The main Jupyter Notebook that serves as the user interface. It handles user input, displays menus, and calls methods from the `ExpenseTracker` class.
-   **`expenseclass.py`**: Contains the core logic of the application within the `ExpenseTracker` class. This class is responsible for:
    -   Initializing the tracker.
    -   Loading and saving expenses to `expenses.csv`.
    -   Adding new expenses.
    -   Generating summary tables and visualizations.
-   **`expenses.csv`**: The CSV file where all expense data is stored. This file is created automatically on the first run.
