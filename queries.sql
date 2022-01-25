-- получили пререквизиты РПД номер ...
SELECT *
FROM public.dataprocessing_items di
WHERE di.id in (
    SELECT wpp.item_id
    FROM public.workprogramsapp_prerequisitesofworkprogram wpp
    where wpp.workprogram_id = 2640
);

-- получили результаты обучения одобренной РПД номер ...
SELECT *
FROM public.dataprocessing_items di
WHERE di.id in (
    SELECT wo.item_id
    FROM public.workprogramsapp_outcomesofworkprogram wo
             JOIN workprogramsapp_expertise we on we.work_program_id = wo.workprogram_id
    WHERE we.expertise_status = 'AC'
      AND wo.workprogram_id = 2640
)
ORDER BY id;

-- получили результаты обучения одобренной РПД номер ... на джойнах
SELECT
    wif.workprogram_id,
    ARRAY_AGG (
        wif.feature
        ORDER BY
            wif.workprogram_id
    ) features
FROM (SELECT wo.workprogram_id,
       CASE
           WHEN di.id in (
               SELECT id
               FROM public.dataprocessing_items di
               --
               WHERE di.id in (
                   SELECT wo.item_id
                   FROM public.workprogramsapp_outcomesofworkprogram wo
                            JOIN workprogramsapp_expertise we on we.work_program_id = wo.workprogram_id
                   WHERE we.expertise_status = 'AC'
               )
           ) THEN 1
           ELSE 0
           END feature
FROM public.dataprocessing_items di
JOIN public.workprogramsapp_outcomesofworkprogram wo on di.id = wo.item_id
JOIN public.workprogramsapp_expertise we on we.work_program_id = wo.workprogram_id
WHERE we.expertise_status = 'AC'
GROUP BY wo.workprogram_id, di.id
ORDER BY wo.workprogram_id, di.id) as wif
GROUP BY wif.workprogram_id
ORDER BY wif.workprogram_id;

-- с агрегацией
SELECT wiei.workprogram_id,
       ARRAY_AGG(
               wiei.entity_id
               ORDER BY
                   wiei.workprogram_id,
                   wiei.entity_id
           ) features
FROM (SELECT wo.workprogram_id, di.id as entity_id
      FROM public.dataprocessing_items di
               JOIN public.workprogramsapp_outcomesofworkprogram wo on di.id = wo.item_id
               JOIN public.workprogramsapp_expertise we on we.work_program_id = wo.workprogram_id
      WHERE we.expertise_status = 'AC'
) as wiei
GROUP BY wiei.workprogram_id
ORDER BY wiei.workprogram_id;

-- получили вектор параметров результатов обучения одобренной РПД номер ...
-- (то есть смотрим все возможные учебные сущности и ставим 0 или 1 в зависимости от наличия)
SELECT id,
       CASE
           WHEN id in (
               SELECT id
               FROM public.dataprocessing_items di
               WHERE di.id in (
                   SELECT wo.item_id
                   FROM public.workprogramsapp_outcomesofworkprogram wo
                            JOIN workprogramsapp_expertise we on we.work_program_id = wo.workprogram_id
                   WHERE we.expertise_status = 'AC'
                     AND wo.workprogram_id = 2640
               )
           ) THEN 1
           ELSE 0
           END feature
FROM public.dataprocessing_items
ORDER BY id;

-- получили вектор параметров результатов обучения одобренной для всех РПД
-- (то есть смотрим все возможные учебные сущности и ставим 0 или 1 в зависимости от наличия)
SELECT id,
       CASE
           WHEN id in (
               SELECT id
               FROM public.dataprocessing_items di
               WHERE di.id in (
                   SELECT wo.item_id
                   FROM public.workprogramsapp_outcomesofworkprogram wo
                            JOIN workprogramsapp_expertise we on we.work_program_id = wo.workprogram_id
                   WHERE we.expertise_status = 'AC'
                     AND wo.workprogram_id IN (
                       SELECT id
                       FROM workprogramsapp_workprogram
                   )
               )
           ) THEN 1
           ELSE 0
           END feature
FROM public.dataprocessing_items
ORDER BY id;

-- получили все айдишники одобренных РПД (считаем, что там норм пререквизиты)
SELECT work_program_id
FROM public.workprogramsapp_expertise we
WHERE we.expertise_status = 'AC';

-- получим пререквизиты всех одобренных РПД
SELECT workprogram_id, item_id
FROM public.dataprocessing_items di
         JOIN public.workprogramsapp_prerequisitesofworkprogram wpp on di.id = wpp.item_id
where wpp.workprogram_id in (
    SELECT work_program_id
    FROM public.workprogramsapp_expertise we
    WHERE we.expertise_status = 'AC'
)
ORDER BY workprogram_id;

-- получим результаты обучения всех одобренных РПД
SELECT workprogram_id, item_id
FROM public.dataprocessing_items di
         JOIN public.workprogramsapp_outcomesofworkprogram wo on di.id = wo.item_id
where wo.workprogram_id in (
    SELECT work_program_id
    FROM public.workprogramsapp_expertise we
    WHERE we.expertise_status = 'AC'
)
ORDER BY workprogram_id;

-- получим все учебные сущности, используемые в пререквизитах / результатах обучения
SELECT id
FROM public.dataprocessing_items
ORDER BY id;

-- получим вообще все РПД
SELECT id
FROM public.workprogramsapp_workprogram

