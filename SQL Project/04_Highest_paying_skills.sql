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

