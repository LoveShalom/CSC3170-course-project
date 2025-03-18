"""
Time: 2024/11/15
Author: Deng Yifan

This is the list of info type and client type, it used for the convenience of message transport.
"""

# client type
Res = "restaurant"
Cli = "client"
Man = "manager"

# Basic message type
log_mes = "login"
regis_mes = "register"
exit_mes = "Exit"

# Client message type
get_client_info = "Get my info"
modify_client_info = "Modify my info"
balance_info = "Get and modify balance"
recent_order_mes = "recent order"
today_order_mas = "Today order"
make_order_mes = "Make order"
refund_mes = "Make refund"

# restaurant message type
get_res_info = "Get res info"
modify_res_info = "Modify res info"

get_food_info = "Get food info"
modify_food_info = "Modify food info"
add_food_info = "Add food"
delete_food_info = "Delete food"

get_employees_info = "Get employees info"
modify_employees_info = "Modify employees info"
add_employees_info = "Add employees"
delete_employees_info = "Delete employees"

new_order_info = "Receive new order!"
order_status_info = "Change order status."

req_refund = "Get request to refund"

# manager message type
req_info_res = "Get request to show restaurant info"
req_info_food = "Get request to show food info"
req_info_employees = "Get request to show employees info"
req_info_order = "Get request to show order"
req_info_manager = "Get request to show manager"

resignation_mes = "manager will resign"

get_workstudy_mes = "Get work-study students info"
modify_workstudy = "Modify work-study students info"
