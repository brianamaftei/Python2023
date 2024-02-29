class Employee:
    def __init__(self, name, ID):
        self.name = name
        self.ID = ID
        self.salary = 0
        self.schedule = {}
        self.tasks = {}

    def add_task(self, task):
        self.tasks[task] = False
        print(f"Task {task} added to the list.")

    def get_tasks(self):
        return self.tasks

    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.pop(task)
            print(f"Task {task} removed from the list.")
        else:
            print("Task not found in the list.")

    def mark_task(self, task):
        if task in self.tasks:
            self.tasks[task] = True
            print(f"Task {task} marked as done.")
        else:
            print("Task not found in the list.")

    def set_tasks(self, tasks):
        self.tasks = tasks

    def get_name(self):
        return self.name

    def get_salary(self):
        return self.salary

    def get_ID(self):
        return self.ID

    def get_schedule(self):
        return self.schedule

    def set_name(self, name):
        self.name = name

    def set_salary(self, salary):
        self.salary = salary

    def set_ID(self, ID):
        self.ID = ID

    def set_schedule(self, schedule):
        self.schedule = schedule

    def modify_schedule(self, day, hours):
        if day in self.schedule:
            self.schedule[day] = hours
            print(f"Schedule for {day} modified to {hours}.")
        else:
            print(f"Day {day} not found in the schedule.")

    def give_raise(self, amount):
        self.salary += amount

    def __str__(self):
        result = "Info:\n"
        all_attributes = vars(self)
        for attribute_name, attribute_value in all_attributes.items():
            if isinstance(attribute_value, list) and all(isinstance(item, Employee) for item in attribute_value):
                result += f"{attribute_name} is {list(employee.name for employee in attribute_value)}\n"
            else:
                result += f"{attribute_name} is {attribute_value}\n"
        return result


class Manager(Employee):
    def __init__(self, name, ID, department):
        super().__init__(name, ID)
        self.department = department
        self.team = []

    def get_department(self):
        return self.department

    def set_department(self, department):
        self.department = department

    def add_employee(self, employee):
        try:
            if isinstance(employee, Employee):
                self.team.append(employee)
                print(f"Employee {employee.name} added to the team.")
            else:
                raise TypeError("Invalid employee object. Please provide an instance of the Employee class.")
        except TypeError as error:
            print(error)

    def give_task(self, employee, task):
        if employee in self.team:
            print(f"Task {task} given to employee {employee.name}.")
            employee.add_task(task)
        else:
            print("Employee not found in the team.")


class Engineer(Employee):
    def __init__(self, name, ID):
        super().__init__(name, ID)
        self.projects = []
        self.skills = []

    def get_skills(self):
        return self.skills

    def set_skills(self, skills):
        self.skills = skills

    def add_skill(self, skill):
        if type(skill) == str:
            self.skills.append(skill)
            print(f"Skill {skill} added to the list.")
        else:
            print("Invalid skill. Please provide a string.")

    def get_projects(self):
        return self.projects

    def add_project(self, project):
        self.projects.append(project)

    def set_projects(self, projects):
        self.projects = projects

    def remove_project(self, project):
        if project in self.projects:
            self.projects.remove(project)
            print(f"Project {project} removed from the list.")
        else:
            print("Project not found in the list.")


class Salesperson(Employee):
    def __init__(self, name, ID, sale_target=None):
        super().__init__(name, ID)
        if sale_target is None:
            sale_target = 0
        self.sale_target = sale_target

    def get_sales(self):
        return self.sales

    def get_projects(self):
        return self.projects

    def get_sale_target(self):
        return self.sale_target

    def set_sales(self, sales):
        self.sales = sales

    def set_projects(self, projects):
        self.projects = projects

    def set_sale_target(self, sale_target):
        if sale_target < 0:
            print("Invalid sale target. Please provide a positive number.")
        elif type(sale_target) != int:
            print("Invalid sale target. Please provide an integer.")
        else:
            self.sale_target = sale_target

    def add_target(self, target):
        if type(target) == int:
            self.sale_target += target
            print(f"Target increased by {target}.")
        else:
            print("Invalid target. Please provide an integer.")

    def add_sale(self, sale):
        if type(sale) == int:
            self.sale_target -= sale
            print(f"Sale added: {sale}.")
        else:
            print("Invalid sale. Please provide an integer.")

    def add_project(self, project):
        self.projects.append(project)


employee1 = Employee("Mara", 12)
employee1.set_salary(1000)
employee1.set_schedule({"Monday": 8, "Tuesday": 8, "Wednesday": 8, "Thursday": 8, "Friday": 8})

engineer1 = Engineer("Alex", 2)
engineer1.set_salary(1500)
engineer1.set_schedule({"Monday": 8, "Tuesday": 8, "Wednesday": 8, "Thursday": 8, "Friday": 8})
engineer1.add_skill("Python")
engineer1.add_skill("Java")
engineer1.add_project("Project1")

manager1 = Manager("Andrei", 1, "IT")
manager1.set_salary(2000)
manager1.set_schedule({"Monday": 8, "Tuesday": 8, "Wednesday": 8, "Thursday": 8, "Friday": 8})
manager1.add_employee(employee1)
manager1.add_employee(engineer1)
manager1.give_task(employee1, "Task1")

employee1.mark_task("Task1")
print(manager1)
print(employee1)
print(engineer1)


salesperson1 = Salesperson("Maria", 3)
salesperson1.set_salary(1000)
salesperson1.set_schedule({"Monday": 8, "Tuesday": 8, "Wednesday": 8, "Thursday": 8, "Friday": 8})
salesperson1.add_sale(100)
print(salesperson1)
