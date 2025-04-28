import json
from pathlib import Path

from rich import print
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TAGS_MAP = {
    "weaktostrong": "weak to strong",
    "sliceoflife": "slice of life",
    "kingdombuilding": "kingdom building",
    "no-harem": "no harem",
    "nonhuman": "non-human",
    "sweetlove": "sweet love",
    "levelup": "level up",
    "sweetlove": "sweet love" 
}


def scrape_tags():
    driver = webdriver.Firefox()

    tag_data_list = []

    try:
        driver.get("https://www.webnovel.com/tag-list")
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.j_table_container"))
        )

        tags_table = driver.find_element(By.CSS_SELECTOR, "div.j_table_container")

        page = 1

        while page <= 3:
            tags_cell = driver.find_elements(By.CSS_SELECTOR, "tr.td200")
            for tag_cell in tags_cell:
                tag = tag_cell.find_element(By.CSS_SELECTOR, "span.db.ell a")

                tag_name = tag.text.lower()

                if tag_name in TAGS_MAP: tag_name = TAGS_MAP[tag_name]

                tag_data_list.append({"name": tag_name, "description": None})

            next_btn = driver.find_element(By.CSS_SELECTOR, "a.j_next_page_tag.ml8")

            if next_btn.is_displayed():
                next_btn.location_once_scrolled_into_view
                next_btn.click()

            page += 1
            tags_table.location_once_scrolled_into_view

        try:
            save_dir = Path("./genres_and_tags")
            save_dir.mkdir(parents=True, exist_ok=True)
            print(save_dir)
            with open(
                f"{save_dir}/webnoveldotcom_tags.json", "w", encoding="utf-8"
            ) as json_file:
                json.dump(tag_data_list, json_file, ensure_ascii=False, indent=4)
        except IOError as e:
            print(e)

        print(
            "Scraping completed. Results saved in ./genres_and_tags/webnoveldotcom_tags.json"
        )

    except Exception as e:
        print(e)

    finally:
        driver.quit()


if __name__ == "__main__":
    scrape_tags()
