echo "Initializing Airflow database..."
password=$(cat standalone_admin_password.txt)

echo "Airflow admin user: admin with password: $password"

sed -i -e "s|<AWS_ACCESS_KEY_ID>|$AWS_ACCESS_KEY_ID|g" -e "s|<AWS_SECRET_ACCESS_KEY>|$AWS_SECRET_ACCESS_KEY|g" /home/airflow/.local/lib/python3.12/site-packages/pyspark/conf/spark-defaults.conf

airflow connections add spark \
    --conn-type spark \
    --conn-host local[*]
