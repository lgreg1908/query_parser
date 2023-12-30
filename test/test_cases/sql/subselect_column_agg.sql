SELECT 
    u.id
    , (SELECT COUNT(*) FROM orders WHERE orders.user_id = u.id) as order_count
    , (SELECT AVG(amount) FROM payments WHERE payments.user_id = u.id) as average_payment
FROM users u 
WHERE u.registration_date BETWEEN '2020-01-01' AND '2020-12-31' AND (u.status = 'active' OR u.id IN (SELECT user_id FROM vip_users));