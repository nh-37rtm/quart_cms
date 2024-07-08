from app_context import default_instance as app

from routes import another_route_controller

from quart.templating import stream_template
from jinja2 import FileSystemLoader

from model.data_model import BlogDescriptorEntryPydantic, IBlogDescriptorEntry
import os

class DefaultRouteController():


    @app.route("/", methods=["GET"])
    async def default():
        return await DefaultRouteController.hello0("index.html")

    @app.route("/<path:name>", methods=["GET"])
    async def hello0(name: str):
        
        from quart import request
        
        full_path = os.path.join('../resources', 'templates', name)
        full_template_path = os.path.join('../resources', 'templates', f"{name}.jinja2")
        
        
        _, extension = os.path.splitext(full_path)     
        
        return_value = None 

        while True:
            
            if extension == 'jinja2' :
                return 'not found', 404
            
            if os.path.exists(full_template_path):
                
                # async def stream_template_generator():
                    
                #     co = await stream_template(full_template_path, context={ 'test': 'aa' })
                #     for value in co:
                #         yield value
                
                # return_value = stream_template_generator()
                app.jinja_env.loader = FileSystemLoader(['../resources/templates/'])
                # app.jinja_env.compile_templates(full_template_path)
                
                
                with open('../resources/data.json') as data_file:
                    data_as_string = "\n".join(data_file.readlines())
                    data = BlogDescriptorEntryPydantic.model_validate_json(data_as_string)
                    t_data= IBlogDescriptorEntry(**data.model_dump())
                    return_value = await stream_template(f'{name}.jinja2', context={"data": t_data})
                
                
                break

            if os.path.exists(full_path):
                
                    async def file_content_generator():
                        with open(full_path, 'rb') as file:
                            
                            while True:
                                data = file.read()
                                if not data:
                                    break
                                
                                yield data

                    return_value = file_content_generator()
                                            
                    break

            # if not any found
            return 'not found', 404
            
        content_type_by_extension = { 
            '.css' : 'text/css',
            '.html' : 'text/html',
            '.js' : 'text/javascript',
            '.pdf': 'application/pdf'
        }

        content_type = None

        if extension in content_type_by_extension:
            content_type = content_type_by_extension[extension]
        else:
            content_type = "Unknown"

        
        return return_value, 200, {'Content-Type': content_type}
    
                
            