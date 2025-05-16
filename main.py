import core
import model

def t():
    instance = model.Instance(
        "test",
        core.parse_people(".test/config/people.csv"),
        core.parse_seat_table(".test/config/seat_table.json"),
        core.parse_ruleset(".test/config/ruleset/default.json"),
    )
    for i in core.Shuffler(instance):
        print(i)

if __name__ == "__main__":
    t()
