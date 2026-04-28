from flask import Flask, render_template, request, redirect, url_for, session, flash
import app
from functools import wraps
""" för att lägga till de senaste comiten i main skriver man 
cd mysite
git pull origin main
"""


#fixa så att man kan se vilka pass man har fått 

#fixa flash meddelanden i alla sidor
#gör en egen start sida för admin. Det ka finnas se teams se medelemar och skicka medelande till teams, skapa teams och kanske se allas todo listor.
###############################################################################
### ska man bara kunna skicka medelande till andra teams eller ska man kunna skicka medelande till andra medlemar privat?
### ska en admin kunna gå in i en medlems todo lista och se vad den har gjort och inte gjort?
### ska jag ha kvar att man kan se vilka teams man är med i?




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
    teams = app.vilket_team_är_användaren_i(user_email)

    email = session.get('user_email')
    task = app.hämta_todo_items(email)

    return render_template('index.html', nyheter=nyheter, teams=teams, task=task, email=email) 

@RT.route('/admin')
@login_required
@admin_required
def admin_tool():
    temas = app.hämta_alla_teams() 
    medlemmar = app.hämta_alla_medlemmar()
    return render_template('admin.html', teams=temas , medlemmar=medlemmar)
    

@RT.route('/handle_admin', methods=['POST'])
@login_required
@admin_required
def handle_admin():
   
    try:
        t_code = request.form.get('spec_kod')    
        emails = request.form.getlist('vem_i_teamet') 

        emails = ",".join(emails)
        
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
        till=request.form.getlist('till_vem')

        till = ",".join(till)

        text = app.skapa_nyhet(title, innehåll, till)
        if text is True:
            flash("Nyheten har skapats och publicerats.", 'success')
        else:
            flash(text, 'error')
        return redirect(url_for('admin_tool'))

    except Exception as e:
        return "Något gick fel", 400
    
@RT.route('/todo')
@login_required
def todo():
    email = session.get('user_email')
    task = app.hämta_todo_items(email)
    return render_template('todo.html', email=email, task=task)


@RT.route('/ny_task', methods=['POST'])
@login_required
def ny_task():
    try:
        user_email = session.get('user_email')
        task = request.form.get('task')
        priority = request.form.get('priority')

        result = app.skapa_todo_item(user_email, task, priority )
        if result != True:
            flash("Ett fel uppstod när Tasken skulle läggas till.", 'error')
        return redirect(url_for('todo'))
    except Exception as e:
        print("Fel vid tillägg av task:", e)
        return "Något gick fel", 400

@RT.route('/radera_task/<task_id>', methods=['POST'])
@login_required
def radera_task(task_id):
    success = app.radera_todo_item(task_id)
    if success:
        return {"status": "success"}, 200
    return {"status": "error"}, 500

@RT.route('/skapa_pass', methods=['POST'])
@login_required
@admin_required
def skapa_pass():
    try:
        pass_data = request.get_json() 
        
        resultat = app.spara_flera_pass(pass_data)
        
        if resultat:
            return {"status": "success"}, 200
        else:
            return {"status": "error", "message": "Kunde inte spara i databasen"}, 500
    except Exception as e:
        print("Fel i skapa_pass route:", e)
        return "Något gick fel", 400
    
if __name__ == '__main__':
    RT.run(debug=True)


