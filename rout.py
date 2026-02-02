from flask import Flask, render_template, request, redirect, url_for, session
import app

RT = Flask(__name__)
RT.secret_key = 'en_väldigt_hemlig_nyckel'

@RT.route('/sign_up')
def sign_in():
    return render_template('sig_up.html')

@RT.route('/handle_sign_up', methods=['POST'])
def handle_sign_up():
    ''' hämtar data från formuläret och skickar det till registrera_anvandare funktionen i app.py'''
    try:
        form_data = {
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password'),
            "role": request.form.get('role')
        }

        result = app.registrera_anvandare(form_data)
        return redirect(url_for('login'))
    
    except Exception as e:
        print("Fel vid hantering av registrering:", e)
        return "Något gick fel.", 400

@RT.route('/')
def login():
    return render_template('login.html')

@RT.route('/handle_login', methods=['POST'])
def handle_login():
    try:
        form_data = {
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }

        result = app.leta_anv(form_data)
        if result:
            # Skapa sessionen här!
            session['logged_in'] = True
            session['user_email'] = form_data['email']
            return redirect(url_for('index'))
        else:
            return "Felaktig e-post eller lösenord.", 401
    except Exception as e:
        return "Något gick fel.", 400

@RT.route('/index')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

if __name__ == '__main__':
    RT.run(debug=True)