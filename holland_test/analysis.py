"""霍兰德职业兴趣测试结果分析和职业建议 - 专业版"""

from typing import Dict, List, Tuple

from .questions import HOLLAND_TYPES
from .scorer import TestResult

# 职业建议库（更全面的职业列表）
CAREER_SUGGESTIONS: Dict[str, List[str]] = {
    "R": [
        "机械工程师", "电气工程师", "土木工程师", "建筑工程师",
        "汽车工程师", "航空工程师", "制造工程师", "工艺工程师",
        "技术员", "机械师", "电工", "木匠", "焊工", "装配工",
        "建筑师", "室内设计师", "景观设计师",
        "农民", "园艺师", "养殖员", "飞行员", "驾驶员",
        "消防员", "警察", "运动员", "健身教练",
        "质量检验员", "设备维护工程师",
    ],
    "I": [
        "科学家（物理、化学、生物、数学等）", "研究员", "研发工程师",
        "数学家", "统计学家", "精算师", "数据科学家",
        "医生", "药剂师", "生物学家", "化学家", "物理学家",
        "计算机科学家", "软件工程师（研发方向）", "算法工程师",
        "数据分析师", "商业分析师", "市场研究员",
        "实验室技术员", "质量工程师",
        "经济学家", "心理学家", "社会学家", "人类学家",
        "工程师（研发方向）", "专利工程师",
        "科研院所研究员", "大学教授（理工科）",
    ],
    "A": [
        "艺术家", "画家", "雕塑家", "设计师（平面、UI、视觉等）",
        "室内设计师", "服装设计师", "工业设计师", "产品设计师",
        "音乐家", "作曲家", "音乐制作人", "DJ",
        "作家", "编剧", "文案策划", "编辑",
        "摄影师", "摄像师", "导演", "演员", "主持人",
        "广告创意总监", "艺术指导", "创意总监",
        "建筑师（设计方向）", "景观设计师",
        "舞蹈家", "编舞", "艺术教师", "美术指导",
        "插画师", "动画师", "游戏设计师",
    ],
    "S": [
        "教师", "大学教授", "培训师", "教育顾问",
        "心理咨询师", "心理治疗师", "职业生涯规划师",
        "社会工作者", "社区工作者", "社工",
        "医生", "护士", "康复师", "理疗师", "营养师",
        "人力资源", "HR", "招聘专员", "员工关系专员",
        "职业顾问", "就业指导师",
        "宗教工作者", "牧师", "神父",
        "志愿者协调员", "NGO工作者",
        "销售（服务导向）", "客户服务", "客户经理",
        "治疗师", "特殊教育教师",
    ],
    "E": [
        "企业家", "创业者", "CEO", "总经理",
        "经理", "部门经理", "区域经理", "项目经理",
        "销售经理", "业务经理", "市场经理",
        "市场营销", "品牌经理", "产品经理",
        "律师", "法官", "检察官",
        "政治家", "政府官员", "公务员（管理岗位）",
        "金融分析师", "投资顾问", "基金经理",
        "房地产经纪人", "保险经纪人",
        "人力资源经理", "组织发展专员",
        "业务开发", "BD经理",
        "公关经理", "媒体关系专员",
        "管理咨询师", "商业顾问",
    ],
    "C": [
        "会计师", "审计师", "财务分析师", "成本会计师",
        "税务专家", "税务顾问",
        "银行职员", "信贷员", "风险控制专员",
        "行政助理", "秘书", "文员",
        "图书管理员", "档案管理员", "资料管理员",
        "数据录入员", "统计员", "质量检查员",
        "办公室经理", "行政经理",
        "出纳", "收银员",
        "物流管理员", "仓库管理员",
        "系统管理员", "数据库管理员",
        "法务专员", "合规专员",
    ],
}

