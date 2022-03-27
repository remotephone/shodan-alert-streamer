# Shodan Alert Streamer

You'll need
- A Shodan API key
- An AWS SNS enabled access key and secret key
- A docker or place to run stacks


## AWS Permissions

I created the following policy, assigned it to a group, and added an IAM user to the group.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "SendMeTexts",
            "Effect": "Allow",
            "Action": "sns:Publish",
            "Resource": "arn:aws:sns:us-west-1:123456789012:my-topic"
        }
    ]
}
```
