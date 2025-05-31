from base_test import BaseTestCase, create_custom_tender
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class OfferTests(BaseTestCase):
    def test_offer_form_elements(self):
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
        
        details_link = driver.find_element(By.XPATH, "//a[contains(text(), 'View Details')]")
        details_link.click()
        
        add_offer_form = driver.find_element(By.XPATH, "//div[@class='add-offer-form']")
        self.assertTrue(add_offer_form.is_displayed())
        
        offerer_name_input = driver.find_element(By.XPATH, "//input[@name='offerer_name']")
        self.assertTrue(offerer_name_input.is_displayed())
        
        offer_price_input = driver.find_element(By.XPATH, "//input[@name='price']")
        self.assertTrue(offer_price_input.is_displayed())
        
        offer_submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        self.assertTrue(offer_submit_button.is_displayed())

    def test_offer_form_empty_price(self):
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
        self.assertIn("Tender Details", driver.title)
        
        offerer_name_input = driver.find_element(By.XPATH, "//input[@name='offerer_name']")
        offerer_name_input.send_keys("Test Offerer")
        
        offer_submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        self.assertTrue(offer_submit_button.is_displayed())
        offer_submit_button.click()
        time.sleep(1)
        
        offerer_name_input = driver.find_element(By.XPATH, "//input[@name='offerer_name']")
        self.assertEqual(offerer_name_input.get_attribute("value"), "Test Offerer", "Offerer name input should still have the value 'Test Offerer'.")

    def test_offer_form_non_numeric_price(self):
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
        
        offerer_name_input = driver.find_element(By.XPATH, "//input[@name='offerer_name']")
        offerer_name_input.send_keys("Test Offerer")
        offer_price_input = driver.find_element(By.XPATH, "//input[@name='price']")
        offer_price_input.send_keys("ten")
        
        offer_submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        self.assertTrue(offer_submit_button.is_displayed())
        offer_submit_button.click()
        time.sleep(1)
        
        offerer_name_input = driver.find_element(By.XPATH, "//input[@name='offerer_name']")
        self.assertEqual(offerer_name_input.get_attribute("value"), "Test Offerer", "Offerer name input should still have the value 'Test Offerer'.")

    def test_offer_form_add(self):
        driver = self.driver
        
        create_custom_tender(
            driver,
            orderer="Active Orderehnjgnjghjjjhfcfhjr",
            price="5000",
            name="Active Tender",
            description="This is a active tender description.",
            start_time="01-05-2000\t13:11:00"
        )
        
        WebDriverWait(driver, 10).until(EC.url_contains("/tenders"))
        tenders_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/tenders']"))
        )
        tenders_button.click()  
        
        details_link = driver.find_element(By.XPATH, "//a[contains(text(), 'View Details')]")
        details_link.click()
        
        add_offer_form = driver.find_element(By.XPATH, "//div[@class='add-offer-form']")
        self.assertTrue(add_offer_form.is_displayed())
        
        offerer_name_input = driver.find_element(By.XPATH, "//input[@name='offerer_name']")
        offerer_name_input.send_keys("Test Offerer")
        
        offer_price_input = driver.find_element(By.XPATH, "//input[@name='price']")
        offer_price_input.send_keys("4500")
        
        offer_submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        self.assertTrue(offer_submit_button.is_displayed())
        offer_submit_button.click()
        time.sleep(7)
        driver.refresh()
        offers_list = driver.find_element(By.XPATH, "//ul[@class='offers-list']")
        self.assertTrue(offers_list.is_displayed())
        offers_items = offers_list.find_elements(By.TAG_NAME, "li")
        self.assertGreater(len(offers_items), 0, "No offers found in the list.")
        first_offer = offers_items[0]
        self.assertIn("Test Offerer", first_offer.text, "Offerer name does not match.") 
        self.assertIn("4500", first_offer.text, "Offer price does not match.")

    def test_offer_not_in_budget(self):
        driver = self.driver
        
        create_custom_tender(
            driver,
            orderer="Active Orderer",
            price="5000",
            name="Active Tender",
            description="This is a active tender description.",
            start_time="01-05-2000\t13:11:00"
        )
        
        WebDriverWait(driver, 10).until(EC.url_contains("/tenders"))
        tenders_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/tenders']"))
        )
        tenders_button.click()
        
        details_link = driver.find_element(By.XPATH, "//a[contains(text(), 'View Details')]")
        details_link.click()
        
        add_offer_form = driver.find_element(By.XPATH, "//div[@class='add-offer-form']")
        self.assertTrue(add_offer_form.is_displayed())
        
        offerer_name_input = driver.find_element(By.XPATH, "//input[@name='offerer_name']")
        offerer_name_input.send_keys("Test Offerer")
        
        offer_price_input = driver.find_element(By.XPATH, "//input[@name='price']")
        offer_price_input.send_keys("5500")
        
        offer_submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        self.assertTrue(offer_submit_button.is_displayed())
        offer_submit_button.click()
        time.sleep(7)
        driver.refresh()
        no_offers_para = driver.find_element(By.XPATH, "//p[@class='no-offers']")
        self.assertTrue(no_offers_para.is_displayed())
        self.assertIn("No offers below maximum price have been submitted", no_offers_para.text, "No offers message does not match.")

    def test_multiple_offers_sorted_correctly_by_price(self):
            driver = self.driver
            create_custom_tender(
                driver,
                orderer="Sort Offer Orderer",
                price="10000",
                name="Sort Offer Tender",
                description="Tender for testing offer sorting.",
                start_time="01-05-2000\t13:11:00"
            )
            
            offer_prices_to_submit = [500, 200, 800]
            for i, price_val in enumerate(offer_prices_to_submit):
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "offerer_name")))
                driver.find_element(By.ID, "offerer_name").send_keys(f"Offerer {i+1}")
                driver.find_element(By.ID, "price").send_keys(str(price_val))
                driver.find_element(By.XPATH, "//button[@type='submit']").click()
                if i < len(offer_prices_to_submit) - 1:
                    WebDriverWait(driver, 10).until(lambda d: d.find_element(By.ID, "offerer_name").get_attribute('value') == "")


            time.sleep(7)
            driver.refresh()

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//ul[@class='offers-list']")))
            offer_elements = driver.find_elements(By.XPATH, "//ul[@class='offers-list']/li")
            self.assertEqual(len(offer_elements), 3, "Incorrect number of offers displayed.")

            displayed_prices = []
            for offer_el in offer_elements:
                price_text = offer_el.text.split("Price:")[1].split("\n")[0].strip()
                displayed_prices.append(int(price_text))
            
            self.assertEqual(displayed_prices, sorted(offer_prices_to_submit, key=int), "Offers are not sorted correctly by price.")
            

    def test_offer_edgecase(self):
        driver = self.driver
        create_custom_tender(
            driver,
            orderer="Edge Case Orderer",
            price="100",
            name="Edge Case Tender",
            description="Tender for testing offer edge cases.",
            start_time="01-05-2000\t13:11:00"
        )
        
        driver.find_element(By.ID, "offerer_name").send_keys("Max Price Offerer")
        driver.find_element(By.ID, "price").send_keys("100")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        time.sleep(7)
        driver.refresh()
        
        header = driver.find_element(By.XPATH, "//h2[contains(text(), 'Submitted Offers')]")
        self.assertTrue(header.is_displayed())
        offers_list = driver.find_element(By.XPATH, "//ul[@class='offers-list']")
        self.assertTrue(offers_list.is_displayed())
        offers_items = offers_list.find_elements(By.TAG_NAME, "li")
        self.assertGreater(len(offers_items), 0, "No offers found in the list.")
        first_offer = offers_items[0]
        self.assertIn("100", first_offer.text, "Offer price does not match.")
        
    def test_multiple_offer_mix(self):
        driver = self.driver
        create_custom_tender(
            driver,
            orderer="Mixed offers",
            price="100",
            name="Mixed offers Tender",
            description="Tender for testing mixed offers.",
            start_time="01-05-2000\t13:11:00"
        )
        
        offer_prices_to_submit = [10, 101]
        for i, price_val in enumerate(offer_prices_to_submit):
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "offerer_name")))
            driver.find_element(By.ID, "offerer_name").send_keys(f"Offerer {i+1}")
            driver.find_element(By.ID, "price").send_keys(str(price_val))
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            if i < len(offer_prices_to_submit) - 1:
                WebDriverWait(driver, 10).until(lambda d: d.find_element(By.ID, "offerer_name").get_attribute('value') == "")


        time.sleep(7)
        driver.refresh()
        
        header = driver.find_element(By.XPATH, "//h2[contains(text(), 'Submitted Offers')]")
        self.assertTrue(header.is_displayed())
        offers_list = driver.find_element(By.XPATH, "//ul[@class='offers-list']")
        self.assertTrue(offers_list.is_displayed())
        offers_items = offers_list.find_elements(By.TAG_NAME, "li")
        self.assertEqual(len(offers_items), 1, "Wrong number of offers displayed.")
        first_offer = offers_items[0]
        self.assertIn("10", first_offer.text, "Offer price does not match.")
        