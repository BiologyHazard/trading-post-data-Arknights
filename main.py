import csv
from fractions import Fraction
from pathlib import Path


def dot_product(a, b):
    return sum(x * y for x, y in zip(a, b))


def item_str(key, value) -> str:
    if value.denominator == 1:
        return f'{key} = {value.numerator}'
    else:
        return f'{key} = {value.numerator} / {value.denominator} = {float(value)}'


for csv_path in Path().glob('*.csv'):
    plan_name = csv_path.stem
    output_path = Path(f'{plan_name}.txt')
    reader = csv.reader(csv_path.read_text('utf-8').splitlines(), delimiter='\t')
    data = list(reader)
    p = [Fraction(row[0][:-1]) / 100 for row in data[1:-1]]
    t = [Fraction(row[1]) for row in data[1:-1]]
    g = [Fraction(row[2]) for row in data[1:-1]]
    l = [Fraction(row[3]) for row in data[1:-1]]
    每秒基础工时获得龙门币 = dot_product(p, l) / dot_product(p, t)
    每天基础工时获得龙门币 = 每秒基础工时获得龙门币 * 86400
    每秒基础工时消耗赤金 = dot_product(p, g) / dot_product(p, t)
    每天基础工时消耗赤金 = 每秒基础工时消耗赤金 * 86400
    每秒基础工时节省赤金 = 每秒基础工时获得龙门币 / 500 - 每秒基础工时消耗赤金
    每天基础工时节省赤金 = 每秒基础工时节省赤金 * 86400
    每秒基础工时印钱 = 每秒基础工时获得龙门币 - 每秒基础工时消耗赤金 * 500
    每天基础工时印钱 = 每秒基础工时印钱 * 86400
    平均每赤金获得龙门币 = 每秒基础工时获得龙门币 / 每秒基础工时消耗赤金
    生产1龙门币需要的秒基础工时 = 1 / 每秒基础工时获得龙门币 + 4320 / 平均每赤金获得龙门币
    钱书基础工时成本比 = 生产1龙门币需要的秒基础工时 / Fraction(54, 5)
    综合生产力 = (每秒基础工时获得龙门币 - 每秒基础工时消耗赤金 * 400 / 钱书基础工时成本比)
    # print(f'{plan_name} 综合生产力 = {float(综合生产力)}')
    items = {
        '每秒基础工时获得龙门币': 每秒基础工时获得龙门币,
        '每天基础工时获得龙门币': 每天基础工时获得龙门币,
        '每秒基础工时消耗赤金': 每秒基础工时消耗赤金,
        '每天基础工时消耗赤金': 每天基础工时消耗赤金,
        '每秒基础工时节省赤金': 每秒基础工时节省赤金,
        '每天基础工时节省赤金': 每天基础工时节省赤金,
        '每秒基础工时印钱': 每秒基础工时印钱,
        '每天基础工时印钱': 每天基础工时印钱,
        '平均每赤金获得龙门币': 平均每赤金获得龙门币,
        '生产 1 龙门币需要的秒基础工时': 生产1龙门币需要的秒基础工时,
        '钱书基础工时成本比': 钱书基础工时成本比,
    }
    s = '\n'.join(item_str(key, value) for key, value in items.items())
    output_path.write_text(s, 'utf-8')
