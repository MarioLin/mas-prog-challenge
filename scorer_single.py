import sys

# assumes files are well formatted
# if you have errors, make sure you double check our input and output format
def main(argv):
    if len(argv) != 2:
        print "Usage: python scorer_single.py [path_to_instance] [path_to_answer]"
        return
    print processTest(argv[0], argv[1])

def processTest(inst, sol):
    fin = open(inst, "r")
    N = int(fin.readline().split()[0])
    d = [[0 for j in range(N)] for i in range(N)]
    for i in xrange(N):
        d[i] = map(int, fin.readline().split())

    fin = open(sol, "r")
    ans = map(lambda x: (int(x) - 1), fin.readline().split())

    count = 0.0
    for i in xrange(N):
        for j in xrange(i + 1, N):
            if d[ans[i]][ans[j]] == 1:
                count += 1
    return "solution value is %d" % count

if __name__ == '__main__':
    main(sys.argv[1:])