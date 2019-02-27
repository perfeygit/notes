def toc(filename,output):
    flag = False  # flag标识行文本是否在代码块内,在的话则忽略
    with open(output,'w',encoding='utf-8'):
        pass
    with open(filename,'r',encoding='utf-8') as f:
        for line in f.readlines():
            if line.startswith('```'):
                flag = not flag
            if flag:
                continue
            if line.startswith('#'):
                with open(output,'a',encoding='utf-8') as f:
                    n,title = len(line.strip().split()[0]),line.strip().split()[1]
                    print(n,title)
                    f.write('{}[{}]({})\n\n'.format(n*'******',title,'https://github.com/perfeygit/notes/blob/master/node.md#'+title))
                    print(title)
    with open(filename,'r',encoding='utf-8') as f1:
        with open(output,'a',encoding='utf-8') as f2:
            f2.write(f1.read())

toc(r'C:\Users\afly\Desktop\nodes\爬虫.md','node.md')
# with open('toc.md','w',encoding='utf-8') as f:
#     f.write('\t\taaa\n')
#     f.write('\t\taaa\n')
#     f.write('\t\taaa\n')