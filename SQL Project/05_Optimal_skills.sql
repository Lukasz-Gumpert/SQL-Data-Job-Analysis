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

