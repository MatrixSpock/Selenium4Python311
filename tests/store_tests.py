import os
import time

import pytest
from selenium import webdriver
from selenium.common import NoSuchElementException
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.definitions import ROOT_DIR


def test_xpath_comparison_button(browser, root_url):
    browser.get(root_url)

    cmp_button = browser.find_element(By.XPATH, "//*[@id='root']/section[1]/div[3]/div[2]/button[2]")
    assert cmp_button.text == 'Comparison'

    cmp_button = browser.find_element(By.XPATH, "/html/body/div/section[1]/div[3]/div[2]/button[2]")
    assert cmp_button.text == 'Comparison'

    cmp_button = browser.find_element(By.XPATH, "(//button[text()='Comparison']//ancestor::div[1]//child::button)[2]")
    assert cmp_button.text == 'Comparison'


def test_css_selectors(browser, root_url):
    browser.get(root_url)

    el1 = browser.find_element(By.CSS_SELECTOR, "button[name='favorites']")
    el2 = browser.find_element(By.CSS_SELECTOR, "button[class='sc-iBYQkv doKaoE']")
    el3 = browser.find_element(By.CSS_SELECTOR, "button.sc-iBYQkv.doKaoE")
    el4 = browser.find_element(By.CSS_SELECTOR, "button[name='favorites'][class='sc-iBYQkv doKaoE']")

    el5 = browser.find_element(By.CSS_SELECTOR, "button[id='goToSelection']")
    el6 = browser.find_element(By.CSS_SELECTOR, "#goToSelection")

    lst = [el1, el2, el3, el4, el5, el6]

    assert all(el is not None for el in lst)


def test_can_add_and_remove_favorites(browser, root_url):
    browser.get(root_url)
    browser.maximize_window()

    browser.find_element(By.PARTIAL_LINK_TEXT, 'selection').click()
    browser.find_element(By.ID, 'goToSelection').click()
    browser.find_element(By.ID, 'carBatteries').click()

    product_block = browser.find_element(By.ID, 'product1')
    product_name_adding_to_favorites = product_block.find_element(By.TAG_NAME, 'a').text
    product_block.find_element(By.NAME, 'addToFavorites').click()

    # browser.find_element(By.CLASS_NAME, 'sc-iBYQkv doKaoE').click()
    browser.find_element(By.NAME, 'favorites').click()

    product_name_in_favorites = browser.find_element(By.ID, 'product1').find_element(By.TAG_NAME, 'a').text

    assert product_name_adding_to_favorites == product_name_in_favorites

    time.sleep(2)
    browser.find_element(By.NAME, 'remove').click()
    time.sleep(2)

    with pytest.raises(NoSuchElementException):
        browser.find_element(By.ID, 'product1')


@pytest.fixture
def browser(scope='module'):
    driver = webdriver.Chrome()
    # driver.maximize_window()
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
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'about_title')))

    about_title = browser.find_element(By.NAME, 'about_title')
    assert about_title.text == 'Information about our company'

    time.sleep(2)
