from App import create_app
from dotenv import load_dotenv

load_dotenv(override=True)

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
