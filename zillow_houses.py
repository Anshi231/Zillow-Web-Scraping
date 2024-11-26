from collections.abc import Iterable
import scrapy
from zillow.proxies import get_smart_proxy_agent
import json

class ZillowHousesSpider(scrapy.Spider):
    name = "zillow_houses"
    allowed_domains = ["www.zillow.com"]
    start_urls = []

    def start_requests(self):
        # Define the payload (searchQueryState and wants)
        search_query_state = {
            "pagination": {},
            "isMapVisible": True,
            "pagination": {"currentPage": 1},
            "mapBounds": {
                "north": 41.0159577359822,
                "south": 40.63666521478589,
                "east": -80.5795277558594,
                "west": -82.18627824414065,
            },
            "regionSelection": [{"regionId": 51260, "regionType": 6}],
            "filterState": {
                "sortSelection": {"value": "globalrelevanceex"},
                "isAllHomes": {"value": True},
            },
            "isEntirePlaceForRent": True,
            "isRoomForRent": False,
            "isListVisible": True,
        }
        wants = {
            "cat1": ["listResults", "mapResults"],
            "cat2": ["total"],
        }

        payload = {
            "searchQueryState": search_query_state,
            "wants": wants,
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41",
            "accept": "*/*",
            "content-type": "application/json",
        }

        # Get proxy configuration
        proxies = get_smart_proxy_agent()

        # Send a PUT request with the payload, headers, and proxy
        yield scrapy.Request(
            url="https://www.zillow.com/async-create-search-page-state",
            method="PUT",
            body=json.dumps(payload),  # Convert payload to JSON string
            headers=headers,
            meta={"proxy": proxies["https"]},  # Use HTTPS proxy
            callback=self.parse,
        )

    def parse(self, response):
       # Path to save the raw JSON response
        raw_json_path = "initial_response.json"

        # Save the raw response body to a file
        with open(raw_json_path, "wb") as f:
            f.write(response.body)

        # Format the saved JSON file
        self.format_json_file(raw_json_path, "formatted_response.json")

        # Print the response for debugging
        self.log(f"Response status: {response.status}")
        self.log(f"Response saved and formatted.")

    @staticmethod
    def format_json_file(input_path, output_path):
        """
        Format a raw JSON file and save it with proper indentation.
        :param input_path: Path to the raw JSON file.
        :param output_path: Path to save the formatted JSON file.
        """
        try:
            with open(input_path, "r") as file:
                data = json.load(file)

            with open(output_path, "w") as formatted_file:
                json.dump(data, formatted_file, indent=4)  # Add indentation

            print(f"Formatted JSON saved to: {output_path}")
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
        except Exception as e:
            print(f"Error while formatting JSON: {e}")


