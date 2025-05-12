-- Create table to store sensor information
CREATE TABLE IF NOT EXISTS sensors (
    _id SERIAL PRIMARY KEY,  -- Unique identifier for each sensor
    _name VARCHAR(255) NOT NULL,  -- Sensor name
    _type VARCHAR(100),  -- Sensor type (e.g., temperature, pressure)
    _location VARCHAR(255),  -- Physical location of the sensor
    _status VARCHAR(50) DEFAULT 'active'  -- Sensor status (active, inactive, etc.)
);

-- Create table to store sensor readings
CREATE TABLE IF NOT EXISTS readings (
    reading_id SERIAL PRIMARY KEY,  -- Unique identifier for each reading
    _id INT REFERENCES sensors(_id) ON DELETE CASCADE,  -- Foreign key referencing the sensors table
    _value NUMERIC NOT NULL,  -- Measurement value
    _timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Timestamp of the reading
    _unit VARCHAR(50),  -- Unit of measurement (e.g., °C, psi)
    status VARCHAR(50) DEFAULT 'valid'  -- Reading status (valid, failed, etc.)
);

-- Create an index on the timestamp column to improve query performance
CREATE INDEX IF NOT EXISTS idx_sensor_readings_timestamp ON readings (_timestamp);
