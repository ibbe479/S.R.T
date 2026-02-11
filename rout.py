from flask import Flask, render_template, request, redirect, url_for, session, flash
import app
from functools import wraps

#fixa startsidan 
#fixa så man kan se vilka teams man är inne i 
# fixa todo lista en egen sida 

RT = Flask(__name__)
RT.secret_key = 'en_väldigt_hemlig_nyckel'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        if not app.är_det_admin(session.get('user_email')): 
            return "Åtkomst nekad.", 403
        return f(*args, **kwargs)
    return decorated_function

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
def home():
    return render_template('start_sida.html')

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
        if result:
            
            session['logged_in'] = True
            session['user_email'] = form_data['email']
            session['is_admin'] = app.är_det_admin(form_data['email'])
            return redirect(url_for('index'))
        else:
            return "Felaktig e-post eller lösenord.", 401
    except Exception as e:
        return "Något gick fel.", 400

@RT.route('/logout')
def logout():
    session.clear() 
    return redirect(url_for('home'))

@RT.route('/index')
@login_required
def index():
    user_email = session.get('user_email')

    nyheter = app.hämta_nyheter_för_användare(user_email) 

    return render_template('index.html', nyheter=nyheter)

@RT.route('/admin')
@login_required
@admin_required
def admin_tool():
    return render_template('admin.html')

@RT.route('/handle_admin', methods=['POST'])
@login_required
@admin_required
def handle_admin():
   
    try:
        t_code = request.form.get('spec_kod')    
        emails = request.form.get('vem_i_teamet') 
        
        result = app.skapa_team( t_code, emails.split(","))

        if result is True:
            flash("Teamet skapades och medlemmarna lades till.")
        else:
            flash(result, 'error')
        return redirect(url_for('admin_tool'))
    except Exception as e:
        return "Något gick fel", 400
    

@RT.route('/nyheter', methods=['post'])
@login_required
@admin_required
def nyheter():
    try:
        title = request.form.get('titel')
        innehåll = request.form.get('message')
        till=request.form.get('till_vem')

        text = app.skapa_nyhet(title, innehåll, till)
        if text is True:
            flash("Nyheten har skapats och publicerats.", 'success')
        else:
            flash(text, 'error')
        return redirect(url_for('admin_tool'))

    except Exception as e:
        return "Något gick fel", 400
    
if __name__ == '__main__':
    RT.run(debug=True)