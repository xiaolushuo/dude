from typing import Dict, List
from unittest import mock

import pytest
from braveblock import Adblocker
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from dude import Scraper
from dude.optional.selenium_scraper import SeleniumScraper


@pytest.fixture()
def scraper_application_with_selenium_parser() -> Scraper:
    scraper = SeleniumScraper()
    scraper.adblock = Adblocker(rules=["https://dude.ron.sh/blockme.css"])
    return Scraper(scraper=scraper)


@pytest.fixture()
def selenium_select(scraper_application: Scraper) -> None:
    @scraper_application.group(css=".custom-group")
    @scraper_application.select(css=".title")
    def title(element: WebElement) -> Dict:
        return {"title": element.text}

    @scraper_application.select(css=".title", group_css=".custom-group")
    def empty(element: WebElement) -> Dict:
        return {}

    @scraper_application.group(css=".custom-group")
    @scraper_application.select(css=".title", url=r"example\.com")
    def url_dont_match(element: WebElement) -> Dict:
        return {"title": element.text}

    @scraper_application.select(css=".url", group_css=".custom-group")
    def url(element: WebElement) -> Dict:
        return {"url": element.get_attribute("href")}


@pytest.fixture()
def selenium_select_with_parser(scraper_application_with_selenium_parser: Scraper) -> None:
    @scraper_application_with_selenium_parser.group(css=".custom-group")
    @scraper_application_with_selenium_parser.select(css=".title")
    def title(element: WebElement) -> Dict:
        return {"title": element.text}

    @scraper_application_with_selenium_parser.select(css=".title", group_css=".custom-group")
    def empty(element: WebElement) -> Dict:
        return {}

    @scraper_application_with_selenium_parser.group(css=".custom-group")
    @scraper_application_with_selenium_parser.select(css=".title", url=r"example\.com")
    def url_dont_match(element: WebElement) -> Dict:
        return {"title": element.text}

    @scraper_application_with_selenium_parser.select(css=".url", group_css=".custom-group")
    def url(element: WebElement) -> Dict:
        return {"url": element.get_attribute("href")}


@pytest.fixture()
def selenium_xpath(scraper_application: Scraper) -> None:
    @scraper_application.select(
        xpath='.//p[contains(@class, "title")]', group_xpath='.//div[contains(@class, "custom-group")]'
    )
    def title(element: WebElement) -> Dict:
        return {"title": element.text}

    @scraper_application.select(
        xpath='.//a[contains(@class, "url")]', group_xpath='.//div[contains(@class, "custom-group")]'
    )
    def url(element: WebElement) -> Dict:
        return {"url": element.get_attribute("href")}


@pytest.fixture()
def selenium_text(scraper_application: Scraper) -> None:
    @scraper_application.select(text="Title", group_css=".custom-group")
    def title(element: WebElement) -> Dict:
        return {"title": element.text}

    @scraper_application.select(xpath='.//a[contains(@class, "url")]', group_css=".custom-group")
    def url(element: WebElement) -> Dict:
        return {"url": element.get_attribute("href")}


@pytest.fixture()
def selenium_regex(scraper_application: Scraper) -> None:
    @scraper_application.select(regex=".*", group_css=".custom-group")
    def title(element: WebElement) -> Dict:
        return {}


@pytest.fixture()
def selenium_setup(scraper_application: Scraper) -> None:
    @scraper_application.select(css=":root", setup=True)
    def check_page(element: WebElement, driver: WebDriver) -> None:
        assert element is not None


@pytest.fixture()
def selenium_navigate(scraper_application: Scraper) -> None:
    @scraper_application.select(css=":root", navigate=True)
    def next_page(element: WebElement, driver: WebDriver) -> bool:
        assert element is not None
        return True


