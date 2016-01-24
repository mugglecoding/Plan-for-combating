from  page_parsing import url_list,get_item_info

for item in url_list.find():
    get_item_info(item['url'])