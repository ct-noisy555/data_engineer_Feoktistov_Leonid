CREATE TABLE "users"(
    "id" bigserial NOT NULL,
    "email" VARCHAR(50) NOT NULL,
    "phone" VARCHAR(20) NOT NULL,
    "nickname" VARCHAR(30) NOT NULL,
    "registration_date" TIMESTAMP(0) WITH
        TIME zone NOT NULL,
        "topics_count" INTEGER NULL,
        "messages_count" INTEGER NULL,
        "created_at" TIMESTAMP(0)
    WITH
        TIME zone NOT NULL,
        "updated_at" TIMESTAMP(0)
    WITH
        TIME zone NOT NULL
);

CREATE INDEX "users_registration_date_index" ON
    "users"("registration_date");
ALTER TABLE
    "users" ADD PRIMARY KEY("id");

CREATE TABLE "topic"(
    "id" bigserial NOT NULL,
    "user_id" bigint NOT NULL,
    "title" VARCHAR(100) NOT NULL,
    "deleted_at" TIMESTAMP(0) WITH
        TIME zone NULL,
        "created_at" TIMESTAMP(0)
    WITH
        TIME zone NOT NULL,
        "updated_at" TIMESTAMP(0)
    WITH
        TIME zone NOT NULL
);

CREATE INDEX idx_topic_user_id ON topic(user_id);
CREATE INDEX idx_topic_created_at ON topic(created_at);
CREATE INDEX idx_topic_deleted_at ON topic(deleted_at);

ALTER TABLE
    "topic" ADD PRIMARY KEY("id");

CREATE TABLE "messages"(
    "id" bigserial NOT NULL,
    "topic_id" bigint NOT NULL,
    "user_id" bigint NULL,
    "content" TEXT NOT NULL,
    "created_at" TIMESTAMP(0) WITH
        TIME zone NOT NULL,
        "updated_at" TIMESTAMP(0)
    WITH
        TIME zone NOT NULL
);

CREATE INDEX idx_messages_topic_id ON messages(topic_id);
CREATE INDEX idx_messages_user_id ON messages(user_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
ALTER TABLE 
    "messages" ADD PRIMARY KEY("id");

CREATE TABLE "logs"(
    "id" bigserial NOT NULL,
    "user_id" bigint NULL,
    "topic_id" bigint NULL,
    "message_id" bigint NULL,
    "action_type" VARCHAR(20) NOT NULL,
    "server_response" BOOLEAN NOT NULL,
    "action_date" TIMESTAMP(0) WITH
        TIME zone NOT NULL
);

CREATE INDEX idx_logs_user_id ON logs(user_id);
CREATE INDEX idx_logs_topic_id ON logs(topic_id);
CREATE INDEX idx_logs_message_id ON logs(message_id);
CREATE INDEX idx_logs_date ON logs(action_date);
CREATE INDEX idx_logs_action_type ON logs(action_type);
CREATE INDEX idx_logs_date_action ON logs(action_date, action_type);