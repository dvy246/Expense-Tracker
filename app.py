import streamlit as st
import pandas as pd
from datetime import datetime
from expenseclass import Expense

# Configure the page
st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# Initialize session state for the expense tracker
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# Title
st.title("💰 Personal Expense Tracker")
st.markdown("---")

# Create two columns for better layout
col1, col2 = st.columns([1, 2])

with col1:
    # Add New Expense Section
    st.subheader("📝 Add New Expense")
    
    with st.form("expense_form"):
        # Amount input
        amount = st.number_input(
            "Amount ($)",
            min_value=0.01,
            step=0.01,
            format="%.2f"
        )
        
        # Category selection with predefined options plus custom input
        category_options = Expense.categories + ["Other"]
        selected_category = st.selectbox("Category", category_options)
        
        # If "Other" is selected, show text input for custom category
        if selected_category == "Other":
            custom_category = st.text_input("Enter custom category")
            final_category = custom_category if custom_category else "miscellaneous"
        else:
            final_category = selected_category
        
        # Date input
        expense_date = st.date_input(
            "Date",
            value=datetime.now().date()
        )
        
        # Expense name/description
        expense_name = st.text_input("Expense Description", placeholder="e.g., Lunch at restaurant")
        
        # Submit button
        submitted = st.form_submit_button("Add Expense", use_container_width=True)
        
        if submitted:
            if amount > 0 and expense_name and final_category:
                try:
                    # Create new expense object
                    new_expense = Expense(
                        name=expense_name,
                        category=final_category,
                        amount=amount,
                        date=expense_date.strftime('%Y-%m-%d')
                    )
                    
                    # Save to CSV
                    new_expense.save_to_csv('expenses.csv')
                    
                    # Add to session state for immediate display
                    st.session_state.expenses.append({
                        'Date': expense_date.strftime('%Y-%m-%d'),
                        'Expense': expense_name,
                        'Category': final_category,
                        'Amount': amount
                    })
                    
                    st.success(f"✅ Expense '{expense_name}' added successfully!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error adding expense: {str(e)}")
            else:
                st.error("❌ Please fill in all fields with valid values.")

with col2:
    # Load and display expenses
    st.subheader("📊 Expense Summary")
    
    try:
        # Try to load expenses from CSV
        if st.session_state.get('force_reload', True):
            try:
                df = pd.read_csv('expenses.csv', names=['Date', 'Expense', 'Category', 'Amount'], header=None)
                if not df.empty:
                    # Convert Date column to datetime for better sorting
                    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                    df = df.sort_values('Date', ascending=False)
                    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
                    
                    # Display the dataframe
                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Calculate and display totals
                    total_amount = df['Amount'].sum()
                    st.metric("Total Expenses", f"${total_amount:.2f}")
                    
                    # Category breakdown
                    category_totals = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
                    
                    st.subheader("💳 Spending by Category")
                    
                    # Display category breakdown as metrics
                    cols = st.columns(min(len(category_totals), 3))
                    for i, (category, amount) in enumerate(category_totals.head(3).items()):
                        with cols[i % 3]:
                            percentage = (amount / total_amount) * 100
                            st.metric(
                                category.title(),
                                f"${amount:.2f}",
                                f"{percentage:.1f}%"
                            )
                    
                    # Visualization section
                    st.subheader("📈 Spending Visualization")
                    
                    # Create tabs for different visualizations
                    tab1, tab2 = st.tabs(["Category Breakdown", "Monthly Trends"])
                    
                    with tab1:
                        if len(category_totals) > 0:
                            # Pie chart
                            fig, ax = plt.subplots(figsize=(10, 8))
                            colors = plt.cm.Set3(range(len(category_totals)))
                            wedges, texts, autotexts = ax.pie(
                                category_totals.values,
                                labels=category_totals.index,
                                autopct='%1.1f%%',
                                startangle=90,
                                colors=colors
                            )
                            ax.set_title('Spending by Category', fontsize=16, fontweight='bold')
                            
                            # Make percentage text more readable
                            for autotext in autotexts:
                                autotext.set_color('white')
                                autotext.set_fontweight('bold')
                            
                            st.pyplot(fig)
                        else:
                            st.info("No data available for category breakdown.")
                    
                    with tab2:
                        # Monthly trends
                        df_copy = df.copy()
                        df_copy['Date'] = pd.to_datetime(df_copy['Date'])
                        df_copy['Month'] = df_copy['Date'].dt.to_period('M')
                        monthly_spending = df_copy.groupby('Month')['Amount'].sum()
                        
                        if len(monthly_spending) > 0:
                            st.line_chart(monthly_spending)
                        else:
                            st.info("Not enough data for monthly trends.")
                    
                else:
                    st.info("📝 No expenses recorded yet. Add your first expense using the form on the left!")
                    
            except FileNotFoundError:
                st.info("📝 No expenses recorded yet. Add your first expense using the form on the left!")
            except Exception as e:
                st.error(f"❌ Error loading expenses: {str(e)}")
                
    except Exception as e:
        st.error(f"❌ Error in expense summary: {str(e)}")

# Sidebar with additional features
with st.sidebar:
    st.header("🛠️ Tools")
    
    # Display current total amount from class
    try:
        total_class_amount = Expense.view_totalamount()
        st.metric("Total from Class", f"${total_class_amount:.2f}")
    except:
        st.metric("Total from Class", "$0.00")
    
    # Available categories
    st.subheader("📋 Available Categories")
    for category in Expense.categories:
        st.write(f"• {category.title()}")
    
    # Clear all expenses button
    if st.button("🗑️ Clear All Expenses", type="secondary"):
        if st.session_state.get('confirm_clear', False):
            try:
                # Clear the CSV file
                with open('expenses.csv', 'w') as f:
                    pass
                # Reset class total
                Expense.total_amount = 0
                # Clear session state
                st.session_state.expenses = []
                st.success("✅ All expenses cleared!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error clearing expenses: {str(e)}")
        else:
            st.session_state.confirm_clear = True
            st.warning("⚠️ Click again to confirm deletion of all expenses.")
    
    if st.session_state.get('confirm_clear', False) and not st.button("🗑️ Clear All Expenses", type="secondary"):
        st.session_state.confirm_clear = False

# Import matplotlib for the visualization
import matplotlib.pyplot as plt
plt.style.use('default')