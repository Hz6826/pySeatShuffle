import core
import model

def test():
    parser = core.SeatTableParserXlsx()
    seat_table = parser.parse(r".test\config\seat_table.xlsx")
    print(seat_table)
    print(parser.metadata)


if __name__ == "__main__":
    test()
