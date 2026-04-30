from supabase import create_client
import os
from dotenv import load_dotenv
from datetime import datetime


base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(base_dir, ".env"))

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def registrera_anvandare(user_data):
    """funktionen används i rout.py för att registrera en användare i Supabase."""
    try:
        response = supabase.table("Users").insert(user_data).execute()
        return response.data
    except Exception as e:
        print("Fel vid registrering:", e)
        return None

def leta_anv(login_data):
    """funktionen används i rout.py för att leta upp en användare i Supabase vid inloggning."""
    try:
        response = supabase.table("Users").select("*").eq("email", login_data["email"]).eq("password", login_data["password"]).execute()
        return response.data
    except Exception as e:
        print("Fel vid inloggning:", e)
        return None
    
def är_det_admin(email):
    """funktionen kontrollerar om användaren är admin."""
    try:
        response = supabase.table("Users").select("role").eq("email", email).execute()
        if response.data and response.data[0]["role"] == "admin":
            return True
        return False
    except Exception as e:
        print("Fel vid kontroll av admin:", e)
        return False

def skapa_team(t_code, emails):
    """funktionen skapar ett team och lägger till medlemmar i Supabase."""
    try:
        clean_emails = [e.strip() for e in emails]

        for email in clean_emails:
            user_check = supabase.table("Users").select("email").eq("email", email).execute()
            if not user_check.data:
                return f"E-postadressen {email} finns inte i systemet."

        code=supabase.table("teams").select("id").eq("id", t_code).execute()

        if code.data:
            return f"Teamnamnet {t_code} är redan upptagen. Vänligen välj en annan."
        
        supabase.table("teams").insert({"id": t_code}).execute()
        

        for email in clean_emails:
            supabase.table("team_mebbers").insert({
                "team_code": t_code, 
                "user_email": email
            }).execute()

        return True
        
    except Exception as e:
        print("Fel i skapa_team:", e)
        return "Ett databasfel uppstod, försök igen senare."
    
def skapa_nyhet(title, innehåll,till):
    """funktionen lägger upp en nyhet i Supabase."""
    try:
        finns_teamet = supabase.table("teams").select("id").eq("id", till).execute()
        if not finns_teamet.data:
            return f"Teamet {till} finns inte. Vänligen kontrollera team namnet."
        
        supabase.table("nyheter").insert({
            "titel": title,
            "innehåll": innehåll
            ,"till_vem": till
        }).execute()
        return True
    except Exception as e:
        print("Fel vid skapande av nyhet:", e)
        return False
 
def hämta_nyheter_för_användare(email):
    """Hämtar nyheter för de team som den inloggade användaren tillhör."""
    try:
        mina_team = supabase.table("team_mebbers").select("team_code").eq("user_email", email).execute()
        
        if not mina_team.data:
            return [] 

        team_list = [rad['team_code'] for rad in mina_team.data]

        nyheter = supabase.table("nyheter").select("*").in_("till_vem", team_list).order("created_at", desc=True).execute()
        return nyheter.data
    except Exception as e:
        print("Fel vid hämtning:", e)
        return []
    
def hämta_alla_teams(): 
    """Hämtar alla team från Supabase."""
    try:
        teams = supabase.table("teams").select("*").execute()
        return teams.data
    except Exception as e:
        print("Fel vid hämtning av teams:", e)
        return []

def hämta_alla_medlemmar():

    """Hämtar alla användare från Supabase."""
    try:
        medlemmar = supabase.table("Users").select("*").execute()
        return medlemmar.data
    except Exception as e:
        print("Fel vid hämtning av medlemmar:", e)
        return []

def vilket_team_är_användaren_i(email):
    """Hämtar alla medlemmar som ingår i samma team som användaren."""
    try:
        mina_team_resp = supabase.table("team_mebbers").select("team_code").eq("user_email", email).execute()
        
        if not mina_team_resp.data:
            return []

        team_koder = [rad['team_code'] for rad in mina_team_resp.data]

        alla_medlemmar = supabase.table("team_mebbers").select("user_email", "team_code").in_("team_code", team_koder).execute()
        
        return alla_medlemmar.data
    except Exception as e:
        print("Fel vid hämtning av teammedlemmar:", e)
        return []

def skapa_todo_item(email, task, prioritet):
    """Skapar en todo-uppgift för en användare."""
    try:
        supabase.table("todo").insert({
            "user": email,
            "task": task,
            "priority": prioritet
        }).execute()
        return True
    except Exception as e:
        print("Fel vid skapande av todo-item:", e)
        return False

def hämta_todo_items(email):
    """Hämtar alla todo-uppgifter för en användare."""
    try:
        response = supabase.table("todo").select("*").eq("user", email).order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        print("Fel vid hämtning av todo-items:", e)
        return []

def radera_todo_item(task_id):
    """Raderar en specifik todo-uppgift baserat på dess ID."""
    try:
        # Vi använder .eq("id", task_id) för att hitta rätt rad
        supabase.table("todo").delete().eq("id", task_id).execute()
        return True
    except Exception as e:
        print("Fel vid radering av todo-item:", e)
        return False
        

def hämta_pass(email):
    """Hämtar endast framtida eller pågående pass för en användare."""
    try:
        response = supabase.table("shifts").select("*").eq("user_id", email).execute()
        alla_pass = response.data
        
        if not alla_pass:
            return []

        nu = datetime.now().isoformat()

        framtida_pass = [p for p in alla_pass if p['end_shift'] >= nu]

        framtida_pass.sort(key=lambda x: x['start_shift'])

        return framtida_pass
        
    except Exception as e:
        print("Fel vid hämtning av pass:", e)
        return []

def spara_flera_pass(pass_lista):
    try:
        response = supabase.table("shifts").upsert(pass_lista).execute()
        return True, "Klart!"
    except Exception as e:
        return False, str(e)



