'''
#### 复利公式 ####

def invest(amount, rate, time):
    print("principal amount:{}".format(amount))
    for t in range(1, time + 1):
        amount = amount * (1 + rate)
        print("year {}: ${}".format(t, amount))

invest(100, .05, 8)
invest(2000, .025, 5)

#### 1~100 所有偶数 ####
def even_print():
    for i in range(1,101):
        if i % 2 == 0:
            print(i)
even_print()


#### 创建10个文本 ####
def text_creation():
    path = '/Users/Hou/Desktop/w/'
    for name in range (1,11):
        with open(path + str(name) + '.txt','w') as text:
            text.write(str(name))
            text.close()
            print('Done')
text_creation()

#### 2 手机号码测试
'''

def number_test():

    while True:
        number = input('Enter Your number :')
        CN_mobile = [134,135,136,137,138,139,150,151,152,157,158,159,182,183,184,187,188,147,178,1705]
        CN_union = [130,131,132,155,156,185,186,145,176,1709]
        CN_telecom = [133,153,180,181,189,177,1700]
        first_three = int(number[0:3])
        first_four = int(number[0:4])

        if len(number) == 11:

            if first_three in CN_mobile or first_four in CN_mobile:
                print('Operator : China Mobile')
                print('We\'re sending verification code via text to your phone:',number)
                break
            elif first_three in CN_telecom:
                print('Operator : China Telecom')
                print('We\'re sending verification code via text to your phone:',number)
                break
            elif first_three in CN_union:
                print('Operator : China Union')
                print('We\'re sending verification code via text to your phone:',number)
                break
            else:
                print('No such a operator')
        else:
            print('Invalid length,your number should be in 11 digits')

number_test()

# 在程序中,常常有一些无限循环的情况,比如当一个程序没有异常发生的时候,让循环一直执行.这时候就需要用到while(true)...break 这种用法
# 如果你使用了 if first_three or first_four in CN_mobile: 会一直得到CN_mobile的结果,这是因为在布尔运算中 130 or 1301 会为True