from flask import Flask, request, redirect, jsonify, make_response, json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import os.path
from AutoIncrement import AutoIncrement

app = Flask(__name__)
jwt = JWTManager(app)
app.config['SECRET_KEY'] = 'SECRET_KEY_BIBLIOTECH'
# now_date = datetime.datetime.today()

_Acces_Token = ''
_Status_Book = ['împrumutată', 'disponibilă', 'blocată']
_Type_User = ['admin', 'user_normal']
_CurrentUser = ''
_NrTranzactii = 0

DB_users = 'DB_users'
_DataUsers = []
start_IncrementUser = 1
autoincrement_user = AutoIncrement(start_IncrementUser, DB_users)

DB_books = 'DB_books'
_DataBooks = []
start_IncrementBook = 1
autoincrement_book = AutoIncrement(start_IncrementBook, DB_books)

DB_transactions = 'DB_transactions'
_DataTransactions = []
start_IncrementTransaction = 1
autoincrement_transaction = AutoIncrement(
    start_IncrementTransaction, DB_transactions)

DB_reviews = 'DB_reviews'
_DataReviews = []
start_IncrementReview = 1
autoincrement_review = AutoIncrement(
    start_IncrementReview, DB_reviews)


def Write_File(fileName, autoincrement, *args):
    with open(str(fileName)+'.txt', 'a+')as file:
        newData = str(autoincrement.next_id()) + ','
        for data in args:
            newData += data + ','
        file.writelines(newData + '\n')


def Read_File_User(fileName):
    with open(str(fileName) + '.txt', 'r') as file:
        lines = file.readlines()

        for line in lines:
            stripLine = line.strip()
            if stripLine == '':
                continue

            data_user = stripLine.split(',')
            _DataUsers.append({
                'id': data_user[0],
                'first_name': data_user[1],
                'last_name': data_user[2],
                'email': data_user[3],
                'password': data_user[4],
                'type': data_user[5],
            })

    return _DataUsers


def Exist_Data(Data, _List):
    for obj in _List:
        if Data in obj.values():
            return True


@ app.route('/register', methods=['GET', 'POST'])
def Register():
    emptyList = False
    if not os.path.exists('DB_users.txt'):
        emptyList = True
        with open('DB_users.txt', 'w'):
            pass
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        typeUser = request.form['typeUser']

        userData = {}
        userData['first_name'] = first_name
        userData['last_name'] = last_name
        userData['email'] = email
        userData['password'] = password
        userData['typUser'] = _Type_User[int(typeUser)]

        if not emptyList:
            allUsers = Read_File_User(DB_users)
            if not Exist_Data(email, allUsers):
                Write_File(DB_users, autoincrement_user, first_name, last_name,
                           email, password, _Type_User[int(typeUser)])
                return make_response(jsonify(userData), 200)
            else:
                return {'error': f'Pentru adresa de email {email} exista deja un cont creat!'}
        else:
            Write_File(DB_users, autoincrement_user, first_name, last_name,
                       email, password, typeUser)
            return make_response(jsonify(userData), 200)
    return {'response': 'Error'}


@app.route('/login', methods=['GET', 'POST'])
def Login():
    global _Acces_Token
    global _CurrentUser
    auth_token = {}
    emptyList = False

    if not os.path.exists('DB_users.txt'):
        emptyList = True
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        if not emptyList:
            allUsers = Read_File_User(DB_users)

            for user in allUsers:
                user_firstName = user['first_name']
                user_lastName = user['last_name']
                _CurrentUser = f'{user_firstName} {user_lastName}'
                # print(_CurrentUser)
            if Exist_Data(email,  allUsers):
                if Exist_Data(password, allUsers):
                    _Acces_Token = create_access_token(identity=email)
                    auth_token = {'token': _Acces_Token}
                    # print(auth_token)
                    return {'token': auth_token}
                else:
                    return {'response': 'Parola gresita!'}
            else:
                return {'response': 'Adresa de email nu corespunde!'}
        else:
            return {'Error': 'Nu exista useri inregistrati!'}
    else:
        return {'response': 'Error'}


def Read_File_book(fileName):
    with open(str(fileName) + '.txt', 'r') as file:
        lines = file.readlines()

        for line in lines:
            stripLine = line.strip()
            if stripLine == '':
                continue

            data_book = stripLine.split(',')
            _DataBooks.append({
                'id': data_book[0],
                'book_name': data_book[1],
                'book_author': data_book[2],
                'book_description': data_book[3],
            })

    return _DataBooks


