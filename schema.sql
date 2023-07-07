
CREATE TABLE movies_and_series (
    id VARCHAR(12) PRIMARY KEY,
    show_id VARCHAR(10),
    type VARCHAR(12),
    title TEXT,
    director TEXT,
    "cast" TEXT,
    country TEXT,
    date_added VARCHAR(22),
    release_year INT,
    rating VARCHAR(12),
    duration VARCHAR(12),
    listed_in TEXT,
    description TEXT,
    duration_int INT,
    duration_type VARCHAR(12),
    platform varchar(10)
);


CREATE TABLE categories (
    id_gen BIGINT PRIMARY KEY,
    genres TEXT
);

CREATE TABLE movies_categories (
    id VARCHAR(10),
    genres TEXT,
    id_gen INT,
    FOREIGN KEY (id_gen) REFERENCES categories (id_gen),
    FOREIGN KEY (id) REFERENCES movies_and_series(id)
);


CREATE TABLE ratings (
    userId INT,
    rating DECIMAL(2,1),
    "date" TIMESTAMP,
    movieId VARCHAR(12),
    FOREIGN KEY (movieId) REFERENCES movies_and_series(id)
);
