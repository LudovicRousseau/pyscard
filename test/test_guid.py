from smartcard.guid import GUIDToStr, strToGUID


def test_roundtrip_string():
    string = "{AD4F1667-EA75-4124-84D4-641B3B197C65}"
    assert GUIDToStr(strToGUID(string)) == string


def test_roundtrip_list_of_ints():
    list_of_ints = [
        103,
        22,
        79,
        173,
        117,
        234,
        36,
        65,
        132,
        212,
        100,
        27,
        59,
        25,
        124,
        101,
    ]
    assert strToGUID(GUIDToStr(list_of_ints)) == list_of_ints
