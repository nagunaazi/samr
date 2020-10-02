import cx_Oracle

connect_string = "DBDW/G3dFks5$e@DBDW"


def fetchOracle():
    cur = None
    con = None
    try:

        print("s1")
        con = cx_Oracle.connect(connect_string)
        print(con)
        if con != None:
            print("Orecle connection version: "+ con.version)
        else:
            print("Oracle connection not done!")
            print(con)

        cur = con.cursor()

        cur.execute("select * from SAPDBC.ZVT_PORTAL_EXBP@SAPPRD")
        dst = cur.fetchall()

        # return dst
        print(dst)
    except Exception  as e:
        print(e)
    except cx_Oracle.DatabaseError as dberror:
        if con:
            con.rollback()
            print(dberror)
            return []
    finally:
        if cur:
            cur.close()
        if con:
            con.close()



print(fetchOracle())