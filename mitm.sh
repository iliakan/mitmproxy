#!/usr/bin/env zsh

# Go to browser
# http://127.0.0.1:8081

# Proxy at
# http://127.0.0.1:8090

source venv/bin/activate

mitmweb --set allow_hosts='github|copilot' --set listen_port=8090 -s chat_completions_view.py -s copilot_codex_view.py -s jsonl_data_view.py
