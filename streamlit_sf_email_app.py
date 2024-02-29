# Snow-Mail - GUI mail box for Snowflake Users!
# Make sure to alter the secrets.toml file path as per the setup
# 'C:/Users/DineshBabu/.streamlit/secrets.toml'
# config.toml has been configured for theme

# stream lit Library Import
import streamlit as st

# Aligning Snowflake Logo and App Name in the same line
col1,mid,col2 = st.columns([1,1,20])
with col1:
    st.image('snow.png', width=60)
# Used markdown for the custom color and font
with col2:
    st.markdown(f'<h1 style="color:#86b6fc;font-family:monospace;text-align:left;font-size:44px;">{"Snow-mail"}</h1>', unsafe_allow_html=True)

# App usage info
st.info('This Streamlit App can be used to send mail to Users only within Snowflake!', icon="ℹ️")

# Snowflake Connection Parameter Markdown
st.markdown("Enter the Snowflake Connection Parameters:")

# Account Name Input
acc_name = st.text_input("Account name")

# Alinging Username, Password, Role Name and Warehouse together
username, password, role_name, warehouse = st.columns(4)
with username:
    user = st.text_input("User name")
with password:
    pwd = st.text_input("Password",type='password') 
with role_name:
    role = st.text_input("Role") 
with warehouse:
    wh = st.text_input("Default Warehouse")

# Building the scecrets.toml file based on the inputs passed
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

# Test connection button to validate the credentials
test_con = st.button("Test Connection")
if test_con:
    #Initialize Snowflake Connection
    conn = st.connection("snowflake")
    conn.__init__("snowflake")
    #Building the secrets.toml file with current credentails  
    with open('C:/Users/DineshBabu/.streamlit/secrets.toml','a') as file:
        file.truncate(0)
        file.write(secret)
    # Running a select statement in Snowflake to test the connection
    test_connection = conn.query("select 123 from dual;")    
    if test_connection.to_string(index=False, header=False) == '123':
        st.success('Valid Connection!', icon="✅")
    # Closing the current connection to handle new connection validation scenario
        conn._instance.close()
    else:
        st.error('Invalid Connection!', icon="🚨")
        conn._instance.close()

# Mail components markdown and inputs
st.markdown("Mail Components:")

email = st.text_input('To')
email_Subject = st.text_input('Subject')
email_body = st.text_area('Message')

# Send Email button to trigger an email
if st.button('Send Email'):
    # Iniatize a connection to snowfalke
    conn = st.connection("snowflake")
    conn.__init__("snowflake")
    # Using cursor to run Notification Integration creation if not exists 
    cur = conn.cursor()
    sql = "CREATE NOTIFICATION INTEGRATION IF NOT EXISTS  my_email_int TYPE = EMAIL ENABLED = TRUE;"
    cur.execute(sql)  
    # Calling the Stored Procedure in Snowflake using the Mail Components Input  
    df = conn.query("CALL SYSTEM$SEND_EMAIL('my_email_int','"+email+"','"+email_Subject+"','"+email_body+"')")
    
    # Output Message based on the result.
    if df.to_string(index=False, header=False) == 'True':
        st.success('Email Sent Successfully!', icon="✅")
    else:
        st.error('This is an error', icon="🚨")
