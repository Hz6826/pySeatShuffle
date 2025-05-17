import core

def test_seat_table_xlsx_parser():
    parser = core.SeatTableParserXlsx()
    seat_table = parser.parse(r".test\config\seat_table.xlsx")
    print(seat_table)
    print(parser.metadata)
    assert parser.metadata.gen_time_cell_pos == (8, 9)
