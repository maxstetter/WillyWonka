import sqlite3

#dict_factory turns tuples into dictionaries.
def dict_factory(cursor, row): 
    d = {}
    for idx, col in enumerate( cursor.description ):
        d[ col[0] ] = row[ idx ]
    return d

class Tickets():
    
    def __init__(self):
        self.connection = sqlite3.connect("ticket_collection.db")
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    def getAllTickets(self):
        self.cursor.execute( "SELECT * FROM tickets" )
        tickets = self.cursor.fetchall()
        return tickets

    def createTicket(self, ename, eage, gname, rtoken ):
        data = [ename, eage, gname, rtoken]
        self.cursor.execute("INSERT INTO tickets (entrant_name, entrant_age, guest_name, random_token) VALUES (?, ?, ?, ?)", data)
        self.connection.commit()