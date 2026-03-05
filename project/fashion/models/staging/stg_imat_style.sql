select
  label_id,
  label_name as style_name
from {{ source('raw', 'imat_label_map') }}
where task_name = 'style'