from collections.abc import Iterable, Sequence
from fractions import Fraction
from typing import Literal, NamedTuple, Self


class 订单详情(NamedTuple):
    概率: Fraction
    需要秒基础工时: int
    消耗赤金: int
    获得龙门币: int


class 贸易站数据:
    def __init__(self, 订单列表: list[订单详情]) -> None:
        self.订单列表: list[订单详情] = 订单列表

    @property
    def 需要秒基础工时期望(self) -> Fraction:
        return sum(订单.概率 * 订单.需要秒基础工时 for 订单 in self.订单列表)  # type: ignore

    @property
    def 消耗赤金期望(self) -> Fraction:
        return sum(订单.概率 * 订单.消耗赤金 for 订单 in self.订单列表)  # type: ignore

    @property
    def 获得龙门币期望(self) -> Fraction:
        return sum(订单.概率 * 订单.获得龙门币 for 订单 in self.订单列表)  # type: ignore

    @property
    def 每秒基础工时获得龙门币(self) -> Fraction:
        return self.获得龙门币期望 / self.需要秒基础工时期望

    @property
    def 每天基础工时获得龙门币(self) -> Fraction:
        return self.每秒基础工时获得龙门币 * 86400

    @property
    def 每秒基础工时消耗赤金(self) -> Fraction:
        return self.消耗赤金期望 / self.需要秒基础工时期望

    @property
    def 每天基础工时消耗赤金(self) -> Fraction:
        return self.每秒基础工时消耗赤金 * 86400

    @property
    def 平均每赤金获得龙门币(self) -> Fraction:
        return self.获得龙门币期望 / self.消耗赤金期望

    @property
    def 每秒基础工时节省赤金(self) -> Fraction:
        return self.每秒基础工时获得龙门币 / 500 - self.每秒基础工时消耗赤金

    @property
    def 每天基础工时节省赤金(self) -> Fraction:
        return self.每秒基础工时节省赤金 * 86400

    @property
    def 每秒基础工时印钱(self) -> Fraction:
        return self.每秒基础工时获得龙门币 - self.每秒基础工时消耗赤金 * 500

    @property
    def 每天基础工时印钱(self) -> Fraction:
        return self.每秒基础工时印钱 * 86400

    @property
    def 生产1龙门币需要的秒基础工时(self) -> Fraction:
        return 1 / self.每秒基础工时获得龙门币 + 4320 / self.平均每赤金获得龙门币

    @property
    def 钱书基础工时成本比(self) -> Fraction:
        return self.生产1龙门币需要的秒基础工时 / Fraction(54, 5)

    @property
    def 书钱基础工时成本比(self) -> Fraction:
        return 1 / self.钱书基础工时成本比

    @classmethod
    def new(cls, 贸易站等级: int, 但书: int | None, 龙舌兰: int | None, 裁缝: str | None) -> Self:
        需要秒基础工时列表: list[int] = [8640, 12600, 16560]
        if 贸易站等级 == 1:
            订单概率列表: list[Fraction] = [Fraction(100, 100)]
        elif 贸易站等级 == 2:
            订单概率列表 = [Fraction(60, 100), Fraction(40, 100)]
        elif 贸易站等级 == 3:
            if 裁缝 is None:
                订单概率列表 = [Fraction(30, 100), Fraction(50, 100), Fraction(20, 100)]
            elif 裁缝 in ("α", "alpha"):
                订单概率列表 = [Fraction(15, 100), Fraction(30, 100), Fraction(55, 100)]
            elif 裁缝 in ("β", "beta"):
                订单概率列表 = [Fraction(5, 100), Fraction(10, 100), Fraction(85, 100)]
            else:
                raise ValueError
        else:
            raise ValueError
        获得龙门币列表: list[int] = [1000, 1500, 2000]
        消耗赤金列表: list[int] = [2, 3, 4]
        if 但书 is None:
            pass
        elif 但书 in (0, 1):
            获得龙门币列表[0] += 500
            获得龙门币列表[1] += 500
            消耗赤金列表[0] += 1
            消耗赤金列表[1] += 1
        elif 但书 == 2:
            获得龙门币列表[0] += 1000
            获得龙门币列表[1] += 1000
            消耗赤金列表[0] += 2
            消耗赤金列表[1] += 2
        else:
            raise ValueError
        if 龙舌兰 is None:
            pass
        elif 龙舌兰 in (0, 1):
            获得龙门币列表[2] += 250
        elif 龙舌兰 == 2:
            获得龙门币列表[2] += 500
        else:
            raise ValueError
        订单列表: list[订单详情] = []
        for 概率, 需要秒基础工时, 消耗赤金, 获得龙门币 in zip(订单概率列表, 需要秒基础工时列表, 消耗赤金列表, 获得龙门币列表):
            订单列表.append(订单详情(概率, 需要秒基础工时, 消耗赤金, 获得龙门币))
        return cls(订单列表)


