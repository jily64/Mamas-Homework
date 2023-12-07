import random
class RSA:
    def __init__(self, arg):
        a = arg.split(" ")
        if a[0] == 'generate':
            self.generate(int(a[1]))

    def check_easy_num(self, a):
        k = 0
        for i in range(2, int(a ** 0.5) + 1):
            if (a % i == 0):
                return False
        return True
    def generate(self, a):

        dig1 = '1'
        dig2 = '9'

        for i in range(a-1):
            dig1+="0"
            dig2+="9"

        nums = []

        while True:
            num1 = random.randint(int(dig1), int(dig2))
            if self.check_easy_num(num1):
                nums.append(num1)
                if len(nums)==2:
                    break

        e = 0


        N = nums[0] * nums[1]
        Ele = (nums[0] - 1) * (nums[1] - 1)
        for i in range(len(str(Ele))-2):
            dig1+="0"
        dig2 = str(Ele)

        print(dig2, dig1)
        print(Ele)
        nums = [19, 41]
        while True:
            e = random.randint(int(dig1), int(dig2))
            if self.check_easy_num(e) and e not in nums:
                break


        print(N, Ele, e)
        print(f"простые числа: {nums}")

    def de_generate(self, a):
        pass


rsa = RSA("generate 2")
