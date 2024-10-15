# +: работает с дробными числами
def isEven(value):
    return value % 2 == 0


# работает быстрее чем isEven
# -: не работает с дробными числами
def myIsEven(value):
    return value & 1 == 0
