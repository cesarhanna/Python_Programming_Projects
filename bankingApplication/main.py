import pandas as pd
import uuid
import sys
import datetime
from colorama import Fore, Back, Style


def customer_options():
    print('WELCOME TO DKB')
    options_menu()
    try:
        choose_options()
    except ValueError:
        print('Invalid option input. Please try again')
        choose_options()


def options_menu():
    print('\nPress ')
    print('\t 0 - Quit')
    print('\t 1 - To add a new branch')
    print('\t 2 - To add a customer to branch')
    print('\t 3 - To make a deposit')
    print('\t 4 - To make a withdrawal')
    print('\t 5 - To print the customer balance')
    print('\t 6 - To print the customer statement')
    print('\t 7 - To edit a branch data')
    print('\t 8 - To edit a customer data')
    print('\t 9 - To remove a branch')
    print('\t 10 - To remove a customer')
    print('\t 11 - To go to main menu')


def choose_options():
    try:
        choice = int(input('Enter your choice: '))
        match choice:
            case 0:
                print('Thank you and goodbye!')
                sys.exit()
            case 1:
                add_new_branch()
            case 2:
                add_new_customer()
            case 3:
                check_acc_for_deposit()
            case 4:
                check_acc_for_withdrawal()
            case 5:
                print_cust()
            case 6:
                print_cust_statement()
            case 7:
                retrieve_branch_data()
            case 8:
                retrieve_customer_data()
            case 9:
                remove_branch()
            case 10:
                remove_customer()
            case 11:
                customer_options()
            case _:
                print(Fore.RED + 'Enter a valid option from the menu')
                print(Fore.RESET)
                options_menu()
                choose_options()
    except ValueError:
        print(Fore.RED + 'You must enter a number from the menu')
        print(Fore.RESET)
        choose_options()


# Initiating empty lists to create the branches and customers database:
customer_data = []
branch_data = []

# Reading the csv files into a dataframe:
customer_csv_to_df = pd.read_csv('C:\\****\\****\\Customer_Data.csv')


def add_new_branch():
    # Initializing a dictionary of branches, that will hold branch key as key and a list of data as value:
    dict_of_branches = {}

    # Enter the 3 characters branch name:
    while len(branch_name := input('Enter branch name: ').upper()) != 3:
        print(Fore.RED + 'Number of characters must be 3')
        print(Fore.RESET)

    # Assert branch name in the list:
    assert_branch_data('Branch_name', branch_name)

    branch_country = input('Enter branch country: ')
    branch_address = input('Enter branch address: ')

    # Assert branch address in the list:
    assert_branch_data('Branch_address', branch_address)

    # Calling the add_branch function and passing the dictionary and the branch name to add the branch:
    Bank.add_branch(dict_of_branches, branch_name, branch_country, branch_address)

    # Returning to the menu after creating a new branch:
    choose_options()


def assert_branch_data(column_name, br_data):
    # Reading the current csv into a dataframe, to check if values exist or not:
    branch_csv_to_df = pd.read_csv('C:\\****\\****\\Branch_Data.csv')

    # Check if the entered branch data exist in the dataframe ignoring the case-sensitive;
    # if it does, recursively enter the branch info again:
    for item in branch_csv_to_df[column_name]:
        # Stripping both strings for comparison:
        if br_data.replace(',', '').replace(' ', '').casefold() in item.replace(',', '').replace(' ', '').casefold():
            print(Fore.RED + '{} already exists, please choose another {}'.format(column_name, column_name))
            print(Fore.RESET)
            add_new_branch()


def add_new_customer():
    # Initializing a dictionary of customers, that will hold branch name as key and a list of data as value:
    dict_of_customers = {}

    # Enter the branch where the customer should be created:
    cust_branch = input('Enter branch name: ').upper()

    # Reading the current csv into a dataframe, to check if values exist or not:
    branch_csv_to_df = pd.read_csv('C:\\****\\****\\Branch_Data.csv')

    # Check if the branch exists in the dictionary or the dataframe:
    if cust_branch in branch_csv_to_df['Branch_name'].values:
        # Calling the add_customer function and passing the dictionary and the branch name,
        # where the customer will be added:
        Branch.add_customer(cust_branch, dict_of_customers)
    else:
        print(Fore.RED + 'Branch does not exist')
        print(Fore.RESET)

    # Return to main menu:
    choose_options()


