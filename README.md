## Demand Paging 
Anastasia Riawan Soenjoto

Simulates demand paging in Python3

Purpose: To simulate demand paging and see how the number of page faults depends on page size, program size, replacement algorithm, and job mix (job mix is defined below and includes locality and multiprogramming level).

The program will take in 6 command line arguments (5 positive integers and a string) , the machine size in words, the page size in words, the size of each process, the "job mix" which determines A, B, and C, the number of references for each process and the replacement algorithm (FIFO, RANDOM, or LRU). Round robin scheduling with quantum q=3 is used. 

### Sample input 
10 10 20 1 10 lru 0

20 10 10 2 10 random 0

20 10 10 2 10 fifo 0
