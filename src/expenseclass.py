
from datetime import datetime
import pandas as pd
import csv
import os
import matplotlib.pyplot as plt
import seaborn as sns 
import sqlalchemy
from sqlalchemy import create_engine
import pyodbc


class Expense:
    categories=['capitalexpenditure',   #the already exisiting categories in the classs
                'work',
                'domestic',
                'personal',
                'miscellaneous']
    total_amount:float=0 #the total amount that is spent on the expense
    def __init__(self,name,category,amount,date):
        self.amount=amount
        self.name=name
        self.date=date
        
        if category in Expense.categories:        #to make sure the catgeories are in classs
                    self.category=category     
        else:
                 raise ValueError('invalid category')
        Expense.total_amount+=self.amount 
                
   
    @classmethod    
    def add_category(cls,new_cat:str):#to add the new category
            if new_cat in cls.categories:
                print("the category already exists")
            else:
                cls.categories.append(new_cat)
                print(f'the category {new_cat}  has been added sucessfully')
      
                
    def increase_expense_amount(self,filepath:str):
        while True:
                user=input("would u like to increase the amount for epense(yes or no)")
                if user=='yes':
                    try:
                        increase_by=input('enter the amount with which u wwant to increase ur amount by ')
                        if increase_by.isdigit():
                            increase_by=float(increase_by)
                        else:
                            print("write a number")
                            continue
                        if increase_by<0:
                            print("please enter a posiitve value")
                        else:
                           self.amount+=increase_by
                           Expense.total_amount+=increase_by
                           print(f'u increased the amount by {increase_by} and the new amount is {self.amount:.2f}')
                           self.update_in_csv(filepath)
                    except ValueError:
                        print("enter a vlid amount ")
                elif user=='no':
                    break
                else:
                    print("please answer with a yes or no ")
         
    
    def decrease_amount(self,filepath:str):
     while self.amount > 0: 
            decrease_ask = input("Do you want to decrease the amount? (yes or no): ").lower()
            
            if decrease_ask == 'no':
                print("No changes made.")
                break
            elif decrease_ask == 'yes':
                try:
                    decreasing_amount = float(input("By how much do you want to decrease the amount? "))
                    if decreasing_amount <= 0:
                        print("Please enter a positive value.")
                    elif decreasing_amount > self.amount:
                        print(f"Cannot decrease by {decreasing_amount}. Current amount is {self.amount:.2f}.")
                    else:
                        self.amount -= decreasing_amount
                        Expense.total_amount-=decreasing_amount
                        print(f"The amount has been decreased by {decreasing_amount}. New amount is {self.amount:.2f}.")
                        try:
                                self.update_in_csv(filepath)
                                print(f'the amount has decreased in the file {filepath}')
                        except Exception:
                            raise ('the file couldnt be updated')
                            
                        
                except ValueError:
                    print("Invalid input! Please enter a numeric value.")
            else:
                print("Please answer with 'yes' or 'no'.")
    
   
   
    
    def change_name(self,new_name,filepath:str) -> None:
        old_name=self.name
        self.name=new_name
        print(f'the new name of the expense is {self.name} and the old name is {old_name}')
        self.update_in_csv(filepath,old_name)
        
     
            
    def update_in_csv(self, filepath:str,old_name=None):
                        try:
                            df = pd.read_csv(filepath, names=['Date', 'Expense', 'Category', 'Amount'], header=None)   #loads the csv file 
                            name_to_match=old_name if old_name else self.name #check the name to locate the row
                            mask = (
                                (df['Expense'] == name_to_match) & 
                                (df['Category'] == self.category) & #locate the row using name catgeory and date
                                (df['Date'] == self.date)
                            )
                            if mask.any():
                                    df = df[~mask] #if any found it deletes the entire row
                            
                                    print(f'no matching expense found of the name {name_to_match}')
                                    updated_row=pd.DataFrame([[self.date, self.name, self.category, self.amount]],columns=['Date', 'Expense', 'Category', 'Amount']) #newdata frame containing 
                                                                                                                                                                    #the new output is made and then joined with the old data frame
                                    df=pd.concat([df,updated_row],ignore_index=True)
                                    df.to_csv(filepath,header=False,index=False) #the new ouptut is loaded into the csv
                        except Exception as e:
                            print(f"Error updating CSV: {e}")
     
    
    @classmethod
    def view_totalamount(cls):
            return cls.total_amount
        
        
    def save_to_csv(self,filepath:str):
            print(f"saving user expense {self.name} to the path {filepath}")
            try:
                with open(filepath, mode='a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([self.date, self.name, self.category, self.amount])
            except Exception as e:
                print(f"The exception occurred is {e}")
     
    @classmethod          
    def filtering_expense(cls,filepath:str):
        df=pd.read_csv(filepath,names=['Date', 'Expense', 'Category', 'Amount'], header=None)
        df['Date']=pd.to_datetime(df['Date'],errors='coerce')
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce') 
        df.dropna(subset=['Date','Amount'],inplace=True)
        df.sort_values(by='Date',inplace=True)
        filtered_df=df.copy()
        while True:
                filtering_ask=input('what do u want to filter the expense data by?:(expense,date,amount,category)')
                if filtering_ask=='date':
                    try:
                        while True:
                            start_date=pd.to_datetime(input("enter the starting date"),errors='coerce')
                            end_date=pd.to_datetime(input("enter the end date"),errors='coerce')
                            try:
                               if pd.isna(start_date) or pd.isna(end_date):
                                            print("Invalid date format. Please enter dates in YYYY-MM-DD format.")
                                            continue
                               else:
                                   break
                            except ValueError:
                                print("enter a valid date to filter")
            
                            filtered_df=filtered_df[(filtered_df['Date']>=start_date) & (filtered_df['Date']<=end_date)]
                            if filtered_df.empty:
                                print("no date available")
                            else:
                                return filtered_df
                    
                    except Exception as e:
                                   print(f'the exception is {e}')
                elif filtering_ask=='category':
                    
                    category_choose=input("write the category u want tot filter the data by").lower()
                    try:
                         if category_choose in filtered_df:
                             filtered_df[filtered_df['Category'].str.lower()==category_choose]
                             return filtered_df
                         if filtered_df.empty:
                             print("nothing in there")
                         else:
                            print('category not found in the file')     
                    except ValueError:
                        print("wrong way")     
                    except Exception as e:
                        raise Warning(f'the exception occured as{e} ')
                    
                elif filtering_ask=='expense':
                    expense_name=input("what expense u want to filter the data by? ").lower()
                    try:
                        if expense_name in filtered_df['Expense'].str.lower().values:
                            filtered_df=filtered_df[filtered_df['Expense'].str.lower()==expense_name]
                            return filtered_df
                        if filtered_df.empty:
                            print("no expense found")
                        else:
                            print("name does not exist in the data ")
                    except ValueError:
                        print("write the correct way")
                    except KeyError:
                        print("the expense column is not there in the file ")
                    
                    except Exception as e:
                        print(f'the exception occured is {e}')
                elif filtering_ask=='amount':
                    try:
                        min_amount=int(input("enter the minimum amount"))
                        max_amount=int(input('enter the maximum amount'))
                        filtered_df=filtered_df[(filtered_df['Amount']>=min_amount)&(filtered_df['Amount']<=max_amount)]
                        if filtered_df.empty:
                            print('no data is available')
                        else:
                            return filtered_df
                    except ValueError:
                        print("invalid input for amount")
                    
                    except Exception as e:
                        print(f"the eror occured is {e}")
                else:
                    print("Invalid filter option. Please choose from 'expense', 'date', 'amount', or 'category'.")
                    continue
                break
       
       
    @classmethod                              
    def summarize_expense(cls,filepath:str):
        print("summarizing expense")
        try:
            df=pd.read_csv(filepath,names=['Date', 'Expense', 'Category', 'Amount'],header=None,parse_dates=['Date'],dtype={'Expense': str, 'Category': str, 'Amount': float})
            df['Date']=pd.to_datetime(df['Date'],errors='coerce')
            df['Amount']=pd.to_numeric(df['Amount'],errors='coerce')
            df['Month']=df['Date'].dt.to_period('M').dt.strftime('%Y-%m').astype(str)
            print(f'the data types in ur df are {df.dtypes}')
            print("\nDate converted to period for monthly grouping:")
            print(df[['Date', 'Month']].head())
            df.dropna(subset=['Amount'],inplace=True)
            
            try:
                summary={'TOTAL AMOUNT':df['Amount'].sum(),
                        'TOTAL BY CATEGORY':df.groupby('Category')['Amount'].sum().to_dict(),
                        'TOTAL BY EXPENSE':df.groupby('Expense')['Amount'].sum().to_dict(),
                        'TOP 3 CATEGORIES':df.groupby('Category')['Amount'].sum().nlargest(3).to_dict(),
                        'TOP 3 EXPENSES':df.groupby("Expense")['Amount'].sum().nlargest(3).to_dict(),
                        'MONTHLY EXPENSES':df.groupby('Month')['Amount'].sum().to_dict()
                }
                try:
                        if not df.empty and df['Amount'].notnull().any():
                                                MOST_EXPENSIVE_EXPENSE = {
                                                    'NAME': df.loc[df['Amount'].idxmax(), 'Expense'],
                                                    'AMOUNT': df['Amount'].max(),
                                                    'CATEGORY': df.loc[df['Amount'].idxmax(), 'Category'],
                                                    'DATE': df.loc[df['Amount'].idxmax(), 'Date'].strftime('%Y-%m-%d')  # Fixed key
                                                }
                                                name, amnt, ct, dat = (
                                                    MOST_EXPENSIVE_EXPENSE['NAME'],
                                                    MOST_EXPENSIVE_EXPENSE['AMOUNT'],
                                                    MOST_EXPENSIVE_EXPENSE['CATEGORY'],
                                                    MOST_EXPENSIVE_EXPENSE['DATE']
                                                )
                        else:
                            MOST_EXPENSIVE_EXPENSE = {'NAME': None, 'AMOUNT': 0, 'CATEGORY': None, 'DATE': None}
                            name, amnt, ct, dat = None, 0, None, None
                            raise LookupError('theres no expense')
                except Exception as e:
                    print(f"the error is {e}")
            
            except Exception as e:
                print(f'this is the error {e}')
            while True:
                print('\n----SUMMARY OPTIONS-----')
                print('1. DISPLAY TOTAL AMOUNT SPENT')
                print('2  DISPLAY TOTAL BY EXPENSE')
                print("3  DISPLAY TOTAL BY CATEGORY ")
                print('4 TOP 3 CATEGORIES ')
                print('5 TOP 3 EXPENSES')
                print('6 MONTHLY SUMMARY ')
                print('7 THE MOST EXPENSIVE EXPENSE')
                print("8 EXIT")
                try:
                        choice=input('choose from (1-8)')
                        if choice=='1':
                            print(f"THE TOTAL AMOUNT SPENT IS {summary['TOTAL AMOUNT']:.2f}")
                        elif choice=='2':
                           for exp,amt in summary['TOTAL BY EXPENSE'].items():
                               print(f"{exp}: ${amt:.2f}")
                        elif choice=='3':
                            for cat,amont in summary['TOTAL BY CATEGORY'].items():
                                print(f"{cat}: ${amont:.2f}")
                        elif choice=='4':
                            for cat,amt in summary['TOP 3 CATEGORIES'].items():        
                                 print(f"{cat}:{amt:.2f}")
                        elif choice=='5':
                            for exp,amt in summary['TOP 3 EXPENSES'].items():
                                print(f"{exp} {amt:.2f}")                            
                        elif choice=='6':
                            for month,amount in summary['MONTHLY EXPENSES'].items():
                                print(f'{month}: ${amount:.2f}')
                        elif choice=='7':
                            if name:
                                print(f"The name of the expense is {name}, amount is {amnt}, category is {ct}, and date is {dat}")
                            else:
                                print("No expenses recorded to identify the most expensive one.")
                        elif choice=='8':
                            print("EXITING")
                            break
                        else:
                            print("please choose within the  options")
                            continue
                except Exception as e:
                    print(f'the error occcured:{e}')
            return summary
        
        except FileNotFoundError:
            print(f'the file {filepath} does not exists')
                                                        
        except Exception as e:
            print(f'the error occured is {e}')
        
    @classmethod   
    def visualize_expense(cls,filepath:str):
        try:
            df= df=pd.read_csv(filepath,names=['Date', 'Expense', 'Category', 'Amount'],header=None,parse_dates=['Date'])
            df['Date']=pd.to_datetime(df['Date'],errors='coerce')
            df['Amount']=pd.to_numeric(df['Amount'],errors='coerce')
            df.dropna(subset=['Amount'],inplace=True)
            while True:
                print("------viusalizing ur expenses-------")
                print("chooose the visualizing method")
                print('1 visualize monthly expenses')
                print('2 visualize daily expenses')
                print('3 visualize yearly expense')
                print('4 visualize expense by category')
                print('5 EXIT')
                option=input("choose from the  options(1-5)")
                if option=='1':
                    print("\nChoose Monthly Expense Visualization Type:")
                    print('1 Line Plot')
                    print('2 scatter plot')
                    print('3 Pie Chart')
                    monthly_expenses= df.groupby([df['Date'].dt.to_period('M').astype(str),'Expense'])['Amount'].sum().reset_index()
                    monthly_expenses.rename(columns={'Date': 'Month'}, inplace=True)
                    monthly_expenses.sort_values(by='Month',inplace=True)
                    plotting_options=input('by what u want to lot ur expenses by(1-3)')
                    plt.figure(figsize=(12,6))
                    try:
                        if plotting_options=='1':
                            plt.figure(figsize=(10,6))
                            sns.lineplot(data=monthly_expenses,color='blue',x='Month',y='Amount',hue='Expense',legend=True)
                            plt.title("MONTHLY EXPENSES")
                            plt.xticks(rotation=30)
                            plt.tight_layout()
                            plt.show()
                        elif plotting_options=='2':
                            sns.scatterplot(data=monthly_expenses,x='Month',y='Amount',color='red',hue='Expense',legend=True)
                            plt.title("scatter plot")
                            plt.tight_layout()
                            plt.show()
                            plt.grid(True)
                        elif plotting_options=='3':
                            monthly_expenses['Expense'] = monthly_expenses['Expense'].astype(str)
                            plt.pie(monthly_expenses['Amount'],labels=monthly_expenses['Expense'],autopct='%.1f%%',startangle=90,colors=sns.color_palette('coolwarm',len(monthly_expenses)))
                            plt.title('Monthly Expenses - pie chart')
                            plt.legend(True)
                            plt.tight_layout()
                            plt.show()
                        else:
                            print("invalid choice")
                     
                    except Exception as e:
                          print(f"the exception occured is {e}")
                   
                    
                elif option=='2':
                    print('VISUALIZING DAILY EXPENSES')
                    try:
                        daily_expenses=df.groupby([df['Date'].dt.date,'Expense'])['Amount'].sum().reset_index()
                        daily_expenses.sort_values(by='Date',inplace=True)
                        plt.figure(figsize=(12,6))
                        sns.lineplot(data=daily_expenses,x='Date',y='Amount',hue='Expense',legend=True)
                        plt.title("Daily Expenses")
                        plt.tight_layout()
                        plt.show()
                    except Exception as e:
                        print(f'the exception occured is {e}')
                        
                elif option=='3':
                        print("Visualizing yearly expenses")
                        try:
                                print('\n CHOOSE THE VISUALIZING OPTION')
                                print('1 line plot')
                                print('2 barplot')
                                print('3 histogram')
                                yearly_expense=df.groupby([df['Date'].dt.to_period('Y').astype(str),'Expense'])['Amount'].sum().reset_index()
                                yearly_expense.rename(columns={'Date':'year'},inplace=True)
                                yearly_expense.sort_values(by='year',inplace=True)
                                while True:
                                    vis_ask=input("choose the option to plot (1-3)")
                                    if not vis_ask.isdigit():
                                        print("enter a numberr")
                                        continue
                                    vis_ask=int(vis_ask)
                                    match vis_ask:
                                        case 1:
                                            plt.figure(figsize=(10,6))
                                            sns.lineplot(data=yearly_expense,x='year',y='Amount',legend=True,hue='Expense')
                                            plt.title("Yearly Expenses")
                                            plt.tight_layout()
                                            plt.xticks(rotation=30)
                                            plt.show()
                                        case 2:
                                            plt.figure(figsize=(10,6))
                                            sns.barplot(data=yearly_expense,x='year',y='Amount',legend=True,hue='Expense',palette='coolwarm')
                                            plt.title("Yearly Expenses")
                                            plt.tight_layout()
                                            plt.xticks()
                                            plt.show()
                                        case 3:
                                            plt.figure(figsize=(10,6))
                                            sns.histplot(data=yearly_expense,x='year',y='Amount',legend=True,hue='Expense',kde=True)
                                            plt.title("Yearly Expenses")
                                            plt.tight_layout()
                                            plt.xticks()
                                            plt.show()
                                        case other:
                                            print("enter in between(1-3)")
                                            continue
                                    break
                                            
                        except Exception as e:
                                 print(f"the exception occured is :{e}")
                                     
                elif option=='4':
                    try:
                        print('visualizing by category')
                        categorical=df.groupby('Category')['Amount'].sum().reset_index()
                        sns.barplot(data=categorical,x='Category',y='Amount',color='yellow')
                        plt.title("Expenses by Category")
                        plt.xlabel("Category")
                        plt.ylabel("Total Expense")
                        plt.tight_layout()
                        plt.show()
                    except Exception as e:
                          print(f"the exception occured is {e}")
                          
                elif option=='5':
                    print("ENDING VISUALIZING")
                    break
                    
                else:
                     print("invalid choice(1-5)")
                     continue
                    
        except FileNotFoundError:
            print(f"the file{filepath} cant be found")
            
            
        except Exception as e:
            print(f"the error occured:{e}")
        
        
    @classmethod   
    def export_expense(cls,filepath:str):
        df=pd.read_csv(filepath,names=['Date', 'Expense', 'Category', 'Amount'], header=None)
        print("\n--- EXPORT OPTIONS ---")
        print("1. Export Full Expense History")
        print("2. Export Filtered Expenses")
        print("3. Export Summary Report")
        print("4  Cancel Export")
        while True:
            try:
                export_option=input("choose the type of export u want to do (1-4)")
                if export_option.isdigit():
                    export_option=int(export_option)
                    if export_option==1:
                        exoort_format=input("choose the export form(csv/excel/sql)").lower()
                        path=input("put the  path where u want to save ur file (eg expense.csv) ")
                        try:
                            if exoort_format=='csv':
                                df.to_csv(path,index=False,mode='x',header=['Date', 'Expense', 'Category', 'Amount'])
                            elif exoort_format=='excel':
                                df.to_excel(path,index=False,sheet_name='ExpenseTRACKING',header=['Date', 'Expense', 'Category', 'Amount'])
                            elif exoort_format=='sql':
                                server=input('Enter Sql server instance name')
                                databse=input("enter than the name of the database")
                                table=input("enter the table name u want to export to ")
                                try:
                                    conn_str=(f'mssql+pyodbc://@{server}/{databse}?'
                                            'driver=ODBC+Driver+17+for+SQL+Server;'
                                            'Trusted_Connection=yes')
                                    engine=create_engine(conn_str)
                                    df.to_sql(name=table,if_exists='append',index=False,dtype={'DATE':sqlalchemy.types.DATE(),
                                                                                            'Expense':sqlalchemy.types.NVARCHAR(250),
                                                                                            'Category':sqlalchemy.types.NVARCHAR(100),
                                                                                            'Amount':sqlalchemy.types.Float()}
                                    )
                                    print(f"Successfully exported {len(df)} rows to {table} in {databse}")
                                except Exception as e:
                                    print(f"error occured while exporting the file in sql server{e}")
                            else:
                               break
                        except Exception as e:
                            print(f"the exception is {e}")   
                            
     

                    elif export_option==2:
                                filtered_df=cls.filtering_expense(filepath)
                                exoort_frmat=input("choose the export form(csv,excel,sql)").lower()
                                path=input("put the  path where u want to save ur file (eg expense.csv) ")
                                if exoort_frmat=='csv':
                                        filtered_df.to_csv(path,index=False,mode='x',header=['Date', 'Expense', 'Category', 'Amount'])
                                elif exoort_frmat=='excel':
                                    filtered_df.to_excel(path,sheet_name='filteredexpense',index=False,header=['Date', 'Expense', 'Category', 'Amount'])
                                elif exoort_frmat=='sql':
                                        server=input('Enter Sql server instance name')
                                        databse=input("enter than the name of the database")
                                        table=input("enter the table name u want to export to ")
                                try:
                                    conn_str=(f'mssql+pyodbc//@{server}/{databse}?'
                                        'driver=ODBC+Driver+17+for+SQL+Server;'
                                        'Trusted_Connrction=yes')
                                    engine=create_engine(conn_str)
                                    filtered_df.to_sql(name=table,if_exists='append',index=False,dtype={'DATE':sqlalchemy.types.DATE(),
                                                                                            'Expense':sqlalchemy.types.NVARCHAR(250),
                                                                                            'Category':sqlalchemy.types.NVARCHAR(100),
                                                                                            'Amount':sqlalchemy.types.Float()}
                                    )
                                    print(f"Successfully exported {len(filtered_df)} rows to {table} in {databse}")
                                    
                                except Exception as e:
                                                print(f"the error occures is{e} ")
                                else:
                                    break
                                            
                    elif export_option==3:
                        try: 
                            summary=cls.summarize_expense(filepath)
                            exoort_frmt=input("choose the export form(csv/excell)").lower()
                            path=input("put the  path where u want to save ur file (eg expense.csv) ")
                            summary_df=pd.DataFrame(summary,orient='indexx')
                            if exoort_frmt=='csv':
                                summary_df.to_csv(path,index=False,mode='x',header=['Date', 'Expense', 'Category', 'Amount'])
                            elif exoort_frmt=='excel':
                                summary_df.to_excel(path,index=False,sheet_name='summary',header=['Date', 'Expense', 'Category', 'Amount'])
                                
                        except Exception as g:
                            (f'the error occured is {g}')
                            
                    elif export_option==4:
                        print("Export Cancelled")
                        break
                    else:
                        print('please choose an option from 1-4')
                break
                        
            except Exception as e:
                print(f'the exception occured is {e}')
    
    
            
    def __repr__(self):
        return(f"the name of the expense is {self.name} and the catehory of the expense is {self.category} and the amount of the expense is {self.amount} and the date of the expense is {self.date}")

