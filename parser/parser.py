from urllib.request import urlopen
import json
import sqlite3 as sq


async def refill():
    base = sq.connect('../main_scripts/test2.db')
    cur = base.cursor()
    cur.execute("DROP TABLE IF EXISTS TWO_New")
    cur.execute("CREATE TABLE IF NOT EXISTS TWO_New ("
                "CITY           TEXT    NOT NULL,"
                "UNIVERSITY     TEXT    NOT NULL,"
                "NAME           TEXT    NOT NULL,"
                "STATUS         TEXT    NOT NULL,"
                "NUMBER         INT     NOT NULL,"
                "PRIOITY        INT     NOT NULL,"
                "SCORE          REAL    NOT NULL,"
                "DEGREE         TEXT    NOT NULL,"
                "SPECIALITY     TEXT    NOT NULL,"
                "FACULTY        TEXT    NOT NULL,"
                "PROGRAM        TEXT    NOT NULL,"
                "YEAR           INT     NOT NULL);")

    for i in range(281211, 281220):
        try:
            url = urlopen("https://abit-help.com.ua/api/speciality/" + str(i))

            data = json.loads(url.read())
            if len(data['entrants']) < 1:
                print(f'SKIP {i}')
                continue
            print(i)

            specialityNumber = data["specialityNumber"]

            lst_data = {'city': data["university"]["region"]["name"], 'university': data["university"]["name"],
                        'degree': data["studyDegree"], 'speciality': specialityNumber + " " + data["name"],
                        'faculty': data["facultyName"], 'program': data["educationalProgram"]}

            for k in lst_data.keys():
                if not lst_data[k]:
                    lst_data[k] = 'Невідомо'

            for j in range(0, len(data['entrants'])):
                name = data["entrants"][j]["name"].lower()
                status = data["entrants"][j]["status"]
                number = data["entrants"][j]["number"]
                prioity = data["entrants"][j]["prioity"]
                score = data["entrants"][j]["score"]
                year = data["entrants"][j]["year"]

                cur.execute("INSERT INTO TWO_New (CITY,UNIVERSITY,NAME,STATUS,NUMBER,PRIOITY,SCORE,DEGREE, SPECIALITY, FACULTY, PROGRAM, YEAR) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (lst_data['city'], lst_data['university'], name, status, int(number), int(prioity), score,
                             lst_data['degree'], lst_data['speciality'], lst_data['faculty'], lst_data['program'], int(year)))
                base.commit()
        except Exception as e:
            print(e)
            continue

    cur.execute("DROP TABLE IF EXISTS TWO;")
    cur.execute("CREATE TABLE TWO AS SELECT * FROM TWO_New;")
    cur.execute("DROP TABLE TWO_New;")
