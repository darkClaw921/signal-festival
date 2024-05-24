# gptWork.py

import asyncio

async def function_one():
    await asyncio.sleep(1)
    return "Function One Completed"

async def function_two():
    await asyncio.sleep(2)
    return "Function Two Completed"


async def main_message(userID:str, message:str):
    await asyncio.sleep(1)
    return f"Message from {userID}: {message}"