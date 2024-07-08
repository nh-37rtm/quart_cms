from app_context import default_instance as app
from logger import default_logger as logger

from quart.utils import MustReloadError

import asyncio
import logging

from model.app_config import AppConfig


def hypercorn_start() :
    
    logging.info("starting application with web server ...")

    from hypercorn.config import Config    
    event_loop = asyncio.new_event_loop()

    hypercorn_config = Config()   
    hypercorn_config.bind = ["0.0.0.0:8000"]  # Change the binding address as needed
    
    # hypercorn_config.loglevel = 
    async def event_loop_coroutine(app, hypercorn_config):
        from hypercorn.asyncio import serve
        await serve(app, hypercorn_config)

    app.load_dependencies()
    routine = event_loop_coroutine(app, hypercorn_config)
    task = event_loop.create_task(routine)
    event_loop.run_until_complete(task)
    
if __name__ == "__main__":
       
    app.load_dependencies() 
    app.generate_model_json_schema()
    logger.info("starting application in debug mode ...")

    app.run(debug= True)
        
    # hypercorn_start()
    
    
    
    
    