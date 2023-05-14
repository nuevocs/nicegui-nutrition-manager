from playwright.async_api import async_playwright
from selectolax.parser import HTMLParser
from dataclasses import dataclass


@dataclass
class SearchTerm:
    name: str
    url: str
    description: str


async def get_search_result(search_term):
    uri = "https://calorie.slism.jp/"
    url = uri + "?searchWord=" + search_term + "&search=検索&x=0&y=0"
    # print(url)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        html = await page.content()

        tree = HTMLParser(html)

        # selectors
        titles_sel = "#contentsTokushuLeft > div.searchItemArea > table > tbody > tr > td > a.searchName"
        urls_sel = "#contentsTokushuLeft > div.searchItemArea > table > tbody > tr > td > a.searchName"
        desc_sel = "#contentsTokushuLeft > div.searchItemArea > table > tbody > tr > td > span.ccds_unit"

        # get data
        titles = [node.text().strip() for node in tree.css(titles_sel)]
        urls = [uri + node.attributes['href'] for node in tree.css(urls_sel)]
        descs = [node.text().strip() for node in tree.css(desc_sel)]

        # list-ize data
        lst = []
        for t, u, d in zip(titles, urls, descs):
            # print(t, u, d)
            search_terms = SearchTerm(
                t, u, d
            )
            lst.append(search_terms)
        # print(lst)

        result = {item.url: f"{item.name} / {item.description}" for item in lst}
        # print(result)
    return result


@dataclass
class IndividualFood:
    title: str
    serving_name: str
    serving_amount: float
    protein: float
    fat: float
    carb: float


async def get_nutrition_detail(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        html = await page.content()

        tree = HTMLParser(html)

        title = "#contentsPadding > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > h1"
        protein = "#protein_content"
        fat = "#fat_content"
        carb = "#carb_content"
        serv_amt = "#serving_content"
        serv_name = "#serving_comment"

        t = tree.css_first(title).text().replace(" ", "")
        svn = tree.css_first(serv_name).text().replace(" ", "")
        sv = float(tree.css_first(serv_amt).text().strip())
        p = float(tree.css_first(protein).text().strip())
        f = float(tree.css_first(fat).text().strip())
        c = float(tree.css_first(carb).text().strip())

        nutrition = IndividualFood(t, svn, sv, p, f, c)

        await browser.close()

    return nutrition
