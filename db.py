import sqlite3
import requests

class DataBase:
    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

        self.cur.execute('''
            create table if not exists countries(
                id INTEGER NOT NULL PRIMARY KEY,
                country_id integer unique,
                name text unique,
                iso3 text unique,
                iso2 text unique,
                lat real,
                lon real
            )
        ''')

    def fetch(self) -> list:
        self.cur.execute('select * from countries')

        return self.cur.fetchall()

    def insert(self, country_id: int, name: str, iso3: str, iso2: str, lat: float, lon: float) -> None:
        self.cur.execute('''
            insert into countries values (?, ?,?,?,?,?,?)
        ''', (None, country_id, name, iso3, iso2, lat, lon))

        self.conn.commit()

    def retrive(self, value: str) -> None:
        _name = self.cur.execute(f'select * from countries where name like "{value}%"').fetchone()
        _iso3 = self.cur.execute(f'select * from countries where iso3 like "{value}%"').fetchone()
        _iso2 = self.cur.execute(f'select * from countries where iso2 like "{value}%"').fetchone()

        if _name:
            return _name
        elif _iso3:
            return _iso3
        else:
            return _iso2


    @staticmethod
    def _get_data() -> dict:
        url = 'https://disease.sh/v3/covid-19/countries'
        _res = requests.get('https://disease.sh/v3/covid-19/countries')

        if _res.status_code:
            return _res.json()

    def populate(self) -> None:
        _ = input('Sure to repopulate the table >>> ')
        if _ in ['y', 'Y', 'yes' 'Yes']:
            self.cur.execute('delete from countries')
            self.conn.commit()

            _data = self._get_data()
            if _data:
                for c in _data:
                    self.cur.execute('insert into countries values (?, ?,?,?,?,?,?)', 
                            (None, c['countryInfo']['_id'], c['country'], c['countryInfo']['iso3'], c['countryInfo']['iso2'],
                            c['countryInfo']['lat'],c['countryInfo']['long']))

                self.conn.commit()

    def __del__(self):
        self.conn.close()

if __name__ == '__main__':
    db = DataBase('db.sqlite3')
    print(db.retrive('E'))
    db.populate()