# 类型特征详细描述
TYPE_DESCRIPTIONS: Dict[str, Dict[str, str]] = {
    "R": {
        "name": "现实型 (Realistic)",
        "characteristics": "实际、稳重、偏好具体的工作任务",
        "likes": "使用工具、机器和设备，户外工作，动手操作",
        "dislikes": "抽象的工作，与人频繁交往，理论分析",
        "work_environment": "需要动手操作的环境，工厂、车间、户外",
        "skills": "机械操作、工具使用、技术维修、实际解决问题的能力",
        "values": "实用、稳定、可见的成果、技能掌握",
    },
    "I": {
        "name": "研究型 (Investigative)",
        "characteristics": "好奇、分析、独立、理性、严谨",
        "likes": "观察、学习、研究、分析和解决问题，独立思考",
        "dislikes": "销售或说服他人，重复性工作，社交活动",
        "work_environment": "实验室、研究机构、学术环境、安静的工作空间",
        "skills": "分析思维、逻辑推理、研究能力、数据处理、问题解决",
        "values": "知识、真理、创新、学术成就、科学发现",
    },
    "A": {
        "name": "艺术型 (Artistic)",
        "characteristics": "创新、独立、情感丰富、富有想象力、敏感",
        "likes": "自由表达、创作、艺术活动、独立工作",
        "dislikes": "结构化的工作，严格遵循规则，重复性任务",
        "work_environment": "灵活、创意导向的环境，工作室、创作空间",
        "skills": "创作能力、艺术技巧、想象力、表达能力、审美能力",
        "values": "自由、创意、自我表达、美感、独特性",
    },
    "S": {
        "name": "社会型 (Social)",
        "characteristics": "友善、合作、善解人意、乐于助人、有同理心",
        "likes": "帮助他人、教学、照顾他人、团队合作",
        "dislikes": "使用机器或工具，技术性工作，独自工作",
        "work_environment": "需要人际交往的环境，学校、医院、社区",
        "skills": "沟通能力、同理心、教学能力、咨询技巧、团队合作",
        "values": "帮助他人、服务社会、人际关系、他人成长",
    },
    "E": {
        "name": "企业型 (Enterprising)",
        "characteristics": "自信、有野心、精力充沛、善于说服、有领导力",
        "likes": "领导、影响他人、销售、管理、竞争",
        "dislikes": "科学研究、细致的观察工作、重复性任务",
        "work_environment": "需要领导和影响力的环境，办公室、会议室",
        "skills": "领导能力、沟通说服、商业思维、组织管理、决策能力",
        "values": "成功、权力、地位、经济利益、影响力",
    },
    "C": {
        "name": "常规型 (Conventional)",
        "characteristics": "细心、有条理、谨慎、服从、可靠",
        "likes": "数据、记录、组织、遵循程序、稳定工作",
        "dislikes": "不确定或非结构化的工作，创新挑战，风险",
        "work_environment": "有序、稳定的办公室环境，标准化的工作流程",
        "skills": "组织能力、数据处理、文件管理、细节关注、程序执行",
        "values": "稳定、安全、秩序、准确性、可靠性",
    },
}

