# Result containing slave status data
RESULT1 = [{
    'slave': ({
        'Replicate_Wild_Do_Table': '',
        'Master_SSL_CA_Path': '',
        'Last_Error': '',
        'Until_Log_File': '',
        'Seconds_Behind_Master': None,
        'Master_User': 'zenoss',
        'Master_Port': 3306L,
        'Until_Log_Pos': 0L,
        'Master_Log_File': 'mysql-bin.000003 ',
        'Read_Master_Log_Pos': 98L,
        'Replicate_Do_DB': '',
        'Master_SSL_Verify_Server_Cert': 'No',
        'Exec_Master_Log_Pos': 98L,
        'Replicate_Ignore_Server_Ids': '',
        'Replicate_Ignore_Table': '',
        'Master_Server_Id': 0L,
        'Relay_Log_Space': 233L,
        'Last_SQL_Error': '',
        'Relay_Master_Log_File': 'mysql-bin.000003 ',
        'Master_SSL_Allowed': 'No',
        'Master_SSL_CA_File': '',
        'Slave_IO_State': '',
        'Relay_Log_File': 'localhost-relay-bin.000001',
        'Replicate_Ignore_DB': '',
        'Last_IO_Error': '',
        'Until_Condition': 'None',
        'Replicate_Do_Table': '',
        'Last_Errno': 0L,
        'Master_Host': '127.0.0.1',
        'Master_SSL_Key': '',
        'Skip_Counter': 0L,
        'Slave_SQL_Running': 'No',
        'Relay_Log_Pos': 4L,
        'Master_SSL_Cert': '',
        'Last_IO_Errno': 0L,
        'Slave_IO_Running': 'No',
        'Connect_Retry': 60L,
        'Last_SQL_Errno': 0L,
        'Replicate_Wild_Ignore_Table': '',
        'Master_SSL_Cipher': ''
    },),
    'db': ({
        'title': 'information_schema',
        'default_collation_name': 'utf8_general_ci',
        'index_size': 9216,
        'table_count': 40L,
        'data_size': 0,
        'default_character_set_name': 'utf8',
        'size': 9216
    },),
    'server': (
        {'Value': '7789', 'Variable_name': 'Handler_read_first'},
        {'Value': '52902', 'Variable_name': 'Handler_read_key'},
        {'Value': '27003', 'Variable_name': 'Handler_read_last'},
        {'Value': '4666', 'Variable_name': 'Handler_read_next'},
        {'Value': '0', 'Variable_name': 'Handler_read_prev'},
        {'Value': '545', 'Variable_name': 'Handler_read_rnd'},
        {'Value': '25922', 'Variable_name': 'Handler_read_rnd_next'}
    ),
    'master': (),
    'server_size': ({
        'index_size': 4143104,
        'data_size': 53423729,
        'size': 57566833
    },),
    'version': (
        {'Value': '5.5.28', 'Variable_name': 'version'},
        {'Value': 'MySQL Community Server (GPL)',
            'Variable_name': 'version_comment'},
        {'Value': 'i686', 'Variable_name': 'version_compile_machine'},
        {'Value': 'Linux', 'Variable_name': 'version_compile_os'}
    ),
    'id': 'root_3306'}
]
# -------------------------------------------------------------------------
# Server results
SERVER_STATUS1 = (
    {'Value': '7789', 'Variable_name': 'Handler_read_first'},
    {'Value': '52902', 'Variable_name': 'Handler_read_key'},
    {'Value': '27003', 'Variable_name': 'Handler_read_last'},
    {'Value': '4666', 'Variable_name': 'Handler_read_next'},
    {'Value': '0', 'Variable_name': 'Handler_read_prev'},
    {'Value': '545', 'Variable_name': 'Handler_read_rnd'},
    {'Value': '25922', 'Variable_name': 'Handler_read_rnd_next'}
)
SERVER_STATUS2 = (
    {'Value': '0', 'Variable_name': 'Handler_read_first'},
    {'Value': '0', 'Variable_name': 'Handler_read_key'},
    {'Value': '0', 'Variable_name': 'Handler_read_last'},
    {'Value': '0', 'Variable_name': 'Handler_read_next'},
    {'Value': '0', 'Variable_name': 'Handler_read_prev'},
    {'Value': '0', 'Variable_name': 'Handler_read_rnd'},
    {'Value': '0', 'Variable_name': 'Handler_read_rnd_next'}
)
# -------------------------------------------------------------------------
# Master results
MASTER_STATUS1 = ({
    'File': 'mysql-bin.000002',
    'Position': '107',
    'Binlog_Do_DB': '',
    'Binlog_Ignore_DB': '',
},)
MASTER_STATUS2 = ()
# -------------------------------------------------------------------------
# Slave results
SLAVE_STATUS1 = ({
    'Replicate_Wild_Do_Table': '',
    'Master_SSL_CA_Path': '',
    'Last_Error': '',
    'Until_Log_File': '',
    'Seconds_Behind_Master': 10,
    'Master_User': 'zenoss',
    'Master_Port': 3306L,
    'Until_Log_Pos': 0L,
    'Master_Log_File': 'mysql-bin.000003 ',
    'Read_Master_Log_Pos': 98L,
    'Replicate_Do_DB': '',
    'Master_SSL_Verify_Server_Cert': 'No',
    'Exec_Master_Log_Pos': 98L,
    'Replicate_Ignore_Server_Ids': '',
    'Replicate_Ignore_Table': '',
    'Master_Server_Id': 0L,
    'Relay_Log_Space': 233L,
    'Last_SQL_Error': '',
    'Relay_Master_Log_File': 'mysql-bin.000003 ',
    'Master_SSL_Allowed': 'No',
    'Master_SSL_CA_File': '',
    'Slave_IO_State': '',
    'Relay_Log_File': 'localhost-relay-bin.000001',
    'Replicate_Ignore_DB': '',
    'Last_IO_Error': '',
    'Until_Condition': 'None',
    'Replicate_Do_Table': '',
    'Last_Errno': 0L,
    'Master_Host': '127.0.0.1',
    'Master_SSL_Key': '',
    'Skip_Counter': 0L,
    'Slave_SQL_Running': 'No',
    'Relay_Log_Pos': 4L,
    'Master_SSL_Cert': '',
    'Last_IO_Errno': 0L,
    'Slave_IO_Running': 'No',
    'Connect_Retry': 60L,
    'Last_SQL_Errno': 0L,
    'Replicate_Wild_Ignore_Table': '',
    'Master_SSL_Cipher': ''
},)
SLAVE_STATUS2 = ()
# -------------------------------------------------------------------------
# Version results
VERSION1 = (
    {'Value': '5.5.28', 'Variable_name': 'version'},
    {'Value': 'MySQL Community Server (GPL)',
        'Variable_name': 'version_comment'},
    {'Value': 'i686', 'Variable_name': 'version_compile_machine'},
    {'Value': 'Linux', 'Variable_name': 'version_compile_os'}
)
