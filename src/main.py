import os
import openai
import constant

# Set up your OpenAI API credentials
openai.api_key = constant.API_KEY

def get_compiled_sql(folder_path):
    file_texts = {}

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                file_texts[filename] = file.read()

    return file_texts

def run_prompt(user_prompt):
    response = openai.Completion.create(
        model= 'text-davinci-003'
        , prompt= user_prompt
        , temperature=0.8
        , max_tokens=1000
        , top_p=1
        , frequency_penalty=0
        , presence_penalty=0
    )
    return response

def extract_response_text(response):
    return response.choices[0].text

target_path = '' # enter in a path within your dbt target directory
compiled_sql_files = get_compiled_sql(target_path)

sql_code = list(compiled_sql_files.values())[0]
prompt = f'Generate a .yml file for a DBT project which only outputs\n - the yml version\n - model name\n - model description\n - column names\n - column descriptions\n for the SQL code:\n {sql_code}'

response = run_prompt(prompt)
output = extract_response_text(response)
print(output)