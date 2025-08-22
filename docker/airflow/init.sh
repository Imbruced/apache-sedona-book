echo "Initializing Airflow database..."
password=$(cat standalone_admin_password.txt)

echo "Airflow admin user: admin with password: $password"

airflow connections add spark \
    --conn-type spark \
    --conn-host local[*]