def branch_to_dataframe(list_of_branches):
    # Creating a pandas dataframe from the dictionary:
    branch_df = pd.DataFrame((k, *x) for k, v in list_of_branches.items() for x in v).reset_index(drop=True)

    # Exporting the dataframe to a .csv file on my local machine:
    branch_df.to_csv('C:\\****\\****\\Branch_Data.csv', header=False, mode='a', index=False)


def customer_to_dataframe(list_of_customers):
    # Creating a pandas dataframe by flattening/exploding the dictionary:
    customer_df = pd.DataFrame((k, *x) for k, v in list_of_customers.items() for x in v).reset_index(drop=True)

    # Exporting the dataframe to a .csv file on my local machine:
    customer_df.to_csv('C:\\****\\****\\Customer_Data.csv', header=False, mode='a', index=False)


def transaction_to_dataframe(list_of_transactions):
    # Creating a pandas dataframe by flattening/exploding the dictionary:
    transaction_df = pd.DataFrame((k, *x) for k, v in list_of_transactions.items() for x in v).reset_index(drop=True)

    # Exporting the dataframe to a .csv file on my local machine:
    transaction_df.to_csv('C:\\****\\****\\Transaction_Data.csv', header=False, mode='a', index=False)


def check_acc_for_deposit():
    # Customer adds his account number:
    account_id = input('Enter account id: ')

    # Reading the current csv into a dataframe, to check if values exist or not:
    cust_df = pd.read_csv('C:\\****\\****\\Customer_Data.csv')

    # Checks if the account number exists in the dataframe:
    if account_id in cust_df['Account_ID'].values:
        # Getting the row index where the account number exists:
        index_of_cust_id = cust_df.index[cust_df['Account_ID'] == account_id].tolist()[0]

        # Getting the balance value located in the 4th column in the dataframe, where the transaction is taking place:
        row_idx = cust_df.iloc[index_of_cust_id]
        balance_value = float(row_idx.iloc[6])

        # Calling the make_deposit function to make a deposit:
        Customers.make_deposit(balance_value, cust_df, account_id)
    else:
        print(Fore.RED + 'Account does not exist')
        print(Fore.RESET)
        check_acc_for_deposit()


def check_acc_for_withdrawal():
    # Customer adds his account number:
    account_id = input('Enter account id: ')

    # Read the updated csv into a dataframe:
    cust_df = pd.read_csv('C:\\****\\****\\Customer_Data.csv')

    # Checks if the account number exists in either the dictionary or the dataframe:
    if account_id in cust_df['Account_ID'].values:
        # Getting the row index where the account number exists:
        index_of_cust_id = cust_df.index[cust_df['Account_ID'] == account_id].tolist()[0]

        # Getting the balance value located in the 4th column in the dataframe, where the transaction is taking place:
        row_idx = cust_df.iloc[index_of_cust_id]
        balance_value = float(row_idx.iloc[6])

        # Making a withdrawal only if the balance is not null:
        if balance_value > 0:
            Customers.make_withdrawal(balance_value, cust_df, account_id)
        else:
            print(Fore.RED + 'Not enough balance to make a withdrawal')
            print(Fore.RESET)
            choose_options()
    else:
        print(Fore.RED + 'Account does not exist')
        check_acc_for_withdrawal()


def print_cust():
    # Entering the customer account number:
    account_id = input('Enter account id: ')

    # Reading the current csv into a dataframe, to check if values exist or not:
    cust_df = pd.read_csv('C:\\****\\****\\Customer_Data.csv')

    # Checks if the account number exists in the dataframe:
    if account_id in cust_df['Account_ID'].values:
        Customers.print_cust_balance(account_id, cust_df)
    else:
        print(Fore.RED + 'Account does not exist')
        print(Fore.RESET)
        print_cust()


def print_cust_statement():
    # Entering the customer account number:
    account_id = input('Enter account id: ')

    # Read the updated csv into a dataframe:
    trans_df = pd.read_csv('C:\\****\\****\\Transaction_Data.csv')

    # Checks if the account number exists in the dataframe:
    if account_id in trans_df['Account_ID'].values:
        Transaction.print_bank_statement(account_id, trans_df)
    else:
        print(Fore.RED + 'Account does not exist')
        print(Fore.RESET)
        print_cust_statement()


