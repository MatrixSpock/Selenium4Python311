import os
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.definitions import ROOT_DIR

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def root_url():
    return os.path.join(ROOT_DIR, 'store', 'index.html')

def test_page_titles_are_correct(browser, root_url):
    # service = Service(executable_path="C:\\webdrivers\\chromedriver.exe")
    # browser = webdriver.Chrome(service=service)

    browser.get(root_url)

    main_title = browser.find_element(By.ID, 'main_title')
    assert main_title.text == 'Batteries online store'

    time.sleep(2)

    # This action opens a new window
    delivery_page_link = browser.find_element(By.LINK_TEXT, 'Payment and delivery')
    delivery_page_link.click()

    # Wait for the new window or tab to open and then switch to it
    WebDriverWait(browser, 10).until(EC.number_of_windows_to_be(2))
    # Get the handle of the current window to switch back to it later if necessary
    original_window = browser.current_window_handle
    # Get the new window handle
    new_window = [window for window in browser.window_handles if window != original_window][0]
    # Switch to the new window
    browser.switch_to.window(new_window)

    # Now, in the new window, wait for the 'delivery_title' element to be present
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'delivery_title')))

    # Locate this element in the new window
    delivery_title = browser.find_element(By.NAME, 'delivery_title')
    assert delivery_title.text == 'Payment and shipping Information'

    time.sleep(2)

    # New Browser Tab opens here
    about_page = browser.find_element(By.LINK_TEXT, 'About company')
    about_page.click()

    # Wait for the new tab to open and then switch to it
    WebDriverWait(browser, 10).until(EC.number_of_windows_to_be(3))
    # Check window handle doesn't match original or previously set "new_window" and then update
    new_window = [window for window in browser.window_handles if window != original_window and window != new_window][0]
    # Switch to the new tab
    browser.switch_to.window(new_window)

    # Wait for the "about_title" element to be present
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME,'about_title')))

    about_title = browser.find_element(By.NAME, 'about_title')
    assert about_title.text == 'Information about our company'

    time.sleep(2)