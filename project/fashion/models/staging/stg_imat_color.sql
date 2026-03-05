select
  label_id,
  label_name as color
from {{ source('raw', 'imat_label_map') }}
where task_name = 'color'