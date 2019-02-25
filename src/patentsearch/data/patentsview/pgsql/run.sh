#!/usr/bin/env bash

# set -euo pipefail
DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi

# we will be keeping the resulting .csv in the scripts folder ready to be imported
SQL_SCRIPTS_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )/sql/" && pwd )"

ERROR="$DIR/err.txt"

docker ps 2 >"$ERROR" 1>/dev/null
if [ -z "$(cat "$ERROR"| grep "permission denied")" ]; then
  dockercommand="docker"
else
  dockercommand="sudo docker"
fi
status="$(${dockercommand} ps -a| grep ps-postgres)"
if [ -z "$status" ];then
  $dockercommand run -v "$SQL_SCRIPTS_FOLDER"/:/sql --name ps-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres
else
  $dockercommand rm -f ps-postgres
  $dockercommand run -v "$SQL_SCRIPTS_FOLDER"/:/sql --name ps-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres
fi
echo "error" > "$ERROR"
while [ ! -z "$(cat "$ERROR")" ]
do
    echo "Getting ready"
    $dockercommand run -e PGPASSWORD=mysecretpassword --rm --link ps-postgres:postgres postgres psql -h postgres -U postgres 2>"$ERROR"
done
echo "Ready"
rm -rf "$ERROR"
export CLIENT
CLIENT="$dockercommand run -v $SQL_SCRIPTS_FOLDER/:/sql -e PGPASSWORD=mysecretpassword --rm --link ps-postgres:postgres postgres psql -h postgres -U postgres"
# TOD
# bats "$DIR/tests.bats"
# for now, just create the single TABLE
$CLIENT -f /sql/brf_sum_text.sql
