from base_test import BaseTestCase, create_custom_tender, BASE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NavigationTests(BaseTestCase):
    def test_home_page_load(self):
        driver = self.driver
        self.assertIn("Landing", driver.title)
        
        header = driver.find_element(By.XPATH, "//h1[contains(text(), 'Welcome!')]")
        self.assertTrue(header.is_displayed())
        
        paragraph = driver.find_element(By.XPATH, "//p[contains(text(), 'Witaj w systemie przetargowym')]")
        self.assertTrue(paragraph.is_displayed())
        
    def test_active_tenders_navigation_empty(self):
        driver = self.driver
        driver.find_element(By.XPATH, "//a[@href='/tenders']").click()
        
        self.assertIn("Active tenders", driver.title)
        
        header = driver.find_element(By.XPATH, "//h1[contains(text(), 'Active Tenders')]")
        self.assertTrue(header.is_displayed())
        
        no_tenders_para = driver.find_element(By.XPATH, "//p[contains(text(), 'No tenders found.')]")
        self.assertTrue(no_tenders_para.is_displayed())
        
    def test_tender_details_invalid_id_shows_landing(self):
        driver = self.driver
        driver.get(f"{BASE_URL}/tenders/aaaaa")
        WebDriverWait(driver, 10).until(EC.title_contains("Landing"))
        self.assertIn("Landing", driver.title)
        self.assertTrue(driver.find_element(By.XPATH, "//h1[contains(text(), 'Welcome!')]").is_displayed())
        
    def test_tender_details_for_not_yet_started_tender_redirects(self):
        driver = self.driver
        create_custom_tender(
            driver,
            orderer="Future Orderer",
            price="5000",
            name="Future Tender",
            description="This is a future tender description.",
            start_time="01-05-2035\t13:11:00",
            end_time="01-05-2040\t13:11:00"
        )
        WebDriverWait(driver, 10).until(EC.title_contains("Landing"))
        self.assertIn("Landing", driver.title)
        self.assertTrue(driver.find_element(By.XPATH, "//h1[contains(text(), 'Welcome!')]").is_displayed()) 
        
    def test_active_tenders_navigation(self):
        driver = self.driver
        create_custom_tender(
            driver,
            orderer="Active Orderer",
            price="5000",
            name="Active Tender",
            description="This is a active tender description.",
            start_time="01-05-2000\t13:11:00",
            end_time="01-05-2040\t13:11:00"
        )
        WebDriverWait(driver, 10).until(EC.url_contains("/tenders"))
        tenders_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/tenders']"))
        )
        tenders_button.click()  
        
        self.assertIn("Active tenders", driver.title)
        
        header = driver.find_element(By.XPATH, "//h1[contains(text(), 'Active Tenders')]")
        self.assertTrue(header.is_displayed())
        
        tenders_table = driver.find_element(By.XPATH, "//table[@class='tenders-table']")
        self.assertTrue(tenders_table.is_displayed())
        
        tenders_rows = tenders_table.find_elements(By.TAG_NAME, "tr")
        self.assertGreater(len(tenders_rows), 1, "No tenders found in the table.")
        
        tender_row = tenders_rows[1]
        tender_cells = tender_row.find_elements(By.TAG_NAME, "td")
        self.assertEqual(len(tender_cells), 6, "Tender row does not have the expected number of cells.")
        
        tender_name = tender_cells[1].text
        tender_orderer = tender_cells[2].text
        
        self.assertEqual(tender_name, "Active Tender", "Tender name does not match.")
        self.assertEqual(tender_orderer, "Active Orderer", "Tender orderer does not match.")
        
    def test_past_tenders_navigation_empty(self):
        driver = self.driver
        active_tenders_button = driver.find_element(By.XPATH, "//a[@href='/tenders/past']")
        active_tenders_button.click()
        
        self.assertIn("Past Tenders", driver.title)
        
        header = driver.find_element(By.XPATH, "//h1[contains(text(), 'Past Tenders')]")
        self.assertTrue(header.is_displayed())
        
        no_tenders_para = driver.find_element(By.XPATH, "//p[contains(text(), 'No tenders found.')]")
        self.assertTrue(no_tenders_para.is_displayed())
        
    def test_past_tenders_navigation(self):
        driver = self.driver
        new_tender_button = driver.find_element(By.XPATH, "//a[@href='/tenders/new']")
        new_tender_button.click()
        
        create_custom_tender(
            driver,
            orderer="Past Orderer",
            price="5000",
            name="Past Tender",
            description="This is a past tender description.",
            start_time="01-05-2015\t13:11:00",
            end_time="01-05-2016\t13:11:00"
        )
        WebDriverWait(driver, 10).until(EC.url_contains("/tenders"))
        tenders_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/tenders/past']"))
        )
        tenders_button.click()          
        
        self.assertIn("Past Tenders", driver.title)
        closed_td = driver.find_element(By.XPATH, "//td[contains(text(), 'Closed')]")
        self.assertTrue(closed_td.is_displayed())
        