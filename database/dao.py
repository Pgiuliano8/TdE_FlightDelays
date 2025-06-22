from database.DB_connect import DBConnect
from model.airport import Airport
from model.archi import Arco


class DAO():

    @staticmethod
    def getNodes(n):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select a.*
                    from flights f, airports a 
                    where (f.ORIGIN_AIRPORT_ID=a.ID or f.DESTINATION_AIRPORT_ID=a.ID)
                    group by a.ID 
                    having count(distinct(f.AIRLINE_ID)) > %s"""

        cursor.execute(query, (n,))

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select a.ID as a1, a2.ID as a2, count(f.ID) as peso
                    from airports a, airports a2, flights f 
                    where (f.ORIGIN_AIRPORT_ID=a.ID and f.DESTINATION_AIRPORT_ID=a2.ID)
                    or (f.ORIGIN_AIRPORT_ID=a2.ID and f.DESTINATION_AIRPORT_ID=a2.ID)
                    group by a.ID, a2.ID """

        cursor.execute(query)

        for row in cursor:
            if row['a1'] in idMap.keys() and row['a2'] in idMap.keys():
                result.append(Arco(idMap[row['a1']], idMap[row['a2']], row['peso']))

        cursor.close()
        conn.close()
        return result

    if __name__ == '__main__':
        print(getNodes(10))