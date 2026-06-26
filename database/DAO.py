from database.DB_connect import DBConnect
from model.artista import Artista


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def getGeneri():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """ select g.GenreId , g.Name 
                    from genre g 
                    """
        cursor.execute(query)
        for row in cursor:
            results.append((row["GenreId"], row["Name"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getArtisti(genereID):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """ select  distinct a2.*
                    from artist a2 , album a , track t 
                    where a2.ArtistId =a.ArtistId 
                    and a.AlbumId =t.AlbumId
                    and t.GenreId = %s
                       """
        cursor.execute(query,(genereID,))
        for row in cursor:
            results.append(Artista(**row))

        cursor.close()
        conn.close()
        return results



    @staticmethod
    def getNodes(genereID):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """ select distinct a.ArtistId , a.Name 
                    from artist a , album a2 , track t 
                    where a.ArtistId =a2.ArtistId 
                    and a2.AlbumId =t.AlbumId 
                    and t.GenreId = %s
                        """
        cursor.execute(query,(genereID,))
        for row in cursor:
            results.append(Artista(**row))

        cursor.close()
        conn.close()
        return results

    @ staticmethod

    def getAcquistiClienti(genereID):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT  i2.CustomerId, a.ArtistId
                    FROM album a, track t, invoiceline i, invoice i2, track t2, album a2
                    WHERE a.AlbumId = t.AlbumId
                    AND t.TrackId = i.TrackId
                    AND i.InvoiceId = i2.InvoiceId
                    AND a.ArtistId = a2.ArtistId
                    AND a2.AlbumId = t2.AlbumId
                    AND t2.GenreId = %s
                    """
        cursor.execute(query, (genereID,))
        for row in cursor:
            results.append((row["CustomerId"], row["ArtistId"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getPopolarita():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """ select  a.ArtistId , sum(i.Quantity ) as popolarita
                    from album a , track t , invoiceline i 
                    where a.AlbumId =t.AlbumId
                    and t.TrackId =i.TrackId 
                    group by a.ArtistId
                                """
        cursor.execute(query)
        for row in cursor:
            results.append((row["ArtistId"], row["popolarita"]))
        cursor.close()
        conn.close()
        return results

