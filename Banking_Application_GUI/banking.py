import datetime
import re
import uuid
from tkinter import *
from tkinter import messagebox, ttk
import customtkinter
import pandas as pd
import psycopg2
import pyperclip
from sqlalchemy import create_engine
from tkcalendar import *
from PIL import Image

# This disables the warning "SettingWithCopyWarning":
pd.options.mode.chained_assignment = None

window = customtkinter.CTk()

customtkinter.set_appearance_mode("Dark")

customtkinter.set_default_color_theme("blue")

window.title('HBANK')

window.geometry("1300x900")


# The code block from 30 until 35 catches the error that the command button to create a branch is throwing:
def show_error(*args):
    error_message = "Field must not be empty and/or must be in the right format"
    messagebox.showerror('Data Error', error_message)


window.report_callback_exception = show_error

widgets_list = []

frames_list = []

# Initiating empty lists to create the branches and customers database:
customer_data = []
branch_data = []

# Establishing the connection to the Database:
conn = psycopg2.connect(host='127.0.0.1',
                        port=******,
                        database='postgres',
                        user='postgres',
                        password='**************',
                        connect_timeout=3)

# Creating the engine that will be responsible to execute sql queries in the Database:
engine = create_engine('postgresql://postgres:************@127.0.0.1:*******/postgres')


def update_database(dataframe, table):
    # Writing the dataframe into the database:
    dataframe.to_sql(name=table, con=engine, schema='banking_app', index=False, if_exists='replace')

    # Committing the changes in the database:
    conn.commit()


def update_trans_database(dataframe, table):
    # Writing the dataframe into the database:
    dataframe.to_sql(name=table, con=engine, schema='banking_app', index=False, if_exists='append')

    # Committing the changes in the database:
    conn.commit()


def login():
    # Fetching credentials from dataframe:
    # cred_df = pd.read_csv(
    # 'C:\\Users\\cesar\\OneDrive\\Documents\\Cesar documents\\Programing Projects\\Bank Application '
    # 'in Python\\Data\\Sign_In_Doc.csv')
    cred_df = pd.read_csv('Sign_In_Doc.csv')

    for i in range(len(cred_df)):
        if (username_entry.get().casefold() == cred_df.iloc[i]['Username'].casefold()) and (
                password_entry.get() == cred_df.iloc[i]['Password']):

            # Forget the first frame in the list of frames:
            list_frames_forget = list(frames_list)[0]
            list_frames_forget.forget()
            options_menu_frame(window, "grey")
        else:
            messagebox.showerror("Login Error", "Login Failed. Please try another username or password")


def create_login_frame(parent, color):
    global frame1
    frame1 = customtkinter.CTkFrame(parent, fg_color=color, corner_radius=0, border_width=1, border_color="grey")
    frame1.pack(fill=BOTH, expand=True)

    frames_list.append(frame1)

    title_label = customtkinter.CTkLabel(frame1, text="HBANK Banking System", font=("Ariel", 25, "bold"),
                                         text_color="black")
    title_label.pack(pady=90)

    username_label = customtkinter.CTkLabel(frame1, text="Username", text_color="black")
    username_label.pack(padx=(0, 75), pady=(100, 0), anchor=customtkinter.CENTER)

    global username_entry
    username_entry = customtkinter.CTkEntry(frame1, placeholder_text="Enter username")
    username_entry.pack()

    password_label = customtkinter.CTkLabel(frame1, text="Password", text_color="black")
    password_label.pack(padx=(0, 75), anchor=customtkinter.CENTER)

    global password_entry
    password_entry = customtkinter.CTkEntry(frame1, placeholder_text="Enter password", show="*")
    password_entry.pack()

    login_button = customtkinter.CTkButton(frame1, text="Login", command=login)
    login_button.pack(pady=20)


def reset():
    for widget in frame3.winfo_children():
        widget.destroy()

    # Embedding an image to frame3 background:
    image = customtkinter.CTkImage(light_image=Image.open('Picture10.jpg'),
                                   size=(300, 300))
    frame3_image_label = customtkinter.CTkLabel(frame3, image=image, text="")
    frame3_image_label.pack(fill="both", expand=True)


def options_menu_frame(parent, color):
    global frame2
    frame2 = customtkinter.CTkFrame(parent, fg_color=color, corner_radius=0, border_width=1, border_color="black")
    frame2.pack(side=LEFT, fill="y", ipadx=100)

    frames_list.append(frame2)

    frame2_label = customtkinter.CTkLabel(frame2, text="Options Menu", font=("Ariel", 18, "bold"), text_color="black")
    frame2_label.pack(pady=40)

    add_branch_button = customtkinter.CTkButton(frame2, text="Add New Branch", width=200, command=create_branch_widgets)
    add_branch_button.pack(pady=10)

    add_customer_button = customtkinter.CTkButton(frame2, text="Add New Customer", width=200,
                                                  command=create_customer_widgets)
    add_customer_button.pack(pady=10)

    make_deposit_button = customtkinter.CTkButton(frame2, text="Make a Deposit", width=200,
                                                  command=create_deposit_widgets)
    make_deposit_button.pack(pady=10)

    make_withdrawal_button = customtkinter.CTkButton(frame2, text="Make a Withdrawal", width=200,
                                                     command=create_withdrawal_widgets)
    make_withdrawal_button.pack(pady=10)

    print_balance_button = customtkinter.CTkButton(frame2, text="Print Customer Balance", width=200,
                                                   command=create_print_balance_widgets)
    print_balance_button.pack(pady=10)

    print_statement_button = customtkinter.CTkButton(frame2, text="Print Customer Statement", width=200,
                                                     command=create_print_statement_widgets)
    print_statement_button.pack(pady=10)

    edit_branch = customtkinter.CTkButton(frame2, text="Edit Branch Data", width=200,
                                          command=create_edit_branch_widgets)
    edit_branch.pack(pady=10)

    edit_customer = customtkinter.CTkButton(frame2, text="Edit Customer Data", width=200,
                                            command=create_edit_customer_widgets)
    edit_customer.pack(pady=10)

    remove_branch = customtkinter.CTkButton(frame2, text="Remove Branch", width=200,
                                            command=create_remove_branch_widgets)
    remove_branch.pack(pady=10)

    remove_customer = customtkinter.CTkButton(frame2, text="Remove Customer", width=200,
                                              command=create_remove_customer_widgets)
    remove_customer.pack(pady=10)

    close_program = customtkinter.CTkButton(frame2, text="Close", fg_color="blue", text_color="white", width=75,
                                            font=("Ariel", 14, "bold"),
                                            command=lambda: window.destroy())
    close_program.pack(side="left", pady=(0, 200), padx=(215, 10))

    reset_program = customtkinter.CTkButton(frame2, text="Reset", fg_color="blue", text_color="white", width=75,
                                            font=("Ariel", 14, "bold"),
                                            command=reset)
    reset_program.pack(side="left", pady=(0, 200), padx=(20, 80))

    global frame3
    frame3 = customtkinter.CTkFrame(parent, fg_color="silver", corner_radius=0, border_width=1,
                                    border_color="black")
    frame3.pack(side=LEFT, fill="y", ipadx=1000)

    frames_list.append(frame3)

    # Embedding an image to frame3 background:
    image = customtkinter.CTkImage(light_image=Image.open('Picture10.jpg'),
                                   size=(300, 300))
    frame3_image_label = customtkinter.CTkLabel(frame3, image=image, text="")
    frame3_image_label.pack(fill="both", expand=True)


