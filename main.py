from pymongo import MongoClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import json_util
import json
import re
from openai import OpenAI
import os
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient("mongodb://localhost:27018/")
db = client["meu_banco"]


class QueryRequest(BaseModel):
    pergunta: str


client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def gerar_prompt(pergunta):
    schema = f"""
Você é um assistente para gerar JSON MongoDB para o banco 'meu_banco', que possui:

Collection: professor
{{ "_id": "int", "nome": "string", "especialidade": "string", "descricao": "string" }}

Collection: aula
{{ "_id": "int", "titulo": "string", "descricao": "string" }}

Collection: agenda_professor
{{ "professor_id": "int", "aula_id": "int", "data_hora": "ISODate", "rocket": "double" }}

Quando precisar fazer subconsultas ou unir dados entre collections, sempre use aggregate com $lookup. 
Nunca tente usar $in ou $nin com pipelines ou documentos complexos. 

Sempre gere datas no formato:
{{ "$gte": ISODate("...") }}

Sempre gere o JSON no formato:

Para find:
{{ "collection": "nome_da_collection", "query": {{...}} }}

Para aggregate:
{{ "collection": "nome_da_collection", "pipeline": [{{"$group": ...}}, ...] }}

Sem explicações extras, apenas o JSON.

Pergunta do usuário: {pergunta}
"""
    return schema


def extrair_json(texto):
    blocos = re.findall(r"```(.*?)```", texto, re.DOTALL)
    if blocos:
        resultado = blocos[0].strip()
    else:
        resultado = texto.strip()
    if resultado.lower().startswith("json"):
        resultado = resultado[4:].strip()
    return resultado


def formata_new_date(texto):
    texto = re.sub(r'ISODate\("([^"]*)"\)', r'"\1"', texto)
    return texto


def limpar_regex_shell(texto):
    texto = re.sub(r'(".*?")\s*:\s*/(.*?)/', r'\1: {"$regex": "\2"}', texto)
    return texto


def garantir_case_insensitive(d):
    if isinstance(d, dict):
        for k, v in d.items():
            if isinstance(v, dict) and "$regex" in v:
                v.setdefault("$options", "i")
            else:
                garantir_case_insensitive(v)
    elif isinstance(d, list):
        for item in d:
            garantir_case_insensitive(item)


def converter_datas_qualquer(query):
    if isinstance(query, dict):
        for k, v in query.items():
            if isinstance(v, dict):
                query[k] = converter_datas_qualquer(v)
            elif isinstance(v, list):
                query[k] = [converter_datas_qualquer(item) for item in v]
            else:
                if k in ["$gte", "$gt", "$lte", "$lt"] and isinstance(v, str):
                    try:
                        query[k] = datetime.fromisoformat(
                            v.replace("Z", "+00:00"))
                    except ValueError:
                        pass
    elif isinstance(query, list):
        return [converter_datas_qualquer(item) for item in query]
    return query


@app.post("/chat")
def chat(req: QueryRequest):
    prompt = gerar_prompt(req.pergunta)
    print("[DEBUG] Prompt enviado ao OpenAI:")
    print(prompt)

    completion = client_openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    print(
        f"[DEBUG] Numero de Tokens usados pela OpenAI: {repr(completion.usage)}")

    resposta_ia = completion.choices[0].message.content
    print(f"[DEBUG] Texto bruto retornado pela OpenAI: {repr(resposta_ia)}")

    resposta_ia = extrair_json(resposta_ia)
    resposta_ia = formata_new_date(resposta_ia)
    resposta_ia = limpar_regex_shell(resposta_ia)
    print(f"[DEBUG] JSON extraído para execução: {repr(resposta_ia)}")

    if not resposta_ia.strip():
        return {"erro": "IA não retornou JSON"}

    try:
        comando = json.loads(resposta_ia)
    except json.JSONDecodeError as e:
        return {"erro": f"JSON inválido mesmo após limpeza: {e}", "texto": resposta_ia}

    garantir_case_insensitive(comando)
    comando = converter_datas_qualquer(comando)  # Aplica em todo o JSON

    collection_name = comando.get("collection")
    if not collection_name:
        return {"erro": "JSON não contém 'collection'."}
    collection = db[collection_name]

    if "query" in comando:
        resultado_cursor = collection.find(comando["query"])
    elif "pipeline" in comando:
        resultado_cursor = collection.aggregate(comando["pipeline"])
    else:
        return {"erro": "JSON não contém 'query' nem 'pipeline'."}

    resultado = list(resultado_cursor)
    print("[DEBUG] Resultado bruto PyMongo:", resultado)

    resultado_serializavel = json.loads(json_util.dumps(resultado))

    resumo_prompt = f"""
    A pergunta da pessoa foi: {req.pergunta}
    Os dados retornados da consulta ao banco foram: {resultado_serializavel}.
    Crie uma resposta curta e objetiva ao usuário, indo direto ao ponto, 
    sem explicações adicionais ou ressalvas, apenas respondendo ao que foi perguntado de forma clara.
    """
    resumo_completion = client_openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": resumo_prompt}]
    )
    resumo = resumo_completion.choices[0].message.content
    print(
        f"[DEBUG] Numero de Tokens usados pela OpenAI (resumo): {repr(resumo_completion.usage)}")
    print(f"[DEBUG] Resposta final do OpenAI: {resumo}")

    return {
        "query_gerada": resposta_ia,
        "dados": resultado_serializavel,
        "resposta": resumo
    }
