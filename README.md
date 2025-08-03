<p align="left">
  <img src="SQL Project\assets\image-2.png" width="150" alt='postgresql'/>
  <img src="SQL Project\assets\image-1.png" width="150" alt='python'/>
</p>

# SQL Data Job Analysis: 

This project explores the current data job market through the lens of skill demand and compensation. By analyzing job postings and salary trends, I identify the most valuable skills to learn for aspiring data professionals. The analysis also includes a breakdown of top paying companies hiring remote data analysts.

# Technologies & Tools Utilized:

- SQL (PostgreSQL)

- Python (NumPy, pandas, matplotlib, sqlalchemy)

- Visual Studio Code

- Git & GitHub

# Analysis:

## 1. Top remote jobs:

Initially, the analysis filters the dataset to include only remote data analyst roles, applying constraints on geographic availability and average yearly compensation.

```sql
WITH top_remote AS (
SELECT  
    job_id,
    jpf.company_id,
    name AS company_name,  
    job_title_short,
    job_location,
    job_schedule_type,
    job_country,
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

SELECT * FROM top_remote
```
<img src="SQL Project\assets\01_top_remote_jobs.png" alt='top remote jobs'>

*Results of the SQL query, visualized via ChatGPT, highlighting the top 10 remote data analyst positions by average annual salary.*

### 3 key insights:

- __Big Tech Leadership:__
Companies like Meta, AT&T, and Pinterest top the list, showing that big tech still offers the best remote data analyst salaries.

- __Geographic Concentration with an Outlier:__
Nine of the ten highest-paying remote roles are offered by U.S.-based companies, reflecting the strong U.S. market for remote analytics positions.
One exception is Mantys (India), an outlier which offers $650 000 average. It may indicate a specialized or senior level role.

- __Wide Salary Dispersion:__
There’s a significant salary spread - from $184 000 at the 10th spot up to $650 000 at the top. This suggests considerable variability based on company, specialization, and possibly seniority even within the “Data Analyst” title.

## 2. Highest paying job skills:

In the second part of the project, I examine which skills are required by the top 10 remote data analyst openings identified in the previous query. To do this, I reuse the initial SQL query and then leverage Python libraries - NumPy, pandas, and Matplotlib to process and visualize the extracted skill data.

```sql

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

```

```py
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
```
<img src="SQL Project\assets\02_Highest_paying_job_skills.png" alt='Highest_paying_job_skill'>

*Results of the SQL query, visualized using matplotlib*

### 3 key insights:
- __Core analytics duo: SQL & Python:__
Nearly every listing calls out SQL and Python as must-have skills, these two form the foundation of remote data analysis work.

- __Visualization counts: Tableau & Excel:__
Tools for sharing insights, especially Tableau and Excel appear in most of the higher-paying roles, underlining the importance of clean, interactive dashboards.

- __Cloud & big-data platforms:__
Beyond basics, many top jobs list cloud/warehouse technologies (AWS, Azure, Snowflake) or big-data frameworks (e.g. Databricks), highlighting that remote analysts often need hands-on experience with scalable data platforms.

## 3. Highest demand skills

Having already identified the top 10 highest-paying remote jobs for analysts and the skills they require, I decided to take a closer look at the most popular skills overall. This time, I analyzed demand across all job types, not just remote roles. In the end, I compared the two sets (all jobs vs remote-only) to uncover any key differences in skill demand between remote and general analytical positions.

```sql

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
),
top_demand_remote AS (
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
                job_work_from_home = True

        GROUP BY 
                skills
        ORDER BY 
                demand DESC
        LIMIT 
                5
)

SELECT * FROM top_demand_remote

```

```py

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

```
<img src="SQL Project\assets\03_Highest_demand_skills.png" alt='Highest_paying_job_skill'>

*Comparison of the most in-demand skills between all jobs and remote-only jobs, visualized using the Matplotlib library.*

### 3 key insights:

- __SQL remains the top skill across all job types__:
SQL is by far the most in-demand skill for data analysts, both in general job postings and remote-only roles. This confirms that proficiency in SQL is a foundational requirement for anyone entering the field.

- __Noticeable gap in remote job availability__:
For every listed skill (SQL, Excel, Python, Tableau, Power BI), the number of remote job postings is significantly lower than the total number of job postings. This highlights that, despite the growing trend of remote work, it still represents a smaller portion of the data analyst job market.

- __Skill ranking is consistent across job types:__
Despite differences in absolute numbers, the order of the most in-demand skills remains nearly identical for both general and remote job postings. This suggests that expectations for data analyst roles are largely the same, regardless of whether the position is remote or not.

