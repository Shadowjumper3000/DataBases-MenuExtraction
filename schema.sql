-- Restaurant table
CREATE TABLE restaurant (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    address VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    email VARCHAR(100),
    website VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Menu table
CREATE TABLE menu (
    id SERIAL PRIMARY KEY,
    restaurant_id INT NOT NULL,
    name VARCHAR(255),
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_restaurant_menu FOREIGN KEY (restaurant_id)
        REFERENCES restaurant(id) ON DELETE CASCADE
);

-- Menu Section table
CREATE TABLE menu_section (
    id SERIAL PRIMARY KEY,
    menu_id INT NOT NULL,
    name VARCHAR(255),
    description TEXT,
    position INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_menu_menu_section FOREIGN KEY (menu_id)
        REFERENCES menu(id) ON DELETE CASCADE
);

-- Menu Item table
CREATE TABLE menu_item (
    id SERIAL PRIMARY KEY,
    menu_section INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    is_available BOOLEAN DEFAULT TRUE,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_menu_section_menu_item FOREIGN KEY (menu_section)
        REFERENCES menu_section(id) ON DELETE CASCADE
);

-- Full-text index for menu_item on name and description
CREATE INDEX ft_index_name_description
    ON menu_item USING gin (to_tsvector('english', name || ' ' || description));

-- Dietary Restriction table
CREATE TABLE dietary_restriction (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT
);

-- Item Restrictions table
CREATE TABLE item_restrictions (
    menu_item_id INT NOT NULL,
    dietary_restriction_id INT NOT NULL,
    PRIMARY KEY (menu_item_id, dietary_restriction_id),
    CONSTRAINT fk_menu_item_item_restrictions FOREIGN KEY (menu_item_id)
        REFERENCES menu_item(id) ON DELETE CASCADE,
    CONSTRAINT fk_dietary_restriction_item_restrictions FOREIGN KEY (dietary_restriction_id)
        REFERENCES dietary_restriction(id) ON DELETE CASCADE
);

-- Processing Log table
CREATE TABLE processing_log (
    id SERIAL PRIMARY KEY,
    menu_id INT NOT NULL,
    action VARCHAR(255),
    description TEXT,
    action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    performed_by VARCHAR(255),
    CONSTRAINT fk_menu_processing_log FOREIGN KEY (menu_id)
        REFERENCES menu(id) ON DELETE CASCADE
);
