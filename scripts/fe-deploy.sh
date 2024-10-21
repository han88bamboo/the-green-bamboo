#!/usr/bin/env bash
set -x

workdir="$(pwd)"
me=$(basename "$0")

help_message="\

Usage: $me [<options>]
Deploy a static website to S3.

Options:

  -h, --help           Show this help information.
  -v, --verbose        Increase verbosity. Useful for debugging.
  -d, --dry-run        To test the deployment script.
  -c, --cf-id          The CloudFront distribution ID that we will deploy to.
  -s, --s3-bucket      The S3 bucket to store static content.
  -n, --domain-name    The website domain name, such as example.com.
  -t, --template       The website template name.
"

# Parse arg flags
parse_args() {
  # Set args from a local environment file, if any.
  if [[ -e ".env" ]]; then
    source .env
  fi

  # If something is exposed as an environment variable, set/overwrite it here.
  # Otherwise, set/overwrite the internal variable instead.
  while :; do
    if [[ $1 == "-h" || $1 == "--help" ]]; then
      echo "$help_message"
      exit 0
    elif [[ $1 == "-v" || $1 == "--verbose" ]]; then
      verbose=true
      shift
    elif [[ $1 == "-d" || $1 == "--dry-run" ]]; then
      dryrun=true
      shift
    elif [[ ($1 == "-c" || $1 == "--cf-id") && -n $2 ]]; then
      DISTRIBUTION_ID=$2
      shift 2
    elif [[ ($1 == "-s" || $1 == "--s3-bucket") && -n $2 ]]; then
      S3_BUCKET=$2
      shift 2
    elif [[ ($1 == "-n" || $1 == "--domain-name") && -n $2 ]]; then
      DOMAIN=$2
      shift 2
    elif [[ ($1 == "-t" || $1 == "--template") && -n $2 ]]; then
      TEMPLATE=$2
      shift 2
    else
      break
    fi
  done
}

# Echo expanded commands as they are executed (for debugging)
enable_expanded_output() {
  if [ $verbose ]; then
    set -o xtrace
    set +o verbose
  fi
}

# To avoid outputting the repo URL, which may contain a secret token
disable_expanded_output() {
  if [ $verbose ]; then
    set +o xtrace
    set -o verbose
  fi
}

main() {
  parse_args "$@"

  enable_expanded_output

  if [ ! "${DISTRIBUTION_ID}" ]; then
    echo "Env Var --cf-id not set!"
    exit 0
  fi

  if [ "${DOMAIN}" ]; then
    case "${DOMAIN}" in
    */)
      echo "Env Var --domain-name = ${DOMAIN}"
      ;;
    *)
      echo "Env Var --domain-name is set but doesn't have a ending-slash!"
      exit 0
      ;;
    esac
  fi

  if [ ! "${S3_BUCKET}" ]; then
    echo "Env Var --s3-bucket not set!"
    exit 0
  fi

  if [ ! "${TEMPLATE}" ]; then
    echo "Env Var --template not set!"
    exit 0
  fi

  cd "${workdir}/.."
  pwd
  echo "Building FE release..."

  if [[ -d "${workdir}/frontend/${TEMPLATE}" ]]; then
    echo "Template exists!!!"

    echo "Removing existing bucket content..."
    if [[ ${dryrun} ]]; then
      aws s3 rm "s3://${S3_BUCKET}/${DOMAIN}" --recursive --dryrun
    else
      aws s3 rm "s3://${S3_BUCKET}/${DOMAIN}" --recursive
    fi

    echo "Uploading new bucket content..."
    if [[ ${dryrun} ]]; then
      aws s3 sync "${workdir}/frontend/${TEMPLATE}" "s3://${S3_BUCKET}/${DOMAIN}" --exclude "LICENSE.txt" --exclude "README.txt" --dryrun
    else
      aws s3 sync "${workdir}/frontend/${TEMPLATE}" "s3://${S3_BUCKET}/${DOMAIN}" --exclude "LICENSE.txt" --exclude "README.txt"
    fi

    if [[ ! ${dryrun} ]]; then
      echo "Invalidate cloudfront objects after new deployment..."
      aws cloudfront create-invalidation --distribution-id "${DISTRIBUTION_ID}" --paths "/${DOMAIN}*"
    fi
  else
    echo "Template doesn't exists!!!"
    exit 0
  fi

}

[[ $1 == --source-only ]] || main "$@"
