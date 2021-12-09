ALTER TABLE movieDatabase.dbo.movies
ALTER COLUMN movie_name VARCHAR(MAX)
SELECT *
FROM movies
WHERE movie_id = '112449' -- Create tables with FK references using cascade to update rows
    -- CREATE TABLE movie_lists
    -- (
    --     list_id  INT NOT NULL
    --         constraint movie_lists_pk
    --             primary key nonclustered,
    --     movie_id int not null
    --         constraint movie_lists_movies_movie_id_fk
    --             references movies
    --             on update cascade
    -- )
    -- go
    -- create table user_list_lookup
    -- (
    --     user_id int not null
    --         constraint user_list_lookup_users_user_id_fk
    --             references users
    --             on update cascade,
    --     movie_list_id int not null
    --         constraint user_list_lookup_movie_lists_list_id_fk
    --             references movie_lists
    --             on update cascade
    -- )
    -- go
alter table movie_lists
add constraint movie_lists_user_list_lookup_movie_list_id_fk foreign key (list_id) references user_list_lookup on update cascade
go
ALTER TABLE user_list_lookup
ADD movie_list_id int NOT NULL IDENTITY (1, 1) PRIMARY KEY
ALTER TABLE users
ADD user_id int NOT NULL IDENTITY (1, 1) PRIMARY KEY
alter table user_list_lookup
add user_id int not null
go
alter table user_list_lookup
add constraint user_list_lookup_users_user_id_fk foreign key (user_id) references users on update cascade
go -- DELETE FROM user_list_lookup
INSERT INTO users
VALUES ('279954@viauc.dk');
SELECT user_id
FROM users
WHERE email = 'rando_mail@rando.com'
INSERT INTO users OUTPUT Inserted.user_id
VALUES('279954@viauc.dk');
INSERT INTO movie_lists
VALUES (1, 9603212)
INSERT INTO user_list_lookup OUTPUT Inserted.movie_list_id
VALUES (2)
INSERT INTO movie_lists OUTPUT Inserted.movie_id,
    Inserted.list_id
VALUES (list_id, movie_id)
SELECT user_id
FROM users
WHERE email = 'e-mail@email.com'
SELECT movieDatabase.dbo.movie_lists.movie_id,
    movieDatabase.dbo.movie_lists.list_id,
    movieDatabase.dbo.users.email
FROM (
        (
            movieDatabase.dbo.users
            INNER JOIN movieDatabase.dbo.user_list_lookup ON movieDatabase.dbo.users.user_id = 2
        )
        INNER JOIN movieDatabase.dbo.movie_lists ON movieDatabase.dbo.movie_lists.list_id = movieDatabase.dbo.user_list_lookup.movie_list_id
        and movieDatabase.dbo.user_list_lookup.user_id = 2
    );
SELECT user_id,
    movie_list_id
FROM user_list_lookup
WHERE user_id = 7
SELECT movie_id
FROM movie_lists
WHERE list_id = 3
DELETE FROM movie_lists
WHERE list_id = 1
    and movie_id = 6320628
SELECT user_id
FROM users
WHERE email = '279954@viauc.dk'