{{ config(
    materialized='table',
    file_format='parquet'
)
}}
select
    lower(`Samplingpoint`) AS sampling_id,
    `Value` AS measurement,
    `Start` AS start_time,
    `End` AS end_time
from {{ source('air_quality', 'observations_raw') }}
where `Validity` = 1 AND `Verification` = 1 AND `Value` IS NOT NULL
