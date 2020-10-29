CREATE
OR REPLACE FUNCTION public.get_users2() RETURNS SETOF users_foo LANGUAGE sql STABLE AS $ function $
SELECT
  count(*)
FROM
  pg_catalog.pg_user $ function $


CREATE
OR REPLACE FUNCTION public.get_random_sleep2() RETURNS SETOF foo LANGUAGE sql STABLE AS $ function $
select
  1
from
  (
    SELECT
      pg_sleep(random() * 2)
  ) as aaa $ function $


CREATE TABLE public.foo (
	id integer NOT NULL,
	CONSTRAINT id_pkey PRIMARY KEY (id)
);


CREATE TABLE public.users_foo (
	count bigint NOT NULL,
	CONSTRAINT count_pkey PRIMARY KEY (count)
);
