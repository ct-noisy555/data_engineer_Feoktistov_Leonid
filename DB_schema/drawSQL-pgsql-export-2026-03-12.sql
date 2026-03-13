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
CREATE INDEX "topic_user_id_created_at_deleted_at_index" ON
    "topic"(
        "user_id",
        "created_at",
        "deleted_at"
    );
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
CREATE INDEX "messages_topic_id_user_id_created_at_index" ON
    "messages"("topic_id", "user_id", "created_at");
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
CREATE INDEX "logs_action_date_index" ON
    "logs"("action_date");
CREATE INDEX "logs_action_type_index" ON
    "logs"("action_type");
CREATE INDEX "logs_server_response_index" ON
    "logs"("server_response");
ALTER TABLE
    "logs" ADD PRIMARY KEY("id");
ALTER TABLE
    "logs" ADD CONSTRAINT "logs_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");
ALTER TABLE
    "logs" ADD CONSTRAINT "logs_topic_id_foreign" FOREIGN KEY("topic_id") REFERENCES "topic"("id");
ALTER TABLE
    "messages" ADD CONSTRAINT "messages_topic_id_foreign" FOREIGN KEY("topic_id") REFERENCES "topic"("id");
ALTER TABLE
    "logs" ADD CONSTRAINT "logs_message_id_foreign" FOREIGN KEY("message_id") REFERENCES "messages"("id");
ALTER TABLE
    "topic" ADD CONSTRAINT "topic_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");