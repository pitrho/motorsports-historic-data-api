#!/bin/bash

BASE_DIR=`dirname $0`

echo ""
echo "This script starts all the services needed to develop the"
echo "motorsports API locally."
echo "-------------------------------------------------------------------"

# Default parameters
#
HOST="127.0.0.1"
PORT="5000"
PROCFILE="bin/procfiles/Procfile.dev"

# Parse the command line flags.
#
while getopts ":np:f:" opt; do
  case $opt in
    n)
      # Get the IP address on a mac.  Only works on a mac.
      #
      HOST=`ifconfig | grep -E 'inet.[0-9]' | grep -v '127.0.0.1' | awk '{ print $2}'|head -n1`
      ;;

    p)
      # Set the port
      #
      PORT=${OPTARG}
      ;;

    f)
      # Set the Procfile
      #
      PROCFILE=${OPTARG}
      if [[ ! -e "$PROCFILE" ]]; then
        die "...your specified $PROCFILE does not exist"
      fi
      ;;

    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

# Custom die function.
#
die() { echo >&2 -e "\nRUN ERROR: $@\n"; exit 1; }

# Check for required programs: Postgres.app, honcho
#
HONCHO=$(command -v honcho || command -v foreman || die "...Error: honcho/foreman is not in your path!  Are you in the right virtualenv?")
POSTGRES="/Applications/Postgres.app"
if [ ! -d "$POSTGRES" ]; then
    die "...Error: cannot find Postgres.app"
fi

# Check for .env file
#
if [[ ! -e "$BASE_DIR/../.env" ]]; then
	die "...You need to have a .env file at $BASE_DIR/../.env"
fi


# Print config
#
echo ""
echo "Configuration:"
echo -e "\tPROCFILE: $PROCFILE"
echo -e "\tHONCO: $HONCO"
echo -e "\tPOSTGRES: $POSTGRES"
echo -e "\tHOST: $HOST"
echo -e "\tPORT: $PORT"
echo -e "\tPATH: $PATH"
echo ""
echo "-------------------------------------------------------------------"

# Start Postgres, which daemonizes, so cannot be used
# with foreman/honcho
#
open $POSTGRES

# Start the other processes.  See bin/Procfile.dev
#
HOST=$HOST PORT=$PORT $HONCHO start -f $PROCFILE

