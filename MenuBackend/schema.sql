-- *! Deprecated

CREATE DATABASE restaurants;
USE restaurants;
-- Restaurant table
CREATE TABLE restaurant (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Use INT AUTO_INCREMENT in MySQL
    name VARCHAR(255) UNIQUE NOT NULL,
    address VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    email VARCHAR(100),
    website VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Menu table
CREATE TABLE menu (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Use INT AUTO_INCREMENT
    restaurant_id INT NOT NULL,  -- Ensure this is of type INT to match restaurant.id
    name VARCHAR(255),
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_restaurant_menu FOREIGN KEY (restaurant_id)
        REFERENCES restaurant(id) ON DELETE CASCADE
);

-- Menu Section table
CREATE TABLE menu_section (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Use INT AUTO_INCREMENT
    menu_id INT NOT NULL,
    name VARCHAR(255),
    description TEXT,
    position INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_menu_menu_section FOREIGN KEY (menu_id)
        REFERENCES menu(id) ON DELETE CASCADE
);

-- Menu Item table
CREATE TABLE menu_item (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Use INT AUTO_INCREMENT
    menu_section INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    is_available BOOLEAN DEFAULT TRUE,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_menu_section_menu_item FOREIGN KEY (menu_section)
        REFERENCES menu_section(id) ON DELETE CASCADE
);

-- Full-text index for menu_item on name and description (MySQL specific)
CREATE FULLTEXT INDEX ft_index_name_description
    ON menu_item(name, description);

-- Dietary Restriction table
CREATE TABLE dietary_restriction (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Use INT AUTO_INCREMENT
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
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Use INT AUTO_INCREMENT
    menu_id INT NOT NULL,
    action VARCHAR(255),
    description TEXT,
    action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    performed_by VARCHAR(255),
    CONSTRAINT fk_menu_processing_log FOREIGN KEY (menu_id)
        REFERENCES menu(id) ON DELETE CASCADE
);
