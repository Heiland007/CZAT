from flask import Flask
from flask import request
import pymysql
import pandas as pd

#odpowiedź zwrotan po zapytaniu, bazowo null, brak działania/error
odp = 'null'

#logowanie do bazy danych
db = pymysql.connect(host='127.0.0.1',user='root', database='users')

cursor = db.cursor()

row = []

app = Flask(__name__)

@app.route('/login', methods=['GET'])
def login():
    global cursor
    global save
    global check
    global odp
    global row

    #pobranie danych z zapytania
    log = request.args.get('log')
    log = str(log)
    pas = request.args.get('pas')
    pas = str(pas)

    #budowa zapytania o istniejacego urzytkownika(logowanie)
    logc = "user='"+log+"'"

    pasc = " password='"+pas+"'"

    step = logc + " and " + pasc

    end = "Select * From login WHERE "+step

    cursor.execute(end)

    #zmiana znaków w pobranych danych
    for row in cursor:
        save = str(row)
        check = save.replace("(", "[").replace(")", "]")

    #sprawdzenie porawności podanych danych
    if check.__contains__(log) == True and check.__contains__(pas) == True:
        odp = '1'
    else:
        odp = '0'

    #informaja zwrotna
    return odp

@app.route('/register', methods=['GET'])
def register():

    global log
    global logc
    global email
    global user
    global cursor
    global odp
    global err1
    global err2

    #pobranie danych z zapytania
    log = request.args.get('log')
    log = str(log)
    pas = request.args.get('pas')
    pas = str(pas)
    email = request.args.get('email')
    email = str(email)

    #budowa polecenia SQL do dodania urzytkownika
    logc = "user='"+log+"'"

    pasc = "'" + pas + "'"

    emailc = "email='" + email + "'"

    log = "'"+log+"'"

    email = "'"+email+"'"

    val = "(" + log + "," + pasc + "," + email + ")"

    inse = "INSERT INTO login(USER, PASSWORD, EMAIL) VALUES"

    end = inse + val

    find = "" + end + ""

    #próba dodania urzytkownaka, informacja o powidzeniu bądź nie
    try:
        # Executing the SQL command
        cursor.execute(find)

        # Commit your changes in the database
        db.commit()

        odp = '1'

        if odp == '1':
            cursor.execute("SELECT ID FROM login ORDER BY ID")
            for i in cursor:
                user = str(i)
                user = user.replace("(", "'").replace(",)", "'")

            find = "INSERT INTO friends(USER_ID) VALUES" + '(' + user + ')'

            cursor.execute("" + find + "")

            db.commit()

    except:
        # Rolling back in case of error
        db.rollback()

        odp = '(0, 0)'

        step1 = "Select * From login WHERE "+logc

        step2 = "Select * From login WHERE "+emailc

        cursor.execute(step1)
        for a in cursor:
            print(a)
            err1 = str(a)

        cursor.execute(step2)
        for b in cursor:
            print(b)
            err2 = str(b)

        if len(err1) == 0:
            log = '1'
        else:
            log = '0'

        if len(err2) == 0:
            email = '1'
        else:
            email = '0'

        odp = "(" + log + "," + email + ")"

    #informacja zwrotna
    return odp

@app.route('/profile', methods=['GET'])
def friends():
    global odp
    global cursor
    global save
    global list

    #identyfikacja urzytkowanika
    log = request.args.get('log')
    log = str(log)
    logc = "user='"+log+"'"
    end = "SELECT ID FROM login WHERE "+logc

    cursor.execute(end)

    #zmiana znakow do wyszukiwania
    for row in cursor:
        save = str(row)
        save = save.replace("(", "'").replace(",)", "'")

    print(save)

    #pobranie listy znajomych urzytkowika
    frie = "SELECT friends_id FROM friends WHERE user_id=" + save

    cursor.execute(frie)

    for row in cursor:
        list = str(row)
        list = list.replace("(", "").replace(",)", "")

    #Pobiueranie nazw użytkowników do wysłania
    odpo = "SELECT User FROM login WHERE ID=" + list

    cursor.execute(odpo)

    for row in cursor:
        tt = str(row)
        tt = tt.replace("(", "").replace(",)", "")

    print(list)
    print(tt)
    odp = tt

    #informacja zwrotna
    return odp

#określenie działajacego portu na jakim ma działać app
app.run(port=3000)

#from flask import Flask
#from flask import request
#import pymysql
#import pandas as pd

#odpowiedź zwrotan po zapytaniu, bazowo null, brak działania/error
#odp = 'null'

##logowanie do bazy danych
#db = pymysql.connect(host='127.0.0.1',user='root', database='users')

#cursor = db.cursor()

#row = []

#app = Flask(__name__)

@app.route('/login_python', methods=['GET'])
def login():
    global cursor
#    global save
#    global check
#    global odp
#    global row

    #pobranie danych z zapytania
    log = request.args.get('log')
    log = str(log)
    pas = request.args.get('pas')
    pas = str(pas)

    #budowa zapytania o istniejacego urzytkownika(logowanie)
#    logc = "user='"+log+"'"

#    pasc = " password='"+pas+"'"

#    step = logc + " and " + pasc

#    end = "Select * From login WHERE "+step

#    cursor.execute(end)

#    #zmiana znaków w pobranych danych
#    for row in cursor:
#        save = str(row)
#        check = save.replace("(", "[").replace(")", "]")

#    #sprawdzenie porawności podanych danych
#    if check.__contains__(log) == True and check.__contains__(pas) == True:
#        odp = '1'
#    else:
#        odp = '0'

#    #informaja zwrotna
    return odp
