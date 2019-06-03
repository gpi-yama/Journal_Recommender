import numpy as np
import MySQLdb

def main():
    rank = np.load("rank.npy").astype("int16")
    print(rank.shape)
    print(rank[1, 9])
    connect = MySQLdb.connect(host='localhost', passwd='myakudo!' , user='root', db='journal', charset='utf8')
    cursor = connect.cursor()
    for i in range(len(rank)):
        print(i)
        sql = "insert into similality values({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10})".format(
            i+1, rank[i, 0], rank[i, 1], rank[i, 2], rank[i, 3],
            rank[i, 4], rank[i, 5], rank[i, 6],
            rank[i, 7], rank[i, 8], rank[i, 9]
        )

        cursor.execute(sql)
    
    connect.commit()

    cursor.close()
    connect.close() 

if __name__ == "__main__":
    main()