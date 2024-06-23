def test_make_row_cell_with_style():
    # 在此定义您的测试数据和依赖项
    tdLs = [...]  # 用您的测试数据替换
    rowIndex = ...  # 用行索引替换
    row = ...  # 用Excel行对象替换
    startCellIndex = ...  # 用起始单元格索引替换
    crossRowEleMetaLs = []  # 初始化为空列表
    workbook = ...  # 用Excel工作簿对象替换
    xssfFont = ...  # 用字体对象替换
    name = ...  # 用名称替换

    # 调用要测试的函数
    make_row_cell_with_style(tdLs, rowIndex, row, startCellIndex, crossRowEleMetaLs, workbook, xssfFont, name)

    # 根据您的测试数据和依赖项来断言预期的结果
    assert ...  # 添加您的断言

def test_get_capture_cell_size():
    # 在此定义您的测试数据和依赖项
    rowIndex = ...  # 用行索引替换
    colIndex = ...  # 用列索引替换
    crossRowEleMetaLs = [...]  # 用CrossRangeCellMeta对象的列表替换

    # 调用要测试的函数
    capture_cell_size = get_capture_cell_size(rowIndex, colIndex, crossRowEleMetaLs)

    # 根据您的测试数据和依赖项来断言预期的结果
    assert ...  # 添加您的断言

# 您可以根据需要添加更多的测试方法，以涵盖各种场景和边缘情况。

if __name__ == "__main__":
    # 使用您选择的测试框架运行测试
    # 例如，如果您使用pytest，可以使用：pytest -v your_test_module.py
    pass
