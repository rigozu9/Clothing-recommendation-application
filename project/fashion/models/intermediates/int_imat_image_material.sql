select
  l.split,
  l.image_id,
  m.label_id as material_id,
  m.material_name
from {{ ref('stg_imat_annotation_labels') }} l
join {{ ref('stg_imat_material') }} m
  on l.label_id = m.label_id