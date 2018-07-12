import boto3
import io
import zipfile
import mimetypes

def lambda_handler(event, context):
    kpsns = boto3.resource('sns')
    kptopic = kpsns.Topic('arn:aws:sns:us-east-1:274271387344:kp_deploy_portfolio_topic')

    try:
        s3 = boto3.resource('s3')
        portfolio_bucket = s3.Bucket('portfolio.plkaushik.info')

        build_bucket = s3.Bucket('portfoliobuild.plkaushik.info')
        portfolio_zip = io.BytesIO()

        build_bucket.download_fileobj('buildkpportfolio.zip',portfolio_zip)

        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj =myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj,nm,
                    ExtraArgs={'ContentType':mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

        kptopic.publish( Message="Portfolio deployed successfully", Subject ="Portfolio Deployed")

    except:
        kptopic.publish( Message="Oops....this Portfolio deployment failed", Subject ="Portfolio Deploy Failed")
        raise

    return 'Hello from Lambda'
