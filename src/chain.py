import json

from src.llm_client import LLMClient
from src.prompts import (
    PROMPT_CLASSIFICACAO,
    PROMPT_PROCESSAMENTO,
    PROMPT_RESPOSTA
)

from src.schemas import (
    ClassificacaoSchema,
    ProcessamentoSchema,
    RespostaSchema
)

class AssistantChain:

    def __init__(self):
        self.llm = LLMClient()

    def etapa1_classificar(self, texto):

        prompt = PROMPT_CLASSIFICACAO.format(texto=texto)

        resposta = self.llm.gerar(prompt)

        try:
            dados = json.loads(resposta)
            return ClassificacaoSchema(**dados)

        except Exception:
            fallback = {
                "tipo": "duvida",
                "urgencia": "baixa",
                "tema": "geral"
            }
            
        return ClassificacaoSchema(**fallback)

    def etapa2_processar(self, classificacao, texto):

        tipo = classificacao.tipo

        if tipo == "reclamacao":
            instrucao = "Extraia problema e impacto"

        elif tipo == "duvida":
            instrucao = "Gere resposta informativa"

        elif tipo == "elogio":
            instrucao = "Agradeça o cliente"

        else:
            instrucao = "Analise sugestão"

        prompt = PROMPT_PROCESSAMENTO.format(
           tipo=tipo,
            texto=texto
        ) + "\n" + instrucao

        resposta = self.llm.gerar(prompt)

        try:
            dados = json.loads(resposta)
            return ProcessamentoSchema(**dados)

        except Exception:
            fallback = {
                "dados_extraidos": {},
                "analise": "Falha no processamento",
                "sentimento": "neutro"
            }

            return ProcessamentoSchema(**fallback)

    def etapa3_responder(self, processamento):

        prompt = PROMPT_RESPOSTA.format(
            dados=processamento.model_dump()
        )

        resposta = self.llm.gerar(prompt)

        try:
            dados = json.loads(resposta)
            return RespostaSchema(**dados)

        except Exception:
            fallback = {
                "resposta": "Não foi possível gerar resposta.",
                "confianca": "baixa",
                "acao_sugerida": "Tentar novamente"
            }

            return RespostaSchema(**fallback)

    def executar(self, texto):

        etapa1 = self.etapa1_classificar(texto)
        etapa2 = self.etapa2_processar(etapa1, texto)
        etapa3 = self.etapa3_responder(etapa2)

        return etapa3.model_dump()