@ app.route('/Post-book', methods=['GET', 'POST'])
def Book():
    _DataBooks.clear()
    emptyList = False
    if not os.path.exists('DB_books.txt'):
        emptyList = True
        with open('DB_books.txt', 'w'):
            pass
    if request.method == "POST":
        id_book = autoincrement_book
        book_name = request.form['book_name']
        book_author = request.form['book_author']
        book_description = request.form['book_description']

        if not emptyList:
            if _Acces_Token:
                allBooks = Read_File_book(DB_books)
                if not Exist_Data(book_name, allBooks):
                    Write_File('DB_books', id_book, book_name,
                               book_author, book_description)
                    bookData = {}
                    bookData['id'] = id_book.Get_ID()
                    bookData['book_name'] = book_name
                    bookData['book_author'] = book_author
                    bookData['book_description'] = book_description

                    return make_response(jsonify(bookData))
                else:
                    return {'response': 'Cartea este deja inregistrata!'}
            else:
                return {'response': 'Please Login'}
        else:
            Write_File('DB_books', id_book, book_name,
                       book_author, book_description)
            bookData = {}
            bookData['id'] = id_book.Get_ID()
            bookData['book_name'] = book_name
            bookData['book_author'] = book_author
            bookData['book_description'] = book_description
            return make_response(jsonify(bookData))
    else:
        return {'response': 'Error'}


@ app.route('/Post-books', methods=['POST'])
def Post_books():
    _DataBooks.clear()
    allBooks = Read_File_book(DB_books)
    Exist_BookName = ''
    New_Book = ''
    bookData = {}
    if request.is_json:
        books = request.get_json()

        for book in books:
            if not Exist_Data(book["book_name"], allBooks):
                New_Book += book['book_name'] + '/'
                Write_File('DB_books', autoincrement_book, book['book_name'],
                           book['book_author'], book['book_description'])
            else:
                Exist_BookName += book['book_name'] + '/'
    return{'response': f'Cartea/Cartile {Exist_BookName} exista deja in Bibliotech'}


@app.route('/Get-book/<book_id>', methods=['GET'])
def Get_Book(book_id):
    _DataBooks.clear()
    if request.method == 'GET':
        allBooks = Read_File_book(DB_books)
        reviews = Read_File_Review(DB_reviews)
        if _Acces_Token:
            bookData = {}
            bookReview = {}
            for review in reviews:
                if book_id == review['book_id']:
                    bookReview['book_id'] = review['book_id']
                    bookReview['book_rating'] = review['book_rating']
                    bookReview['book_review'] = review['text']
                    bookReview['author_review'] = review['author_review']
            #print('review ->', bookReview)
            
            for book in allBooks:
                if book_id == book['id']:
                    bookData['id'] = book['id']
                    bookData['book_name'] = book['book_name']
                    bookData['book_author'] = book['book_author']
                    bookData['book_description'] = book['book_description']
                    bookData['book_status'] = _Status_Book[1]
                    bookData['book_rating'] = bookReview['book_rating']
                    bookData['book_review'] = bookReview['book_review']
                    bookData['author_review'] = bookReview['author_review']
                    return {f'Books {book_id}': bookData}
                else:
                    No_review = {}
                    for book in allBooks:
                        if book_id == book['id']:
                            No_review['id'] = book['id']
                            No_review['book_name'] = book['book_name']
                            No_review['book_author'] = book['book_author']
                            No_review['book_description'] = book['book_description']
                            No_review['book_status'] = _Status_Book[1]
                            return {f'Books {book_id}': No_review}
        else:
            for book in allBooks:
                if book_id == book['id']:
                    SignOut_User = {}
                    SignOut_User['id'] = book['id']
                    SignOut_User['book_name'] = book['book_name']
                    SignOut_User['book_author'] = book['book_author']
                    SignOut_User['book_description'] = book['book_description']
                    SignOut_User['book_status'] = _Status_Book[1]
                    return {f'Books {book_id}': SignOut_User}
    return {'response': f'Book {book_id} does not exist!'}


@ app.route('/Get-books', methods=['GET'])
def Get_Books():
    _DataBooks.clear()
    allBooks = Read_File_book(DB_books)
    if _Acces_Token:
        if allBooks.__len__() > 0:
            return {'Books': allBooks}
        else:
            return {'Response': 'Nu sunt carti disponibile!'}
    return {'response': 'Please Login'}


