from openai import OpenAI
from pprint import pprint
import asyncio
import aiohttp
import json
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

async def polygon_stock_data(session,ticker,startDate,endDate,apikey):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{startDate}/{endDate}?apiKey={apikey}"
    print(url)
    async with session.get(url) as response:
        # Return the JSON content of the response using 'response.json()'
        return await response.json()



async def main():
    client = OpenAI(
        api_key = os.getenv("openai_apikey")
    )
    # List of URLs to fetch data from
    tickers = [
        'MSFT'
    ]

    
    startDate =os.getenv("startDate")
    endDate=os.getenv("endDate")
    apikey= os.getenv("polygon_apikey")

    # Create an aiohttp ClientSession for making asynchronous HTTP requests
    async with aiohttp.ClientSession() as session:
        # Create a list of tasks, where each task is a call to 'fetch_data' with a specific URL
        tasks = [polygon_stock_data(session, ticker,startDate,endDate,apikey) for ticker in tickers]
        
        # Use 'asyncio.gather()' to run the tasks concurrently and gather their results
        results = await asyncio.gather(*tasks)

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": 'system',
                    "content": 'You are a trading guru. Given data on share prices over the past days, write a report of no more than 150 words describing the stocks performance and recommending whether to buy, hold or sell. Use the exaples provided between ### to set the style of your response.'
                },
                {
                    "role": 'user',
                    "content": json.dumps(results)
                }
            ],
            temperature = 1.1,
            presence_penalty =0,
            frequency_penalty =0
        )
        
        pprint(completion.choices[-1].message.content)

if __name__ == "__main__":
    asyncio.run(main())