def create_treeview(dataframe):
    # Creating a horizontal scrollbar for the Treeview:
    # 1. Create the scrollbar object:
    # horizontal_scrollbar = customtkinter.CTkScrollbar(frame3, orientation="horizontal", command=df_treeview.xview)
    horizontal_scrollbar = customtkinter.CTkScrollbar(frame3, orientation="horizontal", width=20)
    # 2. Pack the scrollbar:
    horizontal_scrollbar.pack(side="bottom", fill="x")
    
    # Create the treeview:
    df_treeview = ttk.Treeview(frame3, height=50)
    df_treeview.pack(pady=(50, 0), anchor=customtkinter.S, fill="x")

    # 3. Then, configure the Treeview to use the scrollbar:
    horizontal_scrollbar.configure(command=df_treeview.xview)

    # Create the stype of the treeview:
    tree_style = ttk.Style()
    tree_style.theme_use("clam")
    tree_style.configure("Treeview",
                         background="white",
                         fieldbackground="white",
                         bordercolor="black",
                         rowheight=25,
                         font=('Ariel', 14))
    tree_style.configure("Treeview.Heading", font=('Ariel', 14, "bold"), background="lightblue")

    # Create the headers:
    df_treeview['column'] = list(dataframe.columns)
    df_treeview['show'] = 'headings'

    # Show the headers:
    for header in df_treeview['column']:
        df_treeview.heading(header, text=header)

    # Converting the Telephone column to bigint if it exists in the dataframe:
    list_of_columns = []
    for col_name in dataframe.loc[:]:
        list_of_columns.append(col_name)
    if 'Telephone' in list_of_columns:
        dataframe['Telephone'] = dataframe['Telephone'].astype('int64')

    # Populate the treeview with data:
    df_treeview_rows = dataframe.to_numpy().tolist()
    for row in df_treeview_rows:
        df_treeview.insert("", "end", values=row)

    # The following code until the end of the create_treeview function, makes it possible to copy selected cells from
    # the Treeview:
    def copy_from_treeview(event):
        # Get the selected item (row)
        selected_item = df_treeview.selection()[0]

        # Get the column where the user clicked
        col = df_treeview.identify_column(event.x)

        # Get the value of the selected cell
        cell_value = df_treeview.item(selected_item, option='values')[int(col[1:]) - 1]

        # Copy the cell data to the clipboard
        pyperclip.copy(cell_value)

    # Bind the Control-Key-c event to the tree:
    df_treeview.bind('<Control-Key-c>', copy_from_treeview)


def create_branch_data(branch_name, branch_country, branch_address, branch_key):
    # Initializing a dictionary of branches, that will hold branch key as key and a list of data as value:
    dict_of_branches = {}

    # Reading the branch dataframe into a csv:
    # branch_csv_to_df = pd.read_csv('C:\\Users\\cesar\\OneDrive\\Documents\\Cesar documents\\Programing '
    # 'Projects\\Bank Application in Python\\Data\\Branch_Data.csv')
    branch_csv_to_df = pd.read_csv('Branch_Data.csv')

    # Match the branch name to a regex to make sure it does not contain digits:
    pattern_to_match = re.compile('^\D\D\D')
    matched_pattern = re.match(pattern_to_match, branch_name)

    if len(branch_name) != 3 or matched_pattern is None:
        messagebox.showerror("Data Error", "Number of characters for the branch name must be 3 and/or should not "
                                           "contain digits")

    elif branch_name == "" or branch_country == "" or branch_address == "" or branch_key == "":
        messagebox.showerror("Data Error", "Fields can not be empty")

    elif assert_branch_data(branch_csv_to_df, "Branch_name", branch_name):
        messagebox.showerror("Data Error", "Branch name already exists, please enter another")

    elif assert_branch_data(branch_csv_to_df, "Branch_address", branch_address):
        messagebox.showerror("Data Error", "Branch address already exists, please enter another")

    elif branch_key in branch_csv_to_df['Branch_key'].values:
        messagebox.showerror("Data Error", "Key already exists, please try again")

    elif branch_key <= 0:
        messagebox.showerror("Data Error", "Key must not be null or a negative number")

    else:
        # Calling the add_branch function and passing the required arguments to create the branch:
        Bank.add_branch(dict_of_branches, branch_name, branch_country, branch_address, branch_key)


def assert_branch_data(branch_df, column_name, br_data):
    # Check if the entered branch data exist in the dataframe ignoring the case-sensitive:
    for item in branch_df[column_name]:
        # Stripping both strings for comparison:
        if (br_data.replace(',', '').replace(' ', '').casefold() in item.replace(',', '').replace(' ', '').casefold()
                or br_data in item):
            return True
    return False


def create_customer_data(optionmenu_choice, customer_name, customer_dob, customer_address, customer_tele,
                         customer_init_trans):
    # Initializing a dictionary of customers, that will hold customer key as key and a list of data as value:
    dict_of_customers = {}

    # Creating a branch_key object that holds the optionmenu_choice:
    branch_key = optionmenu_choice

    # Reading the customer dataframe into a csv:
    customer_csv_to_df = pd.read_csv('Customer_Data.csv')

    if optionmenu_choice == "":
        messagebox.showerror("Data Error", "Branch must not be empty")

    elif customer_name == "":
        messagebox.showerror("Data Error", "Name must not be empty")

    elif customer_address == "":
        messagebox.showerror("Data Error", "Address must not be empty")

    elif customer_tele == "" or len(str(customer_tele)) < 10 or len(str(customer_tele)) > 13:
        messagebox.showerror("Data Error", "Telephone must not be empty and must be less than 10 digits or "
                                           "greater than 13 digits")

    # Assert the customer data to add the telephone number according to the condition - different customers can not
    # have same phone number:
    elif assert_create_customer_data(customer_csv_to_df, customer_name, customer_dob, customer_address, customer_tele):
        messagebox.showerror("Data Error", "Telephone number already exists")

    elif customer_init_trans <= 0.0:
        messagebox.showerror("Data Error", "Balance must be greater than 0")

    else:
        # Calling the add_customer function and passing the required arguments to create the customer:
        Branch.add_customer(branch_key, customer_name, customer_dob, customer_address, customer_tele,
                            customer_init_trans, dict_of_customers)


def assert_edit_customer_data(customer_df, customer_name, customer_dob, customer_address, customer_tel):
    # Check if the telephone number already exists and belongs to the same person, if not just return False:
    if customer_tel in customer_df['Telephone'].values:

        # Converting the dataframe to list in order to iterate each row:
        customer_df_list = customer_df.to_numpy().tolist()

        # Loop in the rows and check if the telephone number exists more than once:
        for row in customer_df_list:
            if row[1] == customer_name and row[3] == customer_dob and \
                    row[4] == customer_address:
                if row[5] == customer_tel:
                    return False
                else:
                    return True
    else:
        return False


def assert_create_customer_data(customer_df, customer_name, customer_dob, customer_address, customer_tel):
    # Converting the dataframe to list in order to iterate each row:
    customer_df_list = customer_df.to_numpy().tolist()

    # Loop in the rows and check if the telephone number exists more than once:
    for row in customer_df_list:
        if row[1] != customer_name or row[3] != customer_dob or \
                row[4] != customer_address:
            if row[5] == customer_tel:
                return True
    return False


def create_deposit_data(account_id, deposit_amount):
    # Reading the current csv into a dataframe, to check if values exist or not:
    cust_df = pd.read_csv('Customer_Data.csv')

    # Checks if the account number exists in the dataframe:
    if account_id in cust_df['Account_ID'].values:
        # Getting the row index where the account number exists:
        index_of_cust_id = cust_df.index[cust_df['Account_ID'] == account_id].tolist()[0]

        # Getting the balance value located in the 6th column in the dataframe, where the transaction is taking place:
        row_idx = cust_df.iloc[index_of_cust_id]
        balance_value = float(row_idx.iloc[6])

        # Prevent a deposit of 0 amount:
        if deposit_amount == 0.0:
            messagebox.showerror("Data Error", "Deposit amount can not be 0")

        else:
            # Calling the make_deposit function to make a deposit:
            Customers.make_deposit(balance_value, cust_df, account_id, deposit_amount)

    else:
        messagebox.showerror("Data Error", "Account ID does not exist")


