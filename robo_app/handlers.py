from textwrap import dedent
import json
from aiohttp import web , ClientSession
from aiohttp_security.api import AUTZ_KEY
#from aiohttp_security import remember, forget


from aiohttp_security import (
    remember, forget, authorized_userid,
    check_permission, check_authorized,
)

from db_auth import check_credentials
import aiohttp_jinja2



class Web(object):
    index_template = dedent("""
        <!doctype html>
            <head></head>
            <body>
                <p>{message}</p>
                <form action="/login" method="post">
                  Login:
                  <input type="text" name="login">
                  Password:
                  <input type="password" name="password">
                  <input type="submit" value="Login">
                </form>
                <a href="/logout">Logout</a>
            </body>
    """)


    
    @aiohttp_jinja2.template('index.html')
    async def index(self, request):
        return {}
    #async def index(self, request):
    #    username = await authorized_userid(request)
    #    if username:
    #        template = self.index_template.format(
    #            message='Hello, {username}!'.format(username=username))
    #        message = 'Hello, {username}!'.format(username=username)
    #    else:
    #        template = self.index_template.format(message='You need to login')
    #        message = 'You need to login'
    #    return aiohttp_jinja2.render_template('../front/build/index.html', request, {'message': message})
        #response = web.Response(content_type='text/html', body=(template.encode()))
        #return response
    async def login(self, request):
        raw_payload = await request.read()
        payload = raw_payload.decode(encoding='UTF-8')
        data = json.loads(payload)
        #data = validate_payload(raw_payload, LoginForm)
        #await authorize(request, data['login'], data['password'])
        dbengine = request.app.dbengine
        router = request.app.router
        location = router["index"].url_for().human_repr()
        is_user=await check_credentials(dbengine, data['login'], data['password'] )
        payload = {"location": location, "is_user":is_user}
        response = web.json_response(payload)
      
        await remember(request, response, data['login'])
        
        return response

    async def login2(self, request):
        data = await request.json()
        response = web.HTTPFound('/')
        #form = await request.post()
        login=data['login']
        password=data['password']
        
        #login = form.get('login')
        #password = form.get('password')
        dbengine = request.app.dbengine
        if await check_credentials(dbengine, login, password):
            await remember(request, response, login)
            raise response

        raise web.HTTPUnauthorized(content_type='text/html', body=b'Invalid username/password combination')

    async def logout(self, request):
        await check_authorized(request)
        response = web.Response(content_type='text/html', body=b'You have been logged out')
        await forget(request, response)
        return response

    async def internal_page(self, request):
        await check_permission(request, 'public')
        response = web.Response(content_type='text/html',
                                body=b'This page is visible for all registered users')
        return response

    async def admin_botlist_page(self, request):
        await check_permission(request, 'protected')
        username = await authorized_userid(request)
        #print ( str(data))
        return aiohttp_jinja2.render_template('base3.html', request, {'user_name': username})
        #response = web.Response(content_type='text/html', body=b'You are on protected page')
    #bot_detail_page
    async def admin_botdetail_page(self, request):
        await check_permission(request, 'protected')
        #username = await authorized_userid(request)
        # print ( str(data))
        return aiohttp_jinja2.render_template('base2.html', request, {})

    async def webhook (self, request):
        data = await request.json()
        headers = {
            'Content-Type': 'application/json'
        }
        message = {
            'chat_id': data['message']['chat']['id'],
            'text': data['message']['text']
        }
        async with ClientSession() as session:
            async with session.post(request.app.API_URL % request.app.telegram_token,
                                    data=json.dumps(message),
                                    headers=headers) as resp:
                try:
                    assert resp.status == 200
                except:
                    return web.Response(status=500)
        return web.Response(status=200)
    def configure(self, app):
        router = app.router
        router.add_route('GET', '/', self.index, name='index')
        router.add_route('POST', '/webhook', self.webhook, name= 'webhook')
        router.add_route('POST', '/auth', self.login, name='auth')
        router.add_route('GET', '/logout', self.logout, name='logout')
        router.add_route('GET', '/public', self.internal_page, name='public')
        router.add_route('GET', '/manage', self.admin_botlist_page, name='manage')
        router.add_route('POST', '/options', self.admin_botdetail_page, name='options')
