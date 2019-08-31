# init_db.py
from sqlalchemy import create_engine, MetaData

from settings import config
from models import users, permissions


DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[users, permissions])

#def upgrade(migrate_engine):
#    meta = MetaData(bind=migrate_engine)
#    account = Table('account', meta, autoload=True)
#    emailc = Column('email', String(128))
#    emailc.create(account)


#def downgrade(migrate_engine):
#    meta = MetaData(bind=migrate_engine)
#    account = Table('account', meta, autoload=True)
#    account.c.email.drop()

def sample_data(engine):
    conn = engine.connect()
    conn.execute(users.insert(), [
        {'id': 1,
         'login': 'admin',
         'passwd':'$5$rounds=535000$2kqN9fxCY6Xt5/pi$tVnh0xX87g/IsnOSuorZG608CZDFbWIWBr58ay6S4pD',
         'superuser': True,
         'disabled': False
         }
    ])
    conn.execute(users.insert(), [
        {'id': 2,
         'login': 'moderator',
         'passwd': '$5$rounds=535000$2kqN9fxCY6Xt5/pi$tVnh0xX87g/IsnOSuorZG608CZDFbWIWBr58ay6S4pD',
         'superuser': False,
         'disabled': False
         }
    ])

    conn.execute(users.insert(), [
        {'id': 3,
         'login': 'user',
         'passwd': '$5$rounds=535000$2kqN9fxCY6Xt5/pi$tVnh0xX87g/IsnOSuorZG608CZDFbWIWBr58ay6S4pD',
         'is_superuser': False,
         'disabled': False
         }
    ])

    conn.execute(permissions.insert(), [
        {'id': 1,
         'user_id': 1,
         'perm_name': 'protected',

         }
    ])
    conn.execute(permissions.insert(), [
        {'id': 2,
         'user_id': 2,
         'perm_name': 'public',

         }
    ])
    conn.execute(permissions.insert(), [
        {'id': 3,
         'user_id': 3,
         'perm_name': 'public',

         }
    ])

    conn.close()


if __name__ == '__main__':
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)

    create_tables(engine)
    sample_data(engine)

