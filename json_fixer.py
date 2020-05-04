content = ""

with open('params.json') as f:
    for line in f.readlines():
        for word in line:
            if word[0] == "'":
                word = '"'+word[1:]
            if word[-1] == "'":
                word[-1] = '"'
            content += word
        # content += '\n'
    f.close()
        
with open('params.json', 'w') as f:
    f.write(content)
    f.close()
        
