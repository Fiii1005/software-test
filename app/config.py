# TODO: Use hierarchical toml file to store configs
from datetime import timedelta
import os
import openai

DATABASE = 'softwareengineering'
DATABASE_URL = 'mysql://root:@127.0.0.1:3306/' + DATABASE
JWT_ENCODE_ALGORITHM = 'HS256'
TOKEN_EXPIRE_MINUTES = timedelta(minutes=1800)
API_KEY = 'sk-COnPjO5xelWwaFiH6fB51cA466F94f9c8c60F101C7Ac0d7e'
LLM_MODEL = 'gpt-3.5-turbo'