## 4. Highest paying skills

In this section, we examine how individual skills influence average salary levels for Data Analyst positions. The analysis is based exclusively on job postings that include a specified salary, regardless of location.

```sql
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
```

```py
# Create dataframe
df = pd.read_sql(query,engine)

# Creating horizontal bar chart and printing SQL query result
fig, ax = plt.subplots(figsize=(10,6))
ax = plt.barh(df['skills'].values,df['avrage_compenstation'].values)
plt.xlabel('Avrage_compenstation')
plt.title('Top 25 Highest-Paying Skills for data analyst roles')
plt.gca().invert_yaxis()
plt.show()
```
<img src="SQL Project\assets\04_Highest_paying_skills.png" alt="04_Highest_paying_skills">

*Matplotlib bar chart focusing on 25 data analyst skills that pay the most*

### 3 key insights:

- __SVN stands out dramatically:__ with a reported average compensation of $400,000, which may suggest either rare demand or outlier data.

- __Specialized Tools Pay More:__
Skills like Solidity, Couchbase, and DataRobot offer $150,000+ salaries, highlighting the value of expertise in emerging or enterprise-level technologies.

- __ML and DevOps Tools Are Highly Valued:__
Tools such as TensorFlow, Keras, Pytorch, and Terraform are well represented, showing that ML and data engineering skills remain in high demand and well compensated.

## 5. Optimal skills

In this final section, the goal is to determine the most optimal skills to learn for a career in remote data analysis.
The evaluation is based on two key factors:

- High average annual salary — indicating strong financial value of a skill

- High market demand — showing how frequently the skill appears in job postings

By combining these two metrics, we can highlight the skills that offer both high earning potential and broad career opportunities.

```sql
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
        COUNT(sjd.job_id) > 10
ORDER BY 
        average_compensation DESC,
        demand_count DESC
```

```py
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
```

<img src="SQL Project\assets\05_optimal_skills.png" alt="optimal skills">

*Trade-off between demand and compensation for data analyst skills. Scatter plot visualised using matplotlib.*

### 3 key insights:

- __High Demand Doesn’t Equal High Pay:__
Skills like SQL and Tableau have the most job postings but offer lower average compensation, suggesting that high supply of these skills drives down pay.

- __Niche Skills Pay More:__
Tools like Go, Hadoop, and Snowflake offer the highest salaries despite having far fewer job postings. Specializing in these less common tools may lead to higher earnings.

- __Negative Correlation Between Pay and Demand:__
The downward trend line shows an inverse relationship, as the number of job postings increases, average salary tends to decrease, highlighting a trade-off between market demand and compensation.

## Final conclusion

- __SQL & Python Are Essential:__
Across both remote and general data analyst roles, SQL and Python consistently appear as the most demanded and most frequently required skills. Mastery of these two is a non-negotiable foundation for anyone entering the field.

- __Remote Roles Are High-Paying but Less Available:__
While remote data analyst positions can offer exceptionally high salaries (e.g. $650,000 at Mantys), they are still a smaller share of the total job market.

- __Specialized Skills Command Premium Salaries:__
Tools such as SVN, Solidity, and DataRobot show above-average compensation, often exceeding $150,000. These skills are rarer in the market and reflect a growing value in niche technologies and enterprise solutions.

- __Visualization & Cloud Tools Add Strong Value:__
Proficiency in Tableau, Excel, and cloud platforms like AWS, Azure, and Snowflake is a major plus in top-paying jobs. These tools support not just analysis but also communication of insights and scalable data work.

- __There’s a Trade-Off Between Popularity and Pay:__
The final scatter plot revealed a negative correlation between skill demand and compensation. Widely used tools like SQL and Tableau are in high demand but offer lower pay, while less common skills like Go and Hadoop are associated with higher salaries.

# Final note:

This project not only deepened my understanding of the data analytics job market and its key trends, but also helped me strengthen my technical skill set through hands-on practice with real data.

For the first time, I was able to perform a complete end-to-end analysis entirely within Visual Studio Code, thanks to the use of SQLAlchemy and other core Python tools. Creating a dedicated virtual environment (venv) made me realize the importance of isolating dependencies for each project.

In addition, working with database connections made me more conscious of data security. To handle sensitive information such as credentials safely, I integrated the zero-dependency dotenv module, which allowed me to manage environment variables securely and cleanly.

Overall, this project combined career-relevant insights with valuable technical learning, both of which will serve as a solid foundation for future work in data analytics.




