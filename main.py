from lazyscraper import Request, export_json, export_duckdb
from selectolax.parser import HTMLParser
from time import sleep

def price_parser(value: str) -> int | str:
    try:
        price = int(value.attrs["v-text"].split("|")[-1].replace("'", "").replace("$", "").strip())
        return price
    except:
        return value

def parse(response) -> list:
    parser = HTMLParser(response.text)
    products = parser.css_first('div.grid.grid-flow-dense.grid-cols-2[class~="md:grid-cols-4"]')
    data: list[dict] = []
    for product in products.css("div.group.relative.flex.h-full"):
        text = product.css_first("p.font-sans.text-xs.font-medium.tracking-wider.uppercase[class~='md:text-sm']")
        price = product.css_first("p.flex.items-center.text-xs[class~='xl:hidden'] span")
    
        data.append({"name": text.text(), "price": price_parser(price)})
    return data
                                              

def main():
    for new_arrival in ["mens","womens"]:
        req = Request(
            URL= f"https://www.allbirds.com/collections/{new_arrival}-new-arrivals",
            impersonate= "chrome",
            headers= None,
            params= None,
            proxies= None,
            cookies= None,
        )
        res = req.get()

        data = parse(res)
    
        export_json(data, f"./scraped_data/{new_arrival}.json")
        export_duckdb(data, "scraped.ddb", f"{new_arrival}")
        sleep(2)

main()


