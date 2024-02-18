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


#print('essas poha toda deu certo')


conn.commit()
conn.close()
