import urllib.parse
import urllib.request
import bs4
from log import LOG


def search_fanwiki(game, item=None):

    resp = scrape_wiki(game, item)

    if type(resp) is list:
        if len(resp) > 1:
            message = f'Game "{game}" not found, Did you mean one of the following?\n'
            for i in resp:
                message += f"{i} \n"

            return message
        elif len(resp) == 1:
            message = f'Game "{game}" not found. Did you mean "{resp[0]}"?'
            return message
        else:
            message = f'Game "{game}" not found'
            return message
    else:
        return resp  # returns wiki page link


def scrape_wiki(game, item):
    game.replace(" ", "+")
    LOG.info("request start")

    query = urllib.parse.urlencode({"query": game, "scope": "community"})

    response = urllib.request.urlopen(
        "https://ucp.fandom.com/wiki/Special:SearchCommunity?" + query
    )

    LOG.info("searching result")
    game_soup = bs4.BeautifulSoup(response.read(), "html.parser").find_all(
        attrs="unified-search__result__title", limit=10
    )

    LOG.info("searching complete")

    try:
        game_list = []

        for game_link in game_soup:
            link_title = game_link["data-title"].rsplit(" ", 1)[0]
            if game.lower() in link_title.lower():
                page = game_link.get("href")

                if item:
                    item = item.replace(" ", "+")
                    page = page + \
                        f"Special:Search?query={item}&scope=internal&go=Go"

                return page

            else:
                game_list.append(link_title)
        return game_list

    except AttributeError as e:
        LOG.info(e)
        return "Nothing Found"
