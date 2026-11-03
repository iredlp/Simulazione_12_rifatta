from database.DB_connect import DBConnect
from model.attore import Attore


class DAO():
    @staticmethod
    def getAllRange():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct avg_rating 
                       from ratings r 
                       order by r.avg_rating """

        cursor.execute(query)

        for row in cursor:
            results.append(row["avg_rating"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(voto1, voto2):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """  select distinct n.*
                        from names n, movie m,role_mapping rm, ratings r 
                        where n.date_of_birth is not null and n.date_of_birth <= CURDATE() and n.id =rm.name_id 
                        and rm.category IN ('actor', 'actress')
                        and rm.movie_id =m.id and m.id =r.movie_id 
                        and r.avg_rating between %s and %s"""
            cursor.execute(query, (voto1, voto2))

            for row in cursor:
                result.append(Attore(**row))

            cursor.close()
            cnx.close()
            return result

    @staticmethod
    def getFilmPerAttori(idA, voto1, voto2):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct m.id
                    from names n, movie m ,ratings r ,role_mapping rm 
                    where n.id=%s and r.avg_rating between %s and %s
                    and rm.category IN ('actor', 'actress') and m.worlwide_gross_income is not null
                    and m.id =r.movie_id and rm.name_id =n.id and rm.movie_id =m.id  """

        cursor.execute(query, (idA, voto1, voto2))
        for row in cursor:
            results.append(row["id"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getIncassiPerFilm(idA):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select  COALESCE(
        CAST(REPLACE( REPLACE(REPLACE(m.worlwide_gross_income, '$', ''),  ' ', '' ), 
        ',', '' ) AS DECIMAL(15,2)), 0)   as incasso
            from movie m 
            where m.id=%s  """

        cursor.execute(query, (idA,))
        for row in cursor:
            results.append(row["incasso"])

        cursor.close()
        conn.close()
        return results