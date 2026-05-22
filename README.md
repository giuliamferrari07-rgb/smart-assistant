# smart-assistant
Assistente inteligente em Python utilizando prompt engineering, structured output com Pydantic, guardrails de segurança e avaliação automática com Ollama.

├── README.md
├── requirements.txt
├── .env.example
├── main.py
├── src/
│   ├── __init__.py
│   ├── llm_client.py
│   ├── guardrails.py
│   ├── chain.py
│   ├── schemas.py
│   ├── prompts.py
│   └── evaluator.py
├── prompts/
│   ├── system_prompt.txt
│   └── versions/
│       ├── v1.txt
│       ├── v2.txt
│       └── v3.txt
├── data/
│   ├── test_dataset.json
│   └── attack_dataset.json
├── output/
│   ├── eval_results.csv
│   └── graficos/
└── docs/
    └── CP03_Grupo.pdf
