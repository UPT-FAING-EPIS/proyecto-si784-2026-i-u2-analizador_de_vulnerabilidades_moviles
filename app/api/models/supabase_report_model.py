from supabase import create_client

from app.api.config.settings import ApiSettings


class SupabaseReportModel:
    def __init__(self):
        if not ApiSettings.supabase_url or not ApiSettings.supabase_key:
            raise ValueError("SUPABASE_URL y SUPABASE_KEY son requeridos para la API.")
        self.supabase = create_client(ApiSettings.supabase_url, ApiSettings.supabase_key)

    def user_exists(self, user_id):
        return (
            self.supabase.table("usuarios")
            .select("id")
            .eq("id", user_id)
            .limit(1)
            .execute()
        )

    def create_report(self, payload):
        return self.supabase.table("vulnerabilidades").insert(payload).execute()
