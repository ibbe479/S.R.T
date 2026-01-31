from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()  # läser .env

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

def ansluta_till_db():
    try:
        supabase = create_client(url, key)
        return supabase
    except Exception as e:
        print("Det gick inte att ansluta till db:", e)
        return None

def hamta_data(supabase):
    try:
        response = supabase.table("Users").select("*").execute()
        print(response.data)
    except Exception as e:
        print("Fel vid hämtning:", e)

def main():
    supabase = ansluta_till_db()
    if supabase:
        hamta_data(supabase)

if __name__ == "__main__":
    main()
