import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)

def predict_diabetes(pregnancies, plasma_glucose, diastolic_blood_pressure, triceps_thickness, serum_insulin, bmi, diabetes_pedigree, age):

    data =  {
      "input_data": [
        [
          pregnancies,
          plasma_glucose,
          diastolic_blood_pressure,
          triceps_thickness,
          serum_insulin,
          bmi,
          diabetes_pedigree,
          age
        ]
      ],
      "params": {}
    }

    body = str.encode(json.dumps(data))

    url = 'https://diabetesend.eastus.inference.ml.azure.com/score'
    # Replace this with the primary/secondary key, AMLToken, or Microsoft Entra ID token for the endpoint
    api_key = os.getenv('pass')
    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    # The azureml-model-deployment header will force the request to go to a specific deployment.
    # Remove this header to have the request observe the endpoint traffic rules
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'diabetesdeployment1' }

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
    except urllib.error.HTTPError as error:
        raise Exception("The request failed with status code: " + str(error.code))
    return json.loads(result)[0]
