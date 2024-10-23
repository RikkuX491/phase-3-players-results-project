from models.player import Player
from models.result import Result

def seed_database():
    Result.drop_table()
    Player.drop_table()
    Player.create_table()
    Result.create_table()

    Player.create("alice123")
    Player.create("bob456")

    Result.create(10, 1)
    Result.create(12, 2)
    Result.create(20, 1)

seed_database()
print("🌱 Players and Results successfully seeded! 🌱")