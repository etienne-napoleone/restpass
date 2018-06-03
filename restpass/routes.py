from apistar import Route
from restpass import handlers

routes = [
    Route('/', method='GET', handler=handlers.welcome),
    Route('/ids/', method='GET', handler=handlers.list_ids),
    Route('/ids/{name}', method='GET', handler=handlers.get_id),
    Route('/ids/{name}', method='POST', handler=handlers.create_id),
    Route('/ids/{name}', method='PUT', handler=handlers.update_id),
    Route('/ids/{name}', method='DELETE', handler=handlers.delete_id)
]
