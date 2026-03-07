select
  split,
  image_id,
  array_agg(token order by token) as tokens
from {{ ref('int_imat_image_tokens') }}
group by split, image_id