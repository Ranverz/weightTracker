CREATE TABLE IF NOT EXISTS exercises (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    name TEXT NOT NULL,
    day_of_week INT NOT NULL CHECK (day_of_week BETWEEN 0 AND 6),
    default_unit TEXT NOT NULL DEFAULT 'kg' CHECK (default_unit IN ('kg', 'plates')),
    default_weight NUMERIC(6,2),
    default_reps INT,
    default_sets INT
);

CREATE TABLE IF NOT EXISTS workouts (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    exercise_id INT REFERENCES exercises(id) ON DELETE CASCADE,
    weight NUMERIC(6,2) NOT NULL,
    weight_unit TEXT NOT NULL DEFAULT 'kg' CHECK (weight_unit IN ('kg', 'plates')),
    reps INT NOT NULL,
    sets INT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS weights (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    weight NUMERIC(6,2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_exercises_user_day
    ON exercises (user_id, day_of_week);

CREATE INDEX IF NOT EXISTS idx_workouts_user_exercise_time
    ON workouts (user_id, exercise_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_weights_user_time
    ON weights (user_id, created_at DESC);
