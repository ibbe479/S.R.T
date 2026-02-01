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