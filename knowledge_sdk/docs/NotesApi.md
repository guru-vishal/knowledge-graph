# knowledge_sdk.NotesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_note_notes_post**](NotesApi.md#create_note_notes_post) | **POST** /notes/ | Create Note
[**link_notes_notes_note_id_link_patch**](NotesApi.md#link_notes_notes_note_id_link_patch) | **PATCH** /notes/{note_id}/link | Link Notes
[**list_notes_notes_get**](NotesApi.md#list_notes_notes_get) | **GET** /notes/ | List Notes
[**note_details_notes_note_id_get**](NotesApi.md#note_details_notes_note_id_get) | **GET** /notes/{note_id} | Note Details
[**tag_suggestions_notes_tags_suggestions_get**](NotesApi.md#tag_suggestions_notes_tags_suggestions_get) | **GET** /notes/tags/suggestions | Tag Suggestions


# **create_note_notes_post**
> NoteResponse create_note_notes_post(note_create)

Create Note

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.note_create import NoteCreate
from knowledge_sdk.models.note_response import NoteResponse
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
    api_instance = knowledge_sdk.NotesApi(api_client)
    note_create = knowledge_sdk.NoteCreate() # NoteCreate | 

    try:
        # Create Note
        api_response = api_instance.create_note_notes_post(note_create)
        print("The response of NotesApi->create_note_notes_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotesApi->create_note_notes_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **note_create** | [**NoteCreate**](NoteCreate.md)|  | 

### Return type

[**NoteResponse**](NoteResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **link_notes_notes_note_id_link_patch**
> object link_notes_notes_note_id_link_patch(note_id, note_link_request)

Link Notes

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.note_link_request import NoteLinkRequest
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
    api_instance = knowledge_sdk.NotesApi(api_client)
    note_id = 56 # int | 
    note_link_request = knowledge_sdk.NoteLinkRequest() # NoteLinkRequest | 

    try:
        # Link Notes
        api_response = api_instance.link_notes_notes_note_id_link_patch(note_id, note_link_request)
        print("The response of NotesApi->link_notes_notes_note_id_link_patch:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotesApi->link_notes_notes_note_id_link_patch: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **note_id** | **int**|  | 
 **note_link_request** | [**NoteLinkRequest**](NoteLinkRequest.md)|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_notes_notes_get**
> List[NoteResponse] list_notes_notes_get(tag=tag, keyword=keyword)

List Notes

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.note_response import NoteResponse
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
    api_instance = knowledge_sdk.NotesApi(api_client)
    tag = 'tag_example' # str |  (optional)
    keyword = 'keyword_example' # str |  (optional)

    try:
        # List Notes
        api_response = api_instance.list_notes_notes_get(tag=tag, keyword=keyword)
        print("The response of NotesApi->list_notes_notes_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotesApi->list_notes_notes_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tag** | **str**|  | [optional] 
 **keyword** | **str**|  | [optional] 

### Return type

[**List[NoteResponse]**](NoteResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **note_details_notes_note_id_get**
> NoteResponse note_details_notes_note_id_get(note_id)

Note Details

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.note_response import NoteResponse
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
    api_instance = knowledge_sdk.NotesApi(api_client)
    note_id = 56 # int | 

    try:
        # Note Details
        api_response = api_instance.note_details_notes_note_id_get(note_id)
        print("The response of NotesApi->note_details_notes_note_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotesApi->note_details_notes_note_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **note_id** | **int**|  | 

### Return type

[**NoteResponse**](NoteResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tag_suggestions_notes_tags_suggestions_get**
> List[str] tag_suggestions_notes_tags_suggestions_get()

Tag Suggestions

### Example


```python
import knowledge_sdk
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
    api_instance = knowledge_sdk.NotesApi(api_client)

    try:
        # Tag Suggestions
        api_response = api_instance.tag_suggestions_notes_tags_suggestions_get()
        print("The response of NotesApi->tag_suggestions_notes_tags_suggestions_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotesApi->tag_suggestions_notes_tags_suggestions_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**List[str]**

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

