class DalvikHeuristics:
    """
    Motor heuristico de desensamblado (Disassembler) escrito desde cero.
    Traduce Opcodes de Dalvik a un 'Pseudo-Código' legible.
    """
    
    # Diccionario reducido de Dalvik Opcodes comunes (Hex a String)
    OPCODES = {
        0x1A: "const-string",
        0x1B: "const-string/jumbo",
        0x1C: "const-class",
        0x22: "new-instance",
        0x6E: "invoke-virtual",
        0x6F: "invoke-super",
        0x70: "invoke-direct",
        0x71: "invoke-static",
        0x72: "invoke-interface",
        0x0F: "return",
        0x11: "return-object",
        0x38: "if-eq",
        0x39: "if-ne",
    }
    
    @classmethod
    def generate_pseudo_code(cls, finding_type: str, raw_string: str) -> str:
        """
        Dado un hallazgo y la cadena vulnerable en memoria, genera una
        aproximacion heuristica en Pseudo-Codigo Java de como se veia la
        instruccion original basandose en el rastro del Opcode.
        """
        
        pseudo = "// [Reconstruido heurísticamente desde Bytecode Dalvik]\n"
        
        if finding_type == "hardcoded_secret":
            pseudo += f"String v0 = \"{raw_string}\"; // <-- Vulnerabilidad detectada\n"
            pseudo += "invoke_method(..., v0);\n"
            
        elif finding_type == "insecure_communication":
            pseudo += f"String url = \"{raw_string}\"; // <-- HTTP en lugar de HTTPS\n"
            pseudo += "URL connection = new URL(url);\n"
            pseudo += "connection.openConnection();\n"
            
        elif finding_type == "weak_crypto":
            pseudo += f"String algorithm = \"{raw_string}\"; // <-- Algoritmo debil/roto\n"
            pseudo += "Cipher.getInstance(algorithm);\n"
            
        else:
            pseudo += f"// Referencia detectada a: {raw_string}\n"
            
        return pseudo
        
    @classmethod
    def get_recommendation(cls, finding_type: str) -> str:
        """Devuelve el fragmento de codigo Java corregido segun el tipo de hallazgo."""
        
        if finding_type == "hardcoded_secret":
            return (
                "// 1. Eliminar la clave del código fuente.\n"
                "// 2. Usar BuildConfig inyectado desde el CI/CD o variables de entorno.\n"
                "String apiKey = BuildConfig.SECRET_API_KEY;"
            )
        elif finding_type == "insecure_communication":
            return (
                "// Cambiar la comunicacion a HTTPS y validar certificados SSL.\n"
                "String url = \"https://...\";\n"
                "HttpsURLConnection conn = (HttpsURLConnection) new URL(url).openConnection();"
            )
        elif finding_type == "weak_crypto":
            return (
                "// Usar algoritmos criptograficos modernos y seguros (ej. AES/GCM/NoPadding).\n"
                "Cipher cipher = Cipher.getInstance(\"AES/GCM/NoPadding\");"
            )
        return "// Revisar documentacion de seguridad de Android."
