import aiohttp
import asyncio
import time

start_time = time.time()

pokemons = {}
async def main():
    async with aiohttp.ClientSession() as session:

        for number in range(1, 30):
            pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{number}'
            async with session.get(pokemon_url) as resp:
                pokemon = await resp.json()
                # print(number, pokemon['name'])
                pokemons.update({number:pokemon['name']})


asyncio.run(main())
print(pokemons)
print("--- %s seconds ---" % (time.time() - start_time))