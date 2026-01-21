-- Database select karein
USE college_event;

-- Purana panic data delete karein taaki error na aaye
SET sql_safe_updates = 0;
DELETE FROM admin_knowledge WHERE trigger_word IN ('panic', 'relationship', 'breakup', 'heartbreak');
SET sql_safe_updates = 1;

-- Sahi Syntax ke sath relationship data insert karein
INSERT INTO admin_knowledge (trigger_word, response, emotion) VALUES 
('panic', 'Aap ek jagah baith jayein aur gana sune jo apko acha lagta hai.', 'calm'),
('relationship', 'Rishte trust aur samajh par tikte hain. Communication sabse behtar solution hai.', 'emotional'),
('breakup', 'Breakup ka dard gehra hota hai, lekin ye ant nahi hai. Khud ko waqt dein.', 'sad'),
('heartbreak', 'Dil tutna mushkil hai, par isse aap aur strong banenge. Feelings ko share karein.', 'hurt'),
('toxic relationship', 'Aapki mental peace sabse zaroori hai. Aise rishte se nikalna behtar hai.', 'stressed'),
('one sided love', 'Kisi ko chahna galat nahi, par khud ko khokar nahi. Aap barabar ka pyaar deserve karte hain.', 'lonely'),
('trust issues', 'Bharosa tutne par wapas judne mein waqt lagta hai. Apne partner se baat karein.', 'anxious'),
('cheating', 'Dhoka milna aapki galti nahi hai. Is waqt apni self-worth par focus karein.', 'angry'),
('single', 'Single hona ek mauka hai khud ko janne ka. Apne passion par dhyan dein.', 'neutral');

-- Data check karne ke liye ye query chalayein
SELECT * FROM admin_knowledge;

-- 1. Pehle Users table banayein
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);

-- 2. Chat History ko modify karein Relationship add karne ke liye
ALTER TABLE chat_history ADD COLUMN user_id INT AFTER id;

ALTER TABLE chat_history 
ADD CONSTRAINT fk_user_id 
FOREIGN KEY (user_id) REFERENCES users(user_id) 
ON DELETE CASCADE;