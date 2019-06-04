import numpy as np
import MySQLdb


def main():
    rank = np.load("rank.npy")
    scores = np.load("scores.npy")
    connect = MySQLdb.connect(host='localhost', passwd='myakudo!' , user='root', db='journal', charset='utf8')
    cursor = connect.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS similality (
            id INT(11) NOT NULL AUTO_INCREMENT,
            rank1 INT(11),
            rank2 INT(11),
            rank3 INT(11),
            rank4 INT(11),
            rank5 INT(11),
            rank6 INT(11),
            rank7 INT(11),
            rank8 INT(11),
            rank9 INT(11),
            rank10 INT(11),
            score1 DOUBLE,
            score2 DOUBLE,
            score3 DOUBLE,
            score4 DOUBLE,
            score5 DOUBLE,
            score6 DOUBLE,
            score7 DOUBLE,
            score8 DOUBLE,
            score9 DOUBLE,
            score10 DOUBLE,
            PRIMARY KEY (id)
        )
        """
        )

    for i in range(len(rank)):
        sql = """
            insert into similality values(
                {0},
                {1[0]}, {1[1]}, {1[2]}, {1[3]}, {1[4]}, {1[5]}, {1[6]}, {1[7]}, {1[8]}, {1[9]}, 
                {2[0]}, {2[1]}, {2[2]}, {2[3]}, {2[4]}, {2[5]}, {2[6]}, {2[7]}, {2[8]}, {2[9]})
            """.format(i+1, rank[i], scores[i])

        cursor.execute(sql)
    
    connect.commit()

    cursor.close()
    connect.close() 

    print("finished to insert!")

if __name__ == "__main__":
    main()