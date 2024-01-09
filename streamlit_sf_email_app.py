# streamlit_sf_email_app.py

import streamlit as st

st.info('This Streamlit App can be used to send mail to Users only within Snowflake!', icon="ℹ️")

# Snowflake functionality part starts
st.markdown("Enter the Snowflake Connection Parameters:")

acc_name = st.text_input("Account name")

username, password, role_name, warehouse = st.columns(4)
with username:
    user = st.text_input("User name")
with password:
    pwd = st.text_input("Password",type='password') 
with role_name:
    role = st.text_input("Role") 
with warehouse:
    wh = st.text_input("Default Warehouse")

if acc_name != '' and user != '' and pwd != '' and role != '' and wh != '':
    
    secret = f'''
    # .streamlit/secrets.toml
    [connections.snowflake]
    user = "{user}"
    password = "{pwd}"
    account = "{acc_name}"
    role = "{role}"
    warehouse = "{wh}" 
    client_session_keep_alive = "false"'''


    with open('C:/Users/DineshBabu/.streamlit/secrets.toml','a') as file:
        file.truncate(0)
        file.write(secret)

test_con = st.button("Test Connection")
if test_con:
    # Initialize connection.
    conn = st.connection("snowflake")    
    conn._instance.close()      
    with open('.streamlit/secrets.toml','a') as file:
        file.truncate(0)
        file.write(secret)
    test_connection = conn.query("select 123 from dual;")    
    if test_connection.to_string(index=False, header=False) == '123':
        st.success('Valid Connection!', icon="✅")
    else:
        st.error('Invalid Connection!', icon="🚨")

st.markdown("Mail Components")

email = st.text_input('To')
email_Subject = st.text_input('Subject')
email_body = st.text_area('Message')


if st.button('Send Email'):
    conn = st.connection("snowflake")
    conn.__init__("snowflake")
    cur = conn.cursor()
# Execute a statement that will generate a result set.
    sql = "CREATE NOTIFICATION INTEGRATION IF NOT EXISTS  my_email_int TYPE = EMAIL ENABLED = TRUE;"
    cur.execute(sql)    
    df = conn.query("CALL SYSTEM$SEND_EMAIL('my_email_int','"+email+"','"+email_Subject+"','"+email_body+"')")
    
    if df.to_string(index=False, header=False) == 'True':
        st.success('Email Sent Successfully!', icon="✅")
    else:
        st.error('This is an error', icon="🚨")