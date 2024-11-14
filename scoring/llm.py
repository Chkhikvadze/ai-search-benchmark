import os
import logging
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI(timeout=90.0)

api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    logging.error("Please set the OPENAI_API_KEY environment variable.")
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")


async def call_openai(
    messages, temperature, model, seed=1234, response_format=None, top_p=None
):
    if not api_key:
        return None

    for attempt in range(2):
        logging.info(
            f"Calling Openai. Temperature = {temperature}, Model = {model}, Seed = {seed},  Messages = {messages}"
        )
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                seed=seed,
                response_format=response_format,
                top_p=top_p,
            )
            response = response.choices[0].message.content
            return response

        except Exception as e:
            print(f"Error when calling OpenAI: {str(e)}")
            await asyncio.sleep(0.5)

    return None


async def call_openai_beta(
    messages, temperature, model, seed=1234, response_format=None, top_p=None
):
    if not api_key:
        return None

    for attempt in range(2):
        logging.info(
            f"Calling Openai. Temperature = {temperature}, Model = {model}, Seed = {seed},  Messages = {messages}"
        )
        try:
            response = await client.beta.chat.completions.parse(
                model=model,
                messages=messages,
                temperature=temperature,
                seed=seed,
                response_format=response_format,
                top_p=top_p,
            )
            response = response.choices[0].message.content
            return response

        except Exception as e:
            print(f"Error when calling OpenAI: {str(e)}")
            await asyncio.sleep(0.5)

    return None


async def get_openai_embeddings(text, model="text-embedding-3-small"):
    response = await client.embeddings.create(input=text, model=model)
    return response.data[0].embedding