def create_withdrawal_data(account_id, withdrawal_amount):
    # Reading the current csv into a dataframe, to check if values exist or not:
    cust_df = pd.read_csv('Customer_Data.csv')

    # Checks if the account number exists in the dataframe:
    if account_id in cust_df['Account_ID'].values:
        # Getting the row index where the account number exists:
        index_of_cust_id = cust_df.index[cust_df['Account_ID'] == account_id].tolist()[0]

        # Getting the balance value located in the 6th column in the dataframe, where the transaction is taking place:
        row_idx = cust_df.iloc[index_of_cust_id]
        balance_value = float(row_idx.iloc[6])

        # Prevent a deposit of 0 amount:
        if withdrawal_amount == 0.0 or balance_value <= 0.0:
            messagebox.showerror("Data Error", "Withdrawal amount can not be 0 or not enough balance")

        else:
            # Calling the make_deposit function to make a deposit:
            Customers.make_withdrawal(balance_value, cust_df, account_id, withdrawal_amount)

    else:
        messagebox.showerror("Data Error", "Account ID does not exist")


def print_customer_balance(account_id):
    # Reading the customer_data table from the database into a dataframe:
    cust_table_name = 'customer_data'
    schema = 'banking_app'
    cust_df = pd.read_sql('SELECT * from {}.{};'.format(schema, cust_table_name), con=engine)

    # Checks if the account number exists in the dataframe:
    if account_id in cust_df['Account_ID'].values:
        Customers.print_cust_balance(account_id, cust_df)
    else:
        messagebox.showerror("Data Error", "Account does not exist")


def print_customer_statement(account_id):
    # Reading the transaction_data table from the database into a dataframe:
    trans_table_name = 'transaction_data'
    schema = 'banking_app'
    trans_df = pd.read_sql('SELECT * from {}.{};'.format(schema, trans_table_name), con=engine)

    # Checks if the account number exists in the dataframe:
    if account_id in trans_df['Account_ID'].values:
        Transaction.print_bank_statement(account_id, trans_df)
    else:
        messagebox.showerror("Data Error", "Account does not exist")


def edit_branch_data(radiobutton_choice, optionmenu_choice, new_data):
    # Retrieve the branch dataframe:
    branch_df = pd.read_csv('Branch_Data.csv')

    # Retrieve the customer dataframe; this will be used to reflect the changes in the customer dataframe too:
    customer_df = pd.read_csv('Customer_Data.csv')

    if new_data == "":
        messagebox.showerror("Data Error", "New Data field must not be empty")

    elif radiobutton_choice == "":
        messagebox.showerror("Data Error", "Please choose an option to edit")

    elif optionmenu_choice == "":
        messagebox.showerror("Data Error", "Branch name must not be empty")

    elif radiobutton_choice == 'Branch_name':
        # Match the branch name to a regex to make sure it does not contain digits:
        pattern_to_match = re.compile('^\D\D\D')
        matched_pattern = re.match(pattern_to_match, new_data)

        # Making sure that the branch name's length is exactly 3 digits:
        if len(new_data) != 3 or matched_pattern is None:
            messagebox.showerror("Data Error", "Number of characters for the branch name must be 3 and/or should not "
                                               "contain digits")

        else:
            column_idx = 1
            br_idx = branch_df.index[branch_df['Branch_name'] == optionmenu_choice].tolist()[0]
            # Call the edit_branch function and pass the branch id, the dataframes the new data and the column index:
            Bank.edit_branch(br_idx, branch_df, customer_df, new_data.upper(), column_idx)

    elif radiobutton_choice == 'Branch_country':
        column_idx = 2
        br_idx = branch_df.index[branch_df['Branch_name'] == optionmenu_choice].tolist()[0]
        # Call the edit_branch function and pass the branch id, the dataframes the new data and the column index:
        Bank.edit_branch(br_idx, branch_df, customer_df, new_data, column_idx)

    elif radiobutton_choice == 'Branch_address':
        column_idx = 3
        br_idx = branch_df.index[branch_df['Branch_name'] == optionmenu_choice].tolist()[0]
        # Call the edit_branch function and pass the branch id, the dataframes the new data and the column index:
        Bank.edit_branch(br_idx, branch_df, customer_df, new_data, column_idx)


def edit_customer_data(radiobutton_choice, entry_choice, new_data):
    # Retrieve the customer dataframe:
    customer_df = pd.read_csv('Customer_Data.csv')

    # Convert the Telephone column to bigint, in order to compare the values to the tel number passed to the assert
    # customer data function:
    customer_df['Telephone'] = customer_df['Telephone'].astype('int64')

    # Check if the account ID exists, if it does, perform the editing:
    if entry_choice in customer_df['Account_ID'].values:

        # Retrieving the customer data to assert the uniqueness of the telephone number:
        # 1. Get the customer's name:
        cust_idx = customer_df.index[customer_df['Account_ID'] == entry_choice].tolist()[0]
        customer_idx = customer_df.iloc[cust_idx]
        customer_name = customer_idx.iloc[1]

        # 2. Get the customer's dob:
        cust_idx = customer_df.index[customer_df['Account_ID'] == entry_choice].tolist()[0]
        customer_idx = customer_df.iloc[cust_idx]
        customer_dob = customer_idx.iloc[3]

        # 3. Get the customer's address:
        cust_idx = customer_df.index[customer_df['Account_ID'] == entry_choice].tolist()[0]
        customer_idx = customer_df.iloc[cust_idx]
        customer_address = customer_idx.iloc[4]

        # 3. Get the customer's telephone:
        cust_idx = customer_df.index[customer_df['Account_ID'] == entry_choice].tolist()[0]
        customer_idx = customer_df.iloc[cust_idx]
        customer_telephone = customer_idx.iloc[5]

        if new_data == "":
            messagebox.showerror("Data Error", "New Data field must not be empty")

        elif entry_choice == "":
            messagebox.showerror("Data Error", "Account ID must not be empty")

        elif radiobutton_choice == "":
            messagebox.showerror("Data Error", "Please choose an option to edit")

        elif radiobutton_choice == 'Customer_name':
            # Assert the telephone uniqueness:
            if assert_edit_customer_data(customer_df, new_data, customer_dob, customer_address, int(customer_telephone)):
                messagebox.showerror("Data Error", "Telephone number already exists")
            else:
                column_idx = 1
                cust_idx = customer_df.index[customer_df['Account_ID'] == entry_choice].tolist()[0]
                # Call the edit_customer function and pass the customer index, the dataframe, the new_data and the
                # column index:
                Branch.edit_customer(cust_idx, customer_df, new_data, column_idx)

        elif radiobutton_choice == 'Customer_address':
            # Assert the telephone uniqueness:
            if assert_edit_customer_data(customer_df, customer_name, customer_dob, new_data, int(customer_telephone)):
                messagebox.showerror("Data Error", "Telephone number already exists")
            else:
                column_idx = 4
                cust_idx = customer_df.index[customer_df['Account_ID'] == entry_choice].tolist()[0]
                # Call the edit_customer function and pass the customer index, the dataframe, the new_data and the
                # column index:
                Branch.edit_customer(cust_idx, customer_df, new_data, column_idx)

        elif radiobutton_choice == 'Telephone':
            # Assert the telephone uniqueness:
            if assert_edit_customer_data(customer_df, customer_name, customer_dob, customer_address, int(new_data)):
                messagebox.showerror("Data Error", "Telephone number already exists")

            elif len(str(new_data)) < 10 or len(str(new_data)) > 13:
                messagebox.showerror("Data Error", "Telephone must not be empty and must be less than 10 digits or "
                                                   "greater than 13 digits")

            else:
                column_idx = 5
                cust_idx = customer_df.index[customer_df['Account_ID'] == entry_choice].tolist()[0]
                # Call the edit_customer function and pass the customer index, the dataframe, the new_data and the
                # column index:
                Branch.edit_customer(cust_idx, customer_df, int(new_data), column_idx)

    else:
        messagebox.showerror("Data Error", "Account does not exist or field is empty")


