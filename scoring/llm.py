import os
import logging
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI(timeout=90.0)


async def call_openai(
    messages, temperature, model, seed=1234, response_format=None, top_p=None
):
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        logging.error("Please set the OPENAI_API_KEY environment variable.")
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
