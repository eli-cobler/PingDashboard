import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from datetime import datetime
from ping_dashboard.data.modelbase import SqlAlchemyBase

# Setting log date format for all print statements
# Uses timezone set on the server
log_date_time = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

__factory = None

def global_init(db_file: str):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("You must specify a db file.")

    conn_str = 'sqlite:///' + db_file.strip()
    print(f"{log_date_time} Connecting to DB with {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    import ping_dashboard.data.__all_models
    SqlAlchemyBase.metadata.create_all(engine)

def create_session() -> Session:
    global __factory
    return __factory()