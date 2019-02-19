from bitmap import BitMap

bool_operators = ["AND","OR","NOT_AND","NOT"]
def process_query(search_query):
    res = ""
    if (type(search_query) is str) :
        query = search_query.split(" ")
        bm = ""
        for word in query:
            bm+="1"
        bitmap = BitMap.fromstring(bm)
        for word,index in query:
            res+=word
            if word in bool_operators:
                if (str(word).endswith(")") | str(word).startswith()):
                    print(word)


                if (word == "NOT"):
                    print("perorm negation")
                print(res)
    else:
        print("Object of " + str(type(search_query)))

