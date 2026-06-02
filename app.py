from flask import Flask, render_template, request
import config
# Create a Flask application instance
app = Flask(__name__)
# Load configuration settings from the config.py file
#app.config['SECRET_KEY'] = '123456'
app.config.from_object(config)

# Define a route for the home page127.0.0.1:5000 -view function
@app.route('/')
def home_page():
    return 'Hello, World!'
if __name__ == '__main__':
    # Run the Flask application with new host and port settings
    app.run(debug=True, host='0.0.0.0', port=5050)