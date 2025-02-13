# API Documentation

This document provides a comprehensive overview of the available endpoints in the FastAPI application.

## Table of Contents
- [Introduction](#introduction)
- [Endpoints](#endpoints)
  - [Root Endpoint](#root-endpoint)
  - [Invoke Agent via HTTP](#invoke-agent-via-http)
  - [Invoke Agent via WebSocket](#invoke-agent-via-websocket)
  - [Update Settings](#update-settings)
  - [Get Settings](#get-settings)
  - [Summarize Endpoint](#summarize-endpoint)
- [CORS Configuration](#cors-configuration)
- [Dependencies](#dependencies)
- [Running the Server](#running-the-server)

## Introduction

This API serves multiple purposes:
- **Agent Invocation:** Execute an agent function using given input parameters.
- **Settings Management:** Retrieve and update application settings.
- **Summarization:** Generate and stream summary data.
- **WebSocket Support:** Stream real-time responses through a WebSocket connection.

The application is built with FastAPI and uses Uvicorn as the ASGI server. Custom modules are imported to manage schemas, settings, and agent execution.

## Endpoints

### Root Endpoint

- **URL:** `/`
- **Method:** `GET`
- **Description:** Health check endpoint.
- **Response Example:**
  ```json
  {
    "message": "Service is healthy and running."
  }



## WebSocket API
Invoke Agent via WebSocket
URL: /ws/invoke/{app_id}
Method: WebSocket
Description: Establishes a WebSocket connection to invoke the agent and stream responses in real time.
Path Parameter:
app_id (string): Identifier of the application.
Connection and Message Flow:
Connect: Client connects to the WebSocket endpoint.
Send Message: The client sends a JSON message with the following structure:
{
  "session_id": "string",
  "query": "string"
}

Processing:
The server fetches settings for the specified app_id.
If settings are missing, the server sends an error message back over the WebSocket.
Otherwise, the server invokes the agent function and streams the results.
Streaming Response: The server sends each chunk of the result back to the client as a JSON message over the WebSocket.
Disconnection: If the client disconnects (triggering a WebSocketDisconnect), the server will handle the disconnection gracefully.
Example Client Interaction:
Connect:
ws://<server_address>/ws/invoke/myAppId
Send Request:
{
  "session_id": "abc123",
  "query": "Your query text here"
}

Receive Response:
The client will receive streamed responses such as:

{
  "result": "partial agent response..."
}



