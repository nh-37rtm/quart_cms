from app_context import default_instance as app

from routes import another_route_controller

from quart.templating import stream_template
from jinja2 import FileSystemLoader

from model.data_model import BlogDescriptorEntryPydantic, IBlogDescriptorEntry
import os

content_type_by_extension = { 
    '.css' : 'text/css',
    '.html' : 'text/html',
    '.js' : 'text/javascript',
    '.pdf': 'application/pdf'
}

class DefaultRouteController():


    @app.route("/", methods=["GET"])
    async def default():
        return await DefaultRouteController.templates_route("index.html")
    
    @app.route("/services/<service>", methods=["POST"])
    async def services(service: str):
        return f"service name : {service}", 200, {'Content-Type': 'text/html'}

    
    @app.route("/t/<path:name>", methods=["GET"])
    async def templates_route(name: str):
        
        full_template_path = os.path.join('../resources', 'templates', f"{name}.jinja2")
        full_path = os.path.join('../resources', 'templates', name)
        _, extension = os.path.splitext(full_path)

        return_value = None

        if os.path.exists(full_template_path):
            
            app.jinja_env.loader = FileSystemLoader(['../resources/templates/'])               
            
            with open('../resources/data.json') as data_file:
                data_as_string = "\n".join(data_file.readlines())
                data = BlogDescriptorEntryPydantic.model_validate_json(data_as_string)
                t_data= IBlogDescriptorEntry(**data.model_dump())
                return_value = await stream_template(f'{name}.jinja2', context={"data": t_data, "csrf": "aaaaaaaaaaaaaa"})


        # if not any found
        if return_value is None :
            return f'{name} not found', 404

        content_type = None


        if extension in content_type_by_extension:
            content_type = content_type_by_extension[extension]
        else:
            content_type = "Unknown"

        
        return return_value, 200, {'Content-Type': content_type}

    @app.route("/r/<path:name>", methods=["GET"])
    async def resources_route(name: str):
                
        full_path = os.path.join('../resources', 'templates', name)
        _, extension = os.path.splitext(full_path)
        
        if extension in [ 'jinja2', 'py' ]:
            return f'{name} not found', 404

        return_value = None

        if os.path.exists(full_path):
            
            async def file_content_generator():
                with open(full_path, 'rb') as file:
                    
                    while True:
                        data = file.read()
                        if not data:
                            break
                        
                        yield data

            return_value = file_content_generator()
                                        

        # if not any found
        if return_value is None :
            return f'{name} not found', 404
  
                
        content_type = None
        
        _, extension = os.path.splitext(full_path)

        if extension in content_type_by_extension:
            content_type = content_type_by_extension[extension]
        else:
            content_type = "Unknown"
            
        return return_value, 200, {'Content-Type': content_type}
            