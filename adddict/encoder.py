import codecs

def ReadFile(filePath,encoding):
    with codecs.open(filePath,"r",encoding) as f:
        return f.read()
def WriteFile(filePath,u,encoding):
    with codecs.open(filePath,"w",encoding) as f:
        f.write(u)

def GBK_2_UTF8(src,dst):
    content = ReadFile(src,encoding='gbk')
    WriteFile(dst,content,encoding='utf_8')



src = 'C:\Users\Administrator\Desktop\product_name.csv'
dst = 'C:\Users\Administrator\Desktop\product_name_utf8.csv'
GBK_2_UTF8(src,dst)