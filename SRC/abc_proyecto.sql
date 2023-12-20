
CREATE DATABASE abc_proyecto;
USE abc_proyecto;

CREATE TABLE salario (
  id INT AUTO_INCREMENT PRIMARY KEY,
  dailyrate FLOAT,
  monthlyrate FLOAT,
  percentsalaryhike INT,
  hourlyrate FLOAT,
  employeenumber FLOAT
);

CREATE TABLE abandono_satisfaccion (
  id INT AUTO_INCREMENT PRIMARY KEY,
  attrition VARCHAR(45),
  environmentsatisfaction FLOAT,
  environmentsatisfaction_cat VARCHAR(45), 
  jobinvolvement INT, 
  jobinvolvement_cat VARCHAR(45), 
  jobsatisfaction INT, 
  relationshipsatisfaction INT, 
  relationshipsatisfaction_cat VARCHAR(45), 
  worklifebalance FLOAT, 
  worklifebalance_cat VARCHAR(45), 
  employeenumber FLOAT,
  salario_id INT,
  FOREIGN KEY (salario_id) REFERENCES salario(id)
);

-- Crear la tabla 'detalles_personales'
CREATE TABLE detalles_personales (
  id INT AUTO_INCREMENT PRIMARY KEY,
  age INT,
  gender FLOAT, 
  gender_cat VARCHAR(45), 
  maritalstatus VARCHAR(45), 
  distancefromhome FLOAT, 
  totalworkingyears FLOAT, 
  education INT, 
  education_cat VARCHAR(250), 
  educationfield VARCHAR(250), 
  numcompaniesworked INT, 
  employeenumber FLOAT,
  abandono_satisfaccion_id INT,
  FOREIGN KEY (abandono_satisfaccion_id) REFERENCES abandono_satisfaccion(id)
);

-- Crear la tabla 'condiciones'
CREATE TABLE condiciones (
  id INT AUTO_INCREMENT PRIMARY KEY,
  businesstravel VARCHAR(45), 
  department VARCHAR(45), 
  joblevel INT, 
  jobrole VARCHAR(45), 
  overtime VARCHAR(45), 
  stockoptionlevel INT, 
  trainingtimeslastyear INT, 
  yearsatcompany INT, 
  yearssincelastpromotion INT, 
  yearswithcurrmanager INT, 
  remotework VARCHAR(45), 
  employeenumber FLOAT,
  salario_id INT,
  abandono_satisfaccion_id INT,
  FOREIGN KEY (salario_id) REFERENCES salario(id),
  FOREIGN KEY (abandono_satisfaccion_id) REFERENCES abandono_satisfaccion(id)
);


