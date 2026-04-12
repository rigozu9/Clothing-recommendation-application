with base as (

    select
        i.image_id,
        i.split,
        i.url,
        g.genders
    from {{ ref('stg_imat_images') }} i
    join {{ ref('int_imat_image_gender') }} g
        on i.image_id = g.image_id
       and i.split = g.split
    join {{ ref('int_imat_image_token_lists') }} t
        on i.image_id = t.image_id
       and i.split = t.split
),

gender_filter as (

    select
        image_id,
        split,
        url,
        genders,

        case
            when genders = array['Male']::text[] then 'male'
            when genders = array['Female']::text[] then 'female'
            when genders = array['Neutral']::text[] then 'female'
            else 'other'
        end as swipe_gender_mode

    from base

)

select *
from gender_filter
where swipe_gender_mode in ('male', 'female')