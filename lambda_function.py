import json
import boto3

bedrock = boto3.client("bedrock-runtime")

resume_summary = """
Cloud Engineer with AWS knowledge.
Skills learning: S3, CloudFront, Lambda, Bedrock, Python.
6+ years in Software Testing, QA, and Web Development.
Built AI chatbot using AWS serverless architecture.
"""

def lambda_handler(event, context):
    body = json.loads(event["body"])
    question = body.get("question", "")

    prompt = f"""
You are a recruiter assistant.

Candidate:
{resume_summary}

Question: {question}

Answer in 2 short sentences.
"""

    response = bedrock.invoke_model(
        modelId="amazon.nova-lite-v1:0",
        body=json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"text": prompt}
                    ]
                }
            ],
            "inferenceConfig": {
                "maxTokens": 150,
                "temperature": 0.5
            }
        }),
        contentType="application/json"
    )

    result = json.loads(response["body"].read())

    answer = result["output"]["message"]["content"][0]["text"]

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "answer": answer
        })
    }