type Style = Literal["p / q = v", "p / q", "v"]


def output_str(value: Fraction, style: Style = "p / q = v") -> str:
    if value.denominator == 1:
        return f"{value.numerator}"
    else:
        match style:
            case "p / q = v":
                return f"{value.numerator} / {value.denominator} = {float(value)}"
            case "p / q":
                return f"{value.numerator} / {value.denominator}"
            case "v":
                return f"{float(value)}"


def to_markdown_table(data: Sequence[Iterable[str]], include_header: bool = True) -> str:
    lines: list[str] = []
    if include_header:
        lines.append("| " + " | ".join(data[0]) + " |")
        lines.append("| " + " | ".join("---" for _ in data[0]) + " |")
        data = data[1:]
    for row in data:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


贸易站汇总: dict[str, 贸易站数据] = {
    "1 级龙门币贸易站": 贸易站数据.new(贸易站等级=1, 但书=None, 龙舌兰=None, 裁缝=None),
    "1 级龙门币贸易站，进驻但书 II": 贸易站数据.new(贸易站等级=1, 但书=2, 龙舌兰=None, 裁缝=None),
    "2 级龙门币贸易站": 贸易站数据.new(贸易站等级=2, 但书=None, 龙舌兰=None, 裁缝=None),
    "2 级龙门币贸易站，进驻但书 II": 贸易站数据.new(贸易站等级=2, 但书=2, 龙舌兰=None, 裁缝=None),
    "3 级龙门币贸易站": 贸易站数据.new(贸易站等级=3, 但书=None, 龙舌兰=None, 裁缝=None),
    "3 级龙门币贸易站，进驻裁缝·α": 贸易站数据.new(贸易站等级=3, 但书=None, 龙舌兰=None, 裁缝="α"),
    "3 级龙门币贸易站，进驻裁缝·β": 贸易站数据.new(贸易站等级=3, 但书=None, 龙舌兰=None, 裁缝="β"),
    "3 级龙门币贸易站，进驻但书 II": 贸易站数据.new(贸易站等级=3, 但书=2, 龙舌兰=None, 裁缝=None),
    "3 级龙门币贸易站，进驻龙舌兰 II": 贸易站数据.new(贸易站等级=3, 但书=None, 龙舌兰=2, 裁缝=None),
    "3 级龙门币贸易站，进驻龙舌兰 II、裁缝·α": 贸易站数据.new(贸易站等级=3, 但书=None, 龙舌兰=2, 裁缝="α"),
    "3 级龙门币贸易站，进驻龙舌兰 II、裁缝·β": 贸易站数据.new(贸易站等级=3, 但书=None, 龙舌兰=2, 裁缝="β"),
    "3 级龙门币贸易站，进驻但书 II、龙舌兰 II": 贸易站数据.new(贸易站等级=3, 但书=2, 龙舌兰=2, 裁缝=None),
    "3 级龙门币贸易站，进驻但书 II、龙舌兰 II、裁缝·α": 贸易站数据.new(贸易站等级=3, 但书=2, 龙舌兰=2, 裁缝="α"),
    "3 级龙门币贸易站，进驻但书 II、龙舌兰 II、裁缝·β": 贸易站数据.new(贸易站等级=3, 但书=2, 龙舌兰=2, 裁缝="β"),
}


