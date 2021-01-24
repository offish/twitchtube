from .constants import *
from .logging import Log

from time import sleep
from pathlib import Path

from selenium import webdriver


log = Log()


class Upload:
    def __init__(self, root_profile_directory: str, meta: dict, timeout: int = TIMEOUT):
        self.video = meta.get("file")
        self.title = meta.get("title")
        self.description = meta.get("description")
        self.timeout = timeout

        profile = webdriver.FirefoxProfile(root_profile_directory)
        options = webdriver.FirefoxOptions()
        options.headless = True
        self.driver = webdriver.Firefox(firefox_profile=profile, options=options)

        log.info("Firefox is now running")

    def upload(self) -> (bool, str):

        self.driver.get(YOUTUBE_UPLOAD_URL)
        sleep(self.timeout)

        log.info("Trying to upload video to YouTube...")
        path = str(Path.cwd() / self.video)
        self.driver.find_element_by_xpath(INPUT_FILE_VIDEO).send_keys(path)

        sleep(self.timeout)

        log.info(f"Trying to set {self.title} as title...")
        title_field = self.driver.find_element_by_id(TEXTBOX)
        title_field.click()
        sleep(self.timeout)

        title_field.clear()
        sleep(self.timeout)

        title_field.send_keys(self.title)
        sleep(self.timeout)

        description = self.description
        if description:
            log.info(f"Trying to set {self.description} as description...")
            container = self.driver.find_element_by_xpath(DESCRIPTION_CONTAINER)
            description_field = container.find_element_by_id(TEXTBOX)
            description_field.click()
            sleep(self.timeout)

            description_field.clear()
            sleep(self.timeout)

            description_field.send_keys(self.description)

        log.info("Trying to set video to 'Not made for kids'...")
        kids_section = self.driver.find_element_by_name(NOT_MADE_FOR_KIDS_LABEL)
        kids_section.find_element_by_id(RADIO_LABEL).click()
        sleep(self.timeout)

        self.driver.find_element_by_id(NEXT_BUTTON).click()
        sleep(self.timeout)

        self.driver.find_element_by_id(NEXT_BUTTON).click()
        sleep(self.timeout)

        log.info("Trying to set video visibility to public...")
        public_main_button = self.driver.find_element_by_name(PUBLIC_BUTTON)
        public_main_button.find_element_by_id(RADIO_LABEL).click()
        video_id = self.get_video_id()

        status_container = self.driver.find_element_by_xpath(STATUS_CONTAINER)
        while True:
            in_process = status_container.text.find(UPLOADED) != -1
            if in_process:
                sleep(self.timeout)
            else:
                break

        done_button = self.driver.find_element_by_id(DONE_BUTTON)

        if done_button.get_attribute("aria-disabled") == "true":
            error_message = self.driver.find_element_by_xpath(ERROR_CONTAINER).text
            return False, None

        done_button.click()

        sleep(self.timeout)
        self.driver.get(YOUTUBE_URL)
        self.close()
        return True, video_id

    def get_video_id(self) -> str:
        video_id = None
        try:
            video_url_container = self.driver.find_element_by_xpath(VIDEO_URL_CONTAINER)
            video_url_element = video_url_container.find_element_by_xpath(
                VIDEO_URL_ELEMENT
            )

            video_id = video_url_element.get_attribute(HREF).split("/")[-1]
        except:
            pass
        return video_id

    def close(self):
        self.driver.quit()
        log.info("Closed Firefox")