def remove_branch_data(optionmenu_choice):
    # Make sure the branch is selected:
    if optionmenu_choice == "":
        messagebox.showerror("Data Error", "Please select branch")

    else:
        # Reading the current csv into a dataframe, to check if values exist or not:
        br_dataframe = pd.read_csv('Branch_Data.csv')

        # Retrieve the customer dataframe; this will be used to reflect the changes in the customer dataframe too:
        customer_df = pd.read_csv('Customer_Data.csv')

        # Fetch the index of the branch to be deleted:
        idx = br_dataframe.index[br_dataframe['Branch_name'] == optionmenu_choice].tolist()[0]

        # Call the remove branch function from bank function and pass the index, the branch dataframe, the customer
        # dataframe and the branch name:
        Bank.remove_branch_from_bank(idx, br_dataframe, customer_df, optionmenu_choice)


def remove_customer_data(account_id):
    # Retrieving the customer dataframe:
    cust_dataframe = pd.read_csv('Customer_Data.csv')

    # Make sure an account id is selected:
    if account_id == "":
        messagebox.showerror("Data Error", "Please select an account ID")

    elif account_id in cust_dataframe['Account_ID'].values:

        # Fetch the index of the account ID to be deleted:
        idx = cust_dataframe.index[cust_dataframe['Account_ID'] == account_id].tolist()[0]

        # Call the remove branch function from bank function and pass the index and dataframe:
        Branch.remove_customer_from_branch(idx, cust_dataframe)

    else:
        messagebox.showerror("Data Error", "Account ID does not exist")


def create_branch_widgets():
    for widget in frame3.winfo_children():
        widget.destroy()

    # Initializing the branch key variable:
    branch_key_value = customtkinter.StringVar(value='0')

    frame3_brc_titlelabel = customtkinter.CTkLabel(frame3, text="Create Branch", font=("Ariel", 16, "bold"),
                                                   text_color="black")
    frame3_brc_titlelabel.pack(pady=40, padx=30, anchor=customtkinter.W)

    frame3_brc_label1 = customtkinter.CTkLabel(frame3, text="Branch Name", font=("Ariel", 14), text_color="black")
    frame3_brc_label1.pack(padx=(0, 115), pady=(100, 0), anchor=customtkinter.CENTER)

    frame3_brc_entry1 = customtkinter.CTkEntry(frame3, width=200)
    frame3_brc_entry1.pack()

    frame3_brc_label2 = customtkinter.CTkLabel(frame3, text="Branch Country", font=("Ariel", 14), text_color="black")
    frame3_brc_label2.pack(padx=(0, 103), anchor=customtkinter.CENTER)

    frame3_brc_entry2 = customtkinter.CTkEntry(frame3, width=200)
    frame3_brc_entry2.pack()

    frame3_brc_label3 = customtkinter.CTkLabel(frame3, text="Branch Address", font=("Ariel", 14), text_color="black")
    frame3_brc_label3.pack(padx=(0, 101), anchor=customtkinter.CENTER)

    frame3_brc_entry3 = customtkinter.CTkEntry(frame3, width=200)
    frame3_brc_entry3.pack()

    frame3_brc_label4 = customtkinter.CTkLabel(frame3, text="Branch Key", font=("Ariel", 14), text_color="black")
    frame3_brc_label4.pack(padx=(0, 125), anchor=customtkinter.CENTER)

    frame3_brc_entry4 = customtkinter.CTkEntry(frame3, width=200, textvariable=branch_key_value)
    frame3_brc_entry4.pack()

    frame3_brc_button = customtkinter.CTkButton(frame3, width=80, text="Create", fg_color="green",
                                                command=lambda: create_branch_data(frame3_brc_entry1.get().upper(),
                                                                                   frame3_brc_entry2.get(),
                                                                                   frame3_brc_entry3.get(),
                                                                                   int(branch_key_value.get())))

    frame3_brc_button.pack(pady=20)

    # Make the treeview visible:
    branch_dataframe = pd.read_csv('Branch_Data.csv')
    create_treeview(branch_dataframe)


def create_customer_widgets():
    for widget in frame3.winfo_children():
        widget.destroy()

    # Initializing the option menu variable:
    cus_optionmenu = customtkinter.StringVar()

    # Initializing the customer name variable:
    cus_name = customtkinter.StringVar()

    # Initializing the customer address variable:
    cus_address = customtkinter.StringVar()

    # Initializing the customer telephone variable:
    cus_telephone = customtkinter.StringVar(value='+')

    # Initializing the customer transaction variable:
    cus_transaction = customtkinter.StringVar(value='0.0')

    # Initializing the values of the option menu:
    # 1. Read the csv into a dataframe:
    branch_csv_to_df = pd.read_csv('Branch_Data.csv')

    # 2. Initialize an empty list that will hold the values (branches):
    list_of_options = []

    # 3. Loop in the branches and append the list:
    for branch in branch_csv_to_df['Branch_name']:
        list_of_options.append(branch)

    frame3_cus_titlelabel = customtkinter.CTkLabel(frame3, text="Create Customer", font=("Ariel", 16, "bold"),
                                                   text_color="black")
    frame3_cus_titlelabel.pack(pady=40, padx=30, anchor=customtkinter.W)

    frame3_cus_label1 = customtkinter.CTkLabel(frame3, text="Branch Name", font=("Ariel", 14), text_color="black")
    frame3_cus_label1.pack(padx=(0, 115), pady=(100, 0), anchor=customtkinter.CENTER)

    frame3_cus_optionmenu1 = customtkinter.CTkOptionMenu(frame3, width=200, fg_color="black", values=list_of_options,
                                                         variable=cus_optionmenu)
    frame3_cus_optionmenu1.pack()

    frame3_cus_label2 = customtkinter.CTkLabel(frame3, text="Customer Name", font=("Ariel", 14), text_color="black")
    frame3_cus_label2.pack(padx=(0, 100), anchor=customtkinter.CENTER)

    frame3_cus_entry2 = customtkinter.CTkEntry(frame3, width=200, textvariable=cus_name)
    frame3_cus_entry2.pack()

    frame3_cus_label3 = customtkinter.CTkLabel(frame3, text="Date of Birth", font=("Ariel", 14), text_color="black")
    frame3_cus_label3.pack(padx=(0, 122), anchor=customtkinter.CENTER)

    frame3_cus_cal = Calendar(frame3, selectmode="day", year=2024, month=2, day=1, date_pattern="dd/mm/YYYY",
                              font="Arial 12")
    frame3_cus_cal.pack()

    frame3_cus_label4 = customtkinter.CTkLabel(frame3, text="Customer Address", font=("Ariel", 14), text_color="black")
    frame3_cus_label4.pack(padx=(0, 85), anchor=customtkinter.CENTER)

    frame3_cus_entry4 = customtkinter.CTkEntry(frame3, width=200, textvariable=cus_address)
    frame3_cus_entry4.pack()

    frame3_cus_label5 = customtkinter.CTkLabel(frame3, text="Telephone", font=("Ariel", 14), text_color="black")
    frame3_cus_label5.pack(padx=(0, 133), anchor=customtkinter.CENTER)

    frame3_cus_entry5 = customtkinter.CTkEntry(frame3, width=200, textvariable=cus_telephone)
    frame3_cus_entry5.pack()

    frame3_cus_label6 = customtkinter.CTkLabel(frame3, text="Initial Transaction", font=("Ariel", 14),
                                               text_color="black")
    frame3_cus_label6.pack(padx=(0, 90), anchor=customtkinter.CENTER)

    frame3_cus_entry6 = customtkinter.CTkEntry(frame3, width=200, textvariable=cus_transaction)
    frame3_cus_entry6.pack()

    frame3_brc_button = customtkinter.CTkButton(frame3, text="Create", width=80, fg_color="green",
                                                command=lambda: create_customer_data(cus_optionmenu.get(),
                                                                                     cus_name.get(),
                                                                                     frame3_cus_cal.get_date(),
                                                                                     cus_address.get(),
                                                                                     int(cus_telephone.get()),
                                                                                     float(cus_transaction.get())))

    frame3_brc_button.pack(pady=20)

    # Make the treeview visible:
    customer_dataframe = pd.read_csv('Customer_Data.csv')
    create_treeview(customer_dataframe)


