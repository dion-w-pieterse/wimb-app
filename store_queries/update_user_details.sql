-- :name update_user_details :affected
update user_details
set first_name = :first_name, 
    last_name = :last_name, 
    email = :email, 
    phone = :phone, 
    addr = :addr, 
    city = :city, 
    state = :state, 
    country = :country, 
    zip = :zip, 
    cc_type = :cc_type, 
    cc_num = :cc_num, 
    sec_num = :sec_num
where user_id = :user_id
