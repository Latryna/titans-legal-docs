# TITANS Workspace API Specification

All endpoints use JSON for request and response bodies.  The API is designed to be stateless and easy to integrate with web applications, local scripts or other agents via OpenRouter.

## `\/chat` (POST)

Send a message to a specific agent and receive a response.

* **Parameters**
  * `agent` (string) – target agent identifier, e.g. `"titans"` for the local agent or `"gpt4"` when routing via OpenRouter.
  * `message` (string) – user prompt to send to the agent.
  * `context` (object, optional) – additional context or metadata.
* **Response**
  * `reply` (string) – generated response.
  * `trace` (object, optional) – reasoning trace or references used to generate the reply.

## `\/graph` (GET)

Retrieve the current semantic knowledge graph maintained by the TITANS agent.

* **Response**
  * `nodes` (array) – list of entities with their identifiers and labels.
  * `edges` (array) – relationships between entities, each containing a source, target and relation type.

## `\/memory` (GET / POST)

Access or update the agent’s memory stores.

### GET

Retrieve stored episodes or semantic concepts.

* **Parameters**
  * `type` (string) – `"episodic"` or `"semantic"`.
  * `id` (string, optional) – specific memory identifier; if omitted, all entries of the given type are returned.
* **Response**
  * `items` (array) – list of memory entries matching the query.

### POST

Store a new memory item.

* **Request Body**
  * `type` (string) – `"episodic"` or `"semantic"`.
  * `data` (object) – content to store.
* **Response**
  * `id` (string) – identifier of the newly stored memory entry.

These endpoints are implemented by the TITANS agent as described in `TITANS_agent_interface.tex`.  The workspace API is the primary way for other services (including OpenRouter) to interact with the agent.