@ app.route('/Post-transaction', methods=['GET', 'POST'])
def Post_Transaction():
    _DataBooks.clear()
    global _NrTranzactii
    if request.method == "POST":
        book_id = request.form['book_id']
        borrow_time = request.form['borrow_time']

        if _Acces_Token:
            allBooks = Read_File_book(DB_books)
            TMP_BookName = ''
            for book in allBooks:
                if book['id'] == book_id:
                    TMP_BookName = book['book_name']

            if Exist_Data(book_id, allBooks):
                if int(borrow_time) <= 20:
                    if _NrTranzactii <= 5:
                        Write_File(DB_transactions, autoincrement_transaction,
                                   book_id, borrow_time)
                        _NrTranzactii += 1
                    else:
                        return {'response': 'Nu poti imprumuta mai mult de 5 carti'}
                else:
                    return {'response': 'Cartea nu poate fi imprumutata pe o perioada mai mare de 25 de zile'}
                return {'success': f'Ai imprumutat cartea {TMP_BookName}', 'transactions_id': autoincrement_transaction.Get_ID()}
            else:
                return {'response': f'Book {book_id} does not exist!'}
        else:
            return {'response': 'Please Login'}

    return {'response': 'Error'}


def Read_File_Transaction(fileName):
    with open(str(fileName) + '.txt', 'r') as file:
        lines = file.readlines()

        for line in lines:
            stripLine = line.strip()
            if stripLine == '':
                continue

            data_transaction = stripLine.split(',')
            _DataTransactions.append({
                'id': data_transaction[0],
                'book_id': data_transaction[1],
                'borrow_time': data_transaction[2],
            })

    return _DataTransactions


@ app.route('/Get-transaction/<transaction_id>', methods=['GET'])
def Get_Transaction(transaction_id):
    _DataTransactions.clear()
    emptyList = False
    if not os.path.exists('DB_transactions.txt'):
        emptyList = True
        with open('DB_transactions.txt', 'w'):
            pass
    if request.method == 'GET':
        if not emptyList:
            if _Acces_Token:
                allTransactions = Read_File_Transaction(DB_transactions)
                for transaction in allTransactions:
                    if transaction_id == transaction['id']:
                        TMP_transaction = {}
                        TMP_transaction['id'] = transaction['id']
                        TMP_transaction['book_id'] = transaction['book_id']
                        TMP_transaction['borrow_time'] = transaction['borrow_time']
                        return {f'Transaction {transaction_id}': TMP_transaction}
                return {'response': f'Transaction {transaction_id} does not exist!'}
            else:
                return {'response': 'Please Login'}
        else:
            return {'response': 'Lista de tranzactii este goala'}
    return {'response': 'Error'}


@ app.route('/Get-transactions', methods=['GET'])
def Get_Transactions():
    _DataTransactions.clear()
    emptyList = False
    if not os.path.exists('DB_transactions.txt'):
        emptyList = True
        with open('DB_transactions.txt', 'w'):
            pass
    if request.method == 'GET':
        if not emptyList:
            if _Acces_Token:
                allTransactions = Read_File_Transaction(DB_transactions)
                return {'Transactions': allTransactions}
            else:
                return {'response': 'Please Login'}
        else:
            return {'Response': 'Lista de tranzactii este goala!'}
    else:
        return {'response': 'Error'}


def Read_File_Review(fileName):
    with open(str(fileName) + '.txt', 'r') as file:
        lines = file.readlines()

        for line in lines:
            stripLine = line.strip()
            if stripLine == '':
                continue

            data_review = stripLine.split(',')
            _DataReviews.append({
                'id': data_review[0],
                'book_id': data_review[1],
                'book_rating': data_review[2],
                'text': data_review[3],
                'author_review': data_review[4]
            })

    return _DataReviews


@ app.route('/Post-review', methods=['GET', 'POST'])
def Review():
    _DataBooks.clear()
    if not os.path.exists('DB_reviews.txt'):
        with open('DB_reviews.txt', 'w'):
            pass
    if request.method == "POST":
        book_id = request.form['book_id']
        rating = request.form['rating']
        text = request.form['text']

        if _Acces_Token:
            allBooks = Read_File_book(DB_books)
            if Exist_Data(book_id, allBooks):
                Write_File('DB_reviews', autoincrement_review,
                           book_id, rating, text, _CurrentUser)

                return {'responese': 'Success'}
            else:
                return {'response': 'Cartea nu este inregistrata'}
        else:
            return {'response': 'Please Login'}
    else:
        return {'response': 'Error'}


if __name__ == "__main__":
    app.run(debug=True)


# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
