This program written in Python entails the following features:
1. Adding a new bank branch
2. Adding customers to branch
3. Making deposits and withdrawals
4. Printing the customer's balance
5. Printing the customer's bank statement
6. Editing branch and customer specific data
7. Removing a branch from a bank
8. Removing a customer from a branch

The program is designed as follows:
- The user can create credentials that will be stored in a csv file, in which the user will be authenticated against when trying to login
- All data for branches, customers and transactions are stored in csv files, and copied to postgres database
- Any edit or delete in branch data, will be reflected in all relevant tables
- Transactions will be stored in a transaction table and update the customer balance accordingly
- The printing feature reads from the database table into a pandas dataframe, and the latter will be queried accordingly

This program does not use any GUI, at least at the moment, however, this will be done in a future release.
    
    
