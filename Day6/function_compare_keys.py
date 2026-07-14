from functools import cmp_to_key
def compare(a,b):
    print("a=",a,"b= ",b,",b-a=",b-a)
    return b-a
nums=[3,1,4,2]
sorted_nums=sorted(nums, key=cmp_to_key(compare))
print(sorted_nums)
