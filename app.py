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

def skapa_team(t_name, t_code, emails):
    try:
        clean_emails = [e.strip() for e in emails]

        for email in clean_emails:
            user_check = supabase.table("Users").select("email").eq("email", email).execute()
            if not user_check.data:
                return f"E-postadressen {email} finns inte i systemet."

        code=supabase.table("teams").select("id").eq("id", t_code).execute()
        if code.data:
            return f"Teamkoden {t_code} är redan upptagen. Vänligen välj en annan."
        
        supabase.table("teams").insert({"team_name": t_name, "id": t_code}).execute()

        for email in clean_emails:
            supabase.table("team_mebbers").insert({
                "team_code": t_code, 
                "user_email": email
            }).execute()

        return True
        
    except Exception as e:
        print("Fel i skapa_team:", e)
        return "Ett databasfel uppstod, försök igen senare."