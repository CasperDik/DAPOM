# solutions 3.5 and 3.6
# author: Nick Szirbik
# date: 14 Feb 2022


def checking_various_criteria(table):
    for row in table[1:]:
        name = row[0]
        address = row[1]
        if name[0] == "D" and address[0] == "R":
            print("-selected on first criteria: ", row)

    for row in table[1:]:
        name = row[0]
        if name.find("Pizz") != -1 or name.find("pizz") != -1:
            print("-selected on second criteria: ", row)

    for row in table[1:]:
        name = row[0]
        if (name.find("Pizz") != -1 or name.find("pizz") != -1) or (name.find("Eet") != -1 or name.find("eet") != -1):
            print("-selected on third criteria: ", row)
    #           change the "and" logical operator in the condition above with "or" and see what happens

    # it is actually easier for this kind of check to convert the string that is
    # checked into a lowercase only string, by using the function lower() as below

    for row in table[1:]:
        address = row[1].lower()
        if (address.find("noord") != -1) or (address.find("zuid") != -1) or (address.find("oost") != -1) or (address.find("west") != - 1):
            print("-selected on the final criteria", row)
