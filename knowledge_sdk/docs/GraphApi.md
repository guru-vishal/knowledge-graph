# knowledge_sdk.GraphApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_graph_graph_get**](GraphApi.md#get_graph_graph_get) | **GET** /graph/ | Get Graph


# **get_graph_graph_get**
> GraphResponse get_graph_graph_get()

Get Graph

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.graph_response import GraphResponse
from knowledge_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = knowledge_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with knowledge_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = knowledge_sdk.GraphApi(api_client)

    try:
        # Get Graph
        api_response = api_instance.get_graph_graph_get()
        print("The response of GraphApi->get_graph_graph_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GraphApi->get_graph_graph_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GraphResponse**](GraphResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

