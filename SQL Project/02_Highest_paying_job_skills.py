import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()  # Load data from .env

# Connection data
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# PostgreSQL connection engine
engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Importing SQL query from top_skills.sql
query = '''
WITH top_remote AS (
SELECT  
    job_id,
    name AS company_name,  
    job_title,
    salary_year_avg 
FROM 
    job_postings_fact AS jpf
LEFT JOIN 
    company_dim AS cd ON cd.company_id = jpf.company_id
WHERE 
    salary_year_avg IS NOT NULL AND
    LOWER(job_title_short) = 'data analyst' AND
    job_location = 'Anywhere'
ORDER BY salary_year_avg DESC
LIMIT 10 
)

SELECT 
        skills,
        top_remote.*
FROM 
        top_remote
INNER JOIN 
        skills_job_dim as sjd ON top_remote.job_id = sjd.job_id
INNER JOIN
        skills_dim as sd ON sd.skill_id = sjd.skill_id
ORDER BY
        salary_year_avg
'''

# Creating Pandas Dataframe and printing it
df = pd.read_sql_query(query, engine)
print(df)

# Get the top 10 most frequent skills 
skill_counts = df['skills'].value_counts().head(10)

# Normalize values for color mapping

vmin = skill_counts.min() - 15
vmax = skill_counts.max()

norm = plt.Normalize(vmin=vmin, vmax=vmax)
colors = plt.cm.Blues(norm(skill_counts.values)) 

# Creating horizontal bar chart and printing SQL query result
plt.figure(figsize=(10, 5))
plt.barh(skill_counts.index, skill_counts.values, color=colors)
plt.xlabel('Frequency')
plt.title('Top skills required in 10 best-paid data analyst jobs')
plt.gca().invert_yaxis()
plt.show()


