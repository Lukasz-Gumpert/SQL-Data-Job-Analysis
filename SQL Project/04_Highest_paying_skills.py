import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv() # Load data from .env

# Connection data
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

query = '''
SELECT
        skills,
        ROUND(AVG(salary_year_avg),0) as avrage_compenstation 
FROM 
        job_postings_fact AS jpf
INNER JOIN
        skills_job_dim AS sjd ON jpf.job_id = sjd.job_id
INNER JOIN
        skills_dim AS sd ON sjd.skill_id = sd.skill_id
WHERE
        salary_year_avg IS NOT NULL AND
        LOWER(job_title_short) = 'data analyst'
GROUP BY 
        skills
ORDER BY 
        avrage_compenstation DESC
LIMIT
        25
'''

# Create dataframe
df = pd.read_sql(query,engine)

# Creating horizontal bar chart and printing SQL query result
fig, ax = plt.subplots(figsize=(10,6))
ax = plt.barh(df['skills'].values,df['avrage_compenstation'].values)
plt.xlabel('Avrage_compenstation')
plt.title('Top 25 Highest-Paying Skills for data analyst roles')
plt.gca().invert_yaxis()
plt.show()
