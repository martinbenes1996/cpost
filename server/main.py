
import db
import cache

def run():
    db.initialize()
    cache.fill_db()

if __name__ == "__main__":
    run()