# 类型组合的职业倾向（常见组合）
TYPE_COMBINATIONS: Dict[str, Dict[str, any]] = {
    "RI": {
        "name": "现实-研究型",
        "description": "技术研究与实际应用相结合",
        "careers": ["研发工程师", "技术专家", "产品开发", "质量工程师"],
    },
    "RA": {
        "name": "现实-艺术型",
        "description": "技术与创意相结合",
        "careers": ["工业设计师", "建筑设计师", "产品设计师", "工艺美术师"],
    },
    "RS": {
        "name": "现实-社会型",
        "description": "技术服务于他人",
        "careers": ["技术培训师", "康复师", "特殊教育教师", "技术支持"],
    },
    "RE": {
        "name": "现实-企业型",
        "description": "技术管理与商业结合",
        "careers": ["技术经理", "项目经理", "生产经理", "工程承包商"],
    },
    "RC": {
        "name": "现实-常规型",
        "description": "技术操作与规范管理",
        "careers": ["质量检验员", "设备管理员", "生产调度", "技术文档管理"],
    },
    "IA": {
        "name": "研究-艺术型",
        "description": "科学研究与创意表达",
        "careers": ["科学作家", "科学可视化", "技术编辑", "用户体验研究员"],
    },
    "IS": {
        "name": "研究-社会型",
        "description": "科学研究服务于社会",
        "careers": ["医生", "心理学研究员", "教育研究员", "公共卫生专家"],
    },
    "IE": {
        "name": "研究-企业型",
        "description": "研究与商业应用",
        "careers": ["研发总监", "技术顾问", "专利代理", "技术创业"],
    },
    "IC": {
        "name": "研究-常规型",
        "description": "研究与数据管理",
        "careers": ["数据分析师", "统计员", "质量工程师", "研究助理"],
    },
    "AS": {
        "name": "艺术-社会型",
        "description": "艺术创作服务于他人",
        "careers": ["艺术教师", "艺术治疗师", "社区艺术工作者", "文化传播"],
    },
    "AE": {
        "name": "艺术-企业型",
        "description": "艺术与商业结合",
        "careers": ["广告创意总监", "品牌经理", "艺术经纪人", "创意产业管理"],
    },
    "AC": {
        "name": "艺术-常规型",
        "description": "艺术与规范管理",
        "careers": ["艺术管理", "博物馆管理员", "画廊管理员", "艺术档案管理"],
    },
    "SE": {
        "name": "社会-企业型",
        "description": "服务他人与领导管理",
        "careers": ["人力资源经理", "培训总监", "组织发展", "非营利组织管理"],
    },
    "SC": {
        "name": "社会-常规型",
        "description": "服务与规范管理",
        "careers": ["行政服务", "客户服务管理", "社会服务管理", "教育管理"],
    },
    "EC": {
        "name": "企业-常规型",
        "description": "商业管理与规范执行",
        "careers": ["财务经理", "运营经理", "项目经理", "业务管理"],
    },
}


def get_type_description(type_code: str) -> Dict[str, str]:
    """获取类型详细描述"""
    return TYPE_DESCRIPTIONS.get(type_code, {})


def get_career_suggestions(type_code: str) -> List[str]:
    """获取职业建议"""
    return CAREER_SUGGESTIONS.get(type_code, [])


def analyze_career_tendency(result: TestResult) -> Dict[str, any]:
    """
    分析职业倾向
    
    Args:
        result: 测试结果
        
    Returns:
        职业倾向分析结果
    """
    tendency = {
        "dominant_type": result.primary_type,
        "supporting_types": [result.secondary_type, result.tertiary_type],
        "strength_level": {},
        "work_style": "",
        "team_preference": "",
    }
    
    # 判断强度水平
    for type_code, percentage in result.percentages.items():
        if percentage >= 70:
            tendency["strength_level"][type_code] = "很强"
        elif percentage >= 50:
            tendency["strength_level"][type_code] = "较强"
        elif percentage >= 30:
            tendency["strength_level"][type_code] = "中等"
        else:
            tendency["strength_level"][type_code] = "较弱"
    
    # 判断工作风格
    if result.primary_type in ["R", "I", "A"]:
        tendency["work_style"] = "更适合独立工作或小团队协作"
    elif result.primary_type in ["S", "E"]:
        tendency["work_style"] = "更适合团队合作和人际交往"
    else:
        tendency["work_style"] = "更适合规范化的工作环境"
    
    # 判断团队偏好
    if result.primary_type == "S":
        tendency["team_preference"] = "喜欢团队合作，擅长协调人际关系"
    elif result.primary_type == "E":
        tendency["team_preference"] = "喜欢领导团队，擅长管理和组织"
    elif result.primary_type in ["R", "I"]:
        tendency["team_preference"] = "可以独立工作，也能参与团队项目"
    else:
        tendency["team_preference"] = "更适合独立创作或规范化工作"
    
    return tendency


