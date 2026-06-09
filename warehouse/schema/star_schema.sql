-- DIMENSIONS

CREATE TABLE dim_provider (
    provider_id INT PRIMARY KEY,
    provider_name VARCHAR(50)
);

CREATE TABLE dim_team (
    team_id INT PRIMARY KEY,
    team_name VARCHAR(100)
);

CREATE TABLE dim_model (
    model_id INT PRIMARY KEY,
    model_name VARCHAR(100),
    provider_name VARCHAR(50)
);

CREATE TABLE dim_user (
    user_id VARCHAR(100) PRIMARY KEY,
    team_name VARCHAR(100)
);

-- FACT TABLE

CREATE TABLE fact_ai_usage (
    usage_id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    user_id VARCHAR(100),
    provider_name VARCHAR(50),
    model_name VARCHAR(100),
    team_name VARCHAR(100),
    prompt_tokens INT,
    completion_tokens INT,
    total_tokens INT,
    cost_usd DECIMAL(12,4)
);