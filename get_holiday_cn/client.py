#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/9 13:48
# @Author  : Weiqiang.long
# @Email   : 573925242@qq.com
# @Site    : 
# @File    : client.py
# @Software: PyCharm
# @Description: 获取github仓库的节假日json数据并存到本地文件中

"""
https://github.com/NateScarlet/holiday-cn
国内地址：
https://natescarlet.coding.net/p/github/d/holiday-cn/git/raw/master/{年份}.json
https://cdn.jsdelivr.net/gh/NateScarlet/holiday-cn@master/{年份}.json
数据格式：
interface Holidays {
  /** 完整年份, 整数。*/
  year: number;
  /** 所用国务院文件网址列表 */
  papers: string[];
  days: {
    /** 节日名称 */
    name: string;
    /** 日期, ISO 8601 格式 */
    date: string;
    /** 是否为休息日 */
    isOffDay: boolean;
  }[]
}
"""
import datetime, requests,json

class YearKeyError(Exception):
    '''自定义异常：年份异常'''
    def __init__(self, message):
        self.msg = '年份异常，年份入参为：{0}，请检查入参'.format(message)
    def __str__(self):
        return self.msg

class HolidayError(Exception):
    '''自定义异常：未知异常'''
    def __init__(self):
        self.msg = '主站及备用站点均无法访问，请稍后再试！'

    def __str__(self):
        return self.msg


