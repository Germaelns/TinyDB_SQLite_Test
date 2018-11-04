from tinydb import TinyDB, Query, JSONStorage
from tinydb.middlewares import CachingMiddleware
import os, time, sqlite3, random


def removeTrash():
    try:
        os.remove('tiny.json')
        os.remove('tiny_middleware.json')
        os.remove('lite.db')
        os.remove('result.txt')
    except FileNotFoundError:
        pass
    except PermissionError:
        print(PermissionError)
        os.system('sudo chmod -R 777 tiny.json')
        os.system('sudo chmod -R 777 tiny_middleware.json')
        os.system('sudo chmod -R 777 lite.db')
        os.system('sudo chmod -R 777 result.txt')
        removeTrash()


def tests():
    # Create TinyDB database and insert information

    db_tiny = TinyDB('tiny.json')
    queryTiny = Query()
    count = 0
    print("\nadding information into TinyDB...\n")
    while count < 5000:
        db_tiny.insert({'id': count, 'text': str(random.random())})
        count = count + 1
    print("adding information into TinyDB complete\n")

    # Create SQLite database and insert information

    db_lite = sqlite3.connect('lite.db')
    queryLite = db_lite.cursor()
    queryLite.execute('''CREATE TABLE Strings
                         (id int PRIMARY KEY,text text)''')
    print("adding information into sqlite...\n")
    count = 0
    while count < 5000:
        queryLite.execute("INSERT INTO Strings (id, text) VALUES (" + str(count) + "," + str(random.random()) + ")")
        count = count + 1
    print("adding information into sqlite complete\n")
    db_lite.commit()

    # First test queries

    print("First test\n")
    start_time = time.clock()
    db_tiny.search(queryTiny.id == 4800)  # Query to TinyDB
    timeTiny = (time.clock() - start_time)
    queryLite.execute('''Select * FROM Strings WHERE id=4800''')
    timeLite = ((time.clock() - start_time) - timeTiny)

    print(timeTiny)
    print(timeLite)

    # Create TinyDB database with CachingMiddleware and insert information

    db_tiny_middle = TinyDB('tiny_middleware.json', storage=CachingMiddleware(JSONStorage))
    queryTinyMiddle = Query()
    count = 0
    print("\nadding information into TinyDB CachingMiddleware...\n")
    while count < 5000:
        db_tiny_middle.insert({'text': str(random.random()), 'id': count})
        count = count + 1
    print("adding information into TinyDB CachingMiddleware complete\n")

    # Second test queries

    print("Second test\n")
    start_time = time.clock()
    db_tiny_middle.search(queryTinyMiddle.id == 4800)  # Query to TinyDB
    timeTiny_2 = (time.clock() - start_time)
    queryLite.execute('''Select * FROM Strings WHERE id=4800''')
    timeLite_2 = ((time.clock() - start_time) - timeTiny_2)

    db_lite.close()

    return [timeTiny * 1000, timeLite * 1000, timeTiny_2 * 1000, timeLite_2 * 1000]


removeTrash()
result = tests()
report = "First test:\nTinyDB query time: "+ str(result[0]) +" mc\nSQLite query time: "+ str(result[1]) +" mc\n\n" \
                                                                                                        "Second test (CachingMiddleware):\nTinyDB query time: "+ str(result[2]) +" mc\nSQLite query time: "+ str(result[3]) +" mc\n"

print(report, file=open('result.txt', 'w'))
print(report)