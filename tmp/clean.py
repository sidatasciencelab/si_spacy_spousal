import glob

files = glob.glob("texts/**.txt")
texts = []
for file in files:
    print (file)
    file = file.replace("\\", "/")
    with open (file, "r", encoding="utf-8") as f:
        text = f.read().split("\n\n\n\n")
        print (len(text))
        new = []
        for line in text:
            if "SMITHSONIAN YEAR" in line or "SCIENCE" in line:
                line = "PAGE BREAK"
            line = line.strip()
            if len(line) > 5:
                line = line.replace("\n", " ")
                while "  " in line:
                    line = line.replace("  ", " ")

                new.append(line)

        final = []
        titles = ["Mr.", "Mrs.", "Dr.", "Ms.", "Mr ", "Mrs ", "Miss ", "Ms ", "Dr "]
        x=0
        for item in new:
            i = len(final)-1
            try:
                if "PAGE BREAK" == item:
                    last = final[i]["text"]
                    combined = f"{last} {new[x+1]}"
                    while "  " in combined:
                        combined = combined.replace("  ", " ")
                    del final[i]
                    final.append(combined)
                    x=x+1
                else:
                    final.append(item)
                    x=x+1
            except:
                IndexError
                print (item)
                x=x+1
        absolute = []
        for item in final:

            if item.isupper():
                pass
            else:
                if len(item) > 100:
                    res = [ele for ele in titles if(ele in item)]
                    if bool(res) == True:
                        absolute.append(item)
    for item in absolute:
        texts.append(item)


# with open ("data/corpus.json", "w", encoding="utf-8") as f:
#     json.dump(absolute, f, indent=4)


all = "\n".join(texts)

with open ("data/corpus.txt", "w", encoding="utf-8") as f:
    f.write(all)
