
import sqlite3 as sql
from database import get_connection, init_db

conn = get_connection()


#============================================
# 1.CRUD - CREATE
# ===========================================

def add_department(dept_name, location):

    conn.execute("INSERT INTO departments (dept_name, location) values (?, ?)", (dept_name, location))
    conn.commit()
   
    print(f"Added department {dept_name}")
    
def add_employee(name, email, salary, dept_id, manager_id):
    conn.execute("INSERT INTO employees (name, email, salary, dept_id, manager_id) values (?, ?, ?, ?, ?)", (name, email, salary, dept_id, manager_id,))
    conn.commit()
    
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

#============================================
# 3.CRUD - UPDATE
# ===========================================

def update_emp_dept(emp_id, new_dept_id):
    cursor = conn.execute("UPDATE employees SET dept_id = ? WHERE emp_id = ?", (new_dept_id, emp_id,))
    conn.commit()
    if cursor.rowcount == 0:
        print(f"No employee found with the id {emp_id}")
    else:
        print(f"Updated employee {emp_id} department to {new_dept_id}")


def update_emp_manager(emp_id, new_manager_id):
    if new_manager_id == emp_id:
        print(f"Cannot set employee {emp_id} as their own manager")
        return
    
    cursor = conn.execute("UPDATE employees SET manager_id = ? WHERE emp_id = ?", (new_manager_id, emp_id,))
    conn.commit()
    if(cursor.rowcount == 0):
        print(f"No employee found with the id {emp_id}")
    else:
        print(f"Updated employee {emp_id} manager to {new_manager_id}")

def update_emp_salary(emp_id, new_salary):
    cursor = conn.execute("UPDATE employees SET salary = ? WHERE emp_id = ?",(new_salary, emp_id,))
    conn.commit()
    if(cursor.rowcount == 0):
        print(f"No employee found with the id {emp_id}")
    else:
        print(f"Updated the employee {emp_id} salary to {new_salary}")

#============================================
# 4.CRUD - DELETE
# ===========================================

def delete_department(dept_id):
    try:
        cursor = conn.execute("DELETE FROM Departments WHERE dept_id = ?", (dept_id,))
        conn.commit()
        if cursor.rowcount == 0:
            print(f"No department found with id {dept_id}")
        else:
            print(f"Department {dept_id} deleted successfully")
    except sql.IntegrityError:
        print(f"Cannot delete department {dept_id} -- employees are still assigned to it. "
              f"Reassign or remove them first.")
    
def delete_employee(emp_id):
   
    conn.execute("UPDATE Employees SET manager_id = NULL WHERE manager_id = ?", (emp_id,))
    conn.commit()

    
    cursor = conn.execute("DELETE FROM Employees WHERE emp_id = ?", (emp_id,))
    conn.commit()

    if cursor.rowcount == 0:
        print(f"No employee found with id {emp_id}")
    else:
        print(f"Employee {emp_id} deleted (any direct reports reassigned to no manager)")

#============================================
# 5. Queries
# ===========================================

def query_employee_manager_pairs():
    return conn.execute("""
        SELECT e.name AS employee, m.name AS manager
        FROM Employees e
        LEFT JOIN Employees m ON e.manager_id = m.emp_id
        ORDER BY e.name
    """).fetchall()


def query_employees_no_manager():
    return conn.execute("""
        SELECT emp_id, name
        FROM Employees
        WHERE manager_id IS NULL
        ORDER BY name
    """).fetchall()


def query_direct_report_counts():
    return conn.execute("""
        SELECT m.name AS manager, COUNT(e.emp_id) AS direct_reports
        FROM Employees m
        JOIN Employees e ON e.manager_id = m.emp_id
        GROUP BY m.emp_id
        ORDER BY direct_reports DESC
    """).fetchall()


