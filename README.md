# FlowDesk — Service Request & Approval Portal

## The problem

Service teams need a reliable way to track requests, deadlines and approval handoffs without losing decisions across messages.

## The solution

FlowDesk brings a searchable request queue, priorities, ownership and manager approval into one workspace. Users create requests, record notes, move work through permitted states and review chronological activity.

- Authenticated access and owner-scoped records
- New → In progress → Awaiting approval → Completed
- Manager-only completion approval
- Request validation, deadlines and status filtering
- Persistent storage and CSV exports

## Screenshots

![Request overview](screenshots/FlowDesk_01_Overview.png)
![Scope and activity timeline](screenshots/FlowDesk_02_Request_Detail.png)
![Create request](screenshots/FlowDesk_03_Request_Form.png)

## Explore the implementation

[Models](app/core/models.py) · [Workflow rules](app/core/services.py) · [Tests](app/core/tests.py) · [Run locally](SETUP.md)

The screenshots use illustrative service requests and fictional company names. This is a personal project, not a client engagement. The repository provides the full server application. A separate browser preview is available through GitHub Pages; it does not run the authenticated server backend.


## Browser preview

The `docs/index.html` preview runs in the browser. Changes are saved in browser-local storage. Manager approvals here demonstrate the workflow and do not enforce server authentication.
