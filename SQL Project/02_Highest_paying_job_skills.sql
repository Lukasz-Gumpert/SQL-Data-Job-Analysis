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