def remove_branch():
    # Enter the branch name:
    branch_name = input('Enter branch name: ').upper()

    # Reading the current csv into a dataframe, to check if values exist or not:
    br_dataframe = pd.read_csv('C:\\****\\****\\Branch_Data.csv')

    # Check if branch exists in the dataframe:
    if branch_name in br_dataframe['Branch_name'].values:

        # Fetch the index of the branch to be deleted:
        idx = br_dataframe.index[br_dataframe['Branch_name'] == branch_name].tolist()[0]

        # Call the remove branch function from bank function and pass the index and dataframe:
        Bank.remove_branch_from_bank(idx, br_dataframe)
    else:
        print(Fore.RED + 'Branch does not exist')
        print(Fore.RESET)
        remove_branch()


def remove_customer():
    # Enter the customer account ID:
    account_id = input('Enter account ID: ')

    # Check if account exists:
    cust_dataframe = pd.read_csv('C:\\****\\****\\Customer_Data.csv')
    if account_id in cust_dataframe['Account_ID'].values:

        # Fetch the index of the account ID to be deleted:
        idx = cust_dataframe.index[cust_dataframe['Account_ID'] == account_id].tolist()[0]

        # Call the remove branch function from bank function and pass the index and dataframe:
        Branch.remove_customer_from_branch(idx, cust_dataframe)
    else:
        print(Fore.RED + 'Customer does not exist')
        print(Fore.RESET)
        remove_customer()


def retrieve_branch_data():
    # Creating a list of eit options for name, country and address:
    print('\nPress ')
    print('\t 1 - To edit a branch name')
    print('\t 2 - To edit a branch country')
    print('\t 3 - To edit a branch address')
    print('\t 4 - Back to main menu')

    try:
        choice = int(input('Enter your choice to edit: '))
        match choice:
            case 1:
                # Retrieve the branch dataframe:
                branch_df = pd.read_csv('C:\\****\\****\\Branch_Data.csv')

                # Retrieve the customer dataframe; this will be used to rfelect the changes in the customer dataframe too:
                customer_df = pd.read_csv('C:\\****\\****\\Customer_Data.csv')

                # Enter the branch key and see if it exists in the dataframe:
                branch_key = int(input('Enter branch key: '))
                if branch_key in branch_df['Branch_key'].values:
                    br_idx = branch_df.index[branch_df['Branch_key'] == branch_key].tolist()[0]
                    # Call the edit_branch function and pass the branch id, the dataframes and the column index:
                    Bank.edit_branch(br_idx, branch_df, customer_df, 1)
                else:
                    print(Fore.RED + 'Branch key does not exist')
                    print(Fore.RESET)
                    retrieve_branch_data()

            case 2:
                # Retrieve the branch dataframe:
                branch_df = pd.read_csv('C:\\****\\****\\Branch_Data.csv')

                # Retrieve the customer dataframe; this will be used to rfelect the changes in the customer dataframe too:
                customer_df = pd.read_csv('C:\\****\\****\\Customer_Data.csv')

                # Enter the branch key and see if it exists in the dataframe:
                branch_key = int(input('Enter branch key: '))
                if branch_key in branch_df['Branch_key'].values:
                    br_idx = branch_df.index[branch_df['Branch_key'] == branch_key].tolist()[0]
                    # Call the edit_branch function and pass the branch id, the dataframes and the column index:
                    Bank.edit_branch(br_idx, branch_df, customer_df, 2)
                else:
                    print(Fore.RED + 'Branch key does not exist')
                    print(Fore.RESET)
                    retrieve_branch_data()

            case 3:
                # Retrieve the branch dataframe:
                branch_df = pd.read_csv('C:\\****\\****\\Branch_Data.csv')

                # Retrieve the customer dataframe; this will be used to rfelect the changes in the customer dataframe too:
                customer_df = pd.read_csv('C:\\****\\****\\Customer_Data.csv')

                # Enter the branch key and see if it exists in the dataframe:
                branch_key = int(input('Enter branch key: '))
                if branch_key in branch_df['Branch_key'].values:
                    br_idx = branch_df.index[branch_df['Branch_key'] == branch_key].tolist()[0]
                    # Call the edit_branch function and pass the branch id, the dataframes and the column index:
                    Bank.edit_branch(br_idx, branch_df, customer_df, 3)
                else:
                    print(Fore.RED + 'Branch key does not exist')
                    print(Fore.RESET)
                    retrieve_branch_data()

            case 4:
                # Back to main menu:
                choose_options()

            case _:
                print(Fore.RED + 'Enter a valid option from the menu')
                print(Fore.RESET)
                retrieve_branch_data()
    except ValueError:
        print(Fore.RED + 'You must enter a valid input')
        print(Fore.RESET)
        retrieve_branch_data()


