from openpyxl import Workbook
from openpyxl.styles import Font, NamedStyle


def make_row_cell_with_style(tdLs, rowIndex, row, startCellIndex, crossRowEleMetaLs, workbook, xssfFont, name):
    i = startCellIndex
    for eleIndex in range(len(tdLs)):
        capture_cell_size = get_capture_cell_size(rowIndex, i, crossRowEleMetaLs)
        while capture_cell_size > 0:
            for j in range(capture_cell_size):
                cell = row.cell(row=rowIndex, column=i)
                i += 1
            capture_cell_size = get_capture_cell_size(rowIndex, i, crossRowEleMetaLs)

        thEle = tdLs[eleIndex]
        val = thEle.text.strip()

        if "销项税额13%" in val:
            print("")

        tool_index = None
        if "indexCode" in thEle.attrib:
            index_code = thEle.attrib["indexCode"]
            if index_code:
                key = f"{IndexConst.PREFIX_REDIS_KEY_INDEX}/{index_code}"
                tool_index = redis_util.get(key)
        else:
            val = thEle.text

        td_attributes = get_td_styles(thEle)
        if not val:
            a_element = thEle.find("a")
            if a_element is not None:
                val = a_element.text.strip()
            e = thEle.find("input")
            if e is not None:
                attribute = e.get("value")
                val = attribute if attribute is not None else ""

        row_span = int(thEle.get("rowspan", 1))
        col_span = int(thEle.get("colspan", 1))

        if row_span > 1 or col_span > 1:
            crossRowEleMetaLs.append(CrossRangeCellMeta(rowIndex, i, row_span, col_span))

        if col_span > 1:
            for j in range(1, col_span):
                i += 1
                cell = row.cell(row=rowIndex, column=i)


def get_capture_cell_size(rowIndex, colIndex, crossRowEleMetaLs):
    capture_cell_size = 0
    for crossRangeCellMeta in crossRowEleMetaLs:
        if (crossRangeCellMeta.firstRowIndex < rowIndex and crossRangeCellMeta.lastRow >= rowIndex
                and crossRangeCellMeta.firstColIndex <= colIndex and crossRangeCellMeta.lastCol >= colIndex):
            capture_cell_size = crossRangeCellMeta.lastCol - colIndex + 1
    return capture_cell_size