def analyze_career_positioning(result: TestResult) -> Dict[str, any]:
    """
    分析职业定位
    
    Args:
        result: 测试结果
        
    Returns:
        职业定位分析结果
    """
    positioning = {
        "primary_positioning": "",
        "career_fields": [],
        "suitable_industries": [],
        "career_level": "",
    }
    
    # 主要定位
    primary_desc = TYPE_DESCRIPTIONS[result.primary_type]
    positioning["primary_positioning"] = f"{primary_desc['name']} - {primary_desc['characteristics']}"
    
    # 适合的行业
    industry_mapping = {
        "R": ["制造业", "建筑业", "交通运输", "能源", "农业", "技术服务业"],
        "I": ["科研院所", "高等教育", "医药研发", "信息技术", "咨询研究"],
        "A": ["文化创意", "广告传媒", "设计", "艺术", "娱乐", "出版"],
        "S": ["教育", "医疗健康", "社会服务", "心理咨询", "人力资源"],
        "E": ["商业管理", "金融投资", "销售贸易", "法律", "创业", "政府管理"],
        "C": ["金融服务", "会计审计", "行政服务", "物流", "信息管理"],
    }
    
    for type_code in [result.primary_type, result.secondary_type]:
        positioning["suitable_industries"].extend(industry_mapping.get(type_code, []))
    positioning["suitable_industries"] = list(set(positioning["suitable_industries"]))
    
    # 职业层级建议
    primary_pct = result.percentages[result.primary_type]
    if primary_pct >= 70:
        positioning["career_level"] = "非常适合该领域，可以考虑成为该领域的专家或高级专业人员"
    elif primary_pct >= 50:
        positioning["career_level"] = "比较适合该领域，可以从基础岗位开始，逐步发展为专业人员"
    else:
        positioning["career_level"] = "可以考虑该领域，但建议结合其他兴趣类型寻找更适合的方向"
    
    return positioning


def generate_career_guidance(result: TestResult) -> Dict[str, List[str]]:
    """
    生成职业指导建议
    
    Args:
        result: 测试结果
        
    Returns:
        职业指导建议
    """
    guidance = {
        "immediate_actions": [],
        "skill_development": [],
        "career_path": [],
        "workplace_advice": [],
    }
    
    primary_desc = TYPE_DESCRIPTIONS[result.primary_type]
    
    # 立即行动建议
    guidance["immediate_actions"] = [
        f"深入了解{primary_desc['name']}相关的职业领域",
        "收集该领域的职业信息，了解工作内容和发展前景",
        "寻找该领域的实习或实践机会",
        "与该领域的专业人士交流，了解实际工作情况",
    ]
    
    # 技能发展建议
    skills = primary_desc.get("skills", "").split("、")
    guidance["skill_development"] = [
        f"重点培养{primary_desc['name']}相关的核心技能",
        "通过课程、培训或实践提升专业技能",
        "建立作品集或项目经验，展示相关能力",
        "持续学习和更新该领域的知识和技能",
    ]
    
    # 职业路径建议
    if result.percentages[result.primary_type] >= 70:
        guidance["career_path"] = [
            "可以直接进入该领域，从基础岗位开始",
            "在该领域深耕，成为专业人才",
            "可以考虑在该领域内跨职能发展",
            "长期目标可以是该领域的专家或高级管理人员",
        ]
    else:
        guidance["career_path"] = [
            f"可以考虑以{result.primary_type}为主，结合{result.secondary_type}发展复合型能力",
            "寻找结合多个兴趣类型的职业方向",
            "可以先尝试该领域的工作，根据实际体验调整方向",
            "保持开放心态，探索更多可能性",
        ]
    
    # 工作环境建议
    guidance["workplace_advice"] = [
        f"寻找{primary_desc['work_environment']}的工作环境",
        f"在工作中体现{primary_desc['values']}的价值观",
        f"避免{primary_desc['dislikes']}为主的工作内容",
        "找到适合的工作风格和节奏",
    ]
    
    return guidance
