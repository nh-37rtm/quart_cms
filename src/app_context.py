

from quart import Quart
from model.app_config import AppConfig
from logger import default_logger as logger
from logging import Logger

import datetime

from typing import TypeVar, Generic
import logging
import json

from model.data_model import BlogDescriptorEntryPydantic

T = TypeVar('T')

class CustomQuartAppContext(Quart, Generic[T]):
    
    custom_configuration: AppConfig
    default_logger: Logger = logger

    def load_dependencies(self):
        logging.info('importing dependencies ...')
        import routes.default        


    def generate_model_json_schema(self):
        logging.info('generating json schema ...')

        t = BlogDescriptorEntryPydantic.model_json_schema()
    
        with open('../resources/data.schema.json', '+w') as schema_file:
            schema_file.write(json.dumps(t))

default_instance = CustomQuartAppContext("etp0")


@default_instance.context_processor
def inject_year():
    return {'today_year': datetime.date.today().year}

