from Parsing import Tagtype


def EnumTest():
    assert Tagtype('td') == Tagtype.data            # lookup by value
    assert Tagtype['section'] == Tagtype.section    # lookup by name
    lookupval = 'th'
    lookupname = 'section'
    print(f"Enum name from value: \t{lookupval}\t --> {Tagtype(lookupval).name}")
    print(f"Enum value from name: \t{lookupname}\t --> {Tagtype[lookupname].value}")  # subtle difference in syntax

    # you can loop over an Enum, but you have to put it in a comprehension first
    assert repr([x for x in Tagtype]) == "[<Tagtype.header: 'th'>, <Tagtype.section: 'tr'>, <Tagtype.data: 'td'>, <Tagtype.table: 'table'>]"
    print("full enum list: ")
    print(repr([x for x in Tagtype]))
    print("\ncleaner representation\n")
    tnames, tvals = zip(*[(x.name, x.value) for x in Tagtype])  # note that 'zip(*iterable)' is it's own inverse
    print(f"names = {tnames}")
    print(f"values = {tvals}")


if __name__ == "__main__":
    EnumTest()
