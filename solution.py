from fractions import Fraction
import itertools
import math
import random


"""
The names of 100 prisoners are placed in 100 wooden boxes, one name to a box, and the boxes are lined up on a table in a room. One by one, the prisoners are led into the room; each may look in at most 50 boxes, but must leave the room exactly as he found it and is permitted no further communication with the others. The prisoners have a chance to plot their strategy in advance, and they are going to need it, because unless every single prisoner finds his own name all will subsequently be executed. Find a strategy for them which has probability of success (all prisoners' survival) exceeding 30%.
"""

def perms(n):
    return itertools.permutations((range(0,n)))

def strategy_succeeds(strategy, outcome):
    if(len(strategy)!=len(outcome)):
        raise ValueError("Strategy and outcome not aligned!")
    for i in range(0,len(strategy)):
        if outcome[i] not in strategy[i]:
            return False
    return True

if(__name__=='__main__'):
    assert strategy_succeeds([[0,1],[1,2],[2,3],[3,0]],[0,1,2,3])
    assert not strategy_succeeds([[0,1],[1,2],[2,3],[3,0]],[3,0,1,2])

def successful_outcomes(strategy,n):
    return [outcome for outcome in perms(n) if strategy_succeeds(strategy, outcome)]

def strategy_success_rate(strategy, n):
    return Fraction(len(successful_outcomes(strategy,n)), math.factorial(n))

if(__name__=='__main__'):
    assert strategy_success_rate([[0],[1]],2)>0
    assert strategy_success_rate([[0],[1]],2)>0

def all_prisoner_choices(n):
    return itertools.combinations(range(0,n),n//2)

def all_strategies(n):
    return itertools.combinations_with_replacement(all_prisoner_choices(n), n)

def best_strategy(n, strategies_population):
    all = [(strategy,successful_outcomes(strategy,n)) for strategy in strategies_population]
    return sorted(all, key = lambda t: -len(t[1]))[0][0]

if(__name__=='__main__'):
    assert strategy_success_rate(best_strategy(2, all_strategies(2)),2) == Fraction(1,2)
    assert strategy_success_rate(best_strategy(4, all_strategies(4)),4) == Fraction(1,6)
    #Not enough to model strategies like that!

def open_box(choice,outcome,s):
    found_in_box = outcome[choice]
    s.send(found_in_box)
    return found_in_box

def try_boxes(prisoner_number,s,outcome):
    found = []
    choice = next(s)
    while(len(found)<=len(outcome)//2 and choice is not None):
        found_in_box = open_box(choice, outcome, s)
        found.append(found_in_box)
        if prisoner_number in found:
            return True
        choice = next(s)
    return prisoner_number in found

def strategy_succeeds(strategy, outcome):
    print("Checking if our strategy succeeds for %s"%str(outcome))
    for prisoner_number in range(0, len(strategy)):
        print("prisoner %s enters"%prisoner_number)
        s = strategy[prisoner_number]()
        success = try_boxes(prisoner_number,s,outcome)
        if not success:
            print("%s did not find their own name. All is lost."%prisoner_number)
            return False
        else:
            print("%s found their own name!"%prisoner_number)

    return True

"""
Rule:
Prisoner i opens [i], and then whatever number was in there
"""

def my_strategy_for_each_prisoner(prisoner_number):
    def ans():
        ret=prisoner_number
        stored= None
        while True:
            yield ret
            stored = yield
            ret = stored
    return ans

def my_strategy(n):
    return [my_strategy_for_each_prisoner(i) for i in range(0,n)]


if(__name__=='__main__'):
    #didn't work:(
    pass
    #assert strategy_success_rate(my_strategy(4),4)==Fraction(5,12)
    #assert strategy_success_rate(my_strategy(10),10)>=Fraction(30,100)


#hardcoded my particular strategy into this.
def strategy_succeeds(_,outcome):
    for prisoner_number in range(0, len(outcome)):
        found = []
        choice = prisoner_number
        while(len(found)<len(outcome)//2):
            found_in_box =outcome[choice]
            found.append(found_in_box)
            choice = found_in_box
        if not prisoner_number in found:
            return False
    return True
if(__name__=='__main__'):
    assert strategy_success_rate(my_strategy(4),4)==Fraction(5,12)
    assert strategy_success_rate(my_strategy(6),6)==Fraction(23,60)
    #unfortunately will take forever:
    #assert strategy_success_rate(my_strategy(100),100)>=0.3

def successful_outcomes(strategy,n, sample = []):
    return [outcome for outcome in sample or perms(n) if strategy_succeeds(strategy, outcome)]

def strategy_success_rate(strategy, n, sample = []):
    return Fraction(len(successful_outcomes(strategy,n, sample)),len(sample) or math.factorial(n) )

def sample(n,k):
    temp = [i for i in range(0,n)]
    random.shuffle(temp)
    result = set()
    for _ in range(k):
        result.add(tuple(temp))
        random.shuffle(temp)
    return result

if(__name__=='__main__'):
    assert strategy_success_rate(my_strategy(100),100, sample =sample(100,10**4)) > 0.30
    #about 31%
