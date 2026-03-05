select
  l.split,
  l.image_id,
  s.label_id as style_id,
  s.style_name
from {{ ref('stg_imat_annotation_labels') }} l
join {{ ref('stg_imat_style') }} s
  on l.label_id = s.label_id
