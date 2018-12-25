import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        # image_paths = [x['path'] for ok, x in results if ok]
        # if not image_paths:
        #     raise DropItem("Item contains no images")
        # item['image_paths'] = image_paths
        return item

    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        return 'full/%s' % (image_guid)
