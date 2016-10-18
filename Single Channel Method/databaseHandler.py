import sqlite3 as sql
import sys, argparse

#this allows the user to open up and edit any database on the computer
def main(database):
    try:
        #starts up the server and prints out the version
        con = sql.connect(database)
        cur = con.cursor()

        cur.execute('SELECT SQLITE_VERSION()')
        data = cur.fetchone()

        print(data)
        print('-' * 25)

    except:
        print('Error: ' + sys.exc_info()[0])
        print('Attempting to reconnect with database')
        main(database)
        sys.exit(0)

    
    command = ""
    while command != 'wq':
        #run and executes sql commands as long as the user hasn't put in wq
        command = input(">> ")

        if command != 'wq' or 'help':
            try:
                cur.execute(command)    
                
            except:
                print('Error: ' + sys.exc_info()[0])

        #displays some useful sql commands
        elif command == 'help':
            print('\nUseful Commands:')
            print('CREATE, EX: CREATE TABLE Cars(Id INT, Name TEXT, Price INT)')
            print('INSERT, EX: INSERT INTO Cars VALUES(8, \'Volkswagen\', 21600)')
            print('SELECT, EX: SELECT * FROM Cars, or SELECT Id FROM Cars WHERE Name = \'Toyota\'')
            print('UPDATE, EX: UPDATE Cars SET Price = ? WHERE Id = ?, (newPrice, ID)')
            print('DROP TABLE IF EXISTS Cars')
            print('Note: If select is in your command, all of the returned data will be printed\n')

            try:
                con.commit()
            except:
                print('Commit Error: ' + sys.exc_info()[0])
                print('Rolling back changes')
                con.rollback()

        if 'SELECT' in command:
            rows = cur.fetchall()
            for row in rows:
                print(row)

        
    con.close()

if __name__ == '__main__': #the database name that you will connect to must be entered
    parser = Argument_Parser()
    parser.add_argument('database', help='The database you wish to edit', type= str)

    args = parser.parse_args()

    main(args.database)