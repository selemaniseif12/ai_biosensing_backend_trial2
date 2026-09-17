CREATE TABLE IF NOT EXISTS cart_item (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    item_id TEXT NOT NULL,
    item_name TEXT NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    price_usd NUMERIC(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
