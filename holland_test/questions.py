"""霍兰德职业兴趣测试题目库 - 专业版"""

from dataclasses import dataclass
from typing import List

# 霍兰德六种职业兴趣类型
HOLLAND_TYPES = {
    "R": "现实型 (Realistic)",
    "I": "研究型 (Investigative)",
    "A": "艺术型 (Artistic)",
    "S": "社会型 (Social)",
    "E": "企业型 (Enterprising)",
    "C": "常规型 (Conventional)",
}


@dataclass
class Question:
    """测试题目"""
    id: int
    text: str
    type: str  # R, I, A, S, E, C
    category: str = "interest"  # interest, activity, skill, value


# 测试题目库（每个类型20道题目，共120题）
# 参考标准霍兰德职业兴趣量表(SDS)设计
QUESTIONS: List[Question] = [
    # R - 现实型 (Realistic) - 20题
    Question(1, "我喜欢修理或装配机械设备", "R", "activity"),
    Question(2, "我喜欢使用工具或机器进行实际操作", "R", "activity"),
    Question(3, "我喜欢户外活动和野外工作", "R", "interest"),
    Question(4, "我喜欢做手工制作和工艺工作", "R", "activity"),
    Question(5, "我喜欢建筑、施工或装修工作", "R", "activity"),
    Question(6, "我喜欢操作和驾驶机械设备", "R", "activity"),
    Question(7, "我喜欢园艺、农业或养殖活动", "R", "interest"),
    Question(8, "我喜欢维修和保养各种物品", "R", "activity"),
    Question(9, "我喜欢解决技术性和实用性问题", "R", "skill"),
    Question(10, "我喜欢与物品、机器而非人打交道", "R", "interest"),
    Question(11, "我喜欢阅读机械、技术类书籍杂志", "R", "interest"),
    Question(12, "我喜欢参加技术技能竞赛", "R", "activity"),
    Question(13, "我喜欢制作模型或手工艺品", "R", "activity"),
    Question(14, "我喜欢测量和绘制技术图纸", "R", "skill"),
    Question(15, "我喜欢组装和拆卸各类设备", "R", "activity"),
    Question(16, "我喜欢参与生产制造活动", "R", "activity"),
    Question(17, "我喜欢学习各种实用技能", "R", "interest"),
    Question(18, "我喜欢在工厂或车间工作", "R", "interest"),
    Question(19, "我喜欢从事需要动手能力的工作", "R", "value"),
    Question(20, "我喜欢看到自己制作的产品成果", "R", "value"),
    
    # I - 研究型 (Investigative) - 20题
    Question(21, "我喜欢阅读科学或技术类书籍", "I", "interest"),
    Question(22, "我喜欢做实验或进行科学研究", "I", "activity"),
    Question(23, "我喜欢分析数据和信息", "I", "activity"),
    Question(24, "我喜欢解决复杂的问题", "I", "skill"),
    Question(25, "我喜欢独立思考和研究", "I", "value"),
    Question(26, "我喜欢探索新事物和未知领域", "I", "interest"),
    Question(27, "我喜欢数学或逻辑推理", "I", "skill"),
    Question(28, "我喜欢了解事物的工作原理和本质", "I", "interest"),
    Question(29, "我喜欢进行科学观察和记录", "I", "activity"),
    Question(30, "我喜欢在实验室或研究室工作", "I", "interest"),
    Question(31, "我喜欢阅读学术论文和研究报告", "I", "interest"),
    Question(32, "我喜欢参加学术讨论和研讨会", "I", "activity"),
    Question(33, "我喜欢使用科学方法解决问题", "I", "skill"),
    Question(34, "我喜欢收集和分析各种资料", "I", "activity"),
    Question(35, "我喜欢发现和验证科学规律", "I", "value"),
    Question(36, "我喜欢挑战复杂的智力问题", "I", "interest"),
    Question(37, "我喜欢进行数据统计和分析", "I", "activity"),
    Question(38, "我喜欢提出新的理论或假设", "I", "skill"),
    Question(39, "我喜欢在安静的环境中深入研究", "I", "value"),
    Question(40, "我喜欢通过研究获得新的知识", "I", "value"),
    
    # A - 艺术型 (Artistic) - 20题
    Question(41, "我喜欢创作艺术作品", "A", "activity"),
    Question(42, "我喜欢音乐、戏剧或舞蹈", "A", "interest"),
    Question(43, "我喜欢写作或表达创意想法", "A", "activity"),
    Question(44, "我喜欢设计或装饰工作", "A", "activity"),
    Question(45, "我喜欢摄影、绘画或雕塑", "A", "interest"),
    Question(46, "我喜欢欣赏各种艺术作品", "A", "interest"),
    Question(47, "我喜欢表达自己的想法和感受", "A", "value"),
    Question(48, "我喜欢从事创造性工作", "A", "value"),
    Question(49, "我喜欢独立工作，不受约束", "A", "value"),
    Question(50, "我喜欢参与文化活动", "A", "activity"),
    Question(51, "我喜欢尝试新的艺术表现形式", "A", "interest"),
    Question(52, "我喜欢通过艺术表达情感", "A", "value"),
    Question(53, "我喜欢阅读文学作品和诗歌", "A", "interest"),
    Question(54, "我喜欢参加艺术展览和演出", "A", "activity"),
    Question(55, "我喜欢学习各种艺术技巧", "A", "interest"),
    Question(56, "我喜欢自由的工作环境", "A", "value"),
    Question(57, "我喜欢创作独特和原创的作品", "A", "skill"),
    Question(58, "我喜欢用艺术方式解决问题", "A", "skill"),
    Question(59, "我喜欢展示自己的艺术才能", "A", "value"),
    Question(60, "我喜欢在不同领域寻找灵感", "A", "interest"),
    
    # S - 社会型 (Social) - 20题
    Question(61, "我喜欢帮助他人解决问题", "S", "activity"),
    Question(62, "我喜欢教学或培训他人", "S", "activity"),
    Question(63, "我喜欢照顾和关心他人", "S", "value"),
    Question(64, "我喜欢团队合作和集体活动", "S", "value"),
    Question(65, "我喜欢与人交流沟通", "S", "activity"),
    Question(66, "我喜欢组织社交和公益活动", "S", "activity"),
    Question(67, "我喜欢理解他人的感受和想法", "S", "skill"),
    Question(68, "我喜欢提供咨询或建议", "S", "activity"),
    Question(69, "我喜欢志愿服务工作", "S", "value"),
    Question(70, "我喜欢促进他人的发展和成长", "S", "value"),
    Question(71, "我喜欢参加社区服务活动", "S", "activity"),
    Question(72, "我喜欢处理人际关系问题", "S", "skill"),
    Question(73, "我喜欢在团队中发挥协调作用", "S", "skill"),
    Question(74, "我喜欢了解不同人的需求", "S", "interest"),
    Question(75, "我喜欢通过帮助他人获得满足感", "S", "value"),
    Question(76, "我喜欢参与教育和培训活动", "S", "interest"),
    Question(77, "我喜欢在服务性行业工作", "S", "interest"),
    Question(78, "我喜欢与他人分享知识和经验", "S", "value"),
    Question(79, "我喜欢创造和谐的人际关系", "S", "skill"),
    Question(80, "我喜欢看到他人因为我的帮助而进步", "S", "value"),
    
    # E - 企业型 (Enterprising) - 20题
    Question(81, "我喜欢领导或管理他人", "E", "activity"),
    Question(82, "我喜欢销售或说服他人", "E", "activity"),
    Question(83, "我喜欢制定商业计划和策略", "E", "skill"),
    Question(84, "我喜欢在竞争中获胜", "E", "value"),
    Question(85, "我喜欢组织和管理活动", "E", "activity"),
    Question(86, "我喜欢承担商业风险", "E", "value"),
    Question(87, "我喜欢创业或经营企业", "E", "interest"),
    Question(88, "我喜欢影响或说服他人", "E", "skill"),
    Question(89, "我喜欢承担领导责任", "E", "value"),
    Question(90, "我喜欢追求经济利益和成功", "E", "value"),
    Question(91, "我喜欢参与商业谈判", "E", "activity"),
    Question(92, "我喜欢阅读商业和管理类书籍", "E", "interest"),
    Question(93, "我喜欢制定目标并努力实现", "E", "skill"),
    Question(94, "我喜欢在快节奏的环境中工作", "E", "value"),
    Question(95, "我喜欢建立和维护商业关系", "E", "skill"),
    Question(96, "我喜欢管理项目和团队", "E", "activity"),
    Question(97, "我喜欢参与投资和金融活动", "E", "interest"),
    Question(98, "我喜欢通过努力获得更高的地位", "E", "value"),
    Question(99, "我喜欢处理复杂的商业问题", "E", "skill"),
    Question(100, "我喜欢在商业领域取得成功", "E", "value"),
    
    # C - 常规型 (Conventional) - 20题
    Question(101, "我喜欢整理文件和资料", "C", "activity"),
    Question(102, "我喜欢处理数据和记录", "C", "activity"),
    Question(103, "我喜欢遵循规则和程序", "C", "value"),
    Question(104, "我喜欢有规律的工作", "C", "value"),
    Question(105, "我喜欢使用办公软件", "C", "skill"),
    Question(106, "我喜欢保持整洁有序", "C", "value"),
    Question(107, "我喜欢做预算或财务工作", "C", "activity"),
    Question(108, "我喜欢处理日常事务", "C", "activity"),
    Question(109, "我喜欢稳定的工作环境", "C", "value"),
    Question(110, "我喜欢执行标准化的流程", "C", "activity"),
    Question(111, "我喜欢进行数据录入和整理", "C", "activity"),
    Question(112, "我喜欢使用统计软件分析数据", "C", "skill"),
    Question(113, "我喜欢维护档案和记录系统", "C", "activity"),
    Question(114, "我喜欢在有序的环境中工作", "C", "value"),
    Question(115, "我喜欢处理财务和会计事务", "C", "interest"),
    Question(116, "我喜欢阅读规章制度和操作手册", "C", "interest"),
    Question(117, "我喜欢确保工作的准确性和一致性", "C", "value"),
    Question(118, "我喜欢参与行政管理工作", "C", "activity"),
    Question(119, "我喜欢通过学习提高工作效率", "C", "skill"),
    Question(120, "我喜欢通过规范工作获得成就感", "C", "value"),
]


def get_questions_by_type(question_type: str) -> List[Question]:
    """获取指定类型的题目"""
    return [q for q in QUESTIONS if q.type == question_type]


def get_all_questions() -> List[Question]:
    """获取所有题目"""
    return QUESTIONS


def get_question_count_by_type() -> dict:
    """获取每个类型的题目数量"""
    count = {type_code: 0 for type_code in HOLLAND_TYPES.keys()}
    for q in QUESTIONS:
        count[q.type] += 1
    return count
