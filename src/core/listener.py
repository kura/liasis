import eventlet
from config import config
eventlet.monkey_patch()


s = eventlet.listen((
                     config.get("HOST"), 
                     int(config.get("PORT")), 
                     ))
pool = eventlet.GreenPool(size=int(config.get("MAX_CONNECTIONS")))

