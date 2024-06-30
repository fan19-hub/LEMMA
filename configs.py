import os
prompts_root="prompts/"
scripts_root="scripts"
out_root="out/"
cache_root="data/cache/"
if not os.path.exists(cache_root):
    os.makedirs(cache_root)
imgbed_root="https://raw.githubusercontent.com/fan19-hub/LEMMA/main/"
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
definition_path = "prompts/definition.json"