import os


class ApiSettings:
    app_name = "AnzenCore API"
    api_prefix = "/api/v1"
    supabase_url = os.getenv("SUPABASE_URL", "")
    supabase_key = os.getenv("SUPABASE_KEY", "")
