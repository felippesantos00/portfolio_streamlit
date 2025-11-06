#!/bin/bash

# Arquivo da conversa
ARQ="$1"

# Extrai só as mensagens (tira data, hora e nome do contato)
# Exemplo do formato WhatsApp: "11/09/2025, 21:23 - João: Oi, tudo bem?"
zcat "$ARQ" | cut -d '-' -f2- | cut -d ':' -f2- |
tr '[:upper:]' '[:lower:]' |      # tudo minúsculo
tr -d '[:punct:]' |                # remove pontuação
tr '$' '\n' |                      # quebra em palavras
grep -v -E '^[ 0-9]+$' |            # remove números
grep -Ev -f stopwords.txt |      # remove palavras comuns (lista sua)
sort 
