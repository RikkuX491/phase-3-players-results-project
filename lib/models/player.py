from models.__init__ import CONN, CURSOR

class Player:

    all = []
    
    def __init__(self, username):
        self.username = username
        self.id = None

    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, value):
        if type(value) == str:
            self._username = value
        else:
            raise TypeError("Username must be a string!")
        
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY,
                username TEXT
            )
        """

        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS players
        """

        CURSOR.execute(sql)

    def save(self):
        sql = """
            INSERT INTO players (username)
            VALUES (?)
        """

        CURSOR.execute(sql, (self.username,))
        CONN.commit()

        self.id = CURSOR.lastrowid

        Player.all.append(self)

    @classmethod
    def create(cls, username):
        player = cls(username)
        player.save()
        return player
    
    @classmethod
    def instance_from_db(cls, row):
        player = cls(row[1])
        player.id = row[0]
        return player
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM players
        """

        rows = CURSOR.execute(sql).fetchall()
        cls.all = [cls.instance_from_db(row) for row in rows]
        return cls.all
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM players
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()

        if row:
            return cls.instance_from_db(row)
        else:
            return None
    
    def results(self):
        from models.result import Result

        sql = """
            SELECT * FROM results
            WHERE player_id = ?
        """

        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Result.instance_from_db(row) for row in rows]
        
    def __repr__(self):
        return f"<Player # {self.id}: Username = {self.username}>"