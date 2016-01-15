## 使用说明
1. 需要安装 Scrapy 爬虫框架和 Scrapy MongoDB 数据库连接组件。

    ```bash
    pip install -r reqirements.txt
    ```
2. 运行 MongoDB 数据库，监听本地IP：127.0.0.1 和 端口：27017 。
3. 在程序主目录下面运行

    ```bash
    scrapy crawl sjhm
    ```
4. 抓取数据将保存在数据库 scrapy 中的 bj_58_com_shoujihao_items 的 collection 中。
5. 可以使用 mongo.exe 检查抓取结果，比如我想知道最贵的手机号是哪个？

    ```
    db.bj_58_com_shoujihao_items.find().sort({'price':-1})
    ```

## 检查结果

```json
{ "_id" : ObjectId("56964e6b106a6c1978225ee0"), "price" : 500000, "carrier" : "中国电信", "link" : "http://bj.58.com/shoujihao/24663880646972x.shtml?psid=158957325190407121902605749&entinfo=24663880646972_0", "id" : NumberLong("13311111199") }
{ "_id" : ObjectId("56964f29106a6c1978226336"), "price" : 350000, "carrier" : "中国电信", "link" : "http://bj.58.com/shoujihao/24661085394997x.shtml?psid=122218894190407146582303068&entinfo=24661085394997_0", "id" : NumberLong("13311151981") }
{ "_id" : ObjectId("56964e5a106a6c1978225e58"), "price" : 330000, "carrier" : "中国电信", "link" : "http://bj.58.com/shoujihao/24664285828405x.shtml?psid=114280359190407119585196611&entinfo=24664285828405_0", "id" : NumberLong("13311133439") }
{ "_id" : ObjectId("56964e5b106a6c1978225e79"), "price" : 330000, "carrier" : "中国电信", "link" : "http://bj.58.com/shoujihao/24664178084403x.shtml?psid=151794224190407119832055522&entinfo=24664178084403_0", "id" : NumberLong("15330092555") }
{ "_id" : ObjectId("56964e5a106a6c1978225e56"), "price" : 250000, "carrier" : "中国移动", "link" : "http://bj.58.com/shoujihao/24664295364409x.shtml?psid=114280359190407119585196611&entinfo=24664295364409_0", "id" : NumberLong("13911500222") }
{ "_id" : ObjectId("56964ea1106a6c197822605d"), "price" : 250000, "carrier" : "中国电信", "link" : "http://bj.58.com/shoujihao/24662746148924x.shtml?psid=158976352190407128946494152&entinfo=24662746148924_0", "id" : NumberLong("15300015656") }
{ "_id" : ObjectId("56964f16106a6c19782262da"), "price" : 250000, "carrier" : "中国电信", "link" : "http://bj.58.com/shoujihao/24661293595324x.shtml?psid=142263464190407144061226322&entinfo=24661293595324_0", "id" : NumberLong("17718377707") }
{ "_id" : ObjectId("56964eda106a6c19782261ae"), "price" : 230000, "carrier" : "中国电信", "link" : "http://bj.58.com/shoujihao/24661966057145x.shtml?psid=154739099190407136171340955&entinfo=24661966057145_0", "id" : NumberLong("18088867777") }
{ "_id" : ObjectId("56964f2a106a6c197822633b"), "price" : 200000, "carrier" : "中国移动", "link" : "http://bj.58.com/shoujihao/24661051716537x.shtml?psid=109081748190407146834682016&entinfo=24661051716537_0", "id" : NumberLong("13911590267") }
{ "_id" : ObjectId("56964e79106a6c1978225f58"), "price" : 160000, "carrier" : "中国联通", "link" : "http://bj.58.com/shoujihao/24663497361463x.shtml?psid=115650916190407123755817034&entinfo=24663497361463_0", "id" : NumberLong("17088008811") }
{ "_id" : ObjectId("56964e5a106a6c1978225e53"), "price" : 140000, "carrier" : "中国电信", "link" : "http://bj.58.com/shoujihao/24664303449914x.shtml?psid=114280359190407119585196611&entinfo=24664303449914_0", "id" : NumberLong("13311133441") }
{ "_id" : ObjectId("56964f11106a6c19782262bb"), "price" : 140000, "carrier" : "中国移动", "link" : "http://bj.58.com/shoujihao/24661336396467x.shtml?psid=146550628190407143494958320&entinfo=24661336396467_0", "id" : NumberLong("13911592653") }
{ "_id" : ObjectId("56964eb8106a6c19782260ec"), "price" : 135000, "carrier" : "中国移动", "link" : "http://bj.58.com/shoujihao/24662402942649x.shtml?psid=163887429190407131716074040&entinfo=24662402942649_0", "id" : NumberLong("13911607061") }
{ "_id" : ObjectId("56964ec8106a6c197822614e"), "price" : 100000, "carrier" : "中国移动", "link" : "http://bj.58.com/shoujihao/24662183490747x.shtml?psid=184570087190407134090360907&entinfo=24662183490747_0", "id" : NumberLong("13901390388") }
{ "_id" : ObjectId("56964ec0106a6c1978226115"), "price" : 90000, "carrier" : "中国移动", "link" : "http://bj.58.com/shoujihao/24662320562743x.shtml?psid=107740392190407132832137833&entinfo=24662320562743_0", "id" : NumberLong("13901132108") }
{ "_id" : ObjectId("56964ec0106a6c1978226118"), "price" : 90000, "carrier" : "中国移动", "link" : "http://bj.58.com/shoujihao/24662311497523x.shtml?psid=107740392190407132832137833&entinfo=24662311497523_0", "id" : NumberLong("13911605510") }
{ "_id" : ObjectId("56964e60106a6c1978225ea3"), "price" : 80000, "carrier" : "中国移动", "link" : "http://bj.58.com/shoujihao/24365416994996x.shtml?psid=195085904190407120414815705&entinfo=24365416994996_0", "id" : NumberLong("13439367777") }
{ "_id" : ObjectId("56964ef7106a6c1978226239"), "price" : 80000, "carrier" : "中国联通", "link" : "http://bj.58.com/shoujihao/24395819098932x.shtml?psid=166323417190407139712986962&entinfo=24395819098932_0", "id" : NumberLong("18500737776") }
{ "_id" : ObjectId("56964f20106a6c1978226309"), "price" : 77077, "carrier" : "中国移动", "link" : "http://bj.58.com/shoujihao/24661174197556x.shtml?psid=131988784190407145559241033&entinfo=24661174197556_0", "id" : NumberLong("13911591571") }
{ "_id" : ObjectId("56964f14106a6c19782262c7"), "price" : 68000, "carrier" : "中国移动", "link" : "http://bj.58.com/shoujihao/24364942922551x.shtml?psid=142263464190407144061226322&entinfo=24364942922551_0", "id" : NumberLong("13581839999") }
```