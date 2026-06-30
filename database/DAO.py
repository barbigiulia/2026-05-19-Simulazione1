from database.DB_connect import DBConnect
from model.cliente import Cliente


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def getCountries():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """  select distinct c.Country 
                    from customer c 
                    order by c.Country 
                    """
        cursor.execute(query)
        for row in cursor:
            results.append(row["Country"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNodes(country):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """  select distinct c.*
                    from customer c , invoice i 
                    where c.CustomerId =i.CustomerId 
                    and c.Country =%s
                        """
        cursor.execute(query,(country,))
        for row in cursor:
            results.append(Cliente(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getFatturato(country):
        conn = DBConnect.get_connection()
        results = {}  # serve un DIZIONARIO
        cursor = conn.cursor(dictionary=True)
        query = """  select i.CustomerId , sum(i.Total ) as fatturato
                    from customer c , invoice i 
                    where c.CustomerId = i.CustomerId 
                    and c.Country = %s
                    group by i.CustomerId
                            """
        cursor.execute(query, (country,))
        for row in cursor:
            results[row["CustomerId"]] = float(row["fatturato"])  # conversione !!

        # sum() in sql ritorna decimal.Decimal  --> devo convertirlo subito in float
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getCoppie(country):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """  select distinct  c1.CustomerId as c1 , c2.CustomerId as c2
                    from artist a1 , album al1, track t1, invoiceline i1, 
                    invoice in1, customer c1, artist a2 , album al2, track t2, invoiceline i2, 
                    invoice in2, customer c2
                    where in1.CustomerId != in2.CustomerId 
                    and a1.ArtistId =al1.ArtistId 
                    and al1.AlbumId = t1.AlbumId
                    and t1.TrackId =i1.TrackId 
                    and i1.InvoiceId =in1.InvoiceId 
                    and in1.CustomerId = c1.CustomerId 
                    and a2.ArtistId =al2.ArtistId 
                    and al2.AlbumId = t2.AlbumId
                    and t2.TrackId =i2.TrackId 
                    and i2.InvoiceId =in2.InvoiceId 
                    and in2.CustomerId = c2.CustomerId 
                    and a1.ArtistId = a2.ArtistId 
                    and c1.Country =%s
                    and c2.Country =%s
                    and c1.CustomerId < c2.CustomerId 
                            """
        cursor.execute(query, (country,country))
        for row in cursor:
            results.append((row["c1"], row["c2"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getArtistiPerCliente(country):
        """Ritorna una lista di tuple (CustomerId, ArtistId) -- una riga per ogni
           combinazione cliente-artista acquistato, nel paese indicato"""
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """ select distinct c.CustomerId, ar.ArtistId
                    from customer c, invoice i, invoiceline il, track t, album al, artist ar
                    where c.CustomerId = i.CustomerId
                    and i.InvoiceId = il.InvoiceId
                    and il.TrackId = t.TrackId
                    and t.AlbumId = al.AlbumId
                    and al.ArtistId = ar.ArtistId
                    and c.Country = %s
                """
        cursor.execute(query, (country,))
        for row in cursor:
            results.append((row["CustomerId"], row["ArtistId"]))

        cursor.close()
        conn.close()
        return results