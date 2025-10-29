"""
小学数学知识点体系
适用于三年级上下学期
"""

# 三年级数学知识点体系
KNOWLEDGE_POINTS = {
    "计算能力": {
        "description": "数的运算能力",
        "sub_points": {
            "多位数加减法": {
                "description": "万以内的加减法运算",
                "difficulty": 2,
                "keywords": ["加法", "减法", "万以内", "进位", "退位"]
            },
            "乘法运算": {
                "description": "两位数乘一位数、多位数乘一位数",
                "difficulty": 3,
                "keywords": ["乘法", "×", "乘以", "倍"]
            },
            "除法运算": {
                "description": "除法的认识和计算",
                "difficulty": 3,
                "keywords": ["除法", "÷", "除以", "平均分", "余数"]
            },
            "混合运算": {
                "description": "加减乘除混合运算",
                "difficulty": 4,
                "keywords": ["混合", "递等式", "运算顺序", "括号"]
            },
            "估算": {
                "description": "估算能力",
                "difficulty": 2,
                "keywords": ["估算", "大约", "接近"]
            }
        }
    },

    "几何图形": {
        "description": "图形认识与计算",
        "sub_points": {
            "周长": {
                "description": "图形周长的认识和计算",
                "difficulty": 3,
                "keywords": ["周长", "边长", "一周", "一圈"]
            },
            "面积": {
                "description": "面积的认识和计算",
                "difficulty": 4,
                "keywords": ["面积", "平方", "长方形面积", "正方形面积"]
            },
            "图形认识": {
                "description": "基本图形的认识",
                "difficulty": 2,
                "keywords": ["长方形", "正方形", "三角形", "圆", "平行四边形"]
            },
            "角的认识": {
                "description": "角的认识和分类",
                "difficulty": 2,
                "keywords": ["角", "直角", "锐角", "钝角"]
            }
        }
    },

    "应用能力": {
        "description": "解决实际问题的能力",
        "sub_points": {
            "两步应用题": {
                "description": "需要两步计算的应用题",
                "difficulty": 4,
                "keywords": ["应用题", "解决问题", "两步", "先...再..."]
            },
            "倍数问题": {
                "description": "倍数关系的应用题",
                "difficulty": 3,
                "keywords": ["倍", "是...的几倍", "倍数"]
            },
            "归一问题": {
                "description": "单价、总价类问题",
                "difficulty": 3,
                "keywords": ["单价", "总价", "数量", "每"]
            },
            "归总问题": {
                "description": "求总量的问题",
                "difficulty": 3,
                "keywords": ["一共", "总共", "合计"]
            },
            "相遇问题": {
                "description": "行程相关问题",
                "difficulty": 4,
                "keywords": ["相遇", "同时", "相向", "速度"]
            }
        }
    },

    "时间与测量": {
        "description": "时间、长度、质量等测量",
        "sub_points": {
            "时间计算": {
                "description": "时间的认识和计算",
                "difficulty": 3,
                "keywords": ["时间", "小时", "分钟", "秒", "时刻", "经过"]
            },
            "长度单位": {
                "description": "长度单位的认识和换算",
                "difficulty": 2,
                "keywords": ["米", "分米", "厘米", "毫米", "千米", "长度"]
            },
            "质量单位": {
                "description": "质量单位的认识和换算",
                "difficulty": 2,
                "keywords": ["千克", "克", "吨", "重量", "质量"]
            },
            "单位换算": {
                "description": "各种单位之间的换算",
                "difficulty": 3,
                "keywords": ["换算", "进率", "化成"]
            }
        }
    },

    "数的认识": {
        "description": "数的认识和理解",
        "sub_points": {
            "万以内数的认识": {
                "description": "认识万以内的数",
                "difficulty": 2,
                "keywords": ["万", "千", "百", "十", "个", "位", "数位"]
            },
            "分数初步认识": {
                "description": "简单分数的认识",
                "difficulty": 3,
                "keywords": ["分数", "分之", "几分之几"]
            },
            "小数初步认识": {
                "description": "简单小数的认识",
                "difficulty": 3,
                "keywords": ["小数", "小数点", "十分之"]
            },
            "数的大小比较": {
                "description": "比较数的大小",
                "difficulty": 2,
                "keywords": ["比较", "大于", "小于", "等于", ">", "<", "="]
            }
        }
    },

    "逻辑思维": {
        "description": "逻辑推理和判断能力",
        "sub_points": {
            "规律发现": {
                "description": "发现数列或图形规律",
                "difficulty": 3,
                "keywords": ["规律", "找规律", "按规律", "下一个"]
            },
            "简单推理": {
                "description": "逻辑推理能力",
                "difficulty": 3,
                "keywords": ["推理", "判断", "可能", "一定"]
            },
            "对应关系": {
                "description": "理解数量对应关系",
                "difficulty": 3,
                "keywords": ["对应", "搭配", "组合"]
            }
        }
    }
}


def get_all_knowledge_points():
    """获取所有知识点的扁平列表"""
    all_points = []
    for category, category_data in KNOWLEDGE_POINTS.items():
        for point_name, point_data in category_data["sub_points"].items():
            all_points.append({
                "category": category,
                "name": point_name,
                "description": point_data["description"],
                "difficulty": point_data["difficulty"],
                "keywords": point_data["keywords"]
            })
    return all_points


def match_knowledge_points(question_content, existing_points=None):
    """
    根据题目内容匹配知识点

    Args:
        question_content: 题目内容
        existing_points: 已有的知识点列表

    Returns:
        匹配到的知识点列表
    """
    matched_points = []

    # 如果已经有知识点，先使用已有的
    if existing_points:
        return existing_points

    # 否则根据关键词匹配
    for category, category_data in KNOWLEDGE_POINTS.items():
        for point_name, point_data in category_data["sub_points"].items():
            # 检查关键词是否在题目中
            for keyword in point_data["keywords"]:
                if keyword in question_content:
                    if point_name not in matched_points:
                        matched_points.append(point_name)
                    break

    return matched_points if matched_points else ["未分类"]


def get_knowledge_point_info(point_name):
    """获取知识点详细信息"""
    for category, category_data in KNOWLEDGE_POINTS.items():
        if point_name in category_data["sub_points"]:
            info = category_data["sub_points"][point_name].copy()
            info["category"] = category
            info["name"] = point_name
            return info
    return None


if __name__ == "__main__":
    # 测试
    print("三年级数学知识点体系\n")
    print("=" * 60)

    for category, category_data in KNOWLEDGE_POINTS.items():
        print(f"\n📚 {category} - {category_data['description']}")
        for point_name, point_data in category_data["sub_points"].items():
            difficulty = "★" * point_data["difficulty"]
            print(f"  • {point_name} ({difficulty})")
            print(f"    {point_data['description']}")

    print("\n" + "=" * 60)
    print(f"共 {len(get_all_knowledge_points())} 个知识点")
