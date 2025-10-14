import modules.objectLib as ol
    
if __name__ == "__main__":
    db=ol.dbSelfHost()

    id = ol.createTask("test","test",db)
    
    result = ol.getAll(db)
    for row in result:
        print(row)
