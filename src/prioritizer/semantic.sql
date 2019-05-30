drop table if exists semantic.entities cascade;
drop table if exists semantic.events cascade;

create table semantic.entities as (
    with entities as (
    select
        distinct entity_id::varchar,
        city,
        state,
        county,
        primary_subject,
        poverty,
        grade,
        (min(date) over (partition by entity_id))::timestamp as start_time,
        now()::timestamp as end_time

    from cleaned.projects
    )

    select * from entities
);

create table semantic.events as (
        with events as (
            select
                event_id::varchar,
                entity_id::varchar,
                type,
                price,
                reach,
                date,
                result


            from cleaned.projects
            order by
            date asc
    )
    select et.*, ev.type, ev.price, ev.reach, ev.date, ev.result from semantic.entities et
    inner join events ev on et.entity_id = ev.entity_id
);
