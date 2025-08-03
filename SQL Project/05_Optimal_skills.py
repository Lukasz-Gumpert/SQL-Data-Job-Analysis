import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from adjustText import adjust_text
from dotenv import load_dotenv
import os

load_dotenv()  # Load data from .env

# Connection data
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

query = '''
SELECT  
        sd.skill_id,
        sd.skills,
        COUNT(sjd.job_id) AS demand_count,
        ROUND(AVG(jpf.salary_year_avg)) AS average_compensation
FROM
        job_postings_fact AS jpf
INNER JOIN
        skills_job_dim AS sjd ON jpf.job_id = sjd.job_id
INNER JOIN
        skills_dim AS sd ON sjd.skill_id = sd.skill_id
WHERE
        salary_year_avg IS NOT NULL AND
        LOWER(job_title_short) = 'data analyst' AND
        job_work_from_home = True
GROUP BY
        sd.skill_id
HAVING
        COUNT(sjd.job_id) > 15
ORDER BY 
        average_compensation DESC,
        demand_count DESC
LIMIT 
        20
'''

# Create dataframe
df = pd.read_sql(query,engine)

# Create scatter chart
fig, ax = plt.subplots(figsize=(12, 7))
ax.scatter(df['demand_count'], df['average_compensation'], color='steelblue')


# creating marker labels 
texts = []
for i, row in df.iterrows():
    texts.append(
        ax.text(
            row['demand_count'], 
            row['average_compensation'], 
            row['skills'], 
            fontsize=11,
        )
    )
    
# using adjst_text to increase space between markers and labels
adjust_text(
    texts, 
    ax=ax, 
    expand_text=(10,10),
    arrowprops=dict(
        arrowstyle='-', 
        color='gray', 
        lw=1))

# set labels
ax.set_xlabel('Number of job postings', fontsize=12)
ax.set_ylabel('Average Compensation ($)', fontsize=12)
ax.set_title('Which skills are most optimal for the Data Analyst role?', fontsize=15)

# Creating regression 
x = df['demand_count']
y = df['average_compensation']
m, b = np.polyfit(x, y, 1)
ax.plot(x, m*x + b, color='red', linestyle='--', linewidth=1.5, label='Linear Trend')

ax.legend()
plt.tight_layout()
plt.show()


