-- Sample data for Real Estate Platform

-- Insert sample apartments
INSERT INTO apartments (title, location, type, total_parts, description, rent_price, created_at) VALUES
('Downtown Luxury Apartments', 'Downtown City Center', 'rent', 10, 'Modern apartments in the heart of the city with all amenities', 2500.00, NOW()),
('Seaside Villa Complex', 'Oceanview Boulevard', 'rent', 5, 'Beautiful villas with ocean views and private gardens', 4000.00, NOW()),
('City Center Office Building', 'Business District', 'purchase', NULL, 'Premium office building perfect for businesses', 1500000.00, NOW()),
('Suburban Family Homes', 'Green Valley Suburb', 'rent', 8, 'Family-friendly homes in quiet neighborhood', 1800.00, NOW());

-- Note: You'll need to create super admin first using create_super_admin.py
-- This script only creates sample apartments
