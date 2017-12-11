from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env.development')
load_dotenv(dotenv_path)

PGHOST = os.environ.get("PGHOST")
PGUSER = os.environ.get("PGUSER")
PGPASSWORD = os.environ.get("PGPASSWORD")
PGDATABASE = os.environ.get("PGDATABASE")
JWT_KEY = os.environ.get("JWT_KEY")
