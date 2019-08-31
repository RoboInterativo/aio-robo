import sqlalchemy as sa

from aiohttp_security.abc import AbstractAuthorizationPolicy
from passlib.hash import sha256_crypt

from models import users, permissions;


class DBAuthorizationPolicy(AbstractAuthorizationPolicy):
    def __init__(self, dbengine):
        self.dbengine = dbengine

    async def authorized_userid(self, identity):
        async with self.dbengine.acquire() as conn:
            where = sa.and_(users.c.login == identity,
                            sa.not_(users.c.disabled))
            query = users.count().where(where)
            ret = await conn.scalar(query)
            if ret:
                return identity
            else:
                return None

    async def permits(self, identity, permission, context=None):
        if identity is None:
            return False

        async with self.dbengine.acquire() as conn:
            where = sa.and_(users.c.login == identity,
                            sa.not_(users.c.disabled))
            query = users.select().where(where)
            ret = await conn.execute(query)
            user = await ret.fetchone()
            if user is not None:
                user_id = user[0]
                is_superuser = user[3]
                if is_superuser:
                    return True

                where = permissions.c.user_id == user_id
                query = permissions.select().where(where)
                ret = await conn.execute(query)
                result = await ret.fetchall()

                if ret is not None:
                    for record in result:
                        if record.perm_name == permission:
                            return True

            return False


async def check_credentials(dbengine, username, password):
    async with dbengine.acquire() as conn:
        where = sa.and_(users.c.login == username,
                        sa.not_(users.c.disabled))
        query = users.select().where(where)
        ret = await conn.execute(query)
        user = await ret.fetchone()
        if user is not None:
            hash = user[2]
            return sha256_crypt.verify(password, hash)
    return False
