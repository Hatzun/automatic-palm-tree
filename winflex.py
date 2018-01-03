from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def calculate_age(browser, age):
    solve_for = Select(
        browser.find_element_by_css_selector("#Policy\.SolveFor\|0 > div:nth-child(2) > select:nth-child(1)"))
    solve_for.select_by_index(0)
    solve_for.select_by_index(2)
    input_age = browser.find_element_by_css_selector("#Textbox_Policy\.PremiumYears\.Years\|0 > div:nth-child(1) > input:nth-child(1)")
    client_age = age
    input_age.clear()
    input_age.send_keys(client_age)
    calculate = browser.find_element_by_css_selector("#btnClientCalc")
    calculate.click()
    try:
        wait = WebDriverWait(browser, 15)
        element = wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "#divSnapshotPanel > div:nth-child(1) > div:nth-child(1)"), "Snapshot"))
        print("calculation complete")
    except TimeoutException:
        print("failed")

def get_premiums(browser):
    annual_premium = browser.find_element_by_css_selector("td.columnTextQC:nth-child(6)")
    target_premium = browser.find_element_by_css_selector("td.columnTextQC:nth-child(7)")
    print("Annual Premium: " + annual_premium.text + " " + "Target Premium: " + target_premium.text)


def main():
    browser = webdriver.Firefox()
    browser.get('https://www.winflexweb.com')
    intervals = ["5", "10", "20"]
    age_range = ["35","40","45","50","55","60","65"]

    #Log into the front page by selecting the username box, the tbpassword box, and then clicking the login
    username = browser.find_element_by_css_selector("#tbUsername")
    username.send_keys('transpacificpeggy')
    password = browser.find_element_by_css_selector("#tbPassword")
    password.send_keys('1045TPoffice')
    login = browser.find_element_by_css_selector("#btnlogin")
    login.click()

    #Open illustrations
    illustration_front = browser.find_element_by_css_selector("a.shortcut:nth-child(1)")
    illustration_front.click()

    #Need a wait here for new case button to come up
    new_case = browser.find_element_by_css_selector("a.shortcut:nth-child(1)")
    new_case.click()
    company = browser.find_element_by_css_selector(
        "#lbProductSelectorCompanies > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1)")
    company.click()
    create_client = browser.find_element_by_css_selector("#btnProductSelectorCreate")
    create_client.click()

    #Fill out the insured page
    client_name = browser.find_element_by_css_selector("#Insured\.Name\|0 > div:nth-child(2) > input:nth-child(1)")
    gender_select = Select(
        browser.find_element_by_css_selector("#Insured\.Sex\|0 > div:nth-child(2) > select:nth-child(1)"))
    age = browser.find_element_by_css_selector("#Insured\.Age\|0 > div:nth-child(2) > input:nth-child(1)")

    client_name.send_keys('Valued Client')
    gender_select.select_by_visible_text("Female")
    age.clear()
    client_age = '35'
    age.send_keys(client_age)

    #Solve for page
    solve_for = Select(
        browser.find_element_by_css_selector("#Policy\.SolveFor\|0 > div:nth-child(2) > select:nth-child(1)"))
    solve_for.select_by_visible_text('Premium')
    solve_option = Select(
        browser.find_element_by_css_selector("#Policy\.Premium\|2 > div:nth-child(2) > select:nth-child(1)"))
    solve_option.select_by_visible_text("Guarantee Premium")
    years_to_pay = Select(
        browser.find_element_by_css_selector("#Combo_Policy\.PremiumYears\|0 > div:nth-child(2) > select:nth-child(1)"))
    years_to_pay.select_by_visible_text('Year')


    #Calculate
    calculate = browser.find_element_by_css_selector("#btnClientCalc")
    calculate.click()
    try:
        wait = WebDriverWait(browser, 15)
        element = wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "#divSnapshotPanel > div:nth-child(1) > div:nth-child(1)"), "Snapshot"))
        target_premium = browser.find_element_by_css_selector("td.columnTextQC:nth-child(7)")
        print(target_premium.text)
    except TimeoutException:
        print("failed")
    finally:
        print("finally")

    #Recalculate
    recalculate = browser.find_element_by_css_selector("a.text-primary")
    recalculate.click()