# 导入数据须知

1. 管理员权限打开命令行
  
  a. windows: 开始菜单找到cmd，右键，管理员权限打开
  b. linux: 直接打开
  c. mac: 直接打开

2. 切换到mongodb安装目录的bin目录（Windows）

```shell
  cd /d "C:\Program Files\MongoDB\Server\3.2\bin"
```

3. 运行导入命令

```shell
  mongoimport -d ceshi -c item_info "data_sample.json的文件路径"
```
