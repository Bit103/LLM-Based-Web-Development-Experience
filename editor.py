
from openai import OpenAI
from pathlib import Path
import json
import os





main_path = Path(__file__).resolve().parent
user_data_path = Path(main_path/'api_parameters')
user_data_path.mkdir(parents=True, exist_ok=True)

html_path = Path(main_path/'website_details'/'index.html')
css_path = Path(main_path/'website_details'/'style.css')
def get_api_key():
    api_key_file = Path(user_data_path/"user_api_key.txt")
    if api_key_file.exists():
        with api_key_file.open('r', encoding="utf-8") as f:
            api_key = f.read()
        if not api_key:
            return create_api_key()
        return api_key
    else:
        return create_api_key()

def create_api_key():
    api_key = str(input('What is your API key? Return nothing to cancel the action.'))
    if api_key:
        with Path(user_data_path/"user_api_key.txt").open('w', encoding='utf-8') as f:
            f.write(api_key)
    else:
        return None
    return api_key

def get_base_url():
    json_file = Path(user_data_path/"GYOK_profile.json")
    if json_file.exists():
        with json_file.open('r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                return data["base_url"]
            except Exception:
                return create_base_url()
    else:
        return create_base_url()

def create_base_url():
    json_file = Path(user_data_path/"GYOK_profile.json")
    data_to_be_written = {"base_url":"https://openrouter.ai/api/v1"}
    if base_url := input('What is your base URL? Return nothing to cancel, return default to use OpenRouter.'):
        if base_url=='default':
            pass
        else:
            data_to_be_written["base_url"] = base_url

    else:
        return None
    with json_file.open('w', encoding='utf-8') as f:
        json.dump(data_to_be_written, f)
    return data_to_be_written['base_url']

def load_system_prompt():
    return Path('system_prompt.txt').read_text()

def load_html_css():
    html_file = main_path / 'website_details' / 'index.html'
    css_file = main_path / 'website_details' / 'style.css'
    
    html = html_file.read_text(encoding='utf-8')
    css = css_file.read_text(encoding='utf-8')
    
    return html, css
api_key = get_api_key()
base_url = get_base_url()

client = OpenAI(
    base_url=base_url,
    api_key=api_key,
)



prompt =   load_system_prompt()

while True:
    html, css = load_html_css()
    usrPrompt = input('>')

    response = client.chat.completions.create(
    model="inclusionai/ling-3.0-flash-fin:free",
    messages=[
        {"role": "system", "content": prompt},
        {"role": "system", "content": f'{html}\n ####BELOW IS CSS#### {css}'},
        {"role": "user", "content": usrPrompt}
    ],
    extra_body={
    "provider": {
        "allow_fallbacks": False}})

    print(response.choices[0].message.content)


    try:
        data = json.loads(response.choices[0].message.content)

        if "HTML" in data:
            html_new = data["HTML"]
            html_path.write_text(html_new, encoding="utf-8")

        if "CSS" in data:
            css_new = data["CSS"]
            css_path.write_text(css_new, encoding="utf-8")

    except json.JSONDecodeError:
        print("Error loading JSON. No change was made.")