class getHoliday(object):

    def __init__(self):
        pass

    @staticmethod
    def get_current_year():
        '''获取当前的年份'''
        return datetime.datetime.now().year

    @staticmethod
    def get_current_isoweekday(today=None):
        '''获取当前的星期数（返回数字1-7代表周一到周日）'''
        if not today:
            return datetime.datetime.now().isoweekday()
        else:
            return datetime.datetime.strptime(today, "%Y-%m-%d").isoweekday()

    def get_holiday_json(self, current_year=None):
        '''
        查询仓库中对应年份的json数据
        :param current_year: 要查询的年份
        :return:
        '''
        try:
            with open(f"{current_year}.json",'r',encoding='utf-8') as f:
                return json.load(f)['days']
        except:
            try:
                url = 'https://cdn.jsdelivr.net/gh/NateScarlet/holiday-cn@master/{year}.json'.format(year=current_year)
                res = requests.get(url=url, timeout=5)
                if res.status_code == 200:
                    with open(f"{current_year}.json", 'w', encoding='utf-8') as f:
                        json.dump(res.json(), f, ensure_ascii=False, indent=4)
                    return res.json()['days']
                else:
                    print('主网址请求失败，正在发起重试！！！')
                    url = 'https://natescarlet.coding.net/p/github/d/holiday-cn/git/raw/master/{year}.json'.format(
                        year=current_year)
                    res = requests.get(url=url, timeout=5)
                    if res.status_code == 404:
                        raise YearKeyError(current_year)
                    else:
                        with open(f"{current_year}.json", 'w', encoding='utf-8') as f:
                            json.dump(res.json(), f, ensure_ascii=False, indent=4)
                    return res.json()['days']
            except:
                try:
                    print('主网址发生未知错误，正在请求备用站点！！！')
                    # 主站挂了直接except,并存储到本地
                    url = 'https://natescarlet.coding.net/p/github/d/holiday-cn/git/raw/master/{year}.json'.format(
                        year=current_year)
                    res = requests.get(url=url)
                    if res.status_code == 404:
                        raise YearKeyError(current_year)
                    else:
                        with open(f"{current_year}.json", 'w', encoding='utf-8') as f:
                            json.dump(res.json(), f, ensure_ascii=False, indent=4)
                    return res.json()['days']
                except:
                    raise HolidayError()


    def get_before_and_after_holiday_json(self, current_year=None):
        '''
        查询仓库中前后两年+当年的json数据
        :param current_year: 要查询的年份
        :return:
        '''
        # 年份是按照国务院文件标题年份而不是日期年份，12月份的日期可能会被下一年的文件影响，因此应检查两个文件
        # 所以这里稳定起见，查询当前年份前后一年
        if not current_year:
            current_year = self.get_current_year()
        e_status = 0
        # 防止大于当前年份+2，造成查询仓库json返回404（仓库中最多只会存在当前年份+1的数据）
        if int(current_year) >= int(self.get_current_year()) + 1:
            current_year = self.get_current_year()
            # 如果触发入参年份大于当前年份+2的场景，给个状态标识
            e_status = -1
        year_list = [int(current_year)-1, int(current_year), int(current_year)+1]
        # print(year_list)
        data_list = []
        for i in year_list:
            res = self.get_holiday_json(current_year=i)
            for n in res:
                data_list.append(n)
        return data_list, e_status

    @staticmethod
    def get_weekday_enum_cn(week_day: int) -> str:
        '''获取中文的星期数枚举'''
        #TODO 可能会越界
        return ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][int(week_day)-1]

    def get_today_data(self, today=None, current_year=None):
        '''获取今天的日期数据'''
        if not today:
            today = datetime.datetime.now().strftime('%Y-%m-%d')
        all_holiday_json = self.get_before_and_after_holiday_json(current_year=current_year)
        all_holiday_status = all_holiday_json[1]
        # 判断当前是周几，如果大于周五的话，就代表是休息日
        isoweekday = self.get_current_isoweekday(today=today)
        if isoweekday > 5:
            is_off_day = True
        else:
            is_off_day = False
        today_data = {'name': '', 'date': today, 'isOffDay': is_off_day}
        for i in all_holiday_json[0]:
            # 兼容入参的today格式多样化（如：2020-10-1或者2020-1-1）
            if str(datetime.datetime.strptime(today, "%Y-%m-%d").date()) == i['date']:
                today_data = i
        today_data['week'] = isoweekday
        # 该场景为工作日
        if today_data['name'] == "" and today_data['isOffDay'] == False:
            t_type = 0
        # 该场景为周末
        elif today_data['name'] == "" and today_data['isOffDay'] == True:
            t_type = 1
        # 该场景为节假日
        elif today_data['name'] != "" and today_data['isOffDay'] == True:
            t_type = 2
        elif today_data['name'] != "" and today_data['isOffDay'] == False:
            t_type = 3
        today_data['t_type'] = t_type
        return today_data, all_holiday_status

    def assemble_holiday_data(self, today=None):
        """
        {
          "code": 0,              // 0服务正常。-1服务出错
          "type": {
            "type": enum(0, 1, 2, 3), // 节假日类型，分别表示 工作日、周末、节日、调休。
            "name": "周六",         // 节假日类型中文名，可能值为 周一 至 周日、假期的名字、某某调休。
            "week": enum(1 - 7)    // 一周中的第几天。值为 1 - 7，分别表示 周一 至 周日。
            "status": enum(0, 1)    // 数据场景类型，0来源于仓库中或者正常的上班日，数据可靠；1表示当前传入日期在仓库中未查询到，直接走系统计算，数据不可靠。
          },
          "holiday": {              // 只有当type为2，3时，该对象才存在
            "holiday": false,     // true表示是节假日，false表示是调休
            "name": "国庆调休",  // 节假日的中文名。如果是调休，则是调休的中文名，例如'国庆节调休'
            "date": '2021-10-09'     // 当前请求的日期
          }
        }
        组装数据
        :return:
        """
        # 获取年份
        if not today:
            year_data = datetime.datetime.now().strftime('%Y')
        else:
            year_data = datetime.datetime.strptime(today, "%Y-%m-%d").date().year
        today_d = self.get_today_data(today=today, current_year=year_data)
        today_data, today_status = today_d[0], today_d[1]
        # today_status = self.get_today_data(today=today, current_year=year_data)[1]
        # print(today_data)
        week = today_data['week']
        json_data = {
            'code': 0,
            'type': {
                'type': today_data['t_type'],
                'name': self.get_weekday_enum_cn(week_day=int(week)),
                'week': week,
                'status': today_status
            },
            'holiday': None
        }
        # 如果是节假日或者调休时，需要追加字段
        if today_data['t_type'] not in (0, 1):
            d_dict = {
                'holiday': True,
                'name': today_data['name'],
                'date': today_data['date']
            }
            if today_data['isOffDay'] is False:
                d_dict['holiday'] = False
                d_dict['name'] += '调休'
            json_data['holiday'] = d_dict
        return json_data


def dateRange(start, end, step=1, _format="%Y-%m-%d"):  # 生成日期序列
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, _format) - strptime(start, _format)).days
    return [strftime(strptime(start, _format) + datetime.timedelta(i), _format) for i in range(0, days, step)]

if __name__ == '__main__':
    g = getHoliday()
    # print(getGithubHolidayJson.get_current_isoweekday())
    # print(json.dumps(g.get_before_and_after_holiday_json()))
    # print(getGithubHolidayJson.get_weekday_enum_cn(1))
    # 当天
    print(g.assemble_holiday_data(today='2021-10-9'))
    # print(g.get_holiday_json(current_year=100))
    # for i in dateRange('2021-12-17','2022-12-29'):
    #     print(g.assemble_holiday_data(i))