## 随便打个题目吧

> ok！第二周的大作业估计我也完成了。
> 只是爬虫爬取数据需要太长的时间，懒得等了。

1. 起始位置：http://bj.ganji.com/wu/
2. 起始页面下面有 **二十** 个类目：

    ```python
    categories = [
            'jiaju', 'rirongbaihuo', 'shouji', 'shoujihaoma', 'bangong', 'nongyongpin',
            'jiadian', 'ershoubijibendiannao', 'ruanjiantushu', 'yingyouyunfu', 'diannao',
            'xianzhilipin', 'fushixiaobaxuemao', 'meironghuazhuang', 'shuma', 'laonianyongpin',
            'xuniwupin', 'qitawupin', 'ershoufree', 'wupinjiaohuan',
        ]
    ```
3. 每个类目下面 **若干** 列表页面。
4. 每个列表页面大概 **几十** 个详情页。
5. 每个详情页 **爬取** 数据。

现成的 scrapy 爬虫框架最适合，也是我比较熟悉的内容。

所以直接拿 scrapy 完成作业了，不能运行不要怪我哟。