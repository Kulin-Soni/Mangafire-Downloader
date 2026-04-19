import asyncio, re, aiohttp
from argparse import ArgumentParser
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


async def main() -> None:
    ### Argument Parsing
    parser = ArgumentParser()
    parser.add_argument("url", type=str, help="The mangafire volume or chapter url.")
    parser.add_argument("output_path", type=str, help="The output path for the pdf. [Example: manga/chapter/name.pdf]")
    args = parser.parse_args()

    url: str = args.url
    output: str = args.output_path

    if not re.match(r"^https://mangafire\.to/read/.+$", url):
        print("Not a valid url.")
        return

    # Response Handler and URL listing
    urls = []
    async def _response_handler(response):
        if not any(path in response.url for path in ["/ajax/read/chapter", "/ajax/read/volume"]):
            return
        data = await response.json()
        for url in data['result']['images']:
            urls.append(url[0])


    # Camoufox session
    async with AsyncCamoufox(headless=True) as browser:
        page = await browser.new_page()
        page.on("response", _response_handler)
        await page.goto(url=url)
        await page.wait_for_load_state("networkidle")
    
    # Fetching urls and save as PDF
    await to_pdf(urls, output)


if __name__ == "__main__":
    asyncio.run(main())
