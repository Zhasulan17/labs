''' 
CREATE TABLE phonebook2 (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT UNIQUE NOT NULL
);

CREATE OR REPLACE FUNCTION search_phonebook(pattern TEXT)
RETURNS TABLE(id INT, name TEXT, phone TEXT) AS
$$
BEGIN
    RETURN QUERY
    SELECT phonebook2.id, phonebook2.name, phonebook2.phone
    FROM phonebook2
    WHERE phonebook2.name ILIKE '%' || pattern || '%'
       OR phonebook2.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;


DROP PROCEDURE IF EXISTS upsert_user(text, text);


CREATE OR REPLACE PROCEDURE upsert_user(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO phonebook2 (name, phone)
    VALUES (p_name, p_phone)
    ON CONFLICT (phone)  -- Указываем столбец "phone" таблицы
    DO UPDATE SET name = EXCLUDED.name;
END;
$$;



CREATE OR REPLACE PROCEDURE bulk_insert_users(names TEXT[], phones TEXT[])
LANGUAGE plpgsql
AS
$$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP
        BEGIN
            -- Вставляем пользователя в таблицу
            INSERT INTO phonebook_2 (name, phone)
            VALUES (names[i], phones[i])
            ON CONFLICT (phone)  -- если номер телефона уже существует
            DO UPDATE SET name = EXCLUDED.name;  -- обновляем имя, если есть конфликт
        EXCEPTION
            WHEN unique_violation THEN
                -- Логируем ошибку (если телефон уже существует, можно пропустить)
                RAISE NOTICE 'Phone % already exists, skipping.', phones[i];
        END;
    END LOOP;
END;
$$;

DROP FUNCTION IF EXISTS paginate_phonebook(integer, integer);


CREATE OR REPLACE FUNCTION paginate_phonebook(page_limit INT, page_offset INT)
RETURNS TABLE(id INT, name TEXT, phone TEXT) AS
$$
BEGIN
    RETURN QUERY
    SELECT id, name, phone
    FROM phonebook_2
    ORDER BY id
    LIMIT page_limit OFFSET page_offset;
END;
$$ LANGUAGE plpgsql;

-- Процедура для удаления пользователей по имени или телефону
CREATE OR REPLACE PROCEDURE delete_user_by_name_or_phone(pattern TEXT)
LANGUAGE plpgsql
AS
$$
BEGIN
    DELETE FROM phonebook2
    WHERE name ILIKE '%' || pattern || '%' OR phone ILIKE '%' || pattern || '%';
END;
$$;

'''