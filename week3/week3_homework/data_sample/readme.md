# 导入数据须知

1. 首先运行 mongo shell在数据库中创建一个 collection —— db.createCollection('the_name')
2. 接下来直接在终端/命令行中使用命令导入 json 格式的数据 —— mongoimport -d database_name -c collection_name path/file_name.json
