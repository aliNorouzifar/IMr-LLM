import requests


def generate_response_with_history(conversation, openai_model=None, api_key=None, api_url=None):

    if api_key is None:
        with open(r'C:\Users\kourani\PycharmProjects\IMr-LLM\utils\config\azure_api_key.txt', 'r') as file:
            azure_api_key = file.read().strip()

        with open(r'C:\Users\kourani\PycharmProjects\IMr-LLM\utils\config\azure_endpoint.txt', 'r') as file:
            azure_endpoint = file.read().strip()

        with open(r'C:\Users\kourani\PycharmProjects\IMr-LLM\utils\config\azure_model.txt', 'r') as file:
            azure_model = file.read().strip()

        from openai import AzureOpenAI

        client = AzureOpenAI(
            api_key=azure_api_key,
            api_version="2023-05-15",
            azure_endpoint=azure_endpoint
        )

        response = client.chat.completions.create(model=azure_model, messages=conversation)

        try:
            response_message = response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Connection to OpenAI failed! This is the response: " + str(response))

    else:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": openai_model,
            "messages": conversation,
        }

        complete_url = api_url + "chat/completions"

        response = requests.post(complete_url, headers=headers, json=payload).json()

        try:
            response_message = response["choices"][0]["message"]["content"]
        except Exception as e:
            raise Exception(f"Connection to OpenAI failed! This is the response: " + str(response))

    conversation.append(create_message(response_message, role="system"))

    return response_message, conversation


def create_message(content: str, role="user"):
    message = {"role": role, "content": content}
    return message

