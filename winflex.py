from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class Flexor(object):
    def __init__(self):
        self.browser = webdriver.Chrome()

    def initialize(self):
        """
        Initializes the illustration winflex website by:
        -Finding the username and password fields
        -Filling it with the username and password from before
        -Click the login button
        """

        # Open the browser
        self.browser.get('https://www.winflexweb.com')

        # Login to the front page
        username = self.browser.find_element_by_css_selector("#tbUsername")
        username.send_keys('transpacificpeggy')
        password = self.browser.find_element_by_css_selector("#tbPassword")
        password.send_keys('1045TPoffice')
        login = self.browser.find_element_by_css_selector("#btnlogin")
        login.click()

        # Open illustrations tool
        illustration_front = self.browser.find_element_by_css_selector("a.shortcut:nth-child(1)")
        illustration_front.click()
        try:
            wait = WebDriverWait(self.browser, 15)
            element = wait.until(
                EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, "#divWinFlexShortcuts > div.panel-body > div > a:nth-child(1) > span"),
                    "Start a New Case"))
            print("Initialization Complete")
        except TimeoutException:
            print("Failed to Initialize")

    def new_case(self):
        """Selects the product and get into the forms page"""
        new_case = self.browser.find_element_by_css_selector("a.shortcut:nth-child(1)")
        new_case.click()
        company = self.browser.find_element_by_css_selector(
            "#lbProductSelectorCompanies > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1)")
        company.click()
        create_client = self.browser.find_element_by_css_selector("#btnProductSelectorCreate")
        create_client.click()

    def fill_client(self):
        """ Populates the client info form with initial values"""
        insured_tab = self.browser.find_element_by_css_selector('#QuestionTab0 > a:nth-child(1)')
        insured_tab.click()
        client_name = self.browser.find_element_by_css_selector(
            "#Insured\.Name\|0 > div:nth-child(2) > input:nth-child(1)")
        gender_select = Select(
            self.browser.find_element_by_css_selector("#Insured\.Sex\|0 > div:nth-child(2) > select:nth-child(1)"))
        class_select = Select(
            self.browser.find_element_by_css_selector(r"#Insured\2e Class\7c 0 > div.labelPosLeft > select"))
        age = self.browser.find_element_by_css_selector("#Insured\.Age\|0 > div:nth-child(2) > input:nth-child(1)")

        client_name.send_keys("Valued Client")
        gender_select.select_by_visible_text("Male")
        class_select.select_by_visible_text("Preferred Non-Tobacco")
        age.clear()
        age.send_keys("25")

    def fill_solve(self):
        """ Populates the solve for tab"""
        solve_tab = self.browser.find_element_by_css_selector('#QuestionTab1 > a:nth-child(1)')
        solve_tab.click()
        solve_for = Select(
            self.browser.find_element_by_css_selector("#Policy\.SolveFor\|0 > div:nth-child(2) > select:nth-child(1)"))
        solve_for.select_by_visible_text('Premium')
        solve_option = Select(
            self.browser.find_element_by_css_selector("#Policy\.Premium\|2 > div:nth-child(2) > select:nth-child(1)"))
        solve_option.select_by_visible_text("Guarantee Premium")
        payment_terms = Select(
            self.browser.find_element_by_css_selector(
                "#Combo_Policy\.PremiumYears\|0 > div:nth-child(2) > select:nth-child(1)"))
        payment_terms.select_by_visible_text('Year')
        years_to_pay_input = self.browser.find_element_by_css_selector(
            "#Textbox_Policy\.PremiumYears\.Years\|0 > div:nth-child(1) > input:nth-child(1)")
        years_to_pay_input.clear()
        years_to_pay_input.send_keys("5")

    def update_field(self, element, value):
        update_element = self.browser.find_element_by_css_selector(element)
        update_element.clear()
        update_element.send_keys(value)
        update_element.send_keys(Keys.TAB)

    def calculate(self):
        calculate = self.browser.find_element_by_css_selector("#btnClientCalc")
        calculate.click()
        print("Calculating")
        try:
            wait = WebDriverWait(self.browser, 75)
            element = wait.until(
                EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, "#divResults > div:nth-child(1) > div:nth-child(1) > h2:nth-child(1)")
                    , "Illustration Results"))
            print("Calculation Complete")
        except TimeoutException:
            print("Failed to calculate")

    def print_results(self):
        annual_premium = self.browser.find_element_by_css_selector("td.columnTextQC:nth-child(6)")
        target_premium = self.browser.find_element_by_css_selector("td.columnTextQC:nth-child(7")
        payment_duration = self.browser.find_element_by_css_selector("td.columnTextQC-center:nth-child(9)")
        sacs = self.browser.find_element_by_css_selector("td.columnTextQC-center:nth-child(4)")
        print("Insured is: \n" + sacs.text)
        print("Annual Premium: " + annual_premium.text + " " + "Target Premium: " + target_premium.text)
        print("Payment duration is: " + payment_duration.text)
        return int(annual_premium.text.replace(',', ''))

    def get_tp(self):
        target_premium = self.browser.find_element_by_css_selector("td.columnTextQC:nth-child(7)")
        return int(target_premium.text.replace(',', ''))

    def get_ap(self):
        annual_premium = self.browser.find_element_by_css_selector("td.columnTextQC:nth-child(6)")
        return int(annual_premium.text.replace(',', ''))

    def get_insured(self):
        insured_info = self.browser.find_element_by_css_selector("td.columnTextQC-center:nth-child(4)")
        return insured_info.text

    def reset_form(self):
        recalculate = self.browser.find_element_by_css_selector("a.text-primary")
        recalculate.click()
        print("Resetting..........")
        try:
            wait = WebDriverWait(self.browser, 5)
            element = wait.until(
                EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, "#QuestionTab1 > a"), "Solve For"))
            print("Reset Complete")
        except TimeoutException:
            print("Failed to reset")


