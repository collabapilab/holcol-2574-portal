from flaskr.sql.base import create_connection, dict_factory 
from flaskr.sql.base import sql_fetch_all, sql_fetch_dict_all
from flaskr.db_tools import clean_sql_tables, build_sql_tables, LOCATIONS_TABLE

def locations_all_locations_sql():
    query = f"""
            SELECT * 
            from `locations`
            """
    return sql_fetch_dict_all(query)


def locations_location_names_sql():
    conn = create_connection()
    query = f"""
            SELECT distinct name 
            from `locations`
            """
    result = sql_fetch_all(conn, query)
    return [x[0] for x in result]


def locations_get_location_sql(name):
    query = f"""
            SELECT * 
            from `locations`
            where name='{name}'
            """
    return sql_fetch_dict_all(query)



def customer_resolved_sql(id, years):
    conn = create_connection()
    query = f"""
            SELECT * 
            from `defects` as d
            inner join `customer_defects` as c  on c.id = d.id
            WHERE ( Customer_id = '{id}' AND 
                    ({sql_status_gen("resolved")}) AND
                    ( Submitted_date >= date('now','-{years} year') ) 
                   )
            """
    return sql_fetch_dict_all(conn, query)

def customer_closed_sql(id, years):
    conn = create_connection()
    query = f"""
            SELECT * 
            from `defects` as d
            inner join `customer_defects` as c  on c.id = d.id
            WHERE ( Customer_id = '{id}' AND 
            ({sql_status_gen("closed")}) AND
            ( Submitted_date >= date('now','-{years} year') )  
            )"""
    return sql_fetch_dict_all(conn, query)

def customer_active_sql(id, years):
    conn = create_connection()
    query = f"""
            SELECT * 
            from `defects` as d
            inner join `customer_defects` as c  on c.id = d.id
            WHERE ( Customer_id = '{id}' and 
                  ({sql_status_gen("active")}) AND
                  ( Submitted_date >= date('now','-{years} year') )  
                  )
            """
    return sql_fetch_dict_all(conn, query)

def customer_state_sql(id, state, years):
    conn = create_connection()
    query = f"""
            SELECT *
            from `defects` as d
            inner join `customer_defects` as c  on c.id = d.id
            WHERE ( Customer_id = '{id}' and 
                  ( Status = '{state}' ') AND
                  ( Submitted_date >= date('now','-{years} year') )  
                  )
            """
    return sql_fetch_dict_all(conn, query)


def customer_statecount_sql(id, years):
    conn = create_connection()
    query = f"""
            SELECT Status,COUNT(Status)
            from `defects` as d
            inner join `customer_defects` as c  on c.id = d.id
            WHERE Customer_id = "{id}" AND 
            ( Submitted_date >= date('now','-{years} year') ) 
            GROUP BY Status
            ORDER BY Status DESC"""
    return sql_fetch_all(conn, query)

def customer_submit_by_month_sql( id, years):
    conn = create_connection()
    query = f"""
        SELECT strftime('%Y-%m',Submitted_date) as Month,COUNT(d.id) as Total 
        from `defects` as d
        inner join `customer_defects` as c  on c.id = d.id
        WHERE Submitted_date >= date('now','-{years} year') AND 
        ( Customer_id = '{id}')
        GROUP BY strftime('%Y-%m',Submitted_date)
        ORDER BY Submitted_date ASC
        """
    return sql_fetch_all(conn, query)



def customer_srcountmonth_sql(id, years):
    conn = create_connection()
    query = f"""
        SELECT strftime('%Y-%m',Submitted_date) as Month,SUM(Ticket_count)
        from `defects` as d
        inner join `customer_defects` as c  on c.id = d.id
        WHERE Submitted_date >= date('now','-{int(years)} year') AND (Customer_id = '{id}')
        GROUP BY strftime('%Y-%m',Submitted_date)
        ORDER by Submitted_date ASC
        """
    return sql_fetch_all(conn, query)

def customer_product_count_sql(id, year,limit):
    conn = create_connection()
    query = f"""
        SELECT Product,COUNT(d.id) as Total
        from `defects` as d
        inner join `customer_defects` as c  on c.id = d.id
        WHERE Submitted_date >= date('now','-{int(year)} year') AND (Customer_id='{id}')
        GROUP BY Product
        ORDER BY Total DESC
        {"" if limit == 0 else "LIMIT "+limit }
        """
    return sql_fetch_all(conn, query)

def customer_component_count_sql(id, year,limit):
    conn = create_connection()
    query = f"""
        SELECT Component,COUNT(d.id) as Total 
        from `defects` as d
        inner join `customer_defects` as c  on c.id = d.id
        WHERE Submitted_date >= date('now','-{int(year)} year') AND (Customer_id='{id}')
        GROUP BY Component 
        ORDER BY Total DESC
        {"" if limit == 0 else "LIMIT "+limit }
        """
    return sql_fetch_all(conn, query)

def getAll_sql():
    conn = create_connection()
    cur = conn.cursor()
    query = """
        SELECT distinct Customer_id from customer_defects
        """
    cur.execute(query)
    return cur.fetchall()

def results_update_schema_locations_sql():

    clean_sql_tables('locations')
    build_sql_tables(LOCATIONS_TABLE)
    return '1'