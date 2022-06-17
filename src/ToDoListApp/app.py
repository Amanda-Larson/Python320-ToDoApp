"""set up the api using flask and jsonify"""

from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from flask import jsonify


class Tasks(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from Tasks")
        result = {"Tasks": [i[1] for i in query.cursor.fetchall()]}
        conn.close()
        return jsonify(result)


if __name__ == "__main__":
    db_connect = create_engine("sqlite:///to_do_list.db")

    app = Flask(__name__)

    api = Api(app)
    api.add_resource(Tasks, "/tasks")  # Route_1

    app.run(port=5002)

    db_connect.dispose()

