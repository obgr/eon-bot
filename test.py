test=['5', '4', '2', '5', "3", "1", "3", "5"]

# Functions
def prettifyDice(rolls):
    out =[]
    #out=""
    for i in rolls:
    #for x in range(len(i)): 
        if i == "1":
            emoji=":one:"
        elif i == "2":
            emoji=":two:"
        elif i == "3":
            emoji=":three:"
        elif i == "4":
            emoji=":four:"
        elif i == "5":
            emoji=":five:"
        elif i == "6":
            emoji=":six:"
        else:
            emoji=i
        out.append(str(emoji))
    return ', '.join(out)

output=prettifyDice(test)
#print(*output, sep=", ")
print(output)

#names = ["Sam", "Peter", "James", "Julian", "Ann"]
#print(*names, sep=", ")