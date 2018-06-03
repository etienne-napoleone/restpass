from apistar import App
from restpass import config
from restpass import routes


app = App(routes=routes.routes)


if __name__ == '__main__':
    app.serve(
        config.DEV_SERVER_HOST,
        config.DEV_SERVER_PORT,
        debug=config.DEV_SERVER_DEBUG
    )