def illustrate_suite(flexor, intervals):
    """
    :param flexor: uses the initialized winflex illustration object, Flexor
    :param intervals: the different payment durations
    :return: the target premium and annual premiums
    """
    payment_duration_field = "#Textbox_Policy\.PremiumYears\.Years\|0 > div:nth-child(1) > input:nth-child(1)"
    solve_tab = flexor.browser.find_element_by_css_selector('#QuestionTab1 > a:nth-child(1)')
    solve_tab.click()
    premiums = []
    insured = ""
    for duration in intervals:
        flexor.update_field(payment_duration_field, duration)
        flexor.calculate()
        if duration == "5":
            premiums.append(flexor.get_tp())
            premiums.append(flexor.get_ap())
            insured = flexor.get_insured()
        else:
            premiums.append(flexor.get_ap())
        flexor.reset_form()
    print(insured)
    print(*premiums, sep="\n")

def illustrate_other(flexor, intervals):
    """
    :param flexor: uses the initialized winflex illustration object, Flexor
    :param intervals: the different payment durations
    :return: the target premium and annual premiums
    """
    end_year = ".schedule > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)"
    payment_duration_field = "td.active:nth-child(2) > input:nth-child(1)"
    solve_tab = flexor.browser.find_element_by_css_selector('#QuestionTab1 > a:nth-child(1)')
    solve_tab.click()
    premiums = []
    insured = ""
    for duration in intervals:
        end_button = flexor.browser.find_element_by_css_selector(end_year)
        end_button.click()
        payment_duration = flexor.browser.find_element_by_css_selector(payment_duration_field)
        payment_duration.send_keys(Keys.BACKSPACE)
        payment_duration.send_keys(Keys.BACKSPACE)
        payment_duration.send_keys(Keys.BACKSPACE)
        payment_duration.send_keys(duration)
        payment_duration.send_keys(Keys.TAB)
        flexor.calculate()
        if duration == "5":
            premiums.append(flexor.get_tp())
            premiums.append(flexor.get_ap())
            insured = flexor.get_insured()
        else:
            premiums.append(flexor.get_ap())
        flexor.reset_form()
    print(insured)
    print(*premiums, sep="\n")

def fills(flex):
    flex.new_case()
    flex.fill_client()
    flex.fill_solve()


def illustrate_range(flex, range, interval):
    for age in range:
        insured_tab = flex.browser.find_element_by_css_selector('#QuestionTab0 > a:nth-child(1)')
        insured_tab.click()
        flex.update_field("#Insured\.Age\|0 > div:nth-child(2) > input:nth-child(1)", age)
        illustrate_suite(flex, interval)
        print("Age: " + age + " Completed")


if __name__ == '__main__':
    """
    First initialize the winflex browser with flex = Flexor()
    then use the flex object with the illustrate_range function to illustrate based on age_range and interval
    illustrate_suite just runs the illustrations for that age at the intervals defined.
    """

    interval = ["5", "10"]
    age_range = ["25","30","35","40","45","50","55","60","65"]