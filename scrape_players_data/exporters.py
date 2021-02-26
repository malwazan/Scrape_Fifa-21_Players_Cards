from scrapy.exporters import CsvItemExporter


class HeadlessCsvItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):

        # args[0] is (opened) file handler
        # if file is not empty then skip headers
        if args[0].tell() > 0:
            kwargs['include_headers_line'] = False

        super(HeadlessCsvItemExporter, self).__init__(*args, **kwargs)


# for csv with only 1 header line write
#   scrapy crawl <project_name> -o <output_file> -t headless

# write this in settings.py
# FEED_EXPORTERS = {
#     'headless': 'scrape_flipkart.exporters.HeadlessCsvItemExporter',
# }