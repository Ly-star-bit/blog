# import os
from dotenv import load_dotenv
from pathlib import Path
# dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

# if os.path.exists(dotenv_path):
#     load_dotenv(dotenv_path)
for dotenv_path in Path(Path.cwd()).iterdir():
    if dotenv_path.name.endswith('env'):
        load_dotenv(dotenv_path)
        break

from bluelog import create_app  # noqa

app = create_app('production')

