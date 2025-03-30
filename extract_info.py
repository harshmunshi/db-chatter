import sqlite3

def query_database(query: str):
    """
    Execute a query on the personal_info database and return the results
    
    Args:
        query (str): SQL query to execute
        
    Returns:
        list: Results from the query
    """
    try:
        print("Query: ", query)
        # Connect to the database
        conn = sqlite3.connect('personal_info.db')
        cursor = conn.cursor()

        # Execute query and fetch results
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Close connection
        conn.close()
        
        return results
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

# query = input("Enter a query: ")
# print(query_database(query))