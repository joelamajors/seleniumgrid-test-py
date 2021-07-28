import pytest
import json

# Importing JSON file to get URLs and caps
with open("./all-sites.json", "r") as read_file:
    data = json.load(read_file)
urls = data["urls"]

tags_report = open("tagsreport.json", "w")


@pytest.mark.usefixtures('driver')
class TestGoogleTags:

    def test_google_tags(self, driver):
        tags_report_dict = {}

        for url in urls:
            print(f'\n{url}')
            driver.get(url)

            src_array = []
            # ga_loaded = driver.execute_script('window.ga.loaded ? true : false')
            # src_array.append(f'ga lodaded? {ga_loaded}')

            tags_dict = {}
            tag_dict = {}
            tags = driver.find_elements_by_xpath(
                "//script[contains(@src, 'googletagmanager')]")

            for tag in tags:
                src = tag.get_attribute("src")
                src_array.append(src)
                tag_dict.update({url: src_array})
                tags_dict.update(tag_dict)

            tags_report_dict.update(tags_dict)

        tags_string = json.dumps(tags_report_dict)
        tags_report.write(tags_string)
        tags_report.close()
