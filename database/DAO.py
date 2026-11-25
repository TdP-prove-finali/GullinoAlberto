from database.DB_connect import DBConnect


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
