-- получить инфо по редакторам и созданным ими программам
select first_name, last_name, user_id, workprogram_id, title
from public.workprogramsapp_workprogram_editors editors
         JOIN dataprocessing_user users on editors.user_id = users.id
         JOIN workprogramsapp_workprogram program on editors.workprogram_id = program.id

-- получить все учебные сущности (пререквизиты, результаты обучения), РПД, созданных конкретным пользователем
select *
from public.workprogramsapp_workprogram_editors editors
         JOIN workprogramsapp_workprogram program on editors.workprogram_id = program.id
         JOIN workprogramsapp_outcomesofworkprogram outcomes on program.id = outcomes.workprogram_id
         JOIN workprogramsapp_prerequisitesofworkprogram prerequisites on program.id = prerequisites.workprogram_id
WHERE editors.id = 6839;

-- получить учебные сущности из предыдущего запроса с агрегацией
SELECT data.user_id,
       ARRAY_AGG(
               data.item_id
               ORDER BY
                   data.user_id,
                   data.item_id
           ) entities
FROM (SELECT * FROM dataprocessing_items items
               JOIN workprogramsapp_prerequisitesofworkprogram prerequisites on items.id = prerequisites.workprogram_id
               JOIN workprogramsapp_workprogram program on program.id = prerequisites.workprogram_id
               JOIN workprogramsapp_workprogram_editors editors on program.id = editors.workprogram_id
               UNION ALL SELECT * FROM dataprocessing_items items
               JOIN workprogramsapp_outcomesofworkprogram outcomes on items.id = outcomes.item_id
               JOIN workprogramsapp_workprogram program on program.id = outcomes.workprogram_id
               JOIN workprogramsapp_workprogram_editors editors on program.id = editors.workprogram_id

     ) as data
GROUP BY data.user_id
ORDER BY data.user_id
LIMIT 5;
