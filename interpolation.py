#https://en.wikipedia.org/wiki/Sigmoid_function
#https://www.reddit.com/r/gamedev/comments/4xkx71/sigmoidlike_interpolation/
#https://www.desmos.com/calculator/3zhzwbfrxd

def sigmoid(p, s, step):
    """ p and s are parameters as seen in https://www.desmos.com/calculator/3zhzwbfrxd
        step determines the "sample rate" of the end result"""
    c = (2 / (1 - s)) - 1
    result = []
    
    for x in range(0,100,int(100/step)):
        if x == 0:
            continue
        elif x <= p * 100:
            result.append(((x/100) ** c) / (p ** (c - 1)))
        elif x > p * 100:
            result.append(1 - ((1-(x/100)) ** c) / ((1-p) ** (c - 1)))
    
    return result

if __name__ == '__main__':
    print(sigmoid(0.5 ,0.5, 9))
