from app_context import default_instance as app

import jinja_templating.modules.entry_point as EntryPoint
from jinja_templating.models.customize_one_parameters import CustomizeOneParameters

from model.data_model import BlogDescriptorEntryPydantic
from jinja_templating.modules.renderer_context import RendererContext

import json
import os
import codecs
import asyncio
import multiprocessing

class AnotherRouteController():
    @app.route("/another")
    async def hello():
        
        from quart import request
        
        app.logger.info('another route reached')       
    
        # parameters = CustomizeOneParameters('resources', 'data.json', 'json', 'templates/try.jinja2' )
        # EntryPoint.customizeOne(parameters)
        
        read_descriptor, write_descriptor = os.pipe()
        
        read = open(read_descriptor, 'r')
        write = open(write_descriptor, 'w')
    
        context = RendererContext( custom_controller=None, template_reference_path= 'resources')
                
        with open('resources/data.json') as data_file:
            full_data = "\n".join(data_file.readlines())
            blog = BlogDescriptorEntryPydantic.model_validate_json(full_data)
            
            async def generator():
                while True:
                    data = read.readline()
                    if not data:
                        break
                    yield data
                read.close()


            async def render(context: RendererContext):
                context.render_template(
                    data= blog.model_dump(), template_path= 'templates/try.html.jinja2',
                    output = write)
                
                write.close()
                
                # write.close()
                # write.writelines("dsfsdfsddsf\ndsfsdfsdfsf\sdfdsfdsdsf\n".splitlines())
                # write.close()
                
            # task = app.add_background_task(lambda: render(context))
            
            asyncio.create_task(render(context))

        return generator(), 200, {'X-Something': 'value'}
        #return f'Hello, world : {request.remote_addr}'
        
        
    