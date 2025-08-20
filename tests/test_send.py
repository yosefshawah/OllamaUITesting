import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:3000')

class ComboBoxClickTest(unittest.TestCase):
    def setUp(self):
        options = Options()
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)

    def tearDown(self):
        self.driver.quit()

    def test_select_model_and_send_prompt(self):
        self.driver.get(OLLAMA_URL)

        # 🚿 Clear app state (optional if model is remembered via storage)
        self.driver.execute_script("localStorage.clear(); sessionStorage.clear(); indexedDB.databases().then(dbs => dbs.forEach(db => indexedDB.deleteDatabase(db.name)));")
        self.driver.refresh()
        sleep(2)

        # 🔘 Click the "Select model" button
        select_button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='Select model']"))
        )
        select_button.click()

        # ✅ Wait for popover with model options to appear and click the first model
        model_button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@role="dialog"]//button'))
        )
        model_button.click()

        # ⌨️ Enter text in the prompt input
        prompt_input = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Enter your prompt here"]'))
        )
        prompt_input.send_keys("hello world")
        self.assertIn("hello world", prompt_input.get_attribute("value"))

        # 📨 Wait for and click the submit button
        submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        WebDriverWait(self.driver, 10).until(lambda d: submit_button.is_enabled())

        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", submit_button)
        sleep(2)
        submit_button.click()

        # ⏳ Optional: Wait for a response to appear
        sleep(3)
        avatar_img = WebDriverWait(self.driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'img[alt="Avatar"]'))
        )

        # ✅ Traverse to the parent div and its next sibling
        avatar_container = avatar_img.find_element(By.XPATH, './ancestor::div[1]')
        response_div = avatar_container.find_element(By.XPATH, 'following-sibling::div[1]')

        # ✅ Collect all <p> tags inside the response div
        response_paragraphs = response_div.find_elements(By.TAG_NAME, 'p')
        response_texts = [p.text.strip() for p in response_paragraphs if p.text.strip()]

        # ✅ Print or assert the result
        print("Model response:")
        for line in response_texts:
            print("-", line)

        self.assertGreater(len(response_texts), 0, "No response paragraphs found from the model")


if __name__ == '__main__':
    unittest.main()
