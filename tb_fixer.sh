#!/bin/sh
USER_NAME=$1
sqlplus -s "/ as sysdba" <<EOF >$USER_NAME
whenever sqlerror exit sql.sqlcode;
set heading off
spool $USER_NAME.log
create user $USER_NAME identified by CIN2020#hq543#;
grant DBA to $USER_NAME;
spool off;
exit;
/
EOF
source /tmp/space_issues/space_issues/bin/activate
python /tmp/space_issues/space_issues/bin/disk_space.py $ORACLE_SID $USER_NAME

sqlplus -s "/ as sysdba" <<EOF >$USER_NAME
whenever sqlerror exit sql.sqlcode;
set heading off
spool $USER_NAME.log append
drop user $USER_NAME;
spool off;
exit;
/
EOF

#sh tb_fix.sh INC0865903
