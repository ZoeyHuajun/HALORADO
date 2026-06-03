from flask import Flask, render_template, request,redirect
import config
# Create a Flask application instance
app = Flask(__name__)
# Load configuration settings from the config.py file
#app.config['SECRET_KEY'] = '123456'
app.config.from_object(config)

# Define a route for the home page127.0.0.1:5000 -view function
@app.route('/')
def home_page():
    return render_template('variable.html', hobby='看书')

@app.get('/login')
def login():
    return f'Welcome to the page.'
@app.get('/pub')
def pub():
    name = request.args.get('name')
    if not name:
        return redirect('/login')
    else:
        return f'Welcome, {name}!'

if __name__ == '__main__':
    # Run the Flask application with new host and port settings
    app.run(debug=True, host='0.0.0.0', port=5050)