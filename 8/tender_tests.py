from base_test import BaseTestCase, create_custom_tender
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class TenderTests(BaseTestCase):

    def test_tender_details_for_ended_tender(self):
        driver = self.driver
        create_custom_tender(
            driver,
            orderer="Future Orderer",
            price="5000",
            name="Future Tender",
            description="This is a future tender description.",
            start_time="01-05-2000\t13:11:00",
            end_time="01-05-2001\t13:11:00"
        )
        WebDriverWait(driver, 10).until(EC.title_contains("Tender Details"))
        self.assertIn("Tender Details", driver.title)
        self.assertTrue(driver.find_element(By.XPATH, "//p[@class='no-offers']").is_displayed())       
    
    def test_past_tenders_on_active_list(self):
        driver = self.driver
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
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/tenders']"))
        )
        tenders_button.click()          
        
        self.assertIn("Active tenders", driver.title)
        
        header = driver.find_element(By.XPATH, "//h1[contains(text(), 'Active Tenders')]")
        self.assertTrue(header.is_displayed())
        
        no_tenders_para = driver.find_element(By.XPATH, "//p[contains(text(), 'No tenders found.')]")
        self.assertTrue(no_tenders_para.is_displayed())
    
    def test_active_tenders_on_past_list(self):
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
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/tenders/past']"))
        )
        tenders_button.click()          
        
        self.assertIn("Past Tenders", driver.title)
        
        header = driver.find_element(By.XPATH, "//h1[contains(text(), 'Past Tenders')]")
        self.assertTrue(header.is_displayed())
        
        no_tenders_para = driver.find_element(By.XPATH, "//p[contains(text(), 'No tenders found.')]")
        self.assertTrue(no_tenders_para.is_displayed())
        
    def test_add_tender_navigation(self):
        driver = self.driver
        active_tenders_button = driver.find_element(By.XPATH, "//a[@href='/tenders/new']")
        active_tenders_button.click()
        
        self.assertIn("New Tender", driver.title)
        
        header = driver.find_element(By.XPATH, "//h1[contains(text(), 'New Tender')]")
        self.assertTrue(header.is_displayed())
    
    def test_add_tender_form_elements(self):
        driver = self.driver    
        active_tenders_button = driver.find_element(By.XPATH, "//a[@href='/tenders/new']")
        active_tenders_button.click()
        
        new_tender_form = driver.find_element(By.XPATH, "//form[@action='/tenders/new']")
        self.assertTrue(new_tender_form.is_displayed())
        
        tender_orderer_input = driver.find_element(By.XPATH, "//input[@name='orderer']")
        self.assertTrue(tender_orderer_input.is_displayed())
        
        tender_price_input = driver.find_element(By.XPATH, "//input[@name='max_price']")
        self.assertTrue(tender_price_input.is_displayed())
        self.assertTrue(tender_price_input.get_attribute("type") == "number")
        
        tender_name_input = driver.find_element(By.XPATH, "//input[@name='name']")
        self.assertTrue(tender_name_input.is_displayed())
        
        tender_description_input = driver.find_element(By.XPATH, "//textarea[@name='description']")
        self.assertTrue(tender_description_input.is_displayed())
        
        tender_start_time_input = driver.find_element(By.XPATH, "//input[@name='start_time']")
        self.assertTrue(tender_start_time_input.is_displayed())
        
        tender_end_time_input = driver.find_element(By.XPATH, "//input[@name='end_time']")
        self.assertTrue(tender_end_time_input.is_displayed())

        tender_submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        self.assertTrue(tender_submit_button.is_displayed())
        
    def test_tender_form_validation_empty_fields(self):
        driver = self.driver
        driver.find_element(By.XPATH, "//a[@href='/tenders/new']").click()
        
        tender_submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        tender_submit_button.click()
        self.assertIn("New Tender", driver.title)
        
    def test_tender_form_validation_invalid_price(self):
        driver = self.driver
        create_custom_tender(
            driver,
            orderer="Unrealistic orderer",
            price="-1",
            name="Unrealistic order",
            description="negative price",
            start_time="01-05-2000\t13:11:00"
        )

        self.assertIn("New Tender", driver.title)    
    
    def test_multiple_active_tenders(self):
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
        
        
        
        tenders_table = driver.find_element(By.XPATH, "//table[@class='tenders-table']")
        self.assertTrue(tenders_table.is_displayed())
        
        tenders_rows = tenders_table.find_elements(By.TAG_NAME, "tr")
        self.assertEqual(len(tenders_rows), 3, "Wrong number of tender rows displayed.")
        
        tender_row = tenders_rows[1]
        tender_cells = tender_row.find_elements(By.TAG_NAME, "td")
        self.assertEqual(len(tender_cells), 6, "Tender row does not have the expected number of cells.")
        
    def test_multiple_past_tenders(self):
        driver = self.driver       
        create_custom_tender(
        driver,
            orderer="past Orderer",
            price="5000",
            name="past Tender",
            description="This is a past tender description.",
            start_time="01-05-2000\t13:11:00",
            end_time="01-05-2001\t13:11:00"
        )
        
        create_custom_tender(
            driver,
            orderer="past Orderer",
            price="5000",
            name="past Tender",
            description="This is a past tender description.",
            start_time="01-05-2000\t13:11:00",
            end_time="01-05-2001\t13:11:00"
        )
        
        
        WebDriverWait(driver, 10).until(EC.url_contains("/tenders"))
        tenders_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/tenders/past']"))
        )
        tenders_button.click()  
        
        
        tenders_table = driver.find_element(By.XPATH, "//table[@class='tenders-table']")
        self.assertTrue(tenders_table.is_displayed())
        
        tenders_rows = tenders_table.find_elements(By.TAG_NAME, "tr")
        self.assertEqual(len(tenders_rows), 3, "Wrong number of tender rows displayed.")
        
        tender_row = tenders_rows[1]
        tender_cells = tender_row.find_elements(By.TAG_NAME, "td")
        self.assertEqual(len(tender_cells), 5, "Tender row does not have the expected number of cells.")
        
    def test_active_past_tenders(self):
        driver = self.driver       
        create_custom_tender(
            driver,
            orderer="active Orderer",
            price="5000",
            name="active Tender",
            description="This is a active tender description.",
            start_time="01-05-2020\t13:11:00",
            end_time="01-05-2040\t13:11:00"
        )
        create_custom_tender(
            driver,
            orderer="past Orderer",
            price="5000",
            name="past Tender",
            description="This is a past tender description.",
            start_time="01-05-2000\t13:11:00",
            end_time="01-05-2001\t13:11:00"
        )
        
        WebDriverWait(driver, 10).until(EC.url_contains("/tenders"))
        tenders_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/tenders/past']"))
        )
        tenders_button.click()  
        
        
        tenders_table = driver.find_element(By.XPATH, "//table[@class='tenders-table']")
        self.assertTrue(tenders_table.is_displayed())
        
        tenders_rows = tenders_table.find_elements(By.TAG_NAME, "tr")
        self.assertEqual(len(tenders_rows), 2, "Wrong number of tender rows displayed.")
        
        tender_row = tenders_rows[1]
        tender_cells = tender_row.find_elements(By.TAG_NAME, "td")
        self.assertEqual(len(tender_cells), 5, "Tender row does not have the expected number of cells.")
                
        active_tenders_button = driver.find_element(By.XPATH, "//a[@href='/tenders']")
        active_tenders_button.click()
        
        
        tenders_table = driver.find_element(By.XPATH, "//table[@class='tenders-table']")
        self.assertTrue(tenders_table.is_displayed())
        
        tenders_rows = tenders_table.find_elements(By.TAG_NAME, "tr")
        self.assertEqual(len(tenders_rows), 2, "Wrong number of tender rows displayed.")
        
        tender_row = tenders_rows[1]
        tender_cells = tender_row.find_elements(By.TAG_NAME, "td")
        self.assertEqual(len(tender_cells), 6, "Tender row does not have the expected number of cells.")
        
    def test_tender_expiry_handling(self):
        driver = self.driver
        
        create_custom_tender(
            driver,
            orderer="soon expired Orderer",
            price="5000",
            name="soon expired Tender",
            description="This is a soon expired tender description.",
            start_time="01-05-2000\t13:11:00"
        )
        
        WebDriverWait(driver, 10).until(EC.url_contains("/tenders"))
        tenders_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/tenders']"))
        )
        tenders_button.click()  
        
        tenders_table = driver.find_element(By.XPATH, "//table[@class='tenders-table']")
        self.assertTrue(tenders_table.is_displayed())
        
        tenders_rows = tenders_table.find_elements(By.TAG_NAME, "tr")
        self.assertEqual(len(tenders_rows), 2, "Wrong number of tender rows displayed.")
        time.sleep(5)
        tenders_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/tenders/past']"))
        )
        tenders_button.click()  
        tenders_table = driver.find_element(By.XPATH, "//table[@class='tenders-table']")
        self.assertTrue(tenders_table.is_displayed())
        
        tenders_rows = tenders_table.find_elements(By.TAG_NAME, "tr")
        self.assertEqual(len(tenders_rows), 2, "Wrong number of tender rows displayed.")
            
    def test_details_link_active(self):
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
            
        tenders_table = driver.find_element(By.XPATH, "//table[@class='tenders-table']")
        self.assertTrue(tenders_table.is_displayed())
        details_link = driver.find_element(By.XPATH, "//a[contains(text(), 'View Details')]")
        self.assertTrue(details_link.is_displayed())
        details_link.click()
        self.assertIn("Tender Details", driver.title)
            
        add_offer_form = driver.find_element(By.XPATH, "//div[@class='add-offer-form']")
        self.assertTrue(add_offer_form.is_displayed())
            
    def test_details_link_past(self):
        driver = self.driver
            
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
        self.assertTrue(tenders_button.is_displayed())  
        tenders_button.click()
        
        tenders_table = driver.find_element(By.XPATH, "//table[@class='tenders-table']")
        self.assertTrue(tenders_table.is_displayed())
        details_link = driver.find_element(By.XPATH, "//a[contains(text(), 'View Details')]")
        self.assertTrue(details_link.is_displayed())
        details_link.click()
        self.assertIn("Tender Details", driver.title)
        
        add_offer_form = driver.find_element(By.XPATH, "//div[@class='offers-section']")
        self.assertTrue(add_offer_form.is_displayed())
            
    def test_future_tender_in_ended(self):
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
        
        WebDriverWait(driver, 10).until(EC.url_contains("/tenders"))
        tenders_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/tenders/past']"))
        )
        self.assertTrue(tenders_button.is_displayed())  
        tenders_button.click()
        
        no_tenders_para = driver.find_element(By.XPATH, "//p[contains(text(), 'No tenders found.')]")
        self.assertTrue(no_tenders_para.is_displayed())

    def test_future_tender_in_active(self):
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
        
        
        WebDriverWait(driver, 10).until(EC.url_contains("/tenders"))
        tenders_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/tenders']"))
        )
        self.assertTrue(tenders_button.is_displayed())
        tenders_button.click()  
        
        no_tenders_para = driver.find_element(By.XPATH, "//p[contains(text(), 'No tenders found.')]")
        self.assertTrue(no_tenders_para.is_displayed())