from db import Base, engine
from gui.main_screen import create_main_screen

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    create_main_screen()