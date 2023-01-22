-- получить инфо по редакторам и созданным ими программам
select authors, first_name, last_name, user_id, workprogram_id, title
from public.workprogramsapp_workprogram_editors editors
         JOIN dataprocessing_user users on editors.user_id = users.id
         JOIN workprogramsapp_workprogram program on editors.workprogram_id = program.id
WHERE authors like ('%' || last_name || '%');

-- SELECT data.user_id, ARRAY_AGG(data.item_id ORDER BY data.user_id, data.item_id) entities
-- FROM (SELECT *
--       FROM dataprocessing_items items
--                JOIN workprogramsapp_prerequisitesofworkprogram prerequisites on items.id = prerequisites.workprogram_id
--                JOIN workprogramsapp_workprogram program on program.id = prerequisites.workprogram_id
--                JOIN workprogramsapp_workprogram_editors editors on program.id = editors.workprogram_id
--       UNION ALL
--       SELECT *
--       FROM dataprocessing_items items
--                JOIN workprogramsapp_outcomesofworkprogram outcomes on items.id = outcomes.item_id
--                JOIN workprogramsapp_workprogram program on program.id = outcomes.workprogram_id
--                JOIN workprogramsapp_workprogram_editors editors on program.id = editors.workprogram_id) as data
-- GROUP BY data.user_id
-- ORDER BY data.user_id;

select *
from public.workprogramsapp_workprogram_editors editors
         JOIN dataprocessing_user usr on editors.user_id = usr.id
         JOIN workprogramsapp_workprogram program on editors.workprogram_id = program.id
         JOIN workprogramsapp_outcomesofworkprogram outcomes on program.id = outcomes.workprogram_id
         JOIN workprogramsapp_prerequisitesofworkprogram prerequisites on program.id = prerequisites.workprogram_id
WHERE usr.id = 701;

-- получить все учебные сущности (пререквизиты, результаты обучения), РПД, созданных конкретным пользователем
select *
from public.workprogramsapp_workprogram_editors editors
         JOIN workprogramsapp_workprogram program on editors.workprogram_id = program.id
         JOIN workprogramsapp_outcomesofworkprogram outcomes on program.id = outcomes.workprogram_id
         JOIN workprogramsapp_prerequisitesofworkprogram prerequisites on program.id = prerequisites.workprogram_id
WHERE program.authors like '%Бессмертный%';

-- получить учебные сущности из предыдущего запроса с агрегацией
SELECT data.user_id,
       ARRAY_AGG(
               data.item_id
               ORDER BY
                   data.user_id,
                   data.item_id
           ) entities
FROM ((SELECT *
       FROM dataprocessing_items items
                JOIN workprogramsapp_prerequisitesofworkprogram prerequisites on items.id = prerequisites.workprogram_id
                JOIN workprogramsapp_workprogram program on program.id = prerequisites.workprogram_id
                JOIN workprogramsapp_workprogram_editors editors on program.id = editors.workprogram_id
                JOIN dataprocessing_user users on editors.user_id = users.id
       WHERE last_name like '%' || authors || '%'
       UNION ALL
       SELECT *
       FROM dataprocessing_items items
                JOIN workprogramsapp_outcomesofworkprogram outcomes on items.id = outcomes.item_id
                JOIN workprogramsapp_workprogram program on program.id = outcomes.workprogram_id
                JOIN workprogramsapp_workprogram_editors editors on program.id = editors.workprogram_id
                JOIN dataprocessing_user users on editors.user_id = users.id
       WHERE last_name like '%' || authors || '%'
)) as data
GROUP BY data.user_id
ORDER BY data.user_id
LIMIT 5;

SELECT data.user_id, ARRAY_AGG(data.item_id ORDER BY data.user_id, data.item_id) entities
FROM (SELECT *
      FROM dataprocessing_items items
               JOIN workprogramsapp_prerequisitesofworkprogram prerequisites on items.id = prerequisites.workprogram_id
               JOIN workprogramsapp_workprogram program on program.id = prerequisites.workprogram_id
               JOIN workprogramsapp_workprogram_editors editors on program.id = editors.workprogram_id
               JOIN dataprocessing_user users on editors.user_id = users.id
      WHERE authors like ('%' || last_name || '%')
      UNION ALL
      SELECT *
      FROM dataprocessing_items items
               JOIN workprogramsapp_outcomesofworkprogram outcomes on items.id = outcomes.item_id
               JOIN workprogramsapp_workprogram program on program.id = outcomes.workprogram_id
               JOIN workprogramsapp_workprogram_editors editors on program.id = editors.workprogram_id
               JOIN dataprocessing_user users on editors.user_id = users.id
      WHERE authors like ('%' || last_name || '%')
     ) as data
GROUP BY data.user_id
ORDER BY data.user_id;

select id, name, domain_id
from dataprocessing_items
where id in (26147, 9096, 9097, 9098, 9099, 9100, 9101, 9102, 9095, 9112);

select id, name, domain_id
from dataprocessing_items
where id in (12624, 5040, 12628, 12343, 12418, 12422, 12460, 4430, 10450, 10451, 10452, 10453, 10454, 10455, 10456);

select id, name, domain_id
from dataprocessing_items
where id in (1003, 1500, 2298, 18465, 594, 2284, 21848, 20484, 22818, 1852);


SELECT data.user_id, last_name, title, authors, ARRAY_AGG(data.item_id ORDER BY data.user_id, data.item_id) entities
FROM (SELECT *
      FROM dataprocessing_items items
               JOIN workprogramsapp_prerequisitesofworkprogram prerequisites on items.id = prerequisites.workprogram_id
               JOIN workprogramsapp_workprogram program on program.id = prerequisites.workprogram_id
               JOIN workprogramsapp_workprogram_editors editors on program.id = editors.workprogram_id
               JOIN dataprocessing_user users on editors.user_id = users.id
      WHERE last_name like '%' || authors || '%'
      UNION ALL
      SELECT *
      FROM dataprocessing_items items
               JOIN workprogramsapp_outcomesofworkprogram outcomes on items.id = outcomes.item_id
               JOIN workprogramsapp_workprogram program on program.id = outcomes.workprogram_id
               JOIN workprogramsapp_workprogram_editors editors on program.id = editors.workprogram_id
               JOIN dataprocessing_user users on editors.user_id = users.id
      WHERE last_name like '%' || authors || '%') as data
GROUP BY data.user_id, title, authors, last_name
ORDER BY data.user_id