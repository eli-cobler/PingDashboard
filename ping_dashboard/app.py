import os
from flask import Flask, request, render_template
from ping_dashboard.data import db_session
from ping_dashboard.infrastructure.view_modifiers import response
from ping_dashboard.services import location_service

dir_path = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__, root_path=dir_path)

def main():
    setup_db()
    app.run(debug=True, port=5006)

def setup_db():
    db_file = os.path.join(
        os.path.dirname(__file__),
        'db',
        'ping_dashboard.sqlite')

    db_session.global_init(db_file)

@app.route('/', methods=['GET', 'POST'])
@response(template_file='home/index.html')
def index():
    return {
        'locations':location_service.sorted_server_urls(),
    }


if __name__ == '__main__':
    main()
