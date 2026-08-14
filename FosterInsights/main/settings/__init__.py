import os

from dotenv import load_dotenv

load_dotenv()

env = os.getenv("PROJECT_ENV")

if env == "local":
    from .local import *
else:
    from .prod import *
