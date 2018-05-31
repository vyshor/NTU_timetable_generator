from extract_table import extract_table
from selenium.webdriver import Chrome
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By

URL = 'https://wish.wis.ntu.edu.sg/webexe/owa/aus_schedule.main'
WEBDRIVER_PATH = 'chromedriver'
browser = Chrome(WEBDRIVER_PATH)
browser.get(URL)

select_fr = Select(browser.find_element_by_name('r_course_yr'))
options = browser.find_elements(By.XPATH, '//option')


for x in range(1, len(select_fr.options)):
    select_fr.select_by_index(x)
    if select_fr.first_selected_option.text != ' ' and len(select_fr.first_selected_option.text) != 1 and '--' not in select_fr.first_selected_option.text:
        browser.find_element_by_xpath("//input[@type='button'][@value='Load Class Schedule']").click()
        browser.switch_to.window(browser.window_handles[-1])
        extract_table(browser.page_source)
        browser.close()
        browser.switch_to.window(browser.window_handles[0])

browser.quit()


