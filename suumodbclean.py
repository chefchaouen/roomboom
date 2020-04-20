import pymysql
from datetime import date
from collections import Counter

db = pymysql.connect(host="localhost", user="root", passwd="yip", db="suumo", charset="utf8", autocommit=True)
c = db.cursor()
theday = date.today()

def main():
    c.execute("DELETE FROM listings WHERE walk_station = 0;")
    c.execute("DELETE FROM listings WHERE ward = '';")
    delete_dupes()
    del_floor_area_too_high()
    add_station_table()
    add_station_data()
    c.close()

def delete_dupes():
    dupes_query = "SELECT url FROM listings WHERE date_added = '{}';".format(theday)
    c.execute(dupes_query)
    db_urls = [item[0] for item in list(c.fetchall())]
    dupe_db_urls = [k for k, v in Counter(db_urls).items() if v > 1]
    print(len(dupe_db_urls))
    
    for url in dupe_db_urls:
        del_dupe_query = "DELETE FROM listings WHERE url = '{}';".format(url)
        print(dupe_db_urls.index(url))
        c.execute(del_dupe_query)
        db.commit()

def del_floor_area_too_high():
    floor_area_too_high_query = "DELETE FROM listings WHERE (floor_area/(rent + other_monthly_fees))*10000 > 15;"
    c.execute(floor_area_too_high_query)

def add_station_table():
    drop_query = "DROP TABLE IF EXISTS stations;"
    c.execute(drop_query)
    create_station_table_query = "CREATE TABLE stations SELECT DISTINCT station FROM listings WHERE station <> '';"
    c.execute(create_station_table_query)
    fields = ["avg_rent_other_monthly_fees", "avg_floor_area", "avg_room_age", "avg_walk_station", "avg_room_score", "avg_norm_room_score"]
    for field in fields:
        query = "ALTER TABLE stations ADD {} FLOAT(9,2);".format(field)
        c.execute(query)

def add_station_data():
    get_stations_query = "SELECT station from stations;"
    c.execute(get_stations_query)
    stations = [item[0] for item in list(c.fetchall())]
    fields = {
            "rent + other_monthly_fees":"avg_rent_other_monthly_fees",
            "floor_area":"avg_floor_area",
            "room_age":"avg_room_age",
            "walk_station":"avg_walk_station",
            "room_score":"avg_room_score",
            "norm_room_score":"avg_norm_room_score"
            }
    for station in stations:
        for field, avg_field in fields.items():
            stat_avg_query = "SELECT AVG({}) FROM listings WHERE station='{}';".format(field, station)
            c.execute(stat_avg_query)
            avg_value = round(c.fetchone()[0],2)
            insert_avg_value_query = "UPDATE stations SET {}={} where station='{}';".format(avg_field, avg_value, station)
            print(insert_avg_value_query)
            c.execute(insert_avg_value_query)
if __name__=="__main__":
    main()
