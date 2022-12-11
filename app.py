import os

from src import create_app, dal

port = os.getenv('PORT', 5001)
app = create_app(config_name=os.getenv('APP_ENV', 'dev'))

if __name__ == '__main__':
    dal.create_tables()
    app.run(host='0.0.0.0', port=port)
