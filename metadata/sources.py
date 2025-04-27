import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List

import nh3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from metadata.funcs import dump_json, load_json

REQUIRED_META_TAG_PROPERTIES = [
    "og:title",
    "og:author",
    "og:tag",
]

CATEGORIES = [
    "action",
    "adult",
    "adventure",
    "comedy",
    "drama",
    "ecchi",
    "fantasy",
    "gender bender",
    "harem",
    "historical",
    "horror",
    "josei",
    "martial arts",
    "mature",
    "mecha",
    "mystery",
    "psychological",
    "romance",
    "school life",
    "sci-fi",
    "seinen",
    "shoujo",
    "shoujo ai",
    "shounen",
    "shounen ai",
    "slice of life",
    "smut",
    "sports",
    "supernatural",
    "tragedy",
    "wuxia",
    "xianxia",
    "xuanhuan",
    "yaoi",
    "yuri"
]

class MetadataSource(ABC):
    def __init__(self, root_path: Path, novel_name: str):
        self.output_path = Path("./current_metadata.json")
        self.root_path = root_path
        self.novel_name = novel_name

    @property
    @abstractmethod
    def base_url(self):
        pass

    @property
    def url(self):
        return self.base_url+self.novel_name

    @abstractmethod
    def get_metadata(self):
        pass

    @abstractmethod
    def format_metadata(self, metadata_dict: Dict) -> None:
        pass

    def clean_html(self, html: str) -> str:
        """format and clean given html

        Args:
            html (str): html to be cleaned / formatted

        Returns:
            str: formatted html
        """
        soup = BeautifulSoup(html, "html.parser")

        nh3_tags = nh3.ALLOWED_TAGS
        html = nh3.clean(html, tags=nh3_tags)

        for tag in soup.find_all():
            if "class" in tag.attrs:
                del tag["class"]

        final_html = str(soup)

        final_html = final_html.replace('"', '&quot;').replace("'", '&#39;')

        return final_html

    def merge_current_metadata_to_novel_metadata(self):
        json_to_merge_path = Path(f"{self.root_path}/meta.json")
        try:
            chapters = load_json(json_to_merge_path).get("novel").get("chapters")
            current_metadata_dict = load_json(self.output_path)

            current_metadata_dict["chapters"] = chapters

            new_dict = {"novel": current_metadata_dict}

            dump_json(Path(json_to_merge_path), new_dict)

            logging.info(f"{json_to_merge_path} got successfully merged!")
        except Exception as e:
            logging.error(f"Failed to merge {json_to_merge_path}: {e}")

    def execute(self):
        self.get_metadata()
        self.merge_current_metadata_to_novel_metadata()

    def __str__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

class WebnovelDotComSource(MetadataSource):
    def __init__(self, root_path: Path, novel_name: str):
        super().__init__(root_path, novel_name)

    @property
    def base_url(self):
        return "https://www.webnovel.com/book/"
        
    def format_metadata(self, metadata_dict):
        """formats given dict to stalkers-api standards

        Args:
            metadata_dict (Dict): dict containing metadata retrieved through selenium
        """
        tags: List[str] = metadata_dict.get("tag").split(", ")
        tags = [tag.lower().strip() for tag in tags]

        metadata_dict["categories"] = [genre for genre in CATEGORIES if genre.lower().strip() in tags]
        
        metadata_dict["tags"] = tags
        del metadata_dict["tag"]

        metadata_dict["title"] = metadata_dict["title"].lower()

    def get_metadata(self):
        driver = webdriver.Chrome()
        meta_data = {}
        try:
            driver.get(self.url)

            wait = WebDriverWait(driver, 10)
            # ultima meta tag
            wait.until(
                EC.presence_of_element_located((By.XPATH, "html/head/meta[@property='og:site_name']"))
            )

            meta_tags = driver.find_elements(By.XPATH, "html/head/meta")

            for meta in meta_tags:
                meta_property = meta.get_attribute("property")

                if (meta_property is not None and meta_property in REQUIRED_META_TAG_PROPERTIES):
                    meta_name = meta_property.replace("og:", "")
                    meta_content = meta.get_attribute("content")

                    meta_data.update({meta_name: meta_content})

            novel_description_html = driver.find_element(
                By.CSS_SELECTOR, ".g_wrap .j_synopsis p"
            ).get_attribute("outerHTML")

            novel_description_html = self.clean_html(novel_description_html)

            meta_data.update({"description": novel_description_html})

            self.format_metadata(meta_data)

            dump_json(self.output_path, meta_data)

            print("Meta data processed successfully!")

        except Exception as e:
            logging.error(f"Failed to process metadata: {e}")
        finally:
            driver.quit()

class NovelUpdatesSource(MetadataSource):
    def __init__(self, root_path: Path, novel_name: str):
        super().__init__(root_path, novel_name)

    @property
    def base_url(self):
        return "https://www.novelupdates.com/series/"
    
    def get_metadata(self):
        pass
    