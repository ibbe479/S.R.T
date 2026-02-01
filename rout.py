from flask import Flask, render_template, request, redirect, url_for
import app

RT = Flask(__name__)

@RT.route('/')
def sign_in():
    return render_template('sig_up.html')

@RT.route('/sign_up', methods=['POST'])
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

@RT.route('/login')
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
        if result :
            return f"Välkommen, {result[0]['name']}! Du är inloggad."
        else:
            return "Felaktig e-post eller lösenord.", 401
    except Exception as e:
        print("Fel vid hantering av inloggning:", e)
        return "Något gick fel vid inloggning.", 400





if __name__ == '__main__':
    RT.run(debug=True)