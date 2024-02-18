import scrapy
from scrapy.loader import ItemLoader
from scrapy.spiders import XMLFeedSpider
from scrapy.http import Request
import xmltodict
import os

class WebsiteAnalyzer:  # Replace with your desired class name
    def __init__(self, input_dir, output_file="urls.txt"):
        """
        Initializes the WebsiteAnalyzer with the input directory and output file paths.

        Args:
            input_dir (str): Path to the directory containing XML sitemap files.
            output_file (str, optional): Path to the output file where extracted URLs will be saved. Defaults to "urls.txt".
        """

        self.input_dir = input_dir
        self.output_file = output_file
        self.seen_urls = []  # Track processed URLs

    def parse_sitemap(self, xml_file):
        """
        Parses a single XML sitemap file and extracts relevant URLs, appending them to the output file.

        Args:
            xml_file (str): Path to the XML sitemap file.
        """

        if not os.path.isfile(xml_file):
            print(f"Warning: Skipping non-existent file: {xml_file}")
            return

        with open(xml_file, "r") as xml_file:
            obj = xmltodict.parse(xml_file.read())
        urls = obj['urlset']['url']

        append_mode = "w" if not os.path.exists(self.output_file) else "a"

        with open(self.output_file, append_mode) as text_file:
            for url in urls:
                href = None  # Initialize href in case 'xhtml:link' is missing

                if 'xhtml:link' in url:
                    for link in url['xhtml:link']:
                        if link.get('@hreflang') == "x-default":
                            href = link.get('@href')
                            break  # Stop after finding the first "x-default" hreflang

                if href and href not in self.seen_urls:
                    text_file.write(href + "\n")
                    self.seen_urls.append(href)  # Add extracted URL to the set

    def parse_multiple_sitemaps(self):
        """
        Iterates through all XML files in the input directory, calling `parse_sitemap` for each.
        """

        for filename in os.listdir(self.input_dir):
            if filename.endswith(".xml"):
                xml_file = os.path.join(self.input_dir, filename)
                self.parse_sitemap(xml_file)

if __name__ == "__main__":
    input_dir = "sitemaps/"  # Replace with your actual directory path
    analyzer = WebsiteAnalyzer(input_dir)
    analyzer.parse_multiple_sitemaps()
