with exploded_labels as (
    select
        a.split,
        a.image_id,
        (jsonb_array_elements_text(a.label_ids))::int as label_id
    from {{ source('raw', 'imat_annotations') }} a
),

excluded_images as (
    select distinct
        e.split,
        e.image_id
    from exploded_labels e
    join {{ source('raw', 'imat_label_map') }} m
        on e.label_id = m.label_id
    where m.task_name = 'category'
      and m.label_name in ('Uniforms', 'Lingerie Sleepwear & Underwear', 'Bikinis', 'Swimsuits', 'Underwear', 'Beach & Swim Wear', 'Bra Straps', 'Costumes & Cosplay', 
      'Padded Bras', 'Shoelaces', 'Sports Bras',  'Swimsuit Cover-ups', 'Swimsuits', 'Swim Trunks', 'Thermal Underwear', 'Thongs', 'Pasties', 'Bodysuits', 'Nightgowns')
)

select
    i.split,
    i.image_id,
    i.url
from {{ source('raw', 'imat_images') }} i
left join excluded_images x
    on i.image_id = x.image_id
   and i.split = x.split
where x.image_id is null