def retrieve_customer_data():
    print('\nPress ')
    print('\t 1 - To edit a customer name')
    print('\t 2 - To edit a customer address')
    print('\t 3 - To edit a customer phone number')
    print('\t 4 - Back to main menu')

    try:
        choice = int(input('Enter your choice to edit: '))
        match choice:
            case 1:
                # Retrieve the dataframe:
                customer_df = pd.read_csv('C:\\****\\****\\Customer_Data.csv')
                # Enter the account ID and see if it exists in the dataframe:
                account_ID = input('Enter account ID: ')
                if account_ID in customer_df['Account_ID'].values:
                    cust_idx = customer_df.index[customer_df['Account_ID'] == account_ID].tolist()[0]
                    # Call the edit_customer function and pass the customer index, the dataframe and the column index:
                    Branch.edit_customer(cust_idx, customer_df, 1)
                else:
                    print(Fore.RED + 'Account ID does not exist')
                    print(Fore.RESET)
                    retrieve_customer_data()

            case 2:
                # Retrieve the dataframe:
                customer_df = pd.read_csv('C:\\****\\****\\Customer_Data.csv')
                # Enter the account ID and see if it exists in the dataframe:
                account_ID = input('Enter account ID: ')
                if account_ID in customer_df['Account_ID'].values:
                    cust_idx = customer_df.index[customer_df['Account_ID'] == account_ID].tolist()[0]
                    # Call the edit_customer function and pass the customer index, the dataframe and the column index:
                    Branch.edit_customer(cust_idx, customer_df, 4)
                else:
                    print(Fore.RED + 'Account ID does not exist')
                    print(Fore.RESET)
                    retrieve_customer_data()

            case 3:
                # Retrieve the dataframe:
                customer_df = pd.read_csv('C:\\****\\****\\Customer_Data.csv')
                # Enter the account ID and see if it exists in the dataframe:
                account_ID = input('Enter account ID: ')
                if account_ID in customer_df['Account_ID'].values:
                    cust_idx = customer_df.index[customer_df['Account_ID'] == account_ID].tolist()[0]
                    # Call the edit_customer function and pass the customer index, the dataframe and the column index:
                    Branch.edit_customer(cust_idx, customer_df, 5)
                else:
                    print(Fore.RED + 'Account ID does not exist')
                    print(Fore.RESET)
                    retrieve_customer_data()

            case 4:
                # Back to main menu:
                choose_options()

            case _:
                print(Fore.RED + 'Enter a valid option from the menu')
                print(Fore.RESET)
                retrieve_customer_data()
    except ValueError:
        print(Fore.RED + 'You must enter a number from the menu')
        print(Fore.RESET)
        retrieve_customer_data()


class Bank:
    def __init__(self, bank_name, list_of_branches):
        self.bank_name = bank_name
        self.list_of_branches = list_of_branches

    @staticmethod
    def add_branch(list_of_branches, branch_name, branch_country, branch_address):
        # Creating a data list that will be added as a value in the list_of_branches dictionary:
        data = [branch_name, branch_country, branch_address]
        branch_data.append(data)

        # Reading the current csv into a dataframe, to check if values exist or not:
        branch_csv_to_df = pd.read_csv('C:\\****\\****\\Branch_Data.csv')

        try:
            branch_key = int(input('Enter key: '))

            # Check if the entered branch key exists in the dataframe;
            # if it does, recursively enter the branch info again:
            if branch_key in branch_csv_to_df['Branch_key'].values:
                print(Fore.RED + 'Key already exists, please try again')
                print(Fore.RESET)
                add_new_branch()
            else:
                list_of_branches.setdefault(branch_key, []).append(data)
        except ValueError:
            print(Fore.RED + 'Invalid key input. Please try again')
            print(Fore.RESET)
            add_new_branch()

        # Convert the branch dictionary into a dataframe:
        branch_to_dataframe(list_of_branches)

    @staticmethod
    def remove_branch_from_bank(idx, br_dataframe):
        # Remove the branch from dataframe:
        br_dataframe_updated = br_dataframe.drop(idx, axis=0, inplace=False)

        # Write back the dataframe into the csv:
        br_dataframe_updated.to_csv('C:\\****\\****\\Branch_Data.csv', index=False)

        # Return to main menu:
        choose_options()


    @staticmethod
    def edit_branch(br_idx, branch_df, customer_df, col_idx):
        # Retrieve the branch name based on the row and column id:
        branch_idx = branch_df.iloc[br_idx]
        branch_info = branch_idx.iloc[col_idx]

        branch_info_in_cust_df = branch_info

        # Create a new instance of the dataframe object to be updated:
        branch_df_updated = branch_df
        customer_df_updated = customer_df

        # Check if the column id passed is the branch name, and make it upper:
        if col_idx == 1:
            while len(br_name := input('Enter new branch information: ').upper()) != 3:
                print(Fore.RED + 'Number of characters must be 3')
                print(Fore.RESET)
            branch_df_updated.replace(branch_info, br_name.upper(), inplace=True)
        else:
            branch_df_updated.replace(branch_info, input('Enter new branch information: '), inplace=True)

        # Update the branch name in the customer dataframe:
        # 1. Retrieve the branch name based on the row and column id:
        branch_index = branch_df_updated.iloc[br_idx]
        branch_info_updated = branch_index.iloc[col_idx]
        # 2. Check if the branch name exists in the customer dataframe and update it:
        if branch_info_in_cust_df in customer_df_updated['Branch_name'].values:
            customer_df_updated.replace(branch_info_in_cust_df, branch_info_updated, inplace=True)

        # Write the updated dataframes back to csv:
        branch_df_updated.to_csv('C:\\****\\****\\Branch_Data.csv', index=False)

        customer_df_updated.to_csv('C:\\****\\****\\Customer_Data.csv', index=False)

        # Back to options menu:
        retrieve_branch_data()


