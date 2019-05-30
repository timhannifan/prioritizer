create table semantic.entities as (
        with entities as (
        select
            teacher_acctid,
            schoolid,
            school_ncesid
        from projects
        -- order by
        --     license_num asc, facility asc, facility_aka asc, facility_type asc, address asc,
        --     date asc -- IMPORTANT!!
        --     )

    select
        teacher_acctid,
        schoolid,
        school_ncesid
    from entities
);
