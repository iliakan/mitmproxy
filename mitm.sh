#!/usr/bin/env zsh

source venv/bin/activate

mitmweb --set allow_hosts='github|copilot' --set listen_port=8090 -s chat_completions_view.py -s copilot_codex_view.py -s jsonl_data_view.py
