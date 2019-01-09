#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from time import sleep

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


def wait():
    sleep(1)


def get_driver():
    driver_path = input("Enter path to Chromedriver: ")
    return str(driver_path).strip()


def open_browser(url, driver=get_driver()):
    browser = Chrome(driver)
    browser.get(url)
    return browser


def execute_moves(browser, time_input):
    def find_elem(by, path):
        return browser.find_element(by, path)

    def find_elems(by, path, i):
        return browser.find_elements(by, path)[i]

    moves = [ find_elem(By.XPATH, '//div[@data-tooltip="Driving"]').click()
            , find_elem(By.CLASS_NAME, "goog-menu-button-dropdown").click()
            , find_elems(By.CLASS_NAME, "goog-menuitem-content", 1).click()
            , find_elem(By.CLASS_NAME, "time-input").clear()
            , find_elem(By.CLASS_NAME, "time-input").send_keys(time_input)
            ]

    for move in moves:
        move
        wait()


def get_html(browser):
    return (browser.page_source).encode('utf-8')


def get_travel_info(soup):
    p_time = re.compile(r"(\d+) min")
    p_distance = re.compile(r"(\d*[.]*\d+) mile")
    first_result = soup.find_all(attrs={"data-trip-index": "0"})[0]
    travel_mins = int(p_time.search(first_result.text).group(1))
    travel_miles = float(p_distance.search(first_result.text).group(1))
    return travel_mins, travel_miles


def format_address(raw_address):
    return raw_address.replace(" ", "+")


def addresses_to_url(addr_list):
    url = "https://www.google.com/maps/dir/{}"
    return url.format("/".join(addr_list).replace(" ", "+"))


def locations_to_travel_info(addr_list, time_input):
    url = addresses_to_url(addr_list)
    browser = open_browser(url)
    execute_moves(browser, time_input)
    soup = BeautifulSoup(get_html(browser), "html.parser")
    browser.quit()
    return get_travel_info(soup)


def get_safe_time(time_input):
    return time_input.replace(":", "-").replace(" ", "_")


if __name__ == "__main__":
    addr_to = "200 Willoughby Ave, Brooklyn, NY 11205"
    addr_from = "144 W 14th St, New York, NY 10011"

    travel_mins, travel_miles = \
        locations_to_travel_info([addr_from, addr_to], "3:00 AM")

    print("Travel time: {} minutes".format(travel_mins))
    print("Travel distance: {} miles".format(travel_miles))