class Branch:
    def __init__(self, branch_name, list_of_customers):
        self.branch_name = branch_name
        self.list_of_customers = list_of_customers

    @staticmethod
    def add_customer(cust_branch, list_of_customers):
        # Creating a data list that will be added as a value in the list_of_customers dictionary:
        data = []

        # Creating the key of the customer dictionary element:
        cust_key = cust_branch

        cust_name = input('Enter customer name: ')

        # Creating a unique identified for the customer in hexadecimal format:
        acc_id = uuid.uuid4().hex

        # Entering the date of birth in the right format:
        try:
            cust_DOB = datetime.datetime.strptime(input('Enter customer date of birth: '), '%d/%m/%Y')
        except ValueError:
            print(Fore.RED + 'Enter the date in this format d/m/YYYY')
            print(Fore.RESET)
            add_new_customer()

        # Entering the customer's address:
        cust_address = input('Enter customer address: ')

        # Entering the customer's telephone in the right format:
        try:
            while (len(cust_telephone := input('Enter customer telephone number: ')) < 10) or (len(cust_telephone) > 13):
                print(Fore.RED + 'Telephone number format is wrong')
                print(Fore.RESET)
            # Making sure the telephone number contains only integers:
            int(cust_telephone)
        except ValueError:
            print(Fore.RED + 'Telephone number must not contain letters. Please enter the right data')
            print(Fore.RESET)
            add_new_customer()

        if (acc_id not in list_of_customers.values()) or (acc_id not in customer_csv_to_df['Account_ID'].values):
            balance = float(input('Enter initial transaction: '))

            # Appending the data into the data list:
            data.append(cust_name)
            data.append(acc_id)
            data.append(cust_DOB.date())
            data.append(cust_address)
            data.append(cust_telephone)
            data.append(balance)

            # Updating the values list with the new customer data:
            list_of_customers.setdefault(cust_key, []).append(data)

            print(list_of_customers)

            # Convert the customer dictionary into a dataframe:
            customer_to_dataframe(list_of_customers)
        else:
            print(Fore.RED + 'Account can not be created as it already exists')
            print(Fore.RESET)
            Branch.add_customer(cust_branch, list_of_customers)

    @staticmethod
    def remove_customer_from_branch(idx, cust_dataframe):
        # Remove the customer from dataframe:
        cust_dataframe_updated = cust_dataframe.drop(idx, axis=0, inplace=False)

        # Write back the dataframe into the csv:
        cust_dataframe_updated.to_csv('C:\\****\\****\\Customer_Data.csv', index=False)

        # Return to main menu:
        choose_options()

    @staticmethod
    def edit_customer(cust_idx, customer_df, col_idx):
        # Retrieve the customer name based on the row and column id:
        customer_idx = customer_df.iloc[cust_idx]
        customer_info = customer_idx.iloc[col_idx]

        # Create a new instance of the dataframe object to be updated:
        customer_df_updated = customer_df

        # Check if the column id passed is the customer DOB, and abide by the format:
        try:
            if col_idx == 5:
                while (len(cust_telephone := input('Enter new customer information: ')) < 10) or (
                        len(cust_telephone) > 13):
                    print(Fore.RED + 'Telephone number format is wrong')
                    print(Fore.RESET)
                int(cust_telephone)
                customer_df_updated.replace(customer_info, cust_telephone, inplace=True)
            else:
                customer_df_updated.replace(customer_info, input('Enter new customer information: '), inplace=True)
        except ValueError:
            print(Fore.RED + 'Telephone number format is wrong')
            print(Fore.RESET)
            retrieve_customer_data()

        # Write the updated dataframe back to csv:
        customer_df_updated.to_csv('C:\\****\\****\\Customer_Data.csv', index=False)

        # Back to options menu:
        retrieve_customer_data()


