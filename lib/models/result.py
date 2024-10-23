from models.__init__ import CONN, CURSOR

class Result:
    
    all = []

    def __init__(self, score, player_id):
        self.score = score
        self.player_id = player_id
        self.id = None

    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, value):
        if type(value) == int:
            self._score = value
        else:
            raise TypeError("Score must be an integer!")
        
    @property
    def player_id(self):
        return self._player_id
    
    @player_id.setter
    def player_id(self, value):
        if type(value) == int:
            self._player_id = value
        else:
            raise TypeError("Player id must be an integer!")
        
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY,
                score INTEGER,
                player_id INTEGER
            )
        """

        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE results
        """

        CURSOR.execute(sql)

    def save(self):
        sql = """
            INSERT INTO results (score, player_id)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.score, self.player_id))
        CONN.commit()

        self.id = CURSOR.lastrowid

        Result.all.append(self)

    @classmethod
    def create(cls, score, player_id):
        result = cls(score, player_id)
        result.save()
        return result
    
    @classmethod
    def instance_from_db(cls, row):
        result = cls(row[1], row[2])
        result.id = row[0]
        return result
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM results
        """

        rows = CURSOR.execute(sql).fetchall()
        cls.all = [cls.instance_from_db(row) for row in rows]
        return cls.all
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM results
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()

        if row:
            return cls.instance_from_db(row)
        else:
            return None
    
    def player(self):
        from models.player import Player

        sql = """
            SELECT * FROM players
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (self.player_id,)).fetchone()

        if row:
            return Player.instance_from_db(row)
        else:
            return None

    def __repr__(self):
        return f"<Result # {self.id}: Score = {self.score}, Player ID = {self.player_id}>"