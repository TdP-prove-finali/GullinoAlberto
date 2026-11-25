from database.DAO import DAO
print(DAO.getNumTransazioni(None, None))
print(len(DAO.getFrequenzeProdotti(None, None)))
coppie = DAO.getCoppie(None, None)
print(len(coppie), sum(n for _, _, n in coppie))
print(DAO.getNumTransazioni("morning", None))