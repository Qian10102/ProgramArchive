a,b,c = input().split()                             #同行输入变量a,b,c，用空格分割
if float(c) == 0:
    print("除数不能为0")
else:
    d = float(b)/float(c)                           #d为除法运算结果，且没有按照输入保留小数
    d_str = str(d)                                  #将d转化为字符串，在后面用于判断小数数位
    d_places = len(d_str.split('.')[1])
    if d_places < int(a):
        e = int(a) - d_places + 1
        print_d = format(d,f'.{str(e)}f')
        print(print_d)
    else:
        print_d = round(d,int(a))                   #print_d为按照保留指定小数位数的结果
        print(print_d)