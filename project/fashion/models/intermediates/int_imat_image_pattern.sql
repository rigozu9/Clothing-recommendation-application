select
  l.split,
  l.image_id,
  p.label_id as pattern_id,
  p.pattern_name
from {{ ref('stg_imat_annotation_labels') }} l
join {{ ref('stg_imat_pattern') }} p
  on l.label_id = p.label_id