# Bibliotech
Bibliotech app

    "Bibliotech" is the backend of a book renting app and it was created in Python Flask. 
This was a required task in module three of the courses I took at the 'Academia te fac programator'. 
It uses 4 .txt files to store the data:(DB_books,DB_reviews,DB_transactions,DB_users).
 In addition to the task’s requirements            
I created an algorithm that reads the text files and increment the number of the next item 
that will be added in the file to mimic the auto increment of a real database

https://github.com/Adelin04/Bibliotech/blob/main/Tema-punct%20bonus-Modul3-TFP.pdf

Endpoints
- POST: /register
- POST: /login
- POST: /Post-book
- POST: /Post-books
- GET: /Get-book/<book_id>
- GET: /Get-books
- POST: /Post-transaction
- GET: /Get-transaction/<transaction_id>
- GET : /Get-transactions
- POST : /Post-review
