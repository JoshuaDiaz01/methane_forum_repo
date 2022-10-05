from flask_app import app

#remember to continually add controller files as needed
from flask_app.controllers import controller_user, controller_thought, controller_routes


if __name__=="__main__":
    app.run(debug=True)
    