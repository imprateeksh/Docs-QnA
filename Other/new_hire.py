import json


NEW_HIRE_CHECKLIST= {
        "Team_Name": "GoldenEye",
        "Org": "URL: https://www.ibm.com/in-en/about",
        "About": "Project GoldenEye (GE) is an InnerSource (internal open source) project for IBM Cloud Platform as a Service (PaaS). The goal of Project GoldenEye is both to create a community of IBM Cloud platform developers and to share common infrastructure as code (IaC) and automation assets.",
        "Technical_Doc": "URL: https://github.ibm.com/GoldenEye/documentation/blob/master/README.md",
        "Coding_Guidelines": "URL: https://www.ibm.com/docs/en/z-netview/6.2.0?topic=modules-general-coding-guidelines" ,
        "Access_Requests": "Connect with Team-Admin to get access to the required tools.",
        "Tech_Stack": ["Linux","Openshift", "Terraform", "Python", "SQL", "Shell"],
        "Start": "Just need to setup the machine first and get the access. Start looking for the changes done and tools/technologies used."
}

def present_new_hire_checklist():
    # response = {}
    
    # for section, items in NEW_HIRE_CHECKLIST.items(): # if nested dict
    #     section_info = {}
    #     for item, content in items.items():
    #         if isinstance(content, str):
    #             section_info[item] = content
    #         elif isinstance(content, list):
    #             section_info[item] = content
    #         else:
    #             section_info[item] = "Invalid content type."
    #     response[section] = section_info
    
    return json.dumps(NEW_HIRE_CHECKLIST)
    # return json.dumps(response, indent=None, separators=(',', ':'))
