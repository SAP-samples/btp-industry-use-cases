from flask import Flask, request
import json
import os
from ci_cd_pipeline import ci_cd_pipeline

app = Flask(__name__)

pipeline = ci_cd_pipeline()


@app.route('/v1/webhook',methods=['POST'])
def trigger():

    message = None
    data = dict(request.json)

    os.system('ls -l /mnt/models')

    print(data);
    modified_files = data['commits'][0]['modified']
    print("New commit by: {}".format(data['commits'][0]['author']['name']))
    print("File modified: {}".format(data['commits'][0]['modified']))
    print("File added:: {}".format(data['commits'][0]['added']))
    print("File removed: {}".format(data['commits'][0]['removed']))

    cond1 = False
    cond2 = False

    for file in modified_files:
        print(file)
        if "solution-prod-code/train" in file:
            cond1 = True
        if "solution-prod-code/infer" in file:
            cond2 = True
        print(cond1, cond2)
    
    if cond1 or cond2:
        print("Triggering CI/CD pipeline!")
        message = "Triggering CI/CD pipeline!"
        try:
            pipeline.run_workflow()
            print("Workflow executed successfully")
        except Exception as e:
            print("Error")
    else:
        print("No changes detected.")
        message = "No changes detected."
        try:
            pipeline.run_workflow()
            print("Workflow executed successfully")
        except Exception as e:
            print("Error")

    return message


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=9001)