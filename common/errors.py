
COMMON_ERRORS = {
    "Access Denied": {
        "Description": "This error occurs when a user or service doesn't have the necessary permissions to access a resource.",
        "Solution": "Review and update the permissions for the user or service in the cloud provider's IAM (Identity and Access Management) console."
        },
    "Resource Not Found":{
        "Description": "This error occurs when you try to access a resource that doesn't exist.",
        "Solution": "Verify the resource's name and location. Double-check if you're looking in the right region or project."
    },
    "Timeout":{
        "Description": "Operations can sometimes take longer than expected, and if a timeout occurs, the operation is canceled.",
        "Solution": "Increase the timeout setting for the operation or optimize the operation to complete faster."
    },
    "Insufficient Resources":{
        "Description": "This error happens when there aren't enough resources (such as CPU, memory, or storage) available to perform a task.",
        "Solution": "Scale up the resources allocated to the instance, or optimize your code/application to use resources more efficiently."
    },
    "Service Unavailable":{
        "Description": "This error occurs when a cloud service is temporarily down or not responding.",
        "Solution": "Check the cloud provider's status page for any ongoing outages or maintenance. Wait for the service to come back online."
    },
    "Billing or Subscription Issue":{
        "Description": "This error is related to billing issues, such as expired credit cards or reaching usage limits.",
        "Solution": "Update payment information, resolve billing issues, or consider upgrading your subscription plan if you've reached usage limits."
    },
    "Network Connectivity":{
        "Description": "Network issues can lead to connectivity problems between cloud resources or between the cloud and your local environment.",
        "Solution": "Check your network settings, security groups, firewalls, and ensure the necessary ports are open for communication."
    },
    "Data Loss or Corruption":{
        "Description": "Data loss or corruption can occur due to various reasons, including hardware failures, software bugs, or human errors.",
        "Solution": "Regularly back up your data, implement data redundancy, and consider using data replication and versioning features offered by the cloud provider."
    },
    "API Rate Limit Exceeded":{
        "Description": "Cloud providers often impose rate limits on API requests to prevent abuse.",
        "Solution": "Review the API usage patterns, implement rate limiting on your side, and consider contacting the cloud provider for increased rate limits if needed."
    },
    "Configuration Errors": {
        "Description": "Misconfigured settings can lead to unexpected behavior or security vulnerabilities.",
        "Solution": "Double-check your configuration settings, follow best practices, and use infrastructure-as-code tools to ensure consistent and reproducible configurations."
    }
}