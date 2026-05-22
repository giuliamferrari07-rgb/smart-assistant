from src.guardrails import GuardrailSystem
from src.chain import AssistantChain
from src.evaluator import executar_avaliacao


def modo_interativo():
    guard = GuardrailSystem()
    chain = AssistantChain()

    print("=== SMART ASSISTANT ===")

    while True:
        texto = input("Usuário: ")

        if texto.lower() == "sair":
            break

        seguro, motivo = guard.validar_input(texto)

        if not seguro:
           print(f"[BLOQUEADO] {motivo}")
           continue

        resposta = chain.executar(texto)

        seguro_output, motivo_output = guard.validar_output(
            resposta["resposta"]
        )

        if not seguro_output:
            print(f"[OUTPUT BLOQUEADO] {motivo_output}")
            continue

        print("\nAssistente:")
        print(resposta["resposta"])
        print("-" * 50)


if __name__ == "__main__":
    import sys

    if "--eval" in sys.argv:
        executar_avaliacao()
    else:
        modo_interativo()
