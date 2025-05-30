import core
from model import Person


def test_seat_table_xlsx_parser_and_exporter():
    parser = core.SeatTableParserXlsx()
    seat_table = parser.parse(r".test\config\seat_table.xlsx")
    print(seat_table)
    print(seat_table.metadata)
    assert seat_table.metadata.file_path == r".test\config\seat_table.xlsx"
    assert seat_table.metadata.gen_time_cell_pos == (10, 11)

    seat_table.seat_groups[0].get_seats()[0].set_user(Person("test", {}))

    exporter = core.SeatTableExporter()

    # specify the format
    exporter.export(seat_table, format=core.F_XLSX, path=r".test\run\export\out_from_xlsx.xlsx")
    exporter.export(seat_table, format=core.F_JSON, path=r".test\run\export\out_from_xlsx.json")



def test_seat_table_json_parser():
    parser = core.SeatTableParserJson()
    seat_table = parser.parse(r".test\config\seat_table.json")
    print(seat_table)