def query_dept_headcount_avg_salary():
    return conn.execute("""
        SELECT d.dept_name,
               COUNT(e.emp_id) AS headcount,
               ROUND(AVG(e.salary), 2) AS avg_salary
        FROM Departments d
        LEFT JOIN Employees e ON e.dept_id = d.dept_id
        GROUP BY d.dept_id
        ORDER BY headcount DESC
    """).fetchall()


def query_employees_above_manager_salary():
    return conn.execute("""
        SELECT e.name AS employee, e.salary AS employee_salary,
               m.name AS manager, m.salary AS manager_salary
        FROM Employees e
        JOIN Employees m ON e.manager_id = m.emp_id
        WHERE e.salary > m.salary
    """).fetchall()


def query_highest_paid_per_dept():
    return conn.execute("""
        SELECT d.dept_name, e.name AS employee, e.salary
        FROM Employees e
        JOIN Departments d ON e.dept_id = d.dept_id
        WHERE e.salary = (
            SELECT MAX(e2.salary)
            FROM Employees e2
            WHERE e2.dept_id = e.dept_id
        )
        ORDER BY d.dept_name
    """).fetchall()

#============================================
# 6. MENU / MAIN
# ===========================================

def menu():
    while True:
        print(
            """
==== Employee Management System ====
1.  Add department
2.  Add employee
3.  View all departments
4.  View all employees
5.  View a single employee's full details
6.  Update an employee's department
7.  Update an employee's manager
8.  Update an employee's salary
9.  Delete a department
10. Delete an employee
11. Report: employee-manager pairs (self-join)
12. Report: employees with no manager
13. Report: direct report count per manager
14. Report: department headcount + average salary
15. Report: employees earning more than their manager
16. Report: highest-paid employee per department
0.  Exit
"""
        )
        choice = input("Choose an option: ").strip()
 
        if choice == "1":
            add_department(input("Department name: "), input("Location: "))
 
        elif choice == "2":
            name = input("Name: ")
            email = input("Email: ")
            salary = float(input("Salary: "))
            dept_id = int(input("Department ID: "))
            manager_input = input("Manager ID (leave blank if none): ").strip()
            manager_id = int(manager_input) if manager_input else None
            add_employee(name, email, salary, dept_id, manager_id)
 
        elif choice == "3":
            view_departments()
 
        elif choice == "4":
            view_employees()
 
        elif choice == "5":
            view_employee_details(int(input("Employee ID: ")))
 
        elif choice == "6":
            update_emp_dept(int(input("Employee ID: ")), int(input("New department ID: ")))
 
        elif choice == "7":
            manager_input = input("New manager ID (leave blank for none): ").strip()
            new_manager_id = int(manager_input) if manager_input else None
            update_emp_manager(int(input("Employee ID: ")), new_manager_id)
 
        elif choice == "8":
            update_emp_salary(int(input("Employee ID: ")), float(input("New salary: ")))
 
        elif choice == "9":
            delete_department(int(input("Department ID: ")))
 
        elif choice == "10":
            delete_employee(int(input("Employee ID: ")))
 
        elif choice == "11":
            print("\n-- Employee / Manager pairs --")
            for r in query_employee_manager_pairs():
                print(dict(r))
 
        elif choice == "12":
            print("\n-- Employees with no manager --")
            for r in query_employees_no_manager():
                print(dict(r))
 
        elif choice == "13":
            print("\n-- Direct report count per manager --")
            for r in query_direct_report_counts():
                print(dict(r))
 
        elif choice == "14":
            print("\n-- Department headcount + average salary --")
            for r in query_dept_headcount_avg_salary():
                print(dict(r))
 
        elif choice == "15":
            print("\n-- Employees earning more than their manager --")
            for r in query_employees_above_manager_salary():
                print(dict(r))
 
        elif choice == "16":
            print("\n-- Highest-paid employee per department --")
            for r in query_highest_paid_per_dept():
                print(dict(r))
 
        elif choice == "0":
            print("Exiting. Goodbye!")
            break
 
        else:
            print("Invalid option, try again.")
 
 
def main():
    init_db()
    menu()
 
 
if __name__ == "__main__":
    main()