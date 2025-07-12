import boto3, json, typing, os


def test_lambda(*, FunctionName:str=None, payload:typing.Mapping[str, str]=None):
    payloadStr = json.dumps(payload)
    payloadBytesArr = bytes(payloadStr, encoding='utf8')
    client = boto3.client('lambda')
    try:
        response = client.invoke(
            FunctionName=FunctionName,
            InvocationType="RequestResponse",
            Payload=payloadBytesArr
        )
        response_payload = response['Payload'].read().decode('utf-8')
        print(f"Response: {response_payload}")
    except Exception as e:
        print(f"Error invoking Lambda function: {e}")
        raise e
    

if __name__ == "__main__":
    if len(os.sys.argv) < 2:
        print("Usage: python test_lambda.py <function_name> [payload]")
        exit(1)
    
    # TODO: handle payload from command line
    # TODO: its using the default region, should be able to specify region?
    function_name = os.sys.argv[1]
    test_lambda(FunctionName=function_name)