def create_deposit_widgets():
    for widget in frame3.winfo_children():
        widget.destroy()

    # Initializing the account_id variable:
    account_id_variable = customtkinter.StringVar()

    # Initializing the deposit variable:
    deposit_variable = customtkinter.StringVar(value="0.0")

    frame3_dep_titlelabel = customtkinter.CTkLabel(frame3, text="Make a Deposit", font=("Ariel", 16, "bold"),
                                                   text_color="black")
    frame3_dep_titlelabel.pack(pady=40, padx=30, anchor=customtkinter.W)

    frame3_dep_label1 = customtkinter.CTkLabel(frame3, text="Account ID", font=("Ariel", 14), text_color="black")
    frame3_dep_label1.pack(padx=(0, 130), pady=(100, 0), anchor=customtkinter.CENTER)

    frame3_dep_entry1 = customtkinter.CTkEntry(frame3, width=200, textvariable=account_id_variable)
    frame3_dep_entry1.pack()

    frame3_dep_label2 = customtkinter.CTkLabel(frame3, text="Deposit Amount", font=("Ariel", 14), text_color="black")
    frame3_dep_label2.pack(padx=(0, 101), anchor=customtkinter.CENTER)

    frame3_dep_entry2 = customtkinter.CTkEntry(frame3, width=200, textvariable=deposit_variable)
    frame3_dep_entry2.pack()

    frame3_dep_button = customtkinter.CTkButton(frame3, text="Deposit", width=80, fg_color="green",
                                                command=lambda: create_deposit_data(frame3_dep_entry1.get(),
                                                                                    float(frame3_dep_entry2.get())))
    frame3_dep_button.pack(pady=20)


def create_withdrawal_widgets():
    for widget in frame3.winfo_children():
        widget.destroy()

    # Initializing the account_id variable:
    account_id_variable = customtkinter.StringVar()

    # Initializing the deposit variable:
    withdrawal_variable = customtkinter.StringVar(value="0.0")

    frame3_wit_titlelabel = customtkinter.CTkLabel(frame3, text="Make a Withdrawal", font=("Ariel", 16, "bold"),
                                                   text_color="black")
    frame3_wit_titlelabel.pack(pady=40, padx=30, anchor=customtkinter.W)

    frame3_wit_label1 = customtkinter.CTkLabel(frame3, text="Account ID", font=("Ariel", 14), text_color="black")
    frame3_wit_label1.pack(padx=(0, 130), pady=(100, 0), anchor=customtkinter.CENTER)

    frame3_wit_entry1 = customtkinter.CTkEntry(frame3, width=200, textvariable=account_id_variable)
    frame3_wit_entry1.pack()

    frame3_wit_label2 = customtkinter.CTkLabel(frame3, text="Withdrawal Amount", font=("Ariel", 14), text_color="black")
    frame3_wit_label2.pack(padx=(0, 82), anchor=customtkinter.CENTER)

    frame3_wit_entry2 = customtkinter.CTkEntry(frame3, width=200, textvariable=withdrawal_variable)
    frame3_wit_entry2.pack()

    frame3_wit_button = customtkinter.CTkButton(frame3, text="Withdraw", width=80, fg_color="green",
                                                command=lambda: create_withdrawal_data(frame3_wit_entry1.get(),
                                                                                       float(frame3_wit_entry2.get())))
    frame3_wit_button.pack(pady=20)


def create_print_balance_widgets():
    for widget in frame3.winfo_children():
        widget.destroy()

    # Initializing the account_id variable:
    account_id_variable = customtkinter.StringVar()

    frame3_bal_titlelabel = customtkinter.CTkLabel(frame3, text="Print Balance", font=("Ariel", 16, "bold"),
                                                   text_color="black")
    frame3_bal_titlelabel.pack(pady=40, padx=30, anchor=customtkinter.W)

    frame3_bal_label1 = customtkinter.CTkLabel(frame3, text="Account ID", font=("Ariel", 14), text_color="black")
    frame3_bal_label1.pack(padx=(0, 130), pady=(100, 0), anchor=customtkinter.CENTER)

    frame3_bal_entry1 = customtkinter.CTkEntry(frame3, width=200, textvariable=account_id_variable)
    frame3_bal_entry1.pack()

    frame3_bal_button = customtkinter.CTkButton(frame3, text="Print", width=80, fg_color="green",
                                                command=lambda: print_customer_balance(frame3_bal_entry1.get()))
    frame3_bal_button.pack(pady=20)


def create_print_statement_widgets():
    for widget in frame3.winfo_children():
        widget.destroy()

    # Initializing the account_id variable:
    account_id_variable = customtkinter.StringVar()

    frame3_sta_titlelabel = customtkinter.CTkLabel(frame3, text="Print Statement", font=("Ariel", 16, "bold"),
                                                   text_color="black")
    frame3_sta_titlelabel.pack(pady=40, padx=30, anchor=customtkinter.W)

    frame3_sta_label1 = customtkinter.CTkLabel(frame3, text="Account ID", font=("Ariel", 14), text_color="black")
    frame3_sta_label1.pack(padx=(0, 130), pady=(100, 0), anchor=customtkinter.CENTER)

    frame3_sta_entry1 = customtkinter.CTkEntry(frame3, width=200, textvariable=account_id_variable)
    frame3_sta_entry1.pack()

    frame3_sta_button = customtkinter.CTkButton(frame3, text="Print", width=80, fg_color="green",
                                                command=lambda: print_customer_statement(frame3_sta_entry1.get()))
    frame3_sta_button.pack(pady=20)


def create_edit_branch_widgets():
    for widget in frame3.winfo_children():
        widget.destroy()

    # Initializing the radio button variable:
    br_radiobutton = customtkinter.StringVar()

    frame3_ebr_titlelabel = customtkinter.CTkLabel(frame3, text="Edit Branch", font=("Ariel", 16, "bold"),
                                                   text_color="black")
    frame3_ebr_titlelabel.pack(pady=40, padx=30, anchor=customtkinter.W)

    frame3_ebr_radio1 = customtkinter.CTkRadioButton(frame3, text="Edit Branch Name", text_color="black",
                                                     value="Branch_name", variable=br_radiobutton)
    frame3_ebr_radio1.pack(pady=(120, 0), padx=(0, 19), anchor=customtkinter.CENTER)

    frame3_ebr_radio2 = customtkinter.CTkRadioButton(frame3, text="Edit Branch Country", text_color="black",
                                                     value="Branch_country", variable=br_radiobutton)
    frame3_ebr_radio2.pack(pady=(20, 0), padx=(0, 10), anchor=customtkinter.CENTER)

    frame3_ebr_radio3 = customtkinter.CTkRadioButton(frame3, text="Edit Branch Address", text_color="black",
                                                     value="Branch_address", variable=br_radiobutton)
    frame3_ebr_radio3.pack(pady=(20, 0), padx=(0, 7), anchor=customtkinter.CENTER)

    # Initializing the option menu variable:
    br_optionmenu = customtkinter.StringVar()

    # Initializing the values of the option menu:
    # 1. Read the csv into a dataframe:
    branch_csv_to_df = pd.read_csv('Branch_Data.csv')

    # 2. Initialize an empty list that will hold the values (branches):
    list_of_options = []

    # 3. Loop in the branches and append the list:
    for branch in branch_csv_to_df['Branch_name']:
        list_of_options.append(branch)

    frame3_ebr_label1 = customtkinter.CTkLabel(frame3, text="Branch Key", font=("Ariel", 14), text_color="black")
    frame3_ebr_label1.pack(padx=(0, 10), pady=(60, 0))

    frame3_ebr_optionmenu1 = customtkinter.CTkOptionMenu(frame3, width=200, fg_color="black", values=list_of_options,
                                                         variable=br_optionmenu)
    frame3_ebr_optionmenu1.pack()

    frame3_ebr_label2 = customtkinter.CTkLabel(frame3, text="New Data", font=("Ariel", 14), text_color="black")
    frame3_ebr_label2.pack(pady=(10, 0), anchor=customtkinter.CENTER)

    # Initializing the data entry variable:
    br_newdata = customtkinter.StringVar()

    frame3_ebr_entry2 = customtkinter.CTkEntry(frame3, width=200, textvariable=br_newdata)
    frame3_ebr_entry2.pack()

    frame3_ebr_button1 = customtkinter.CTkButton(frame3, text="Edit", width=100, fg_color="green",
                                                 command=lambda: edit_branch_data(br_radiobutton.get(),
                                                                                  br_optionmenu.get(),
                                                                                  frame3_ebr_entry2.get()))
    frame3_ebr_button1.pack(pady=20)

    # Make the treeview visible:
    create_treeview(branch_csv_to_df)


