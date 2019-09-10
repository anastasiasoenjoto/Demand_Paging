import sys
import queue


# calculate the nextWord
#input: current process, values of ABC, current word, random integer, size of each process
#output: next word
def nextWord(r, process, cases, word, S):
    A = cases[process][0]
    B = cases[process][1]
    C = cases[process][2]
    y = r/2147483648

    if y < A:
        w = (word + 1 + S) % S
        return w
    elif y < A + B:
        w = (word - 5 + S) % S
        return w
    elif y < A+B+C:
        w = (word + 4 + S) % S
        return w
    elif y >= A+B+C:
        return -1



# reads random integer from the random-numbers.txt file
#input: counter to remember the last line read
#output: random integer

def rand(c):
    f = open("random-numbers.txt", 'r')
    content = f.read()
    content = content.split()
    x = content[c]
    x = int(x)
    return x


#checks if there is free frame
#input: frame table, current process, current page, pageFault table, fifoQueue, lrulsit, replacement algorithm, current time
#output: return -1 if no free frame and have to evict, else return frame number
def checkFreeFrame(frame, process, page, pageFault, fifoQueue, lruList, R, time):
    # condition to change frames: process change, page change
    # return frame number if free frame else return -1

    for f in range(len(frame)):
        if page == frame[f][0] and process == frame[f][1]:
            pageFault[process] = False
            if R == "lru":
                lruList[f] = time
            return f

    for f in range(len(frame) - 1, -1, -1):
        if frame[f][0] == None and frame[f][2] > 0:
            pageFault[process] = True
            if R == "fifo":
                fifoQueue.put(f)
            elif R == "lru":
                lruList[f] = time
            frame[f][3] = time

            return f
    pageFault[process] = True

    return -1



def main():

    M = int(sys.argv[1])
    P = int(sys.argv[2])
    S = int(sys.argv[3])
    J = int(sys.argv[4])
    N = int(sys.argv[5])
    R = sys.argv[6]

    noOfFrames = int(M/P)
    frames = [[None, None, P, None]] * noOfFrames


    # decides number of process and values of ABC according to the job mix
    if J == 1:
        processReferenced = [0] * 1
        cases = [[1, 0, 0]] * 1

    else:
        processReferenced = [0] * 4
        if J == 2:
            cases = [[1, 0, 0]] * 4

        elif J == 3:
            cases = [[0,0,0]] * 4

        elif J == 4:
            cases = [[0.75, 0.25, 0], [0.75, 0, 0.25], [0.75, 0.125, 0.125], [0.5, 0.125, 0.125]]

    pFault = [True] * len(processReferenced)
    fault = [0] * len(processReferenced)
    residencyTime = [0] * len(processReferenced)
    eviction = [0] * len(processReferenced)
    print(len(frames))
    print("The machine size is ", M)
    print("The page size is ", P)
    print("The process size is ", S)
    print("The job mix number is ", J)
    print("The number of references per process is ", N)
    print("The replacement algorithm is ", R,"\n")

    print("Calculating faults and average residency: ")
    print()

    time = 0
    c = 0
    nextOption = [-1] * len(processReferenced)
    fifoQueue = queue.Queue(maxsize = noOfFrames)
    lruList = [0] * noOfFrames


    while sum(processReferenced) < (N * len(processReferenced)):
        for process in range(len(processReferenced)):
            for ref in range(3):
                if processReferenced[process] < N:
                    # simulate this reference for this process
                    # first reference of the process
                    if nextOption[process] == -1:
                        if processReferenced[process] == 0:
                            word = (111 * (process + 1) + S) % S

                    else:
                        word = nextOption[process]
                        pFault[process] = False



                    processReferenced[process] += 1
                    pageNumber = word // P
                    time += 1
                    f = checkFreeFrame(frames, process, pageNumber, pFault, fifoQueue, lruList, R, time)

                    #has free frame or page and process found in frame
                    if f != -1:
                        frames[f] = [pageNumber, process, frames[f][2] - 1, frames[f][3]]
                        printFrame = f
                    #if no free frame have to decide which to evict
                    else:

                        if R == "fifo":
                            replace = fifoQueue.get()
                            residencyTime[frames[replace][1]] += (time - frames[replace][3])
                            eviction[frames[replace][1]] += 1

                            frames[replace] = [pageNumber, process, P, time]

                            printFrame = replace
                            fifoQueue.put(replace)

                        elif R == "lru":
                            replace = min(lruList)
                            replaceIndex = lruList.index(replace)
                            residencyTime[frames[replaceIndex][1]] += (time - frames[replaceIndex][3])
                            eviction[frames[replaceIndex][1]] += 1

                            frames[replaceIndex] = [pageNumber, process, P, time]

                            printFrame = replaceIndex
                            lruList[replaceIndex] = time

                        elif R == "random":
                            replace = rand(c)
                            c += 1
                            replace = (replace+noOfFrames) % noOfFrames
                            residencyTime[frames[replace][1]] += (time - frames[replace][3])
                            eviction[frames[replace][1]] += 1
                            frames[replace] = [pageNumber, process, P, time]
                            printFrame = replace



                    if pFault[process] == True:
                        fault[process] += 1
                        pf = "Fault"
                    else:
                        pf = "Hit"


                    # calculate the next reference for this process

                    r = rand(c)
                    c += 1

                    option = nextWord(r, process, cases, word, S)

                    if option == -1:
                        x = rand(c)
                        c += 1
                        nextOption[process] = (x + S) % S
                    else:
                        nextOption[process] = option


    for process in range(len(fault)):
        if eviction[process] != 0:
            avg = residencyTime[process]/eviction[process]
            print("Process ", process+1, "had", fault[process], "faults and ", avg, "average residency.")
        else:
            print("Process ", process+1, "had", fault[process], "faults.")
            print("With no evictions, the average residence is undefined.")
    if sum(eviction)!= 0:
        totalResidence = sum(residencyTime)/sum(eviction)
        print("The total number of faults is ", sum(fault), "and the overall average residency is ",totalResidence)
    else:
        print("The total number of faults is ", sum(fault),".")
        print("With no evictions, the overall average residence is undefined")



main()





