with gender_labels as (

    select
        al.split,
        al.image_id,
        lm.label_name as gender
    from {{ ref('stg_imat_annotation_labels') }} al
    join {{ ref('stg_imat_label_map') }} lm
        on al.label_id = lm.label_id
    where lm.task_name = 'gender'

),

grouped as (

    select
        split,
        image_id,
        array_agg(distinct gender) as genders
    from gender_labels
    group by split, image_id

)

select * from grouped