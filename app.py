from supabase import create_client
import os
from dotenv import load_dotenv



load_dotenv()  # läser .env

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

def skapa_team(team_name, team_code, email_input):
    try:
        # 1. Skapa teamet i 'teams'-tabellen
        # Vi sparar både namnet och den manuella koden
        team_resp = supabase.table("teams").insert({
            "team_name": team_name,
            "team_code": team_code  # Se till att denna kolumn finns i Supabase!
        }).execute()
        
        if not team_resp.data:
            return None
            
        new_team_id = team_resp.data[0]["id"] # Databasens interna UUID

        # 2. Dela upp e-poststrängen till en lista och rensa mellanslag
        email_lista = [e.strip() for e in email_input.split(',')]

        # 3. Koppla varje användare
        for mail in email_lista:
            # Hämta användarens UUID från 'Users'
            user_resp = supabase.table("Users").select("id").eq("email", mail).execute()
            
            if user_resp.data:
                u_id = user_resp.data[0]["id"]
                
                # Skapa raden i kopplingstabellen
                supabase.table("team_mebbers").insert({
                    "team_id": new_team_id,
                    "user_id": u_id
                }).execute()

        return team_resp.data
    except Exception as e:
        print("Fel i skapa_team:", e)
        return None
    