columns = [
    "贸易站名称",
    "每秒基础工时获得龙门币",
    "每天基础工时获得龙门币",
    "每秒基础工时消耗赤金",
    "每天基础工时消耗赤金",
    "平均每赤金获得龙门币",
    "每秒基础工时节省赤金",
    "每天基础工时节省赤金",
    "每秒基础工时印钱",
    "每天基础工时印钱",
    "生产 1 龙门币需要的秒基础工时",
    "钱书基础工时成本比",
    "书钱基础工时成本比",
]


lines: list[str] = []
for 贸易站名称, 贸易站 in 贸易站汇总.items():
    lines.append(f"## {贸易站名称}")
    lines.append(f"")

    data: list[list[str]] = [["概率", "需要秒基础工时", "消耗赤金数", "获得龙门币"]]
    for 订单 in 贸易站.订单列表:
        data.append([
            f"{output_str(订单.概率 * 100, "v")}%",
            f"{订单.需要秒基础工时}",
            f"{订单.消耗赤金}",
            f"{订单.获得龙门币}",
        ])
    data.append([
        "综合",
        output_str(贸易站.需要秒基础工时期望, "v"),
        output_str(贸易站.消耗赤金期望, "v"),
        output_str(贸易站.获得龙门币期望, "v"),
    ])

    lines.append(to_markdown_table(data))
    lines.append(f"")

    lines.append(f"- 每秒基础工时获得龙门币 = {output_str(贸易站.每秒基础工时获得龙门币)}")
    lines.append(f"- 每天基础工时获得龙门币 = {output_str(贸易站.每天基础工时获得龙门币)}")
    lines.append(f"- 每秒基础工时消耗赤金 = {output_str(贸易站.每秒基础工时消耗赤金)}")
    lines.append(f"- 每天基础工时消耗赤金 = {output_str(贸易站.每天基础工时消耗赤金)}")
    lines.append(f"- 平均每赤金获得龙门币 = {output_str(贸易站.平均每赤金获得龙门币)}")
    lines.append(f"- 每秒基础工时节省赤金 = {output_str(贸易站.每秒基础工时节省赤金)}")
    lines.append(f"- 每天基础工时节省赤金 = {output_str(贸易站.每天基础工时节省赤金)}")
    lines.append(f"- 每秒基础工时印钱 = {output_str(贸易站.每秒基础工时印钱)}")
    lines.append(f"- 每天基础工时印钱 = {output_str(贸易站.每天基础工时印钱)}")
    lines.append(f"- 生产 1 龙门币需要的秒基础工时 = {output_str(贸易站.生产1龙门币需要的秒基础工时)}")
    lines.append(f"- 钱书基础工时成本比 = {output_str(贸易站.钱书基础工时成本比)}")
    lines.append(f"- 书钱基础工时成本比 = {output_str(贸易站.书钱基础工时成本比)}")
    lines.append("")


for style in ("p / q", "v"):
    data: list[list[str]] = [columns]

    for 贸易站名称, 贸易站 in 贸易站汇总.items():
        line = [
            贸易站名称,
            output_str(贸易站.每秒基础工时获得龙门币, style),
            output_str(贸易站.每天基础工时获得龙门币, style),
            output_str(贸易站.每秒基础工时消耗赤金, style),
            output_str(贸易站.每天基础工时消耗赤金, style),
            output_str(贸易站.平均每赤金获得龙门币, style),
            output_str(贸易站.每秒基础工时节省赤金, style),
            output_str(贸易站.每天基础工时节省赤金, style),
            output_str(贸易站.每秒基础工时印钱, style),
            output_str(贸易站.每天基础工时印钱, style),
            output_str(贸易站.生产1龙门币需要的秒基础工时, style),
            output_str(贸易站.钱书基础工时成本比, style),
            output_str(贸易站.书钱基础工时成本比, style),
        ]
        data.append(line)

    lines.append(to_markdown_table(data))
    lines.append("")

with open("output.md", "w", encoding="utf-8") as fp:
    fp.write("\n".join(lines))
