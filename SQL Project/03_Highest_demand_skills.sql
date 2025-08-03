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