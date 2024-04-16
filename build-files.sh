echo "Running build files..."
echo "Building project packages..."
python3 -m pip install -r requirements.txt

echo "Migrating Database..."
python3 manage.py makemigrations
python3 manage.py migrate

echo "Collecting Static Files..."
python3 manage.py collectstatic --no-input --clear