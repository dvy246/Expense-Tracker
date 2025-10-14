import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from expense_tracker import ExpenseTracker

# Page Configuration
st.set_page_config(
    page_title="Expense Tracker Pro",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for aesthetic design
st.markdown("""
    <style>
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Card styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    
    /* Custom title */
    .custom-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(120deg, #ffffff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 20px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Metric styling */
    .stMetric {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 15px;
        border-radius: 10px;
        color: white;
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 30px;
        font-weight: 600;
        transition: transform 0.2s;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Form styling */
    .stForm {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95);
    }
    
    /* Success/Error messages */
    .stSuccess, .stError {
        border-radius: 10px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize expense tracker
if 'tracker' not in st.session_state:
    st.session_state.tracker = ExpenseTracker()

# Title
st.markdown('<h1 class="custom-title">💰 Expense Tracker Pro</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎨 Dashboard Controls")
    st.markdown("---")
    
    # Date range filter
    st.markdown("#### 📅 Filter by Date")
    date_filter = st.radio(
        "Select Period",
        ["All Time", "This Month", "Last 30 Days", "Last 7 Days", "Custom Range"],
        label_visibility="collapsed"
    )
    
    if date_filter == "Custom Range":
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("From", datetime.now() - timedelta(days=30))
        with col2:
            end_date = st.date_input("To", datetime.now())
    
    st.markdown("---")
    
    # Category filter
    st.markdown("#### 🏷️ Filter by Category")
    df_all = st.session_state.tracker.get_expenses()
    if not df_all.empty:
        categories = ['All Categories'] + sorted(df_all['Category'].unique().tolist())
        selected_category = st.selectbox("Category", categories, label_visibility="collapsed")
    else:
        selected_category = 'All Categories'
    
    st.markdown("---")
    
    # Quick stats
    total = st.session_state.tracker.get_total()
    st.markdown("#### 📊 Quick Stats")
    st.metric("Total Expenses", f"${total:,.2f}")
    
    if not df_all.empty:
        avg_expense = df_all['Amount'].mean()
        expense_count = len(df_all)
        st.metric("Average Expense", f"${avg_expense:,.2f}")
        st.metric("Total Transactions", f"{expense_count}")
    
    st.markdown("---")
    
    # Danger zone
    with st.expander("⚠️ Danger Zone", expanded=False):
        if st.button("🗑️ Clear All Data", type="secondary", use_container_width=True):
            if st.session_state.tracker.clear_all_expenses():
                st.success("All expenses cleared!")
                st.rerun()

# Main content area
tab1, tab2, tab3, tab4 = st.tabs(["📝 Add Expense", "📊 Dashboard", "📈 Analytics", "📋 All Expenses"])

# Tab 1: Add Expense
with tab1:
    st.markdown("### Add New Expense")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("add_expense_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            
            with col_a:
                description = st.text_input("📝 Description", placeholder="e.g., Grocery shopping")
                category = st.selectbox("🏷️ Category", ExpenseTracker.CATEGORIES)
            
            with col_b:
                amount = st.number_input("💵 Amount ($)", min_value=0.01, step=0.01, format="%.2f")
                date = st.date_input("📅 Date", value=datetime.now())
            
            submit_col1, submit_col2, submit_col3 = st.columns([1, 1, 1])
            with submit_col2:
                submitted = st.form_submit_button("➕ Add Expense", use_container_width=True)
            
            if submitted:
                if description and amount > 0:
                    if st.session_state.tracker.add_expense(
                        date.strftime('%Y-%m-%d'),
                        description,
                        category,
                        amount
                    ):
                        st.success(f"✅ Added: {description} - ${amount:.2f}")
                        st.rerun()
                    else:
                        st.error("❌ Failed to add expense")
                else:
                    st.warning("⚠️ Please fill in all fields")
    
    with col2:
        st.markdown("### 💡 Quick Tips")
        st.info("""
        - Be specific with descriptions
        - Choose the right category
        - Add expenses regularly
        - Review your spending weekly
        """)

# Tab 2: Dashboard
with tab2:
    df = st.session_state.tracker.get_expenses()
    
    if not df.empty:
        # Apply filters
        if date_filter == "This Month":
            df = df[df['Date'].dt.month == datetime.now().month]
        elif date_filter == "Last 30 Days":
            df = df[df['Date'] >= (datetime.now() - timedelta(days=30))]
        elif date_filter == "Last 7 Days":
            df = df[df['Date'] >= (datetime.now() - timedelta(days=7))]
        elif date_filter == "Custom Range":
            df = df[(df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)]
        
        if selected_category != 'All Categories':
            df = df[df['Category'] == selected_category]
        
        if not df.empty:
            # Top metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_spent = df['Amount'].sum()
                st.metric("💰 Total Spent", f"${total_spent:,.2f}")
            
            with col2:
                avg_expense = df['Amount'].mean()
                st.metric("📊 Average", f"${avg_expense:,.2f}")
            
            with col3:
                max_expense = df['Amount'].max()
                st.metric("📈 Highest", f"${max_expense:,.2f}")
            
            with col4:
                transaction_count = len(df)
                st.metric("🧾 Transactions", transaction_count)
            
            st.markdown("---")
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Spending by Category")
                category_totals = df.groupby('Category')['Amount'].sum().reset_index()
                fig = px.pie(
                    category_totals,
                    values='Amount',
                    names='Category',
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(
                    showlegend=False,
                    height=400,
                    margin=dict(t=0, b=0, l=0, r=0)
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 💳 Top Categories")
                top_categories = category_totals.nlargest(5, 'Amount')
                fig = px.bar(
                    top_categories,
                    x='Amount',
                    y='Category',
                    orientation='h',
                    color='Amount',
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(
                    showlegend=False,
                    height=400,
                    margin=dict(t=0, b=0, l=0, r=0),
                    xaxis_title="Amount ($)",
                    yaxis_title=""
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Recent transactions
            st.markdown("### 🕒 Recent Transactions")
            recent_df = df.sort_values('Date', ascending=False).head(5)
            recent_df['Date'] = recent_df['Date'].dt.strftime('%Y-%m-%d')
            recent_df['Amount'] = recent_df['Amount'].apply(lambda x: f"${x:,.2f}")
            st.dataframe(
                recent_df[['Date', 'Description', 'Category', 'Amount']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("📭 No expenses found for the selected filters")
    else:
        st.info("📝 No expenses yet. Add your first expense in the 'Add Expense' tab!")

# Tab 3: Analytics
with tab3:
    df = st.session_state.tracker.get_expenses()
    
    if not df.empty:
        st.markdown("### 📈 Spending Trends")
        
        # Daily spending trend
        daily_spending = df.groupby(df['Date'].dt.date)['Amount'].sum().reset_index()
        daily_spending.columns = ['Date', 'Amount']
        
        fig = px.line(
            daily_spending,
            x='Date',
            y='Amount',
            title='Daily Spending Trend',
            markers=True
        )
        fig.update_traces(line_color='#667eea', line_width=3)
        fig.update_layout(
            height=400,
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📅 Monthly Overview")
            df['Month'] = df['Date'].dt.to_period('M').astype(str)
            monthly = df.groupby('Month')['Amount'].sum().reset_index()
            
            fig = px.bar(
                monthly,
                x='Month',
                y='Amount',
                color='Amount',
                color_continuous_scale='Plasma'
            )
            fig.update_layout(
                height=400,
                showlegend=False,
                xaxis_title="Month",
                yaxis_title="Amount ($)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🏆 Category Breakdown")
            category_data = df.groupby('Category').agg({
                'Amount': ['sum', 'count', 'mean']
            }).round(2)
            category_data.columns = ['Total', 'Count', 'Average']
            category_data = category_data.sort_values('Total', ascending=False)
            category_data['Total'] = category_data['Total'].apply(lambda x: f"${x:,.2f}")
            category_data['Average'] = category_data['Average'].apply(lambda x: f"${x:,.2f}")
            st.dataframe(category_data, use_container_width=True)
        
        # Heatmap
        st.markdown("### 🗓️ Spending Heatmap")
        df['DayOfWeek'] = df['Date'].dt.day_name()
        df['Week'] = df['Date'].dt.isocalendar().week
        
        heatmap_data = df.groupby(['Week', 'DayOfWeek'])['Amount'].sum().reset_index()
        heatmap_pivot = heatmap_data.pivot(index='DayOfWeek', columns='Week', values='Amount')
        
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_pivot = heatmap_pivot.reindex(days_order)
        
        fig = px.imshow(
            heatmap_pivot,
            labels=dict(x="Week", y="Day", color="Amount ($)"),
            color_continuous_scale='RdYlGn_r',
            aspect='auto'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📊 Add some expenses to see analytics!")

# Tab 4: All Expenses
with tab4:
    df = st.session_state.tracker.get_expenses()
    
    if not df.empty:
        st.markdown("### 📋 All Expenses")
        
        # Search and filter
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            search = st.text_input("🔍 Search expenses", placeholder="Search by description...")
        with col2:
            sort_by = st.selectbox("Sort by", ["Date", "Amount", "Category", "Description"])
        with col3:
            sort_order = st.selectbox("Order", ["Descending", "Ascending"])
        
        # Apply search
        display_df = df.copy()
        if search:
            display_df = display_df[display_df['Description'].str.contains(search, case=False, na=False)]
        
        # Apply sorting
        ascending = sort_order == "Ascending"
        display_df = display_df.sort_values(by=sort_by, ascending=ascending)
        
        # Format for display
        display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
        display_df['Amount'] = display_df['Amount'].apply(lambda x: f"${x:,.2f}")
        
        # Display table
        st.dataframe(
            display_df[['Date', 'Description', 'Category', 'Amount']],
            use_container_width=True,
            hide_index=True,
            height=500
        )
        
        # Export options
        st.markdown("### 💾 Export Data")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"expenses_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.info("📭 No expenses to display. Start tracking your expenses!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: white; padding: 20px;'>
        <p>💰 Expense Tracker Pro | Track Smart, Save More</p>
    </div>
    """,
    unsafe_allow_html=True
)
