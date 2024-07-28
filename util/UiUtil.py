
def is_i_want_answer_page(d):
    """
    判断是否是答题开始页面
    """
    is_find1 = d(text="答题练习").exists(timeout=2)
    is_find2 = d(text="答题竞赛").exists(timeout=2)
    return is_find1 and is_find2