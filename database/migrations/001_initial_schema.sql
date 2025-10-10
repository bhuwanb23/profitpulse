-- Migration: 001_initial_schema.sql
-- Description: Initial database schema for SuperHack AI Platform
-- Created: 2024-03-15
-- Version: 1.0.0

-- This migration creates the initial database structure
-- Run this after creating the database

-- The schema is already defined in database/schemas/init.sql
-- This file serves as a migration record

-- To apply this migration:
-- 1. Create the database: createdb superhack_db
-- 2. Run the schema: psql -d superhack_db -f database/schemas/init.sql
-- 3. Optionally load sample data: psql -d superhack_db -f database/seeds/sample_data.sql

-- Migration completed successfully
SELECT 'Migration 001_initial_schema completed' as status;
