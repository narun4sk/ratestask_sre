#! /bin/bash --

set -e

HOST="$1"
PORT="$2"
shift 2
CMD="$@"

until netcat -w1 -zv "${HOST}" "${PORT}"; do
  >&2 echo "Database on ${HOST}:${PORT} is unavailable"
  >&2 echo "Sleeping..."
  sleep 1
done

>&2 echo "Database is up - executing command:"
>&2 echo "# ${CMD}"
exec ${CMD}
