import sqlite3

conn = sqlite3.connect('cards.db')
cursor = conn.cursor()

""" cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE,
                    password TEXT
                )''') """

#cursor.execute("""
#INSERT INTO users (email, password)
#VALUES('daianeraimann@gmail.com', 'doga123')
#               """)

#cursor.execute('''ALTER TABLE flash_cards ADD COLUMN tema''')
'''
cursor.execute("""  
    ALTER TABLE flash_cards 
    ADD COLUMN data_hora_revisao DATETIME  
""")

cursor.execute(""" 
    UPDATE flash_cards
    SET data_hora_revisao = CURRENT_TIMESTAMP
""")

cursor.execute(""" 
    ALTER TABLE flash_cards
    ADD COMUMN acertou BOOLEAN DEFAULT NULL

""")
'''

'''cursor.execute(""" 
    ALTER TABLE flash_cards 
    ADD COLUMN id 
""")

cursor.execute(""" 
    UPDATE flash_cards
    SET id = INTERGER PRIMARY KEY AUTOINCREMENT
""")'''

'''cursor.execute(""" 
    CREATE TABLE flash_cards_lgpd AS
    SELECT * FROM flash_cards
    WHERE 1 = 0;

""")'''
cursor.execute(""" UPDATE flash_cards SET acertou = NULL;
 """)

"""for row in cursor.fetchall():
    print(row)"""



print('zerou saporra')


conn.commit()
conn.close()
