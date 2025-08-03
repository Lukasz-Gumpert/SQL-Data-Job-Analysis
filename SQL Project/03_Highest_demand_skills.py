import numpy as np
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

engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

query_all = '''
WITH top_demand_all AS (
        SELECT
                skills,
                count(sjd.job_id) AS demand
        FROM
                job_postings_fact AS jpf
        INNER JOIN
                skills_job_dim AS sjd ON jpf.job_id = sjd.job_id
        INNER JOIN
                skills_dim AS sd ON sjd.skill_id = sd.skill_id
        WHERE
                LOWER(jpf.job_title_short) = 'data analyst'
        GROUP BY 
                skills
        ORDER BY 
                demand DESC
        LIMIT 
                5
)

SELECT * FROM top_demand_all

'''

query_remote = '''
WITH top_demand_remote AS (
        SELECT
                skills,
                count(sjd.job_id) AS demand
        FROM
                job_postings_fact AS jpf
        INNER JOIN
                skills_job_dim AS sjd ON jpf.job_id = sjd.job_id
        INNER JOIN
                skills_dim AS sd ON sjd.skill_id = sd.skill_id
        WHERE
                LOWER(jpf.job_title_short) = 'data analyst' AND
                jpf.job_work_from_home = True
        GROUP BY 
                skills
        ORDER BY 
                demand DESC
        LIMIT 
                5
)

SELECT * FROM top_demand_remote
'''

# Create Dataframe for all and remote only jobs
df_all = pd.read_sql_query(query_all, engine)
df_remote = pd.read_sql_query(query_remote, engine)

# Ensure same skill descdending order
df_all = df_all.sort_values(by="demand",ascending=False)
df_remote = df_remote.sort_values(by="demand",ascending=False)

# Extract values 
skills = df_all["skills"].values
demand_all = df_all["demand"].values
demand_remote = df_remote["demand"].values

# Bar positioning settings
y_pos = np.arange(len(skills))
bar_width = 0.3

# Create hotiontal Bar chart
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(y_pos - bar_width/2, demand_all, height=bar_width, label='All jobs', color='skyblue')
ax.barh(y_pos + bar_width/2, demand_remote, height=bar_width, label='Remote jobs', color='orange')

# Set Y axis, labels and legend size
ax.set_yticks(y_pos)
ax.set_yticklabels(skills)
ax.invert_yaxis()
ax.set_xlabel("Number of Job Postings")
ax.set_title("Top Skills Demand: All vs Remote")
ax.legend(prop={'size': 15})

plt.tight_layout()
plt.show()



