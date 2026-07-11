from database import get_connection, init_db

conn = get_connection()


#============================================
# 1.CRUD - CREATE
# ===========================================

def add_department(dept_name, location):

    conn.execute("INSERT INTO departments (dept_name, location) values (?, ?, ?)", (dept_name, location))
    conn.commit()
    conn.close()
    print(f"Added department {dept_name}")
    
def add_employee(name, email, salary, dept_id, manager_id):
    conn.execute("INSERT INTO employees (name, email, salary, dept_id, manager_id) values (?, ?, ?, ?, ?)", (name, email, salary, dept_id, manager_id,))
    conn.commit()
    conn.close()
    print(f"Added employee {name}")

#============================================
# 2.CRUD - READ
# ===========================================

def view_departments():
    rows = conn.execute("SELECT * FROM departments").fetchall()

    for r in rows:
        print(dict(r))
    
    return rows

def view_employees():
    rows = conn.execute("SELECT * FROM employees").fetchall()

    for r in rows:
        print(dict(r))
    
    return rows

def view_employee_details(emp_id):
    row = conn.execute("""
                            SELECT e.name AS employee_name,
                                    e.email,
                                    e.salary,
                                    d.dept_name,
                                    d.location,
                                    m.name AS manager_name
                                FROM Employees e
                                JOIN Departments d ON e.dept_id = d.dept_id
                                LEFT JOIN Employees m ON e.manager_id = m.emp_id
                                WHERE e.emp_id = ?;
                        """, (emp_id,)).fetchone()
    
    conn.commit()
    if row is None:
        print(f"No employee found with the employee id {emp_id}")
        return
    print(dict(row))