@pytest.fixture()
def async_selenium_select(scraper_application: Scraper) -> None:
    @scraper_application.group(css=".custom-group")
    @scraper_application.select(css=".title")
    async def title(element: WebElement) -> Dict:
        return {"title": element.text}

    @scraper_application.select(css=".title", group_css=".custom-group")
    async def empty(element: WebElement) -> Dict:
        return {}

    @scraper_application.group(css=".custom-group")
    @scraper_application.select(css=".title", url=r"example\.com")
    async def url_dont_match(element: WebElement) -> Dict:
        return {"title": element.text}

    @scraper_application.select(css=".url", group_css=".custom-group")
    async def url(element: WebElement) -> Dict:
        return {"url": element.get_attribute("href")}


@pytest.fixture()
def async_selenium_xpath(scraper_application: Scraper) -> None:
    @scraper_application.select(
        xpath='.//p[contains(@class, "title")]', group_xpath='.//div[contains(@class, "custom-group")]'
    )
    async def title(element: WebElement) -> Dict:
        return {"title": element.text}

    @scraper_application.select(
        xpath='.//a[contains(@class, "url")]', group_xpath='.//div[contains(@class, "custom-group")]'
    )
    async def url(element: WebElement) -> Dict:
        return {"url": element.get_attribute("href")}


@pytest.fixture()
def async_selenium_text(scraper_application: Scraper) -> None:
    @scraper_application.select(text="Title", group_css=".custom-group")
    async def title(element: WebElement) -> Dict:
        return {"title": element.text}

    @scraper_application.select(xpath='.//a[contains(@class, "url")]', group_css=".custom-group")
    async def url(element: WebElement) -> Dict:
        return {"url": element.get_attribute("href")}


@pytest.fixture()
def async_selenium_setup(scraper_application: Scraper) -> None:
    @scraper_application.select(css=":root", setup=True)
    async def check_page(element: WebElement, driver: WebDriver) -> None:
        assert element is not None


@pytest.fixture()
def async_selenium_navigate(scraper_application: Scraper) -> None:
    @scraper_application.select(css=":root", navigate=True)
    async def next_page(element: WebElement, driver: WebDriver) -> bool:
        assert element is not None
        return True


@pytest.mark.parametrize(
    "browser_type",
    (
        "chromium",
        "firefox",
    ),
)
def test_full_flow(
    scraper_application: Scraper,
    selenium_select: None,
    selenium_setup: None,
    selenium_navigate: None,
    expected_data: List[Dict],
    test_url: str,
    browser_type: str,
) -> None:
    assert scraper_application.has_async is False
    assert len(scraper_application.rules) == 6
    mock_save = mock.MagicMock()
    scraper_application.save(format="custom")(mock_save)
    scraper_application.run(urls=[test_url], pages=2, format="custom", parser="selenium", browser_type=browser_type)
    mock_save.assert_called_with(expected_data, None)


def test_full_flow_without_setup_and_navigate(
    scraper_application: Scraper,
    selenium_select: None,
    expected_data: List[Dict],
    test_url: str,
) -> None:
    assert scraper_application.has_async is False
    assert len(scraper_application.rules) == 4
    mock_save = mock.MagicMock()
    scraper_application.save(format="custom")(mock_save)
    scraper_application.run(urls=[test_url], pages=2, format="custom", parser="selenium")
    mock_save.assert_called_with(expected_data, None)


def test_full_flow_xpath(
    scraper_application: Scraper,
    selenium_xpath: None,
    selenium_setup: None,
    selenium_navigate: None,
    expected_data: List[Dict],
    test_url: str,
) -> None:
    assert scraper_application.has_async is False
    assert len(scraper_application.rules) == 4
    mock_save = mock.MagicMock()
    scraper_application.save(format="custom")(mock_save)
    scraper_application.run(urls=[test_url], pages=2, format="custom", parser="selenium")
    mock_save.assert_called_with(expected_data, None)


def test_full_flow_text(
    scraper_application: Scraper,
    selenium_text: None,
    selenium_setup: None,
    selenium_navigate: None,
    expected_data: List[Dict],
    test_url: str,
) -> None:
    assert scraper_application.has_async is False
    assert len(scraper_application.rules) == 4
    mock_save = mock.MagicMock()
    scraper_application.save(format="custom")(mock_save)
    scraper_application.run(urls=[test_url], pages=2, format="custom", parser="selenium")
    mock_save.assert_called_with(expected_data, None)


