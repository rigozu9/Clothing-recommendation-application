select
  l.split,
  l.image_id,
  c.label_id as color_id,
  c.color_name
from {{ ref('stg_imat_annotation_labels') }} l
join {{ ref('stg_imat_color') }} c
  on l.label_id = c.label_id
