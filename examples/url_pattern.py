from dude import select


@select(css="a.url", url=r".*\.html")
def result_url(element):
    return {"url": element.get_attribute("href")}


@select(css=".title", url=r".*\.html")
def result_title(element):
    return {"title": element.text_content()}


@select(css=".description", url=r".*\.html")
def result_description(element):
    return {"description": element.text_content()}


if __name__ == "__main__":
    from pathlib import Path

    import dude

    html = f"file://{(Path(__file__).resolve().parent / 'dude.html').absolute()}"
    dude.run(urls=[html])
