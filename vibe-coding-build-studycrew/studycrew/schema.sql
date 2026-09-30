-- StudyCrew database (Cloudflare D1). Only what's needed; rows are deleted after 14 days by the daily cron.
CREATE TABLE IF NOT EXISTS groups (
  id TEXT PRIMARY KEY,
  subject TEXT NOT NULL,
  chapter TEXT NOT NULL,
  slot TEXT NOT NULL,
  place TEXT NOT NULL,
  created_at INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS students (
  id TEXT PRIMARY KEY,
  key TEXT NOT NULL UNIQUE,
  first_name TEXT NOT NULL,
  class_name TEXT NOT NULL,
  subject TEXT NOT NULL,
  chapter TEXT NOT NULL,
  slots TEXT NOT NULL,
  group_id TEXT NOT NULL REFERENCES groups(id),
  created_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS groups_topic ON groups (subject, chapter);
CREATE INDEX IF NOT EXISTS students_group ON students (group_id);
