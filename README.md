# Personal Expense Tracker (Web App)

## Overview

The Personal Expense Tracker is a web-based application built with Python and Streamlit to help users effectively manage and analyze their daily expenses. It features a clean, interactive user interface for adding new expenses, viewing a complete transaction summary, and visualizing spending habits with a dynamic pie chart.

All expense data is saved to a `expenses.csv` file, ensuring that your financial records are persistent and automatically loaded each time you use the app.



## Key Features

-   **Interactive Web Interface:** A modern and intuitive UI built with Streamlit, making it easy to track expenses.
-   **Add Expenses with Ease:** A simple form allows you to quickly add new expenses with an amount, category, and date.
-   **Dynamic Data Display:** View a clear, tabulated summary of all recorded expenses that updates in real-time.
-   **Data Persistence:** Automatically saves all transactions to `expenses.csv` and loads them on startup.
-   **Instant Spending Visualization:** Generates a pie chart to visually break down spending by category, helping you understand where your money is going.
-   **Clean Architecture:** Built with a professional, object-oriented design that cleanly separates the backend logic from the frontend UI.

## Technologies Used

-   **Python**
-   **Streamlit:** For building the interactive web user interface.
-   **Pandas:** For data manipulation and creating dataframes.
-   **Matplotlib:** For data visualization and generating the spending chart.

## Setup and Installation

To run this project locally, you need to have Python and the required libraries installed.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/expense-tracker.git](https://github.com/your-username/expense-tracker.git)
    cd expense-tracker
    ```

2.  **Install the required libraries:**
    ```bash
    pip install streamlit pandas matplotlib
    ```

## How to Run the Project

1.  **Navigate to the project directory** in your terminal.
2.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
3.  The application will open automatically in your web browser.

## Code Structure

-   **`app.py`**: The main Streamlit application file. It handles the entire user interface, including input forms, data display, and chart rendering by calling methods from the `ExpenseTracker` class.
-   **`expenseclass.py`**: Contains the core backend logic of the application within the `ExpenseTracker` class. This class is responsible for:
    -   Loading and saving expenses to `expenses.csv`.
    -   Adding new expense records.
    -   Providing the data summary and the visualization plot.
-   **`expenses.csv`**: The CSV file where all expense data is stored. This file is created automatically on the first run if it doesn't exist.
