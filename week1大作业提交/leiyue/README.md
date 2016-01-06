# 第一周大作业
## 要点
1. 爬取数据量大，直接用了 scrapy 。
2. 动态内容需要 scrapyjs ，需要运行 docker ，可惜我是 x86 的 windows 。
3. json 文件的编码处理耽误了时间，本来周日就可以提交。

## 运行
```shell
scrapy crawl pbdn -o items.json -t json
```

## 结果
可以使用 process_json.py 检查结果。