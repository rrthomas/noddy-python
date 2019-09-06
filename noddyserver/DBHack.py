import sqlite3

class DBHack:
    def __init__(self, file):
        self.conn = sqlite3.connect(file)

    def list(self):
        errors = []

        try:
            results = [license[0] for license in self.conn.cursor().execute("select license from noddysync").fetchall()]
        except sqlite3.Error as e:
            errors.append(e.args[0])

        return results, errors

    def recreate(self):
        results, errors = [], []
        
        try:
            self.conn.cursor().execute("drop table noddysync")
            self.conn.commit()
        except sqlite3.Error as e:
            errors.append(e.args[0])
        
        try:
            self.conn.cursor().execute("create table noddysync(license text)")
            self.conn.commit()
        except sqlite3.Error as e:
            errors.append(e.args[0])
        return results, errors

    def insert(self, license):
        results, errors = [], []

        try:
            self.conn.cursor().execute("insert into noddysync values(?)",  (license,))
            self.conn.commit()
        except sqlite3.Error as e:
            errors.append(e.args[0])

        return results, errors