def create_edit_customer_widgets():
    for widget in frame3.winfo_children():
        widget.destroy()

    # Initializing the radio button variable for name and address:
    cus_radiobutton = customtkinter.StringVar()

    frame3_ecs_titlelabel = customtkinter.CTkLabel(frame3, text="Edit Customer", font=("Ariel", 16, "bold"),
                                                   text_color="black")
    frame3_ecs_titlelabel.pack(pady=40, padx=30, anchor=customtkinter.W)

    frame3_ecs_radio1 = customtkinter.CTkRadioButton(frame3, text="Edit Customer Name", text_color="black",
                                                     value="Customer_name", variable=cus_radiobutton)
    frame3_ecs_radio1.pack(pady=(120, 0), padx=(0, 4), anchor=customtkinter.CENTER)

    frame3_ecs_radio2 = customtkinter.CTkRadioButton(frame3, text="Edit Customer Address", text_color="black",
                                                     value="Customer_address", variable=cus_radiobutton)
    frame3_ecs_radio2.pack(pady=(20, 0), padx=(9, 0), anchor=customtkinter.CENTER)

    frame3_ecs_radio3 = customtkinter.CTkRadioButton(frame3, text="Edit Customer Telephone", text_color="black",
                                                     value="Telephone", variable=cus_radiobutton)
    frame3_ecs_radio3.pack(pady=(20, 0), padx=(23, 0), anchor=customtkinter.CENTER)

    frame3_ecs_label1 = customtkinter.CTkLabel(frame3, text="Account ID", font=("Ariel", 14), text_color="black")
    frame3_ecs_label1.pack(padx=(0, 10), pady=(60, 0))

    frame3_ecs_entry1 = customtkinter.CTkEntry(frame3, width=300)
    frame3_ecs_entry1.pack(padx=(0, 10))

    frame3_ecs_label2 = customtkinter.CTkLabel(frame3, text="New Data", font=("Ariel", 14), text_color="black")
    frame3_ecs_label2.pack(pady=(10, 0), anchor=customtkinter.CENTER)

    # Initializing the data entry variable:
    cus_newdata = customtkinter.StringVar()

    frame3_ecs_entry2 = customtkinter.CTkEntry(frame3, width=200, textvariable=cus_newdata)
    frame3_ecs_entry2.pack()

    frame3_ecs_button1 = customtkinter.CTkButton(frame3, text="Edit", width=80, fg_color="green",
                                                 command=lambda: edit_customer_data(cus_radiobutton.get(),
                                                                                    frame3_ecs_entry1.get(),
                                                                                    frame3_ecs_entry2.get()))
    frame3_ecs_button1.pack(pady=20)

    # Make the treeview visible:
    customer_csv_to_df = pd.read_csv('Customer_Data.csv')
    create_treeview(customer_csv_to_df)


def create_remove_branch_widgets():
    for widget in frame3.winfo_children():
        widget.destroy()

    # Initializing the option menu button variable:
    remove_br_optionmenu = customtkinter.StringVar()

    frame3_rbr_titlelabel = customtkinter.CTkLabel(frame3, text="Remove Branch", font=("Ariel", 16, "bold"),
                                                   text_color="black")
    frame3_rbr_titlelabel.pack(pady=40, padx=30, anchor=customtkinter.W)

    # Initializing the values of the option menu:
    # 1. Read the csv into a dataframe:
    branch_csv_to_df = pd.read_csv('Branch_Data.csv')

    # 2. Initialize an empty list that will hold the values (branches):
    list_of_options = []

    # 3. Loop in the branches and append the list:
    for branch in branch_csv_to_df['Branch_name']:
        list_of_options.append(branch)

    frame3_rbr_label1 = customtkinter.CTkLabel(frame3, text="Branch Key", font=("Ariel", 14), text_color="black")
    frame3_rbr_label1.pack(padx=(0, 10), pady=(60, 0))

    frame3_rbr_optionmenu1 = customtkinter.CTkOptionMenu(frame3, width=200, fg_color="black", values=list_of_options,
                                                         variable=remove_br_optionmenu)
    frame3_rbr_optionmenu1.pack()

    frame3_rbr_button1 = customtkinter.CTkButton(frame3, text="Remove",
                                                 width=100, fg_color="green",
                                                 command=lambda: remove_branch_data(remove_br_optionmenu.get()))
    frame3_rbr_button1.pack(pady=20)

    # Make the treeview visible:
    create_treeview(branch_csv_to_df)


def create_remove_customer_widgets():
    for widget in frame3.winfo_children():
        widget.destroy()

    frame3_rcs_titlelabel = customtkinter.CTkLabel(frame3, text="Remove Customer", font=("Ariel", 16, "bold"),
                                                   text_color="black")
    frame3_rcs_titlelabel.pack(pady=40, padx=30, anchor=customtkinter.W)

    frame3_rcs_label1 = customtkinter.CTkLabel(frame3, text="Account ID", font=("Ariel", 14), text_color="black")
    frame3_rcs_label1.pack(padx=(0, 10), pady=(60, 0))

    frame3_rcs_entry1 = customtkinter.CTkEntry(frame3, width=300)
    frame3_rcs_entry1.pack(padx=(0, 10))

    frame3_rcs_button1 = customtkinter.CTkButton(frame3, text="Remove", width=80, fg_color="green",
                                                 command=lambda: remove_customer_data(frame3_rcs_entry1.get()))
    frame3_rcs_button1.pack(pady=20)

    # Make the treeview visible:
    customer_csv_to_df = pd.read_csv('Customer_Data.csv')
    create_treeview(customer_csv_to_df)


