from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import pandas as pd
import json, re, time
import os


input_path = os.path.join("..", "..", "dataset", "data.jsonl")
output_path = os.path.join("..", "..", "results", "andi_result.jsonl")

questions = []
with open(input_path, 'r') as file:
    for line in file:
        questions.append(json.loads(line.strip()))
df = pd.DataFrame(questions, columns=['id','question','expected_answer'])

questions_list = df['question'].to_list()

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}  # disable images from being loaded to improve speeds
chrome_options = Options()
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)  
driver.get("https://andisearch.com")


responses = []
responses_links = []
with open(output_path, "a") as file:
    for index, question in enumerate(questions_list[:10]):
        item = {}
        driver.refresh()
        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'rcw-input'))
        )
        
        input_box.clear()
        input_box.send_keys(question)
        input_box.send_keys(Keys.RETURN)
        time.sleep(15)
        try:
            response_var = driver.find_elements(By.CSS_SELECTOR, 'div.lw-response')
            if response_var:
                p_tags = response_var[-1].find_elements(By.TAG_NAME, "p")
                if len(p_tags)>1:
                    andi_ans = p_tags[1].text
                    andi_ans = re.sub(u"(\u2018|\u2019)", "'", andi_ans) 
                else:
                    andi_ans = driver.find_elements(By.CLASS_NAME, 'lw-chat-blockquote')[0].text
                    andi_ans = re.sub(u"(\u2018|\u2019)", "'", andi_ans)

            link_div = WebDriverWait(driver, 25).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[class="meta"]')                    
                )
            )


            item["id"] = df["id"].iloc[index]
            item["question"] = df["question"].iloc[index]
            item["expected-answer"] = df["expected_answer"].iloc[index]
            item["andi-answer"] = andi_ans
            item["andi-links"] = link_div.text
            file.write(json.dumps(item)+'\n')

        except TimeoutException:
            print(f"Timeout while waiting for response to question: '{question}'")
            continue