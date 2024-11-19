from fastapi import FastAPI, HTTPException
import aiohttp


app = FastAPI()


@app.get("/recipe/recipeName")
async def get_recipe_by_name(recipeName: str) -> dict:
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={recipeName}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            if data.get("meals") is None:
                raise HTTPException(status_code=404, detail="Recipe not found")
            return data


async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
