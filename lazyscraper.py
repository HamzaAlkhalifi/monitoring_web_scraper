from curl_cffi.requests import Session, Response
import os
import json
import duckdb
from time import sleep

class Request:
    def __init__(self, URL: str, headers: dict | None , params: dict | None , 
                 proxies: dict | None, cookies: dict | None, impersonate: str) -> None:
        
        self.url = URL
        self.headers = headers
        self.params = params
        self.proxies = proxies
        self.cookies = cookies
        self.impersonate = impersonate
        
    def get(self) -> Response :
        with Session() as session:
            try:
                match self.cookies:
                
                    case cookies if cookies is not None: 
                        match self.proxies:
                            case proxies if proxies is not None:
                                self.response = session.get(
                                    self.url, 
                                    params=self.params, 
                                    headers=self.headers, 
                                    proxies=self.proxies,
                                    cookies=self.cookies,
                                    impersonate=self.impersonate
                                )
                            case None:
                                self.response = session.get(
                                    self.url, 
                                    params=self.params, 
                                    headers=self.headers,
                                    cookies=self.cookies,
                                    impersonate=self.impersonate
                                )
                    case None:
                        match self.proxies:
                            case proxies if proxies is not None:
                                if os.path.isfile("cookies.json"):
                                    with open("cookies.json", "r") as f:
                                        cookies = json.load(f)
                                        self.cookies = cookies

                                    self.response = session.get(
                                        self.url, 
                                        params=self.params, 
                                        headers=self.headers, 
                                        proxies=self.proxies,
                                        cookies= self.cookies,
                                        impersonate=self.impersonate
                                    )
                                else:
                                    self.response = session.get(
                                        self.url, 
                                        params=self.params, 
                                        headers=self.headers, 
                                        proxies=self.proxies,
                                        impersonate=self.impersonate
                                    )
                                    with open("cookies.json", "w") as f:
                                        json.dump(self.response.cookies.get_dict(), f, indent=4)

                            case None:
                                if os.path.isfile("cookies.json"):
                                    with open("cookies.json", "r") as f:
                                        cookies = json.load(f)
                                        self.cookies = cookies

                                    self.response = session.get(
                                        self.url, 
                                        params=self.params, 
                                        headers=self.headers, 
                                        cookies= self.cookies,
                                        impersonate=self.impersonate
                                    )
                                else:
                                    self.response = session.get(
                                        self.url, 
                                        params=self.params, 
                                        headers=self.headers, 
                                        impersonate=self.impersonate
                                    )
                                    with open("cookies.json", "w") as f:
                                        json.dump(self.response.cookies.get_dict(), f, indent=4)

            except Exception as e:
                raise Exception(f"Error:\n{e}") 


            print("""
                 ============================================================
                ====================== REQUEST INFO ==========================
                 ============================================================
                  """)
            print(f"url: {self.url}")
            print(f"headers: {self.headers}")
            print(f"params: {self.params}")
            print(f"proxies: {self.proxies}")
            print(f"cookies: {self.cookies}")
            print(f"stauts_code: {self.response.status_code}")
            print("""
                =============================================================
                =============================================================
                  """)
            print("\n"*3)
        return self.response
    


def export_json(data: list[dict], file_name: str) -> None:
    try:
        with open(file_name, "r") as f:
            old_data = json.load(f)
    except Exception as e:
        old_data = []
    old_data.extend(data)
    with open(file_name, "w") as f:
        json.dump(old_data, f, indent=4)    
    print("finished loading data")
    print("\n"*2)
            

def type_to_duckdb_type(value):
    if isinstance(value, int):
        return 'INTEGER'
    elif isinstance(value, float):
        return 'DOUBLE'
    else:
        return 'VARCHAR'

def export_duckdb(data: list[dict], file_name: str, table_name: str) -> None:
    try:
        with duckdb.connect(file_name) as db:
            columns= ",".join(f"{key} {type_to_duckdb_type(value)}" for key, value in data[0].items())
            db.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} ({columns})
                      """)

            placeholder= ",".join(["?" for _ in data[0].keys()])
            values= [tuple(value.values()) for value in data]
            db.executemany(f"""
                INSERT INTO {table_name}
                VALUES ({placeholder})
                       """, values)
            print(f"finished loading data")
    except Exception as e:
        raise Exception(f"Error:\n{e}")
        
