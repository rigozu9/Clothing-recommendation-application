with all_tokens as (
  select
    split,
    image_id,
    'color:' || replace(replace(lower(attr), ' ', '_'), '-', '_') as token
  from (
    select split, image_id, unnest(colors) as attr
    from {{ ref('int_imat_image_attributes') }}
  ) c

  union all

  select
    split,
    image_id,
    'material:' || replace(replace(lower(attr), ' ', '_'), '-', '_') as token
  from (
    select split, image_id, unnest(materials) as attr
    from {{ ref('int_imat_image_attributes') }}
  ) m

  union all

  select
    split,
    image_id,
    'pattern:' || replace(replace(lower(attr), ' ', '_'), '-', '_') as token
  from (
    select split, image_id, unnest(patterns) as attr
    from {{ ref('int_imat_image_attributes') }}
  ) p

  union all

  select
    split,
    image_id,
    'style:' || replace(replace(lower(attr), ' ', '_'), '-', '_') as token
  from (
    select split, image_id, unnest(styles) as attr
    from {{ ref('int_imat_image_attributes') }}
  ) s
)

select * from all_tokens