class Customers:
    def __init__(self, deposit, withdrawal):
        self.deposit = deposit
        self.withdrawal = withdrawal

    @staticmethod
    def make_deposit(balance_value, cust_df, account_id):
        try:
            # Making the transaction:
            deposit = float(input('Enter deposit: '))
        except ValueError:
            print(Fore.RED + 'Invalid deposit. Please try again')
            print(Fore.RESET)
            Customers.make_deposit(balance_value, cust_df)

        # Creating the timestamp of the transaction:
        deposit_timestamp = Transaction.transaction_timestamp()

        # Calculating the balance after the transaction is made:
        dep_value = balance_value + deposit

        # Replace the old balance with the new calculated balance and export the new dataframe to csv:
        updated_customer_df = cust_df
        updated_customer_df.replace(balance_value, dep_value, inplace=True)
        updated_customer_df.to_csv('C:\\****\\****\\Customer_Data.csv', index=False)

        # Fetch the customer name with a specific account ID:
        idx = updated_customer_df.index[updated_customer_df['Account_ID'] == account_id].tolist()[0]
        row_idx = updated_customer_df.iloc[idx]
        cust_name = row_idx.iloc[1]

        # Assign the withdrawal value with None:
        wtd_value = None

        # Call the add_transaction function and pass the necessary parameters:
        Transaction.add_transaction(account_id, cust_name, deposit, wtd_value, deposit_timestamp)

        # Back to the main menu:
        choose_options()

    @staticmethod
    def make_withdrawal(balance_value, cust_df, account_id):
        try:
            # Making the transaction:
            withdrawal = float(input('Enter withdrawal: '))
        except ValueError:
            print(Fore.RED + 'Invalid withdrawal. Please try again')
            print(Fore.RESET)
            Customers.make_withdrawal(balance_value, cust_df)

        # Creating the timestamp of the transaction:
        withdrawal_timestamp = Transaction.transaction_timestamp()

        # Calculating the balance after the transaction is made:
        wd_value = balance_value - withdrawal

        # Replace the old balance with the new calculated balance and export the new dataframe to csv:
        updated_customer_df = cust_df
        updated_customer_df.replace(balance_value, wd_value, inplace=True)
        updated_customer_df.to_csv('C:\\****\\****\\Customer_Data.csv', index=False)

        # Fetch the customer name with a specific account ID:
        idx = updated_customer_df.index[updated_customer_df['Account_ID'] == account_id].tolist()[0]
        row_idx = updated_customer_df.iloc[idx]
        cust_name = row_idx.iloc[1]

        # Assign the deposit value with None:
        dp_value = None

        # Call the add_transaction function and pass the necessary parameters:
        Transaction.add_transaction(account_id, cust_name, dp_value, withdrawal, withdrawal_timestamp)

        # Back to the main menu:
        choose_options()

    @staticmethod
    def print_cust_balance(account_id, cust_df):
        # Searching for the account id in the dataframe and printing the row where the id belongs:
        updated_customer_df = cust_df
        balance_sheet = updated_customer_df.loc[updated_customer_df['Account_ID'] == account_id]
        print(balance_sheet)

        # Back to the main menu:
        choose_options()


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

        # Converting the dictionary of transactions into a dataframe:
        transaction_to_dataframe(list_of_transactions)

    @staticmethod
    def print_bank_statement(account_id, trans_df):
        # Searching for the account id in the dataframe and printing the row where the id belongs:
        updated_trans_df = trans_df
        bank_statement = updated_trans_df.loc[updated_trans_df['Account_ID'] == account_id]
        print(bank_statement)

        # Back to the main menu:
        choose_options()

    @staticmethod
    def transaction_timestamp():
        # Getting the current time:
        current_time = datetime.datetime.now()

        # Changing the format of the current time:
        trans_ts = datetime.datetime.strftime(current_time, '%H:%M:%S %m/%d/%Y')
        return trans_ts


if __name__ == '__main__':
    customer_options()
