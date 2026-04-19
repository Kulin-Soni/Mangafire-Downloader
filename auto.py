###
# This is an optional script if you want to bulk download many volumes or chapters,
# since Mangafire uses sequential integers to index volumes and chapters. To use, simply
# put the base url in the 'PAGE_BASE_URL' variable, and decide the limits using 'START' & 'END' variables.
# !!! There's a slight chance that Mangafire CDN will try to block your IP, so I suggest download volumes less frequently.
###

import asyncio, aiohttp
from camoufox.async_api import AsyncCamoufox
from img2pdf import convert
from pathlib import Path
from tqdm import tqdm
from typing import List

async def to_pdf(urls: List[str], output_path: str):
    chunks: List[bytes] = []
    async with aiohttp.ClientSession() as client:
        for url in tqdm(urls, desc="Downloading", unit="page"):
            response = await client.get(url)
            response.raise_for_status()
            chunk = await response.read()
            chunks.append(chunk)

    output = Path(output_path)
    if not output.as_posix().endswith(".pdf"):
        output = Path(output.parent / f"{output.stem}.pdf")
    output.parent.mkdir(parents=True, exist_ok=True)

    if chunks:
        with open(output, "wb") as f:
            f.write(convert(chunks)) # type: ignore
    
    print("Saved", output.name, "\n")


async def main() -> None:

    PAGE_BASE_URL = "https://mangafire.to/read/bleach22.jjrxn/en/volume-" # the base url
    START = 1 # starting position
    END = 75 # end position

    urls = []
    async def _response_handler(response):
        if not any(path in response.url for path in ["/ajax/read/chapter", "/ajax/read/volume"]):
            return
        data = await response.json()
        for url in data['result']['images']:
            urls.append(url[0])


    for i in range(START, END+1):
        async with AsyncCamoufox(headless=True) as browser:
            page = await browser.new_page()
            page.on("response", _response_handler)
            await page.goto(url=f"{PAGE_BASE_URL}{i}")
            await page.wait_for_load_state("networkidle")
            await to_pdf(urls, f"manga/Bleach_Vol_{i}")
            urls = []
    


if __name__ == "__main__":
    asyncio.run(main())
