import gentb
import timeit

tests = ['''
for vec in gentb.gen_ex_pat(12):
    pass
    #print(vec)
'''
]

if __name__ == "__main__":
    i = 0
    for test in tests:
        i += 1
        result = timeit.timeit(test, setup='import gentb', number=1)
        print("Test ",i , " took ", result, " seconds")