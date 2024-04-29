# get_holiday_cn
获取中国法定节假日

### 支持的python版本
python3.x

### 功能点
1. 传入日期获取中国法定节假日

### 说明
依赖[NateScarlet/holiday-cn](https://github.com/NateScarlet/holiday-cn)

### 安装
```shell script
pip install get_holiday_cn
```

### 数据说明
```
{
      "code": 0,              // 0服务正常。-1服务出错
      "type": {
        "type": enum(0, 1, 2, 3), // 节假日类型，分别表示 工作日、周末、节日、调休。
        "name": "周六",         // 节假日类型中文名，可能值为 周一 至 周日、假期的名字、某某调休。
        "week": enum(1 - 7)    // 一周中的第几天。值为 1 - 7，分别表示 周一 至 周日。
        "status": enum(0, 1)    // 数据场景类型，0来源于仓库中的节假日或调休日；1表示当前传入日期在仓库中未查询到，直接走系统计算，可能为工作日或还未公布的节假日。
      },
      "holiday": {            // 只有当type为2，3时，该对象才存在
        "holiday": false,     // true表示是节假日，false表示是调休
        "name": "国庆节调休",  // 节假日的中文名。如果是调休，则是调休的中文名，例如'国庆节调休'
        "date": '2021-10-09'     // 当前请求的日期
      }
}
```

### 使用
```python
from get_holiday_cn.client import getHoliday

client = getHoliday()
# 获取今日数据
print(client.assemble_holiday_data())
# 指定日期获取数据
print(client.assemble_holiday_data(today='2021-10-01'))
```

### 2022/12/27 更新说明
刚刚推送了v1.0.5版本，在此版本前可能会获取到空数组的2023年json文件，导致现在23年假期更新后还是无法查到；如出现下图所示，可以删除本地已缓存的`2023.json`文件，下次再请求时会自动获取最新的数据
![企业微信截图_20221227160706](https://user-images.githubusercontent.com/22344864/209655031-1a3b4185-6b8c-436c-aaee-8371c6e2e1aa.png)

