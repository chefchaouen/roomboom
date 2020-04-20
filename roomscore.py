import pymysql, re, datetime

db = pymysql.connect(host="localhost", user="root", passwd="yip", db="suumo", charset="utf8")
c = db.cursor()

fields_to_score = ['floor_area', 'room_age', 'walk_station', 'ward', 'bldg_mat', 'tky_dist']

def get_score(field):
    try: 
        c.execute("ALTER TABLE listings DROP COLUMN {}_score;".format(field))
    except:
        pass
    if field == "ward":
        c.execute("ALTER TABLE listings ADD COLUMN ward_score FLOAT GENERATED ALWAYS AS (CASE ward WHEN '千代田' THEN 1 WHEN '中央' THEN 0.8 WHEN '港' THEN 0.8 WHEN '新宿' THEN 0.8 WHEN '文京' THEN 0.4 WHEN '台東' THEN 0.4 WHEN '墨田' THEN 0.4 WHEN '江東' THEN 0.4 WHEN '品川' THEN 0.6 WHEN '目黒' THEN 0.8 WHEN '大田' THEN 0.4 WHEN '世田谷' THEN 0.8 WHEN '渋谷' THEN 0.8 WHEN '中野' THEN 0.6 WHEN '杉並' THEN 0.6 WHEN '豊島' THEN 0.4 WHEN '北' THEN 0.2 WHEN '荒川' THEN 0.2 WHEN '板橋' THEN 0.2 WHEN '練馬' THEN 0.2 WHEN '足立' THEN 0.2 WHEN '葛飾' THEN 0.2 WHEN '江戸川' THEN 0.2 ELSE 0 END);")
    elif field == 'bldg_mat':
        c.execute("ALTER TABLE listings ADD COLUMN bldg_mat_score FLOAT GENERATED ALWAYS AS (CASE bldg_mat WHEN '鉄筋コン' THEN 1 WHEN '鉄骨鉄筋' THEN 1 WHEN '鉄骨プレ' THEN 1 WHEN 'プレコン' THEN 1 WHEN 'ブロック' THEN 1 WHEN '鉄骨' THEN 0.7 WHEN '軽量鉄骨' THEN 0.5 WHEN '気泡コン' THEN 0.5 WHEN '木造' THEN 0.3 WHEN 'その他' THEN 0.3 END);")
    else:
        c.execute("SELECT AVG({}) FROM listings;".format(field))
        field_avg = c.fetchone()[0]
        c.execute("SELECT STDDEV({}) FROM listings;".format(field))
        field_stddev = c.fetchone()[0]
        #print("The average {} is {} and the standard deviation is {}.".format(field, field_avg, field_stddev))
        add_field_score_query = "ALTER TABLE listings ADD COLUMN {}_score FLOAT GENERATED ALWAYS AS (({} - {}) / {});".format(field, field, field_avg, field_stddev)
        #print(add_field_score_query)
        c.execute(add_field_score_query)

def main():    
    try:
        c.execute("ALTER TABLE listings DROP COLUMN norm_room_score;")
    except:
        pass
    try:
        c.execute("ALTER TABLE listings DROP COLUMN room_score;")
    except:
        pass
    for i in fields_to_score:
        get_score(i)
    c.execute("ALTER TABLE listings ADD COLUMN room_score FLOAT GENERATED ALWAYS AS ({}_score - {}_score - {}_score + {}_score + {}_score - {}_score);".format(*fields_to_score))
    c.execute("SELECT MIN(room_score) FROM listings;")
    min_room_score = c.fetchone()[0]
    c.execute("SELECT MAX(room_score) FROM listings;")
    max_room_score = c.fetchone()[0]
    c.execute("ALTER TABLE listings ADD COLUMN norm_room_score FLOAT GENERATED ALWAYS AS (((room_score - {})/({} - {}))*100);".format(min_room_score, max_room_score, min_room_score))

if __name__=="__main__":
    main()
