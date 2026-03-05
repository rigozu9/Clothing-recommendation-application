with all_labels as (
  select split, image_id, 'color' as attr_type, color_name as attr_value
  from {{ ref('int_imat_image_color') }}

  union all
  select split, image_id, 'style' attr_type, style_name as attr_value
  from {{ ref('int_imat_image_style') }}

  union all
  select split, image_id, 'material', material_name as attr_value
  from {{ ref('int_imat_image_material') }}

  union all
  select split, image_id, 'pattern', pattern_name as attr_value
  from {{ ref('int_imat_image_pattern') }}
),

agg as (
  select
    split,
    image_id,
    coalesce(array_agg(distinct attr_value) filter (where attr_type='color'), '{}'::text[]) as colors,
    coalesce(array_agg(distinct attr_value) filter (where attr_type='material'), '{}'::text[]) as materials,
    coalesce(array_agg(distinct attr_value) filter (where attr_type='pattern'), '{}'::text[]) as patterns,
    coalesce(array_agg(distinct attr_value) filter (where attr_type='style'), '{}'::text[]) as styles
  from all_labels
  group by split, image_id
)

select * from agg