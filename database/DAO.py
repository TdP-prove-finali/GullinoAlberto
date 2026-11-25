from database.DB_connect import DBConnect
from model.prodotto import Prodotto

# Filtro opzionale: se il parametro e' None non filtra.
# Parametri in quest'ordine: (fascia, fascia, giorno, giorno)
FILTRO = """
          and (%s is null or t.fascia_giornata = %s)
          and (%s is null or t.tipo_giorno = %s)
          """

class DAO():

    @staticmethod
    def getAllProdotti():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select p.nome
                from prodotti p
                order by p.nome
                """

        cursor.execute(query)

        for row in cursor:
            results.append(row["nome"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getProdottiVendibili():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                select p.id_prodotto, p.nome, p.categoria,
                       s.prezzo, s.costo, s.peso_g, s.priorita
                from prodotti p, prodottisimulati s
                where p.id_prodotto = s.id_prodotto
                  and p.vendibile_online
                order by p.nome
                """
        cursor.execute(query)
        results = []
        for row in cursor:
            results.append(Prodotto(row["id_prodotto"], row["nome"], row["categoria"],
                                    float(row["prezzo"]), float(row["costo"]),
                                    int(row["peso_g"]), float(row["priorita"])))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNumTransazioni(fascia, giorno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                select count(distinct d.id_transazione) as n
                from dettagliordine d, transazioni t, prodotti p
                where d.id_transazione = t.id_transazione
                  and d.id_prodotto = p.id_prodotto
                  and p.vendibile_online
                """ + FILTRO
        cursor.execute(query, (fascia, fascia, giorno, giorno))
        n = cursor.fetchone()["n"]
        cursor.close()
        conn.close()
        return int(n)

    @staticmethod
    def getFrequenzeProdotti(fascia, giorno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                select d.id_prodotto, count(*) as n
                from dettagliordine d, transazioni t, prodotti p
                where d.id_transazione = t.id_transazione
                  and d.id_prodotto = p.id_prodotto
                  and p.vendibile_online
                """ + FILTRO + """
                group by d.id_prodotto
                """
        cursor.execute(query, (fascia, fascia, giorno, giorno))
        results = {}
        for row in cursor:
            results[row["id_prodotto"]] = int(row["n"])
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getCoppie(fascia, giorno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                select d1.id_prodotto as p1, d2.id_prodotto as p2, count(*) as n
                from dettagliordine d1, dettagliordine d2, transazioni t,
                     prodotti pa, prodotti pb
                where d1.id_transazione = d2.id_transazione
                  and d1.id_prodotto < d2.id_prodotto
                  and d1.id_transazione = t.id_transazione
                  and pa.id_prodotto = d1.id_prodotto and pa.vendibile_online
                  and pb.id_prodotto = d2.id_prodotto and pb.vendibile_online
                """ + FILTRO + """
                group by d1.id_prodotto, d2.id_prodotto
                """
        cursor.execute(query, (fascia, fascia, giorno, giorno))
        results = []
        for row in cursor:
            results.append((row["p1"], row["p2"], int(row["n"])))
        cursor.close()
        conn.close()
        return results
