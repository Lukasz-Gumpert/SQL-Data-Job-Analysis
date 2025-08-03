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