@pytest.mark.parametrize(
    "browser_type",
    (
        "chromium",
        "firefox",
    ),
)
def test_full_flow_async(
    scraper_application: Scraper,
    async_selenium_select: None,
    async_selenium_setup: None,
    async_selenium_navigate: None,
    expected_data: List[Dict],
    test_url: str,
    browser_type: str,
) -> None:
    assert scraper_application.has_async is True
    assert len(scraper_application.rules) == 6
    mock_save = mock.MagicMock()
    scraper_application.save(format="custom")(mock_save)
    scraper_application.run(urls=[test_url], pages=2, format="custom", parser="selenium", browser_type=browser_type)
    mock_save.assert_called_with(expected_data, None)


def test_full_flow_async_with_sync_setup_and_navigate(
    scraper_application: Scraper,
    async_selenium_select: None,
    selenium_setup: None,
    selenium_navigate: None,
    expected_data: List[Dict],
    test_url: str,
) -> None:
    assert scraper_application.has_async is True
    assert len(scraper_application.rules) == 6
    mock_save = mock.MagicMock()
    scraper_application.save(format="custom")(mock_save)
    scraper_application.run(urls=[test_url], pages=2, format="custom", parser="selenium")
    mock_save.assert_called_with(expected_data, None)


def test_full_flow_async_without_setup_and_navigate(
    scraper_application: Scraper,
    async_selenium_select: None,
    expected_data: List[Dict],
    test_url: str,
) -> None:
    assert scraper_application.has_async is True
    assert len(scraper_application.rules) == 4
    mock_save = mock.MagicMock()
    scraper_application.save(format="custom")(mock_save)
    scraper_application.run(urls=[test_url], pages=2, format="custom", parser="selenium")
    mock_save.assert_called_with(expected_data, None)


def test_full_flow_xpath_async(
    scraper_application: Scraper,
    async_selenium_xpath: None,
    async_selenium_setup: None,
    async_selenium_navigate: None,
    expected_data: List[Dict],
    test_url: str,
) -> None:
    assert scraper_application.has_async is True
    assert len(scraper_application.rules) == 4
    mock_save = mock.MagicMock()
    scraper_application.save(format="custom")(mock_save)
    scraper_application.run(urls=[test_url], pages=2, format="custom", parser="selenium")
    mock_save.assert_called_with(expected_data, None)


def test_full_flow_text_async(
    scraper_application: Scraper,
    async_selenium_text: None,
    async_selenium_setup: None,
    async_selenium_navigate: None,
    expected_data: List[Dict],
    test_url: str,
) -> None:
    assert scraper_application.has_async is True
    assert len(scraper_application.rules) == 4
    mock_save = mock.MagicMock()
    scraper_application.save(format="custom")(mock_save)
    scraper_application.run(urls=[test_url], pages=2, format="custom", parser="selenium")
    mock_save.assert_called_with(expected_data, None)


def test_unsupported_regex(
    scraper_application: Scraper,
    selenium_regex: None,
    expected_data: List[Dict],
    test_url: str,
) -> None:
    assert scraper_application.has_async is False
    assert len(scraper_application.rules) == 1
    mock_save = mock.MagicMock()
    scraper_application.save(format="custom")(mock_save)
    with pytest.raises(Exception):
        scraper_application.run(urls=[test_url], pages=2, format="custom", parser="selenium")


def test_scraper_with_parser(
    scraper_application_with_selenium_parser: Scraper,
    selenium_select_with_parser: None,
    expected_data: List[Dict],
    test_url: str,
) -> None:
    assert scraper_application_with_selenium_parser.has_async is False
    assert scraper_application_with_selenium_parser.scraper is not None
    assert len(scraper_application_with_selenium_parser.scraper.rules) == 4
    mock_save = mock.MagicMock()
    mock_save.return_value = True
    scraper_application_with_selenium_parser.save(format="custom")(mock_save)
    scraper_application_with_selenium_parser.run(urls=[test_url], pages=2, format="custom", parser="selenium")
    mock_save.assert_called_with(expected_data, None)
