select
  a.split,
  a.image_id,
  (jsonb_array_elements_text(a.label_ids))::int as label_id
from {{ source('raw', 'imat_annotations') }} as a