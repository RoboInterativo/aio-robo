from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date,Boolean,
    PrimaryKeyConstraint, UniqueConstraint,     ForeignKeyConstraint)

metadata = MetaData()


users = Table(
    'users', metadata,
    Column('id', Integer, nullable=False),
    Column('login', String(256), nullable=False),
    Column('passwd', String(256), nullable=False),
    Column('is_superuser', Boolean, nullable=False, server_default='FALSE'),
    Column('disabled', Boolean, nullable=False, server_default='FALSE'),

    # indices
    PrimaryKeyConstraint('id', name='user_pkey'),
    UniqueConstraint('login', name='user_login_key'),
)


permissions = Table(
    'permissions', metadata,
    Column('id', Integer, nullable=False),
    Column('user_id', Integer, nullable=False),
    Column('perm_name', String(64), nullable=False),

    # indices
    PrimaryKeyConstraint('id', name='permission_pkey'),
    ForeignKeyConstraint(['user_id'], [users.c.id],     name='user_permission_fkey', ondelete='CASCADE'),
)
