import jwt.utils
from app_context import default_instance as app
from quart import request

import model.google.models as google_models
import aiohttp


import jwt


VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'
SITE_SECRET = '6LeDFkgqAAAAADx-b9H4M-dRlBEcXhl_w6xdYqFn'

class ServicesRouteController():

    @app.route("/services/<service>", methods=["POST"])
    async def services(service: str):  

        # parse_form = re.compile('([\w\-]+)=(.*?)(?:\&|$)')
        # form_dict = dict(re.findall(parse_form, data))
        
        form_dict, _ = await request.make_form_data_parser().parse(
            body=request.data, 
            mimetype='application/x-www-form-urlencoded', 
            content_length= request.content_length
        )

        if not 'csrf_token' in form_dict:
            return 'unauthorized', 401      

        value = jwt.decode(form_dict['csrf_token'], "secret", algorithms=["HS256"])
        

        query = google_models.site_verify_query(
            secret=SITE_SECRET,
            response=form_dict['g-recaptcha-response']
        )
        
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                'https://www.google.com/recaptcha/api/siteverify',
                data= query.__dict__)
            
            # response = session.get(f'https://www.google.com/recaptcha/api/siteverify?secret=6LeruOMpAAAAADd2H-NRFcKDJWty89o4kOuEGKB5&response={form_dict["g-recaptcha-response"]}')
            
            json_response = await response.json()
            # response = json.loads(json_response)
            # site_verify_response = google_models.site_verify_response.from_ (json_response)
            
            if not json_response['success'] is True:
                return 'access denied', 403
        
        
        
        return f"service name : {service} : <br />{request.view_args} <br />body: {request.body}", 200, {'Content-Type': 'text/html'}

    
    