class Bank:
    def __init__(self, bank_name, list_of_branches):
        self.bank_name = bank_name
        self.list_of_branches = list_of_branches

    @staticmethod
    def add_branch(list_of_branches, branch_name, branch_country, branch_address, branch_key):
        # Creating a data list that will be added as a value in the list_of_branches dictionary:
        data = [branch_name, branch_country, branch_address]
        branch_data.append(data)

        # Populate the dictionary with the data:
        list_of_branches.setdefault(branch_key, []).append(data)

        # Creating a pandas dataframe from the dictionary:
        branch_df = pd.DataFrame((k, *x) for k, v in list_of_branches.items() for x in v).reset_index(drop=True)

        # Exporting the dataframe to a .csv file on my local machine:
        branch_df.to_csv('Branch_Data.csv', header=False, mode='a', index=False)

        # Reading the csv into a dataframe which will be passed to the update_database function:
        df_to_db = pd.read_csv('Branch_Data.csv')

        # Identifying the table name in the database:
        db_table_name = 'branch_data'

        # Call the update_database function and pass the table name and the dataframe:
        update_database(df_to_db, db_table_name)

        # Update the treeview:
        df_branch_to_treeview = pd.read_csv('Branch_Data.csv')
        create_treeview(df_branch_to_treeview)

        # Pop up message that the transaction is completed:
        messagebox.showinfo("Transaction", "Branch created successfully")

        # Reset the widgets by calling the create_branch_widgets function where the widgets will be destroyed:
        create_branch_widgets()

    @staticmethod
    def edit_branch(br_idx, branch_df, customer_df, new_data, col_idx):
        # Retrieve the branch name based on the row and column id:
        branch_idx = branch_df.iloc[br_idx]
        branch_info = branch_idx.iloc[col_idx]

        # Initialize a dataframe that will hold the info to update the customer dataframe at the same time:
        branch_info_in_cust_df = branch_info

        # Create a new instance of the dataframe object to be updated:
        branch_df_updated = branch_df
        customer_df_updated = customer_df

        # Check if the column id passed is the branch name, if so edit it:
        if col_idx == 1:
            branch_df_updated.at[br_idx, "Branch_name"] = new_data

        # Check if the column id passed is the branch country, if so edit it:
        elif col_idx == 2:
            branch_df_updated.at[br_idx, "Branch_country"] = new_data

        # Check if the column id passed is the branch address, if so edit it:
        elif col_idx == 3:
            branch_df_updated.at[br_idx, "Branch_address"] = new_data

        # Update the branch name in the customer dataframe:
        # 1. Retrieve the branch name based on the row and column id:
        branch_index = branch_df_updated.iloc[br_idx]
        branch_info_updated = branch_index.iloc[col_idx]
        # 2. Check if the branch name exists in the customer dataframe and update it:
        if branch_info_in_cust_df in customer_df_updated['Branch_name'].values:
            customer_df_updated.replace(branch_info_in_cust_df, branch_info_updated, inplace=True)

        # Write the updated dataframes back to csv:
        branch_df_updated.to_csv('Branch_Data.csv', index=False)

        customer_df_updated.to_csv('Customer_Data.csv', index=False)

        # Converting the Telephone column to bigint, so it reflects accordingly everytime the table gets replaced in
        # the database:
        customer_df_updated['Telephone'] = customer_df_updated['Telephone'].astype('int64')

        # Update the branch and customer tables in the database:
        brchdb_table_name = 'branch_data'
        update_database(branch_df_updated, brchdb_table_name)
        custdb_table_name = 'customer_data'
        update_database(customer_df_updated, custdb_table_name)

        # Pop up message that the transaction is completed:
        messagebox.showinfo("Transaction", "Data edited successfully")

        # Reset the widgets by calling the create_edit_branch_widgets function where the widgets will be destroyed:
        create_edit_branch_widgets()

        # Show the Treeview:
        create_treeview(branch_df_updated)

    @staticmethod
    def remove_branch_from_bank(idx, br_dataframe, cust_dataframe, br_name):
        # Remove the branch from dataframe:
        br_dataframe_updated = br_dataframe.drop(idx, axis=0, inplace=False)

        # Remove the customers from the dataframe that belong to the deleted branch:
        brc_name = cust_dataframe[cust_dataframe['Branch_name'] == br_name].index
        cust_dataframe_updated = cust_dataframe.drop(brc_name)

        # Write back the dataframes into the csv:
        br_dataframe_updated.to_csv('Branch_Data.csv', index=False)
        cust_dataframe_updated.to_csv('Customer_Data.csv', index=False)

        # Converting the Telephone column to bigint, so it reflects accordingly everytime the table gets replaced in
        # the database:
        cust_dataframe_updated['Telephone'] = cust_dataframe_updated['Telephone'].astype('int64')

        # Identifying the table names in the database:
        # 1. Branch table:
        brcdb_table_name = 'branch_data'
        # 2. Customer table:
        custdb_table_name = 'customer_data'

        # Call the update database function and pass the table name and the dataframe:
        # 1.Updating the branch table in the database:
        update_database(br_dataframe_updated, brcdb_table_name)
        # 2. Updating the customer table in the database:
        update_database(cust_dataframe_updated, custdb_table_name)

        # Pop up message that the transaction is completed:
        messagebox.showinfo("Transaction", "Records deleted successfully")

        # Reset the widgets by calling the create_edit_branch_widgets function where the widgets will be destroyed:
        create_remove_branch_widgets()

        # Show the Treeview:
        create_treeview(br_dataframe_updated)


class Branch:
    def __init__(self, branch_name, list_of_customers):
        self.branch_name = branch_name
        self.list_of_customers = list_of_customers

    @staticmethod
    def add_customer(branch_name, customer_name, customer_dob, customer_address, customer_tele, customer_init_trans,
                     list_of_customers):
        # Creating the key of the customer dictionary element:
        cust_key = branch_name

        # Creating a unique identified for the customer in hexadecimal format:
        acc_id = uuid.uuid4().hex

        # Creating a balance object and giving it the initial transaction value:
        balance = customer_init_trans

        # Creating a data list that will be added as a value in the list_of_customers dictionary:
        data = [customer_name, acc_id, customer_dob, customer_address, customer_tele, balance]

        # Updating the values list with the new customer data:
        list_of_customers.setdefault(cust_key, []).append(data)

        # Creating a pandas dataframe by flattening/exploding the dictionary:
        customer_df = pd.DataFrame((k, *x) for k, v in list_of_customers.items() for x in v).reset_index(drop=True)

        # Exporting the dataframe to a .csv file on my local machine:
        customer_df.to_csv('Customer_Data.csv', header=False, mode='a', index=False)

        # Reading the csv into a dataframe which will be passed to the update_database function:
        df_to_db = pd.read_csv('Customer_Data.csv')

        # Converting the Telephone column to bigint, so it reflects accordingly everytime the table gets replaced in
        # the database:
        df_to_db['Telephone'] = df_to_db['Telephone'].astype('int64')

        # Identifying the table name in the database:
        db_table_name = 'customer_data'

        # Call the update_database function and pass the table name and the dataframe:
        update_database(df_to_db, db_table_name)

        # Update the treeview:
        df_customer_to_treeview = pd.read_csv('Customer_Data.csv')
        create_treeview(df_customer_to_treeview)

        # Pop up message that the transaction is completed:
        messagebox.showinfo("Transaction", "Customer created successfully")

        # Reset the widgets by calling the create_customer_widgets function where the widgets will be destroyed:
        create_customer_widgets()

    @staticmethod
    def edit_customer(cust_idx, customer_df, new_data, col_idx):
        # Create a new instance of the dataframe object to be updated:
        customer_df_updated = customer_df

        try:
            # Check if the column id passed is the customer name, if so edit it:
            if col_idx == 1:
                customer_df_updated.at[cust_idx, "Customer_name"] = new_data

            # Check if the column id passed is the customer address, if so edit it:
            elif col_idx == 4:
                customer_df_updated.at[cust_idx, "Customer_address"] = new_data

            # Check if the column id passed is the customer telephone, if so edit it:
            elif col_idx == 5:
                customer_df_updated.at[cust_idx, "Telephone"] = new_data

        except ValueError:
            messagebox.showerror("Data Error", "Telephone format is wrong")

        # Write the updated dataframe back to csv:
        customer_df_updated.to_csv('Customer_Data.csv', index=False)

        # Converting the Telephone column to bigint, so it reflects accordingly everytime the table gets replaced in
        # the database:
        customer_df_updated['Telephone'] = customer_df_updated['Telephone'].astype('int64')

        # Update the customer table in the database:
        custdb_table_name = 'customer_data'
        update_database(customer_df_updated, custdb_table_name)

        # Pop up message that the transaction is completed:
        messagebox.showinfo("Transaction", "Data edited successfully")

        # Reset the widgets by calling the create_edit_branch_widgets function where the widgets will be destroyed:
        create_edit_customer_widgets()

        # Show the Treeview:
        create_treeview(customer_df_updated)

    @staticmethod
    def remove_customer_from_branch(idx, cust_dataframe):
        # Remove the customer from dataframe:
        cust_dataframe_updated = cust_dataframe.drop(idx, axis=0, inplace=False)

        # Write back the dataframe into the csv:
        cust_dataframe_updated.to_csv('Customer_Data.csv', index=False)

        # Converting the Telephone column to bigint, so it reflects accordingly everytime the table gets replaced in
        # the database:
        cust_dataframe_updated['Telephone'] = cust_dataframe_updated['Telephone'].astype('int64')

        # Identifying the table name in the database:
        custdb_table_name = 'customer_data'

        # Call the update database function and pass the table name and the dataframe:
        update_database(cust_dataframe_updated, custdb_table_name)

        # Pop up message that the transaction is completed:
        messagebox.showinfo("Transaction", "Records deleted successfully")

        # Reset the widgets by calling the create_edit_branch_widgets function where the widgets will be destroyed:
        create_remove_customer_widgets()

        # Show the Treeview:
        create_treeview(cust_dataframe_updated)


