import re


class GuardrailSystem:

    def __init__(self):
        self.patterns = [
            r"ignore instructions",
            r"forget rules",
            r"jailbreak",
            r"dan mode",
            r"reveal prompt",
            r"system prompt",
            r"developer mode"
        ]

    def validar_input(self, texto):

        if len(texto) > 500:
            return False, "Texto muito longo"

        proibidos = ["<", ">", "{", "}"]

        for c in proibidos:
            if c in texto:
                return False, "Caracteres proibidos"

        for pattern in self.patterns:
            if re.search(pattern, texto.lower()):
                return False, f"Ataque detectado: {pattern}"
            
        return True, "Seguro"

    def validar_output(self, resposta):

        termos_bloqueados = [
            "system prompt",
            "ignore instructions",
            "prompt secreto"
        ]

        for termo in termos_bloqueados:
            if termo in resposta.lower():
                return False, "Vazamento detectado"

        return True, "Seguro"
