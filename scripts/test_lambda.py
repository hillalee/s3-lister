import boto3, json, typing

def test_lambda(*, FunctionName:str=None, payload:typing.Mapping[str, str]=None):
    if FunctionName == None:
        raise Exception('ERROR: FunctionName parameter cannot be NULL')
    payloadStr = json.dumps(payload)
    payloadBytesArr = bytes(payloadStr, encoding='utf8')
    client = boto3.client('lambda')
    return client.invoke(
        FunctionName=FunctionName,
        InvocationType="RequestResponse",
        Payload=payloadBytesArr
    )