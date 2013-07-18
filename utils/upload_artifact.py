import requests
import argparse
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import uuid
import json


parser = argparse.ArgumentParser(description="Upload a file as an Alexandria artifact")
parser.add_argument('artifact_type', type=str, nargs=1)
parser.add_argument('artifact_uri', type=str, nargs=1)
parser.add_argument('build_id', type=int, nargs=1)
parser.add_argument('username', type=str, nargs=1)
parser.add_argument('api_key', type=str, nargs=1)
parser.add_argument('--host', type=str, default="http://localhost:8000/")
parser.add_argument('--pass_through', action='store_true')
parser.add_argument('-k', '--aws_key', type=str)
parser.add_argument('-s', '--aws_secret', type=str)
parser.add_argument('-b', '--bucket', type=str)
args = parser.parse_args()

if args.host[-1:] != "/":
	print args.host[-1:]
	args.host += "/"

args.artifact_type = args.artifact_type[0].strip()
args.artifact_uri = args.artifact_uri[0].strip()
args.build_id = args.build_id[0]
args.username = args.username[0].strip()
args.api_key = args.api_key[0].strip()

print args

if not args.pass_through:
	random_uuid = str(uuid.uuid4())
	print "Uploading contents of %s to S3. Bucket is %s, and storage key is %s." % (args.artifact_uri, args.bucket, random_uuid)
	s3 = S3Connection(args.aws_key, args.aws_secret)
	bucket = s3.get_bucket(args.bucket)
	storage_key = Key(bucket)
	storage_key.key = random_uuid
	storage_key.set_contents_from_filename(args.artifact_uri)
	storage_key.make_public()

	dl_url = "https://s3.amazonaws.com/%s/%s" % (args.bucket, random_uuid)

	post_data = {'type': args.artifact_type, 'build': args.build_id, 'download_url': dl_url, 'username': args.username, 'api_key': args.api_key, 'format':'json'}

	post_url = args.host + "api/v0/artifact/?username=%s&api_key=%s" % (args.username, args.api_key)

	print "Posting artifact..."
	r = requests.post(post_url, data=json.dumps(post_data), headers={'content-type':'application/json'})
	if r.status_code >= 400:
		print "Status code was: " + str(r.status_code)
		print "Post returned: \n" + r.text
		exit(1)
	print "Done"

else:
	payload = open(args.artifact_uri, 'rb')
	artifact_data = {'build_id': args.build_id, 'type': args.artifact_type}
	api_header = "ApiKey: %s:%s" % (args.username, args.api_key)
	post_url = args.host + "upload/"
	p = requests.post(post_url, data=artifact_data, headers={"Authorization": api_header}, files={'payload': payload})
	if p.status_code >= 400:
		print "Status code was: " + str(p.status_code)
		#print "Post returned: \n" + p.text
		f = open("out", "w")
		f.write(p.text)
		f.close()
		exit(1)
	print "Done"