psql --dbname=postgres -a -q -f ./createdb.sql
# psql --dbname=library -a -q -f ./backup.sql



export AUTH0_DOMAIN='hadi-alnehlawi.eu.auth0.com'
export ALGORITHMS=['RS256']
export API_AUDIENCE='library'

export DATABASE_URL="postgresql://admin:admin@localhost:5432/library"

export ADMIN_TOKEN=""
export ADMIN_TOKEN="$admin_token"

export USER_TOKEN=""
export USER_TOKEN="$user_admin_variable"
