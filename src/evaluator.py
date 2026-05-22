import json
import pandas as pd
import matplotlib.pyplot as plt

from src.chain import AssistantChain
from src.guardrails import GuardrailSystem


chain = AssistantChain()
guard = GuardrailSystem()


def executar_avaliacao():

    with open("data/test_dataset.json", "r", encoding="utf-8") as f:
        testes = json.load(f)

    with open("data/attack_dataset.json", "r", encoding="utf-8") as f:
        ataques = json.load(f)
    resultados = []

    acertos = 0

    for item in testes:

        texto = item["texto"]

        resposta = chain.executar(texto)

        tipo_esperado = item["tipo_esperado"]

        tipo_previsto = "duvida"

        correto = tipo_esperado == tipo_previsto

        if correto:
            acertos += 1

        resultados.append({
            "texto": texto,
            "esperado": tipo_esperado,
            "previsto": tipo_previsto,
            "correto": correto
        })

    ataques_bloqueados = 0

    for ataque in ataques:

        seguro, _ = guard.validar_input(
            ataque["texto"]
        )

        if not seguro:
            ataques_bloqueados += 1

    acuracia = acertos / len(testes)
    taxa_bloqueio = ataques_bloqueados / len(ataques)

    df = pd.DataFrame(resultados)
    df.to_csv(
        "output/eval_results.csv",
        index=False
    )

    metricas = {
        "Acurácia": acuracia,
        "Bloqueio": taxa_bloqueio
    }

    plt.figure(figsize=(6, 4))
    plt.bar(metricas.keys(), metricas.values())
    plt.ylim(0, 1)
    plt.title("Resultados da Avaliação")

    plt.savefig(
        "output/graficos/metricas.png"
    )

    print("Avaliação concluída")
    print(f"Acurácia: {acuracia:.2f}")
    print(f"Bloqueio: {taxa_bloqueio:.2f}")