class Customers:
    def __init__(self, deposit, withdrawal):
        self.deposit = deposit
        self.withdrawal = withdrawal

    @staticmethod
    def make_deposit(balance_value, cust_df, account_id, deposit_amount):
        # Creating the timestamp of the transaction:
        deposit_timestamp = Transaction.transaction_timestamp()

        # Calculating the balance after the transaction is made:
        dep_value = balance_value + deposit_amount

        # Replace the old balance with the new calculated balance and export the new dataframe to csv:
        updated_customer_df = cust_df
        updated_customer_df.replace(balance_value, dep_value, inplace=True)
        updated_customer_df.to_csv('Customer_Data.csv', index=False)

        # Fetch the customer name with a specific account ID:
        idx = updated_customer_df.index[updated_customer_df['Account_ID'] == account_id].tolist()[0]
        row_idx = updated_customer_df.iloc[idx]
        cust_name = row_idx.iloc[1]

        # Assign the withdrawal value with None:
        wtd_value = None

        # Call the add_transaction function and pass the necessary parameters:
        Transaction.add_transaction(account_id, cust_name, deposit_amount, wtd_value, deposit_timestamp)

    @staticmethod
    def make_withdrawal(balance_value, cust_df, account_id, withdrawal_amount):
        # Creating the timestamp of the transaction:
        withdrawal_timestamp = Transaction.transaction_timestamp()

        # Calculating the balance after the transaction is made:
        wd_value = balance_value - withdrawal_amount

        # Replace the old balance with the new calculated balance and export the new dataframe to csv:
        updated_customer_df = cust_df
        updated_customer_df.replace(balance_value, wd_value, inplace=True)
        updated_customer_df.to_csv('Customer_Data.csv', index=False)

        # Fetch the customer name with a specific account ID:
        idx = updated_customer_df.index[updated_customer_df['Account_ID'] == account_id].tolist()[0]
        row_idx = updated_customer_df.iloc[idx]
        cust_name = row_idx.iloc[1]

        # Assign the deposit value with None:
        dp_value = None

        # Call the add_transaction function and pass the necessary parameters:
        Transaction.add_transaction(account_id, cust_name, dp_value, withdrawal_amount, withdrawal_timestamp)

    @staticmethod
    def print_cust_balance(account_id, cust_df):
        # Searching for the account id in the dataframe and printing the row where the id belongs:
        updated_customer_df = cust_df
        balance_sheet = updated_customer_df.loc[updated_customer_df['Account_ID'] == account_id]

        # Reset the widgets by calling the create_print_balance_widgets function where the widgets will be destroyed:
        create_print_balance_widgets()

        # Update the treeview:
        create_treeview(balance_sheet)

        # Pop up message that the transaction is completed:
        messagebox.showinfo("Transaction", "Print is successful")


class Transaction:
    def __init__(self, bank_statement):
        self.bank_statement = bank_statement

    @staticmethod
    def add_transaction(account_id, customer_name, deposit, withdrawal, trs_timestamp):
        # Initializing an empty dictionary for every transaction:
        list_of_transactions = {}

        # Initializing a data list containing the dataframe fields, in addition to the account ID:
        data = [customer_name, deposit, withdrawal, trs_timestamp]

        # Creating the dictionary of transactions:
        list_of_transactions.setdefault(account_id, []).append(data)

        # Creating a pandas dataframe of the transactions by flattening/exploding the dictionary:
        transaction_df = pd.DataFrame((k, *x) for k, v in list_of_transactions.items() for x in v).reset_index(
            drop=True)

        # Renaming the column names:
        transaction_df.rename(
            columns={0: 'Account_ID', 1: 'Customer_name', 2: 'Deposit', 3: 'Withdrawal', 4: 'Timestamp'}, inplace=True)

        # Exporting the dataframe to a csv file:
        transaction_df.to_csv('Transaction_Data.csv', header=True, mode='w', index=False)

        if deposit is None:
            # Reset the widgets by calling the create_withdrawal_widgets function where the widgets will be destroyed:
            create_withdrawal_widgets()
            # Update the treeview:
            create_treeview(transaction_df)
            # Pop up message that the transaction is completed:
            messagebox.showinfo("Transaction", "Withdrawal made successfully")
        else:
            # Reset the widgets by calling the create_deposit_widgets function where the widgets will be destroyed:
            create_deposit_widgets()
            # Update the treeview:
            create_treeview(transaction_df)
            # Pop up message that the transaction is completed:
            messagebox.showinfo("Transaction", "Deposit made successfully")

        # Reading the csv into a dataframe which will be passed to update the database:
        # 1. Reading the transaction table:
        transdf_to_db = pd.read_csv('Transaction_Data.csv')
        # 2. Reading the customer table:
        custdf_to_db = pd.read_csv('Customer_Data.csv')

        # Converting the Telephone column to bigint, so it reflects accordingly everytime the table gets replaced in
        # the database:
        custdf_to_db['Telephone'] = custdf_to_db['Telephone'].astype('int64')

        # Identifying the table names in the database:
        # 1. Transaction table:
        transdb_table_name = 'transaction_data'
        # 2. Customer table:
        custdb_table_name = 'customer_data'

        # Call the update database functions and pass the table name and the dataframe:
        # 1.Updating the customer table in the database:
        update_database(custdf_to_db, custdb_table_name)
        # 2. Updating the transaction table in the database:
        update_trans_database(transdf_to_db, transdb_table_name)

    @staticmethod
    def print_bank_statement(account_id, trans_df):
        # Searching for the account id in the dataframe and printing the row where the id belongs:
        updated_trans_df = trans_df
        bank_statement = updated_trans_df.loc[updated_trans_df['Account_ID'] == account_id]

        # Reset the widgets by calling the create_print_statement_widgets function where the widgets will be destroyed:
        create_print_statement_widgets()

        # Update the treeview:
        create_treeview(bank_statement)

        # Pop up message that the transaction is completed:
        messagebox.showinfo("Transaction", "Print is successful")

    @staticmethod
    def transaction_timestamp():
        # Getting the current time:
        current_time = datetime.datetime.now()

        # Changing the format of the current time:
        trans_ts = datetime.datetime.strftime(current_time, '%H:%M:%S %m/%d/%Y')
        return trans_ts


# Running the window:
create_login_frame(window, "silver")